/* ═══════════════════════════════════════════════════════════
   CodeLearn — Global JS Utilities
═══════════════════════════════════════════════════════════ */

'use strict';

/* ── Auth helpers ── */
const Auth = {
  isLoggedIn: () => localStorage.getItem('cl_logged') === 'true',
  getUser:    () => JSON.parse(localStorage.getItem('cl_user') || '{}'),
  setUser:    (u) => localStorage.setItem('cl_user', JSON.stringify(u)),
  login: (email, password) => {
    // Mock login — replace with real API
    const user = {
      id:       'u_001',
      name:     email.split('@')[0].replace(/[._]/g,' ').replace(/\b\w/g, c => c.toUpperCase()),
      email:    email,
      role:     'student',
      avatar:   email.substring(0,2).toUpperCase(),
      xp:       1250,
      level:    4,
      streak:   7,
      joinedAt: new Date().toISOString(),
    };
    localStorage.setItem('cl_logged', 'true');
    localStorage.setItem('cl_user', JSON.stringify(user));
    return user;
  },
  logout: () => {
    localStorage.removeItem('cl_logged');
    localStorage.removeItem('cl_user');
    window.location.href = '/pages/auth/login.html';
  },
  requireAuth: () => {
    if (!Auth.isLoggedIn()) {
      window.location.href = '/pages/auth/login.html';
      return false;
    }
    return true;
  }
};

/* ── Toast notifications ── */
const Toast = {
  container: null,
  init() {
    if (!this.container) {
      this.container = document.getElementById('toast-container');
      if (!this.container) {
        this.container = document.createElement('div');
        this.container.id = 'toast-container';
        document.body.appendChild(this.container);
      }
    }
  },
  show(msg, type = 'info', duration = 3000) {
    this.init();
    const icons = { success: '✓', error: '✕', info: 'ℹ', warning: '⚠' };
    const el = document.createElement('div');
    el.className = `toast-item ${type}`;
    el.innerHTML = `<span>${icons[type] || 'ℹ'}</span><span>${msg}</span>`;
    this.container.appendChild(el);
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transform = 'translateX(20px)';
      el.style.transition = '.3s ease';
      setTimeout(() => el.remove(), 300);
    }, duration);
  },
  success: (msg) => Toast.show(msg, 'success'),
  error:   (msg) => Toast.show(msg, 'error'),
  info:    (msg) => Toast.show(msg, 'info'),
};

/* ── Navbar user render ── */
function renderNavUser() {
  const user = Auth.getUser();
  const nameEl   = document.getElementById('nav-user-name');
  const avatarEl = document.getElementById('nav-avatar');
  if (nameEl)   nameEl.textContent   = user.name || 'Utilisateur';
  if (avatarEl) avatarEl.textContent = user.avatar || user.name?.substring(0,2).toUpperCase() || '?';
}

/* ── Sidebar active link ── */
function setActiveSidebarItem() {
  const path = window.location.pathname;
  document.querySelectorAll('.sidebar-item').forEach(item => {
    const href = item.getAttribute('href') || '';
    if (href && path.includes(href.split('/').pop().replace('.html',''))) {
      item.classList.add('active');
    }
  });
}

/* ── Progress bar animate ── */
function animateProgressBars() {
  document.querySelectorAll('.cl-progress-fill[data-width]').forEach(bar => {
    setTimeout(() => {
      bar.style.width = bar.dataset.width + '%';
    }, 300);
  });
}

/* ── Number counter animation ── */
function animateCounters() {
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseInt(el.dataset.count);
    const duration = 1200;
    const step = target / (duration / 16);
    let current = 0;
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = Math.floor(current).toLocaleString();
      if (current >= target) clearInterval(timer);
    }, 16);
  });
}

/* ── On DOM ready ── */
document.addEventListener('DOMContentLoaded', () => {
  renderNavUser();
  setActiveSidebarItem();
  animateProgressBars();
  animateCounters();
});
