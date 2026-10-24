/**
 * browser.js — Browser session manager (single persistent session)
 *
 * First principles: an agent drives ONE browser for a whole task, not a new
 * one per command. Launching Chromium costs ~1-2s; reusing it costs ~0.
 * So we keep a singleton session + page, and expose primitives on top.
 *
 * Uses the Termux system Chromium directly (no extra binary download).
 */
// Playwright computes its browser cache directory during module import. On
// Termux/Android it does not recognize process.platform === "android" and
// crashes before launch. Provide an explicit cache path before importing it;
// the server uses the system Chromium executable below, so this directory is
// only a safe import-time fallback and does not trigger a browser download.
import { mkdirSync, accessSync, constants } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MODULE_DIR = dirname(fileURLToPath(import.meta.url));

// Android/Termux commonly has no /tmp. Chromium creates shared-memory and
// profile files there during launch, so point all temporary-file users at the
// writable Termux temp directory before importing/launching Playwright.
if (process.platform === 'android' || process.env.PREFIX?.includes('/com.termux/')) {
  const termuxTmp = join(process.env.PREFIX || '/data/data/com.termux/files/usr', 'tmp');
  mkdirSync(termuxTmp, { recursive: true });
  process.env.TMPDIR ||= termuxTmp;
  process.env.TMP ||= termuxTmp;
  process.env.TEMP ||= termuxTmp;
}

process.env.PLAYWRIGHT_BROWSERS_PATH ||= join(MODULE_DIR, '..', '.playwright-browsers');
const { chromium } = await import('playwright');

const CHROME_CANDIDATES = [
  process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE,
  '/data/data/com.termux/files/usr/lib/chromium/chrome',
  '/data/data/com.termux/files/usr/bin/chromium-browser',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/usr/bin/google-chrome',
].filter(Boolean);

const LAUNCH_ARGS = [
  '--no-sandbox',
  '--disable-dev-shm-usage',
  '--disable-gpu',
  '--disable-setuid-sandbox',
  '--no-first-run',
  '--no-zygote',
  '--single-process',
];

/** Resolve a usable Chromium binary path. */
function resolveExecutable() {
  for (const p of CHROME_CANDIDATES) {
    try {
      accessSync(p, constants.X_OK);
      return p;
    } catch { /* try next */ }
  }
  return undefined; // let Playwright use its bundled browser if present
}

export class BrowserSession {
  constructor({ headless = true, viewport = { width: 1280, height: 800 } } = {}) {
    this.headless = headless;
    this.viewport = viewport;
    this.browser = null;
    this.context = null;
    this.page = null;
    this._launching = null;
  }

  /** Launch once; concurrent callers share the same promise. */
  async ensure() {
    if (this.page && !this.page.isClosed()) return this.page;
    if (this._launching) return this._launching;

    this._launching = (async () => {
      const executablePath = resolveExecutable();
      this.browser = await chromium.launch({
        executablePath,
        headless: this.headless,
        args: LAUNCH_ARGS,
        chromiumSandbox: false,
      });
      this.context = await this.browser.newContext({
        viewport: this.viewport,
        userAgent:
          'Mozilla/5.0 (Linux; Android 13; Termux) AppleWebKit/537.36 ' +
          '(KHTML, like Gecko) Chrome/156.0.0.0 Mobile Safari/537.36',
        ignoreHTTPSErrors: true,
      });
      this.page = await this.context.newPage();
      this.page.setDefaultTimeout(30000);
      this.page.setDefaultNavigationTimeout(45000);
      this._launching = null;
      return this.page;
    })().catch((e) => {
      this._launching = null;
      throw e;
    });

    return this._launching;
  }

  async close() {
    try { if (this.context) await this.context.close(); } catch { /* ignore */ }
    try { if (this.browser) await this.browser.close(); } catch { /* ignore */ }
    this.browser = this.context = this.page = null;
  }

  /** Path for a screenshot artifact inside the workspace tmp dir. */
  static shotPath(name) {
    const dir = join(process.env.HOME || tmpdir(), 'cow', 'tmp');
    mkdirSync(dir, { recursive: true });
    const safe = String(name || 'shot').replace(/[^a-zA-Z0-9._-]/g, '_');
    return join(dir, `${Date.now()}-${safe}.png`);
  }
}
