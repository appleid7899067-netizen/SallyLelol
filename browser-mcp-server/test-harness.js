#!/usr/bin/env node
/**
 * test-harness.js — drive the MCP server over stdio exactly like a client.
 * Verifies: handshake, tools/list, navigate, snapshot, get_text, screenshot, close.
 */
import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dir = dirname(fileURLToPath(import.meta.url));
const serverPath = join(__dir, 'src', 'index.js');
const TARGET = process.argv[2] || 'https://example.com';

const child = spawn('node', [serverPath], { stdio: ['pipe', 'pipe', 'pipe'] });
let buf = '';
const pending = new Map();
let idc = 0;

child.stderr.on('data', (d) => process.stderr.write(`[server] ${d}`));
child.stdout.on('data', (d) => {
  buf += d.toString();
  let idx;
  while ((idx = buf.indexOf('\n')) >= 0) {
    const line = buf.slice(0, idx).trim();
    buf = buf.slice(idx + 1);
    if (!line) continue;
    let msg;
    try { msg = JSON.parse(line); } catch { continue; }
    if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  }
});

function rpc(method, params) {
  const id = ++idc;
  return new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(new Error(`timeout: ${method}`)), 90000);
    pending.set(id, (m) => { clearTimeout(t); resolve(m); });
    child.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n');
  });
}

const notify = (method, params) =>
  child.stdin.write(JSON.stringify({ jsonrpc: '2.0', method, params }) + '\n');

/**
 * Call a tool and split the reply the same way a real client would:
 *  - `text`      = ordinary content parts joined for reading
 *  - `artifacts` = local file paths announced as "ARTIFACT: <path>"
 * Keeping these separate is what makes assertions deterministic — a screenshot
 * must not inflate the length checks meant for human-readable text.
 */
const call = async (name, args = {}) => {
  const r = await rpc('tools/call', { name, arguments: args });
  const parts = (r.result?.content || []).map((c) => c.text || '');
  const artifacts = parts
    .filter((t) => t.startsWith('ARTIFACT:'))
    .map((t) => t.slice('ARTIFACT:'.length).trim());
  const text = parts.filter((t) => !t.startsWith('ARTIFACT:')).join('\n');
  return { isError: !!r.result?.isError, text, artifacts, raw: r };
};

const pass = [];
const fail = [];
const check = (label, ok, extra = '') => {
  (ok ? pass : fail).push(label);
  console.log(`${ok ? '✅' : '❌'} ${label}${extra ? ' — ' + extra : ''}`);
};

(async () => {
  let r = await rpc('initialize', {
    protocolVersion: '2024-11-05',
    capabilities: {},
    clientInfo: { name: 'test-harness', version: '1.0.0' },
  });
  check('initialize handshake', r.result?.serverInfo?.name === 'slilelo-browser',
    r.result?.serverInfo?.name);
  notify('notifications/initialized', {});

  r = await rpc('tools/list', {});
  const tools = (r.result?.tools || []).map((t) => t.name);
  check('tools/list returns >= 12 tools', tools.length >= 12, `${tools.length} tools`);
  check('tools/list wires each action',
    ['navigate', 'snapshot', 'click', 'fill', 'get_text', 'evaluate', 'screenshot', 'close']
      .every((n) => tools.includes(n)),
    tools.join(','));

  let out = await call('navigate', { url: TARGET });
  check('navigate to target', !out.isError && /navigated/.test(out.text),
    out.text.split('\n')[0]);

  out = await call('snapshot');
  check('snapshot returns refs', !out.isError && /\[\]|\[e\d+\]|no interactive/.test(out.text),
    out.text.split('\n')[0]);

  // Ground truth: ask the page itself (in-page DOM) for its visible text length
  // and a distinctive fragment, then require get_text to agree. This asserts
  // against live page content instead of a hardcoded phrase that a site can
  // silently change (example.com did exactly that).
  const probeOut = await call('evaluate', {
    script:
      '(function(){var t=(document.body&&document.body.innerText)||"";' +
      'var words=t.replace(/\\s+/g," ").trim().split(" ");' +
      'return {len:t.length, first:words.slice(0,4).join(" ")};})()',
  });
  const probe = (() => {
    try { return JSON.parse(probeOut.text.replace(/^evaluate result:\s*/, '')); }
    catch { return {}; }
  })();

  out = await call('get_text');
  // The distinctive leading fragment must appear in what get_text returns,
  // and the returned text must be comparable in size to the real body text.
  const fragment = String(probe.first || '').split(' ')[0];
  const hasFragment = fragment.length > 2 && out.text.includes(fragment);
  const sizeOk = out.text.length > 0 && (!probe.len || out.text.length >= Math.min(probe.len, 200));
  check('get_text returns live page text',
    !out.isError && hasFragment && sizeOk,
    `${out.text.length} chars (dom=${probe.len ?? '?'}), fragment="${fragment}" found=${hasFragment}`);

  check('evaluate returns value', !out.isError && /evaluate result/.test(probeOut.text),
    probeOut.text.replace(/\n/g, ' ').slice(0, 60));

  out = await call('screenshot', { name: 'selftest' });
  const shot = out.artifacts[0];
  const onDisk = shot ? existsSync(shot) : false;
  check('screenshot saves a real file',
    !out.isError && /saved/.test(out.text) && onDisk,
    shot ? `${shot} (${onDisk ? 'exists' : 'MISSING'})` : 'no ARTIFACT line');

  out = await call('close');
  check('close session', !out.isError && /closed/.test(out.text));

  console.log(`\n=== ${pass.length} passed, ${fail.length} failed ===`);
  child.kill();
  process.exit(fail.length ? 1 : 0);
})().catch((e) => { console.error('HARNESS ERROR:', e); child.kill(); process.exit(1); });
