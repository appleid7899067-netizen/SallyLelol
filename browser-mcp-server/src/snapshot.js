/**
 * snapshot.js — Token-efficient page snapshot with stable element refs.
 *
 * Problem: dumping page HTML blows up the context window.
 * Solution: walk the DOM, keep only interactive/meaningful nodes, assign each
 * a short ref (e1, e2, ...) that later actions can target. This is what makes
 * a browser usable by an agent rather than a human.
 */
import { randomUUID } from 'node:crypto';

/**
 * In-page function: build a compact list of interesting nodes and tag each
 * with a data attribute so later Playwright calls can resolve it by ref.
 *
 * IMPORTANT: this function body is serialized and executed INSIDE the page
 * (page.evaluate), so it must be self-contained. Any helper it needs must be
 * declared inside it — module-scope constants are NOT visible there.
 */
/* eslint-disable no-undef */
export function snapshotInPage(namespace) {
  const INTERACTIVE = new Set([
    'a', 'button', 'input', 'select', 'textarea', 'option', 'summary',
    'label', 'details', 'iframe', 'audio', 'video',
  ]);

  const KEEP_ROLES = new Set([
    'button', 'link', 'textbox', 'checkbox', 'radio', 'combobox', 'menuitem',
    'tab', 'option', 'searchbox', 'switch', 'slider', 'heading',
  ]);

  const REF_ATTR = `data-mcp-ref-${namespace}`;
  const out = [];
  let counter = 0;

  const visible = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width <= 0 && r.height <= 0) return false;
    const s = window.getComputedStyle(el);
    return s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0';
  };

  const text = (el) =>
    (el.getAttribute('aria-label') || el.innerText || el.value || el.placeholder || el.title || '')
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, 120);

  const all = document.querySelectorAll('*');
  for (const el of all) {
    if (counter > 400) break;
    const tag = el.tagName.toLowerCase();
    const role = el.getAttribute('role') || '';
    const isInteractive = INTERACTIVE.has(tag) || el.isContentEditable;
    const isHeading = /^h[1-6]$/.test(tag);
    const keepRole = KEEP_ROLES.has(role);
    if (!isInteractive && !isHeading && !keepRole) continue;
    if (!visible(el)) continue;
    if (tag === 'input' && el.type === 'hidden') continue;

    const ref = `e${++counter}`;
    el.setAttribute(REF_ATTR, ref);
    out.push({
      ref,
      tag,
      role: role || (isHeading ? 'heading' : tag),
      name: text(el),
      type: el.getAttribute('type') || undefined,
      href: tag === 'a' ? el.getAttribute('href') || undefined : undefined,
      value: 'value' in el && el.value ? String(el.value).slice(0, 80) : undefined,
      disabled: el.disabled === true || el.getAttribute('aria-disabled') === 'true' || undefined,
      checked: el.type === 'checkbox' || el.type === 'radio' ? el.checked : undefined,
    });
  }
  return out;
}
/* eslint-enable no-undef */

/** Render snapshot nodes as a compact, model-friendly text tree. */
// eslint-disable-next-line no-unused-vars
export function renderSnapshot(nodes, { url, title } = {}) {
  const lines = [`URL: ${url || 'about:blank'}`, `TITLE: ${title || ''}`, ''];
  if (!nodes.length) {
    lines.push('(no interactive elements found)');
    return lines.join('\n');
  }
  for (const n of nodes) {
    const bits = [`[${n.ref}]`, n.role || n.tag];
    if (n.name) bits.push(`"${n.name}"`);
    if (n.href) bits.push(`-> ${n.href}`);
    if (n.value) bits.push(`= "${n.value}"`);
    if (n.checked !== undefined) bits.push(n.checked ? '(checked)' : '(unchecked)');
    if (n.disabled) bits.push('(disabled)');
    lines.push(bits.join(' '));
  }
  return lines.join('\n');
}

export const newNamespace = () => randomUUID().slice(0, 8);
