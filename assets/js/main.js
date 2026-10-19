(function () {
  // 모바일 메뉴
  var btn = document.querySelector('.menu-btn');
  var gnb = document.querySelector('.gnb');
  if (btn && gnb) {
    btn.addEventListener('click', function () {
      var open = gnb.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // 메인 슬라이드
  var slides = document.querySelectorAll('.hero .slide');
  var dots = document.querySelectorAll('.hero .dots button');
  if (slides.length > 1) {
    var cur = 0, timer;
    var go = function (n) {
      slides[cur].classList.remove('on'); dots[cur].classList.remove('on');
      cur = (n + slides.length) % slides.length;
      slides[cur].classList.add('on'); dots[cur].classList.add('on');
    };
    var start = function () { timer = setInterval(function () { go(cur + 1); }, 5000); };
    dots.forEach(function (d, i) { d.addEventListener('click', function () { clearInterval(timer); go(i); start(); }); });
    start();
  }

  // 퀵메뉴 슬라이드
  var track = document.querySelector('.q-track ul');
  if (track) {
    var pos = 0;
    var move = function (dir) {
      var items = track.children.length;
      var per = window.innerWidth <= 860 ? 2 : 4;
      var max = Math.max(0, items - per);
      pos = Math.min(max, Math.max(0, pos + dir));
      track.style.transform = 'translateX(' + (-pos * 100 / per) + '%)';
    };
    document.querySelector('.q-prev').addEventListener('click', function () { move(-1); });
    document.querySelector('.q-next').addEventListener('click', function () { move(1); });
  }

  // 게시판 목록: 검색과 페이지 나누기
  var table = document.querySelector('.board-table');
  if (table) {
    var per = parseInt(table.getAttribute('data-paged'), 10) || 10;
    var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));
    var input = document.getElementById('q');
    var paging = document.querySelector('.paging');
    var cnt = document.querySelector('.cnt');
    var empty = document.querySelector('.board-empty');
    var filtered = rows, page = 1;

    var render = function () {
      var pages = Math.max(1, Math.ceil(filtered.length / per));
      if (page > pages) page = pages;
      rows.forEach(function (r) { r.style.display = 'none'; });
      filtered.slice((page - 1) * per, page * per).forEach(function (r) { r.style.display = ''; });
      cnt.textContent = filtered.length;
      empty.hidden = filtered.length > 0;
      paging.innerHTML = '';
      if (pages > 1) {
        for (var i = 1; i <= pages; i++) {
          var b = document.createElement('button');
          b.type = 'button'; b.textContent = i;
          if (i === page) b.className = 'on';
          b.addEventListener('click', (function (n) { return function () { page = n; render(); }; })(i));
          paging.appendChild(b);
        }
      }
    };
    var search = function () {
      var q = input.value.trim().toLowerCase();
      filtered = rows.filter(function (r) { return !q || r.textContent.toLowerCase().indexOf(q) > -1; });
      page = 1; render();
    };
    input.addEventListener('input', search);
    input.form.addEventListener('submit', search);
    render();
  }
})();
