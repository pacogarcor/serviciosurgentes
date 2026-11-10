(function () {
  // Menú móvil
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open);
    });
  }

  // Desplegable de provincias
  var drop = document.querySelector('.drop');
  if (drop) {
    var btn = drop.querySelector('.drop__btn');
    var filter = drop.querySelector('.drop__filter');
    var items = drop.querySelectorAll('.drop__list li');
    var setOpen = function (v) {
      drop.classList.toggle('is-open', v);
      btn.setAttribute('aria-expanded', v);
      if (v && window.innerWidth > 860) setTimeout(function () { filter.focus(); }, 50);
    };
    btn.addEventListener('click', function (e) { e.stopPropagation(); setOpen(!drop.classList.contains('is-open')); });
    document.addEventListener('click', function (e) { if (!drop.contains(e.target)) setOpen(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
    filter.addEventListener('input', function () {
      var q = norm(filter.value);
      items.forEach(function (li) { li.style.display = norm(li.textContent).indexOf(q) > -1 ? '' : 'none'; });
    });
  }

  function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').trim(); }

  // Buscador de la portada
  var form = document.getElementById('buscador');
  if (form) {
    var input = document.getElementById('q');
    var opts = document.querySelectorAll('#lista-provincias option');
    var err = form.querySelector('.search__err');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = norm(input.value), hit = null;
      opts.forEach(function (o) { if (!hit && norm(o.value) === q) hit = o; });
      if (!hit) opts.forEach(function (o) { if (!hit && norm(o.value).indexOf(q) === 0) hit = o; });
      if (hit) { window.location.href = 'provincias/' + hit.dataset.slug + '.html'; }
      else { err.hidden = false; }
    });
    input.addEventListener('input', function () { err.hidden = true; });
  }

  // Filtro del cuadrante de provincias
  var filtro = document.getElementById('filtro');
  if (filtro) {
    var cells = document.querySelectorAll('.pcell');
    var vacio = document.getElementById('sin-resultados');
    filtro.addEventListener('input', function () {
      var q = norm(filtro.value), n = 0;
      cells.forEach(function (c) {
        var ok = norm(c.textContent).indexOf(q) > -1;
        c.classList.toggle('is-hidden', !ok); if (ok) n++;
      });
      vacio.hidden = n > 0;
    });
  }
})();
