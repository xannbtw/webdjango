// Admin Panel JS

document.addEventListener('DOMContentLoaded', function () {

  // ── Sidebar toggle (mobile) ─────────────────────────────
  const sidebar  = document.getElementById('sidebar');
  const overlay  = document.getElementById('sidebarOverlay');
  const menuBtn  = document.getElementById('menuBtn');
  const closeBtn = document.getElementById('sidebarToggle');

  function openSidebar() {
    sidebar.classList.add('open');
    overlay.classList.add('open');
  }
  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('open');
  }

  if (menuBtn)  menuBtn.addEventListener('click', openSidebar);
  if (closeBtn) closeBtn.addEventListener('click', closeSidebar);
  if (overlay)  overlay.addEventListener('click', closeSidebar);

  // ── Auto-dismiss messages after 5s ─────────────────────
  document.querySelectorAll('.alert').forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity 0.4s';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 400);
    }, 5000);
  });

  // ── Confirm delete links ────────────────────────────────
  document.querySelectorAll('.action-btn--danger').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!confirm('¿Seguro que quieres eliminar este elemento?')) {
        e.preventDefault();
      }
    });
  });

});
