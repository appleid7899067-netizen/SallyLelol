/**
 * Nova UI — UX Interaction Layer v1.0.0
 * Nova Modern Stack — ลุลูกเล่นปฏิสัมผัสน่าสนใจ
 * Non-destructive: ใช้อนุภาค DOM ที่เกา่ ไม่ทำลาย
 */

(function () {
  'use strict';

  /* ========================= Utilities ========================= */
  const $ = (selector, context = document) => context.querySelector(selector);
  const $$ = (selector, context = document) => [...context.querySelectorAll(selector)];
  const escapeHtml = (str) => {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  };

  /* ========================= Toast system ========================= */
  const toastQueue = [];
  let toastContainer;

  function getToastContainer() {
    if (!toastContainer) {
      toastContainer = document.createElement('nova-toast');
      document.body.appendChild(toastContainer);
    }
    return toastContainer;
  }

  const icons = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' };

  function showToast({ type = 'info', message, duration = 3500, icon } = {}) {
    const toast = document.createElement('nova-toast');
    toast.className = `toast-${type}`;
    toast.innerHTML = `
      <span class="nova-toast-icon">${icon || icons[type]}</span>
      <span class="nova-toast-message">${escapeHtml(message)}</span>
      <button class="nova-toast-close">&times;</button>
    `;
    const container = getToastContainer();
    container.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add('show'));

    let dismissed = false;
    toast.querySelector('.nova-toast-close').addEventListener('click', () => dismiss(toast));

    const timer = setTimeout(() => {
      if (!dismissed) dismiss(toast);
    }, duration);

    toast._timer = timer;
    toast.dismiss = () => { dismissed = true; clearTimeout(timer); };
    return toast;
  }

  function dismiss(toast) {
    if (!toast) return;
    toast.classList.remove('show');
    setTimeout(() => {
      const container = getToastContainer();
      if (container.contains(toast)) container.removeChild(toast);
      if (container.children.length === 0) toast.remove();
    }, 250);
  }

  window.novaToast = Object.assign(showToast, { dismiss, error: (m, d) => showToast({ type: 'error', message: m, duration: d }), success: (m, d) => showToast({ type: 'success', message: m, duration: d }), warning: (m, d) => showToast({ type: 'warning', message: m, duration: d }), info: (m, d) => showToast({ type: 'info', message: m, duration: d }) });

  /* ========================= Skeleton loader ========================= */
  function createSkeleton(options = {}) {
    const { lines = 1, widths = ['100%', '75%', '50%'], type = 'list', className = '' } = options;
    const container = document.createElement('nova-skeleton');
    container.className = `nova-skeleton ${type} ${className}`;
    if (type === 'image') container.style.height = '200px';

    for (let i = 0; i < lines; i++) {
      const line = document.createElement('nova-skeleton');
      line.className = `nova-skeleton line ${widths[i] || 'medium'}`;
      container.appendChild(line);
    }
    return container;
  }

  window.novaSkeleton = createSkeleton;

  /* ========================= Modal ========================= */
  const modals = [];
  let lastFocusedElement;

  function showModal(content, options = {}) {
    const { title, header, footer, size = '560px', backdrop = true, closeOnBackdrop = true, onClose } = options;
    lastFocusedElement = document.activeElement;

    const backdropEl = document.createElement('nova-modal-backdrop');
    backdropEl.style.zIndex = 'var(--nova-z-overlay)';
    if (backdrop) {
      backdropEl.innerHTML = `
        <nova-modal style="max-width: ${size}">
          ${header ? header : `
            <div class="nova-modal-header">
              <span>${title || 'Dialog'}</span>
              <button class="nova-modal-close">&times;</button>
            </div>
          `}
          <div class="nova-modal-body">${content}</div>
          ${footer ? `<div class="nova-modal-footer">${footer}</div>` : ''}
        </nova-modal>
      `;
    } else {
      backdropEl.innerHTML = `<nova-modal style="max-width: ${size}">${content}</nova-modal>`;
    }

    backdropEl.addEventListener('click', (e) => {
      if (closeOnBackdrop && e.target === backdropEl) closeModal(backdropEl);
    });
    backdropEl.querySelector('.nova-modal-close')?.addEventListener('click', () => closeModal(backdropEl));

    document.body.appendChild(backdropEl);
    requestAnimationFrame(() => backdropEl.classList.add('show'));

    const modal = { element: backdropEl, content: backdropEl.querySelector('nova-modal'), close: () => closeModal(backdropEl) };
    modals.push(modal);

    if (onClose) modal.close = () => { onClose(); closeModal(backdropEl); };
    return modal;
  }

  function closeModal(backdropEl) {
    if (!backdropEl) return;
    backdropEl.classList.remove('show');
    setTimeout(() => {
      backdropEl.remove();
      const idx = modals.findIndex(m => m.element === backdropEl);
      if (idx > -1) modals.splice(idx, 1);
      if (lastFocusedElement) lastFocusedElement.focus();
      if (modals.length === 0) {
        document.body.style.overflow = '';
      }
    }, 250);
  }

  function openModal(content, options) {
    return showModal(content, options);
  }

  window.novaModal = { open: openModal, close: closeModal, all: modals };

  /* ========================= Copy to clipboard ========================= */
  async function copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      return true;
    }
  }

  window.novaCopy = copyToClipboard;

  /* ========================= Auto-convert custom elements ========================= */
  const elementMap = {
    'nova-message': class NovaMessage extends HTMLElement {
      connectedCallback() {
        this.classList.add('nova-message');
        if (!this.querySelector('[slot="avatar"]')) {
          const avatar = document.createElement('nova-message-avatar');
          avatar.textContent = this.dataset.avatar || (this.classList.contains('user') ? 'U' : 'A');
          this.prepend(avatar);
        }
      }
    },
    'nova-tool-card': class NovaToolCard extends HTMLElement {
      connectedCallback() {
        this.classList.add('nova-tool-card');
        const status = this.dataset.status || 'running';
        if (status !== 'none') this.classList.add(status);
      }
    },
    'nova-tool-progress': class NovaToolProgress extends HTMLElement {
      connectedCallback() {
        this.classList.add('nova-tool-progress');
        this.style.width = '100%';
        this.innerHTML = `<nova-tool-progress-bar style="width: ${this.dataset.percent || 0}%"></nova-tool-progress-bar>`;
      }
    },
    'nova-typing-indicator': class NovaTypingIndicator extends HTMLElement {
      connectedCallback() {
        this.classList.add('nova-typing-indicator');
        this.innerHTML = '<nova-typing-dot></nova-typing-dot><nova-typing-dot></nova-typing-dot><nova-typing-dot></nova-typing-dot>';
      }
    },
    'nova-code-block': class NovaCodeBlock extends HTMLElement {
      async connectedCallback() {
        this.classList.add('nova-code-block');
        const lang = this.dataset.lang || 'code';
        const code = this.textContent.trim();
        this.innerHTML = `
          <div class="nova-code-header">
            <span class="nova-code-lang">${escapeHtml(lang)}</span>
            <button class="nova-code-copy" data-lang="${escapeHtml(lang)}">Copy</button>
          </div>
          <pre class="nova-code-body">${escapeHtml(code)}</pre>
        `;
        this.querySelector('.nova-code-copy').addEventListener('click', async () => {
          const btn = this.querySelector('.nova-code-copy');
          btn.textContent = 'Copied!';
          btn.classList.add('copied');
          await copyToClipboard(code);
          setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
        });
      }
    },
    'nova-skeleton': class NovaSkeleton extends HTMLElement {
      connectedCallback() {
        this.classList.add('nova-skeleton');
      }
    }
  };

  Object.entries(elementMap).forEach(([tag, cls]) => {
    if (!customElements.get(tag)) customElements.define(tag, cls);
  });

  /* ========================= Auto-run custom elements ========================= */
  function upgradeElements() {
    $$('#nova-message, nova-tool-card, nova-tool-progress, nova-typing-indicator, nova-code-block, nova-skeleton').forEach(el => {
      if (el instanceof HTMLElement && !el.isConnected || true) {
        if (!document.querySelector(`#${el.id}`)) { /* noop - customElements upgrades automatically */ }
      }
    });
  }

  document.addEventListener('DOMContentLoaded', upgradeElements);
  const observer = new MutationObserver(upgradeElements);
  observer.observe(document.body, { childList: true, subtree: true });
  upgradeElements();

  /* ========================= Export ========================= */
  window.nova = { toast: window.novaToast, modal: window.novaModal, skeleton: window.novaSkeleton, copy: window.novaCopy };
})();
