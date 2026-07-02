// ============ CampusConnect main.js ============

document.addEventListener('DOMContentLoaded', () => {
  initHamburger();
  initToasts();
  initNotifDropdown();
  initLiveSearch('navSearchInput', 'navSearchResults');
  initLiveSearch('mobileSearchInput', null);
  initPageLoader();
  initConfirmDeletes();
});

function initHamburger() {
  const btn = document.getElementById('hamburgerBtn');
  const menu = document.getElementById('mobileMenu');
  if (!btn || !menu) return;
  btn.addEventListener('click', () => {
    btn.classList.toggle('open');
    menu.classList.toggle('open');
  });
}

function initToasts() {
  document.querySelectorAll('.toast').forEach(toast => {
    const hideAfter = parseInt(toast.dataset.autohide || '6000', 10);
    const timer = setTimeout(() => dismissToast(toast), hideAfter);
    const closeBtn = toast.querySelector('.toast-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        clearTimeout(timer);
        dismissToast(toast);
      });
    }
  });
}

function dismissToast(toast) {
  toast.classList.add('hide');
  setTimeout(() => toast.remove(), 260);
}

window.showToast = function (message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const icons = { success: '✅', error: '⚠️', warning: '⚠️', info: 'ℹ️' };
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.dataset.autohide = '6000';
  toast.innerHTML = `<span class="toast-icon">${icons[type] || icons.info}</span><span class="toast-msg">${message}</span><button class="toast-close" aria-label="Dismiss">&times;</button>`;
  container.appendChild(toast);
  initToasts();
};

function initNotifDropdown() {
  const btn = document.getElementById('notifBtn');
  const dropdown = document.getElementById('notifDropdown');
  if (!btn || !dropdown) return;
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.classList.toggle('show');
  });
  document.addEventListener('click', (e) => {
    if (!dropdown.contains(e.target) && e.target !== btn) {
      dropdown.classList.remove('show');
    }
  });
}

function initLiveSearch(inputId, resultsId) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const resultsBox = resultsId ? document.getElementById(resultsId) : null;
  let debounceTimer;

  input.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const query = input.value.trim();
    if (query.length < 2) {
      if (resultsBox) resultsBox.classList.remove('show');
      return;
    }
    debounceTimer = setTimeout(() => runSearch(query, resultsBox), 250);
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      window.location.href = `/lost/?q=${encodeURIComponent(input.value.trim())}`;
    }
  });

  document.addEventListener('click', (e) => {
    if (resultsBox && !resultsBox.contains(e.target) && e.target !== input) {
      resultsBox.classList.remove('show');
    }
  });
}

function runSearch(query, resultsBox) {
  if (!resultsBox) return;
  fetch(`/api/search/?q=${encodeURIComponent(query)}`)
    .then(res => res.json())
    .then(data => {
      resultsBox.innerHTML = '';
      if (!data.results.length) {
        resultsBox.innerHTML = `<div class="nsr-empty">No items found for "${escapeHtml(query)}"</div>`;
      } else {
        data.results.forEach(item => {
          const a = document.createElement('a');
          a.href = item.url;
          a.className = 'nsr-item';
          a.innerHTML = `
            <div>
              <div style="font-weight:600;">${escapeHtml(item.title)}</div>
              <div style="color:var(--text-muted); font-size:.78rem;">${escapeHtml(item.location)}</div>
            </div>
            <span class="nsr-tag nsr-tag-${item.type.toLowerCase()}">${item.type}</span>
          `;
          resultsBox.appendChild(a);
        });
      }
      resultsBox.classList.add('show');
    })
    .catch(() => {});
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function initPageLoader() {
  const loader = document.getElementById('pageLoader');
  if (!loader) return;
  window.addEventListener('load', () => {
    setTimeout(() => loader.classList.add('hide'), 250);
  });
}

function initConfirmDeletes() {
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', (e) => {
      if (!confirm(el.dataset.confirm || 'Are you sure?')) {
        e.preventDefault();
      }
    });
  });
}
