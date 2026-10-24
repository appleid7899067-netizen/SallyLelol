#!/usr/bin/env node
/**
 * browser-cli.mjs — one-shot CLI over the Browser MCP engine.
 *
 * Why this exists: the MCP server speaks stdio JSON-RPC, which is great for a
 * client but awkward from a shell. This wrapper lets an agent (or a human) run
 * a single browser action per process:
 *
 *   node browser-cli.mjs navigate https://example.com
 *   node browser-cli.mjs text
 *   node browser-cli.mjs shot out.png
 *   node browser-cli.mjs eval "document.title"
 *   node browser-cli.mjs click "e3"
 *   node browser-cli.mjs fill "e1" "hello" --submit
 *   node browser-cli.mjs scroll down 600
 *
 * Persistence: each process is short-lived, so we cannot keep a live Chromium
 * in memory between calls. Instead we persist the last URL + cookies in a
 * profile dir, and re-open the page on the next call. That keeps commands
 * stateless from the caller's point of view while still feeling "stateful".
 *
 * Exit code 0 = success, 1 = action error (message on stderr).
 */
import { BrowserActions } from './src/actions.js';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const STATE_DIR = process.env.BROWSER_CLI_STATE || join(process.env.HOME, 'cow', 'tmp', 'browser-cli');
const STATE_FILE = join(STATE_DIR, 'state.json');

function loadState() {
  try {
    return JSON.parse(readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { url: null };
  }
}

function saveState(patch) {
  try {
    mkdirSync(STATE_DIR, { recursive: true });
    const next = { ...loadState(), ...patch };
    writeFileSync(STATE_FILE, JSON.stringify(next, null, 2));
  } catch { /* state is a convenience, never fatal */ }
}

function usage() {
  console.log(`browser-cli — drive Chromium from the shell

Usage:
  node browser-cli.mjs navigate <url> [--wait load|domcontentloaded|networkidle]
  node browser-cli.mjs snapshot
  node browser-cli.mjs text
  node browser-cli.mjs eval "<javascript>"
  node browser-cli.mjs click <ref|css|text>
  node browser-cli.mjs fill <ref|css|label> "<value>" [--submit]
  node browser-cli.mjs press <key>
  node browser-cli.mjs select <ref|css> "<option>"
  node browser-cli.mjs scroll <up|down|left|right> [px]
  node browser-cli.mjs wait [<css-selector>]
  node browser-cli.mjs back
  node browser-cli.mjs forward
  node browser-cli.mjs shot [out.png] [--full]
  node browser-cli.mjs close
  node browser-cli.mjs self-test [url]

State: last URL kept in ${STATE_FILE}`);
}

/** Parse argv into { action, positionals, flags }. */
function parseArgs(argv) {
  const [action, ...rest] = argv;
  const positionals = [];
  const flags = {};
  for (let i = 0; i < rest.length; i++) {
    const tok = rest[i];
    if (tok.startsWith('--')) {
      const key = tok.slice(2);
      const next = rest[i + 1];
      if (next !== undefined && !next.startsWith('--')) {
        flags[key] = next;
        i++;
      } else {
        flags[key] = true;
      }
    } else {
      positionals.push(tok);
    }
  }
  return { action, positionals, flags };
}

async function main() {
  const { action, positionals, flags } = parseArgs(process.argv.slice(2));

  if (!action || action === 'help' || action === '-h' || action === '--help') {
    usage();
    process.exit(action ? 0 : 1);
  }

  const actions = new BrowserActions();
  const state = loadState();

  // Resume the previous URL unless this call is itself a navigate.
  const resume = async () => {
    if (action !== 'navigate' && state.url) {
      try {
        await actions.navigate({ url: state.url, wait_until: 'domcontentloaded' });
      } catch { /* page may be gone; let the action report its own error */ }
    }
  };

  let result;
  try {
    switch (action) {
      case 'navigate': {
        const url = positionals[0];
        if (!url) throw new Error('navigate needs a <url>');
        result = await actions.navigate({ url, wait_until: flags.wait || 'domcontentloaded' });
        saveState({ url: result.url });
        break;
      }
      case 'snapshot':
        await resume();
        result = await actions.snapshot({});
        break;
      case 'text':
        await resume();
        result = await actions.getText({});
        break;
      case 'eval':
        await resume();
        result = await actions.evaluate({ script: positionals.join(' ') });
        break;
      case 'click':
        await resume();
        result = await actions.click({ target: positionals[0], timeout: flags.timeout ? Number(flags.timeout) : undefined });
        break;
      case 'fill':
        await resume();
        result = await actions.fill({ target: positionals[0], text: positionals.slice(1).join(' '), submit: !!flags.submit });
        break;
      case 'press':
        await resume();
        result = await actions.press({ key: positionals[0] });
        break;
      case 'select':
        await resume();
        result = await actions.select({ target: positionals[0], value: positionals.slice(1).join(' ') });
        break;
      case 'scroll':
        await resume();
        result = await actions.scroll({ direction: positionals[0] || 'down', amount: positionals[1] ? Number(positionals[1]) : 500 });
        break;
      case 'wait':
        await resume();
        // `wait` settles the page; if a CSS selector is given we wait for it.
        result = await actions.wait({ selector: positionals[0], timeout: flags.timeout ? Number(flags.timeout) : 15000 });
        break;
      case 'back':
        await resume();
        result = await actions.back({});
        saveState({ url: null }); // history moved; force explicit navigate next time
        break;
      case 'forward':
        await resume();
        result = await actions.forward({});
        saveState({ url: null });
        break;
      case 'shot':
        await resume();
        result = await actions.screenshot({ name: positionals[0], full_page: !!flags.full });
        break;
      case 'close':
        result = await actions.close({});
        saveState({ url: null });
        break;
      case 'self-test': {
        const url = positionals[0] || 'https://example.com';
        const nav = await actions.navigate({ url });
        const txt = await actions.getText({});
        const shot = await actions.screenshot({ name: 'cli-selftest' });
        await actions.close({});
        result = {
          text: `self-test ok\n  navigate -> ${nav.url} (${nav.status})\n  text -> ${txt.text.length} chars\n  shot -> ${shot.path}`,
          artifacts: [shot.path],
        };
        break;
      }
      default:
        throw new Error(`unknown action: ${action}\n\n${usage()}`);
    }
  } catch (err) {
    console.error(`❌ ${action}: ${err.message}`);
    process.exit(1);
  }

  // Print the human-readable text; list artifacts on their own lines.
  const text = result?.text ?? '';
  const artifacts = result?.artifacts ?? (result?.path ? [result.path] : []);
  if (text) console.log(text);
  for (const a of artifacts) console.log(`ARTIFACT: ${a}`);
}

main().catch((err) => {
  console.error(`❌ fatal: ${err.message}`);
  process.exit(1);
});
