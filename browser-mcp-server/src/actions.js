/**
 * actions.js — Tool implementations on top of a BrowserSession.
 *
 * Each action takes plain args and returns a plain-text result plus optional
 * artifact path. No MCP specifics here, so this layer is testable in isolation.
 */
import { BrowserSession } from './browser.js';
import { snapshotInPage, renderSnapshot, newNamespace } from './snapshot.js';

export class BrowserActions {
  constructor(session = new BrowserSession()) {
    this.session = session;
    this.ns = newNamespace();
    this.lastSnapshot = [];
  }

  /** Resolve a target that may be a ref (e1), a CSS selector, or text. */
  async locate(target) {
    const page = await this.session.ensure();
    const ref = String(target || '').trim();
    if (!ref) throw new Error('target is required');

    if (/^e\d+$/.test(ref)) {
      const attr = `[data-mcp-ref-${this.ns}="${ref}"]`;
      const byRef = page.locator(attr).first();
      if (await byRef.count()) return byRef;
    }
    // CSS selector
    try {
      const byCss = page.locator(ref).first();
      if (await byCss.count()) return byCss;
    } catch { /* not a valid selector, fall through */ }
    // Visible text
    const byText = page.getByText(ref, { exact: false }).first();
    if (await byText.count()) return byText;
    throw new Error(`target not found: ${ref}`);
  }

  async navigate({ url, wait_until = 'domcontentloaded' }) {
    if (!url || !/^https?:\/\//i.test(url)) {
      throw new Error('url must start with http:// or https://');
    }
    const page = await this.session.ensure();
    const resp = await page.goto(url, { waitUntil: wait_until, timeout: 45000 });
    const title = await page.title();
    const snap = await this.snapshot({});
    return {
      status: resp ? resp.status() : null,
      url: page.url(),
      title,
      text: `navigated -> ${page.url()} (status ${resp ? resp.status() : 'n/a'})\n\n${snap.text}`,
    };
  }

  async snapshot({}) {
    const page = await this.session.ensure();
    const nodes = await page.evaluate(snapshotInPage, this.ns);
    this.lastSnapshot = nodes;
    return {
      url: page.url(),
      title: await page.title(),
      count: nodes.length,
      text: renderSnapshot(nodes, { url: page.url(), title: await page.title() }),
    };
  }

  async click({ target, timeout = 15000 }) {
    const el = await this.locate(target);
    await el.scrollIntoViewIfNeeded().catch(() => {});
    await el.click({ timeout });
    const page = await this.session.ensure();
    await page.waitForLoadState('domcontentloaded', { timeout: 5000 }).catch(() => {});
    const snap = await this.snapshot({});
    return { text: `clicked ${target}\n\n${snap.text}` };
  }

  async fill({ target, text, submit = false }) {
    const el = await this.locate(target);
    await el.scrollIntoViewIfNeeded().catch(() => {});
    await el.fill(String(text ?? ''));
    if (submit) {
      await el.press('Enter');
      const page = await this.session.ensure();
      await page.waitForLoadState('domcontentloaded', { timeout: 5000 }).catch(() => {});
    }
    const snap = await this.snapshot({});
    return { text: `filled ${target}${submit ? ' + Enter' : ''}\n\n${snap.text}` };
  }

  async select({ target, value }) {
    const el = await this.locate(target);
    await el.selectOption(String(value));
    const snap = await this.snapshot({});
    return { text: `selected "${value}" on ${target}\n\n${snap.text}` };
  }

  async press({ key }) {
    const page = await this.session.ensure();
    await page.keyboard.press(key);
    const snap = await this.snapshot({});
    return { text: `pressed ${key}\n\n${snap.text}` };
  }

  async screenshot({ name, full_page = false }) {
    const page = await this.session.ensure();
    const out = BrowserSession.shotPath(name);
    await page.screenshot({ path: out, fullPage: !!full_page });
    return { path: out, text: `screenshot saved: ${out}` };
  }

  async getText({}) {
    const page = await this.session.ensure();
    const body = (await page.evaluate(() => document.body?.innerText || '')) || '';
    const text = body.replace(/\n{3,}/g, '\n\n').trim().slice(0, 8000);
    return { text: text || '(page is empty)' };
  }

  async evaluate({ script }) {
    const page = await this.session.ensure();
    const result = await page.evaluate(script);
    let rendered;
    try { rendered = JSON.stringify(result, null, 2); } catch { rendered = String(result); }
    return { text: `evaluate result:\n${String(rendered).slice(0, 6000)}` };
  }

  async wait({ selector, timeout = 15000 }) {
    const page = await this.session.ensure();
    if (selector) {
      await page.waitForSelector(selector, { timeout });
      return { text: `selector appeared: ${selector}` };
    }
    await page.waitForLoadState('networkidle', { timeout }).catch(() => {});
    return { text: 'page settled (networkidle)' };
  }

  async scroll({ direction = 'down', amount = 600 }) {
    const page = await this.session.ensure();
    const dy = direction === 'up' ? -Math.abs(amount) : Math.abs(amount);
    await page.mouse.wheel(0, dy);
    const snap = await this.snapshot({});
    return { text: `scrolled ${direction} ${Math.abs(amount)}px\n\n${snap.text}` };
  }

  async back({}) {
    const page = await this.session.ensure();
    await page.goBack({ waitUntil: 'domcontentloaded', timeout: 20000 }).catch(() => {});
    const snap = await this.snapshot({});
    return { text: `back -> ${page.url()}\n\n${snap.text}` };
  }

  async forward({}) {
    const page = await this.session.ensure();
    await page.goForward({ waitUntil: 'domcontentloaded', timeout: 20000 }).catch(() => {});
    const snap = await this.snapshot({});
    return { text: `forward -> ${page.url()}\n\n${snap.text}` };
  }

  async close({}) {
    await this.session.close();
    return { text: 'browser session closed' };
  }
}
