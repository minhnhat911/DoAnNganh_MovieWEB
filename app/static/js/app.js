// ===== Helpers =====
const $  = (sel, root=document) => root.querySelector(sel);
const $$ = (sel, root=document) => Array.from(root.querySelectorAll(sel));

// ===== FOOTER: năm + back-to-top =====
(() => {
  const yearEl = $('#year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  const backTop = $('.back-to-top');
  if (backTop) {
    backTop.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
})();

// ===== RANK: carousel ngang =====
(() => {
  const container = $('.carousel-container');
  const leftBtn   = $('#left-btn');
  const rightBtn  = $('#right-btn');
  if (!container || !leftBtn || !rightBtn) return;

  leftBtn.addEventListener('click', () => {
    container.scrollBy({ left: -200, behavior: 'smooth' });
  });
  rightBtn.addEventListener('click', () => {
    container.scrollBy({ left: 200, behavior: 'smooth' });
  });
})();

// ===== HERO SLIDER =====
(() => {
  const slider = $('#heroSlider');
  if (!slider) return; // trang không có slider thì bỏ qua

  const track  = $('.track', slider);
  const slides = track ? Array.from(track.children) : [];
  const prevBtn= $('.prev', slider);
  const nextBtn= $('.next', slider);
  const dotsBox= $('.dots', slider);
  if (!track || slides.length === 0 || !dotsBox) return;

  let index = 0;
  const total = slides.length;
  const AUTOPLAY_MS = 3000;

  // Tạo dots
  const dots = slides.map((_, i) => {
    const b = document.createElement('button');
    b.setAttribute('aria-label', `Tới slide ${i + 1}`);
    b.addEventListener('click', () => goTo(i));
    dotsBox.appendChild(b);
    return b;
  });

  function update() {
    track.style.transform = `translateX(-${index * 100}%)`;
    dots.forEach((d, i) => d.classList.toggle('active', i === index));
  }
  function goTo(i) { index = (i + total) % total; update(); resetAutoplay(); }
  const next = () => goTo(index + 1);
  const prev = () => goTo(index - 1);

  if (prevBtn) prevBtn.addEventListener('click', prev);
  if (nextBtn) nextBtn.addEventListener('click', next);

  // Autoplay + pause khi hover
  let timer = setInterval(next, AUTOPLAY_MS);
  function resetAutoplay() { clearInterval(timer); timer = setInterval(next, AUTOPLAY_MS); }
  slider.addEventListener('mouseenter', () => clearInterval(timer));
  slider.addEventListener('mouseleave', resetAutoplay);

  // Vuốt mobile
  let startX = 0, deltaX = 0, isTouch = false;
  slider.addEventListener('touchstart', (e) => {
    isTouch = true; startX = e.touches[0].clientX; deltaX = 0; clearInterval(timer);
  }, { passive: true });
  slider.addEventListener('touchmove', (e) => { if (isTouch) deltaX = e.touches[0].clientX - startX; }, { passive: true });
  slider.addEventListener('touchend', () => {
    if (!isTouch) return;
    const THRESHOLD = 50;
    if (deltaX > THRESHOLD) prev();
    else if (deltaX < -THRESHOLD) next();
    isTouch = false; resetAutoplay();
  });

  // Phím mũi tên
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft')  prev();
    if (e.key === 'ArrowRight') next();
  });

  update();
})();

// ===== BOOTSTRAP DROPDOWN: đồng bộ hidden <-> show =====
(() => {
  // Ẩn cứng tất cả menu ngay khi load (phòng CSS khác làm hiện)
  $$('.dropdown-menu').forEach(m => m.setAttribute('hidden',''));

  $$('.dropdown').forEach(dd => {
    dd.addEventListener('show.bs.dropdown', () => {
      dd.querySelector('.dropdown-menu')?.removeAttribute('hidden');
    });
    dd.addEventListener('hide.bs.dropdown', () => {
      setTimeout(() => dd.querySelector('.dropdown-menu')?.setAttribute('hidden',''), 0);
    });
  });
})();

//VIDEO
// VIDEO
document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('myVideo');
    const episodeButtons = document.querySelectorAll('.episode-button');
    const videoSection = document.getElementById('videoSection'); // Giả định bạn có một div bao quanh video player

    if (!video || episodeButtons.length === 0) {
        console.warn('Không tìm thấy #myVideo hoặc nút tập phim.');
        return;
    }

    // Nhấp đúp để fullscreen
    video.addEventListener('dblclick', () => {
        if (video.requestFullscreen) video.requestFullscreen();
        else if (video.webkitRequestFullscreen) video.webkitRequestFullscreen();
        else if (video.msRequestFullscreen) video.msRequestFullscreen();
    });

    //
    episodeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const src = this.dataset.src;
            const episodeNumber = this.dataset.episodeNumber;

            if (!src) {
                console.warn(`Thiếu data-src trên Tập ${episodeNumber}`);
                return;
            }

            //
            if (videoSection) {
                videoSection.style.display = 'block';
            }
            window.scrollTo({ top: 140, behavior: 'smooth' });

            //

            // Xóa tất cả các thẻ <source> cũ
            while (video.firstChild) {
                video.removeChild(video.firstChild);
            }

            const source = document.createElement('source');
            source.src  = src;
            source.type = src.endsWith('.mp4') ? 'video/mp4' : '';

            // Tùy chọn: nếu bạn dùng HLS/DASH, cần thêm logic kiểm tra type khác ở đây

            source.onerror = () => console.error('Không load được nguồn video:', src);
            video.appendChild(source);

            video.load();
            video.play().catch(err => console.log('Không auto play được:', err));

            // 3. Cập nhật trạng thái nút (Tùy chọn)
            episodeButtons.forEach(btn => btn.classList.remove('btn-warning'));
            this.classList.add('btn-warning');

            console.log(`Đã tải Tập ${episodeNumber} từ nguồn: ${src}`);
        });
    });
});

function showEditForm(commentId) {
    document.getElementById('edit-form-' + commentId).style.display = 'block';
}
function hideEditForm(commentId) {
    document.getElementById('edit-form-' + commentId).style.display = 'none';
}

// ===== CSRF =====
function getCsrfToken() {
  const el = document.querySelector('meta[name="csrf-token"]');
  return el ? el.getAttribute('content') : null;
}

// ===== POST /watch/<episode_id> với progress (giây) =====
async function updateWatchProgress(episodeId, progressSeconds) {
  try {
    const headers = { "Content-Type": "application/json" };
    const csrf = getCsrfToken();
    if (csrf) headers["X-CSRFToken"] = csrf;

    const res = await fetch(`/watch/${episodeId}`, {
      method: "POST",
      headers,
      credentials: "same-origin",
      body: JSON.stringify({ progress: Math.floor(progressSeconds || 0) })
    });
    return res.ok;
  } catch (e) {
    console.error("[Progress Save] error:", e);
    return false;
  }
}

let saveInterval = null;
let currentEpisodeId = null;
let lastSentAt = 0;

// ===== Bắt đầu theo dõi tiến trình cho 1 episode + 1 player =====
function startProgressTracking(episodeId, player) {
  currentEpisodeId = episodeId;

  // clear interval cũ
  if (saveInterval) clearInterval(saveInterval);
  lastSentAt = 0;

  // gửi 0s ngay khi bắt đầu để có record
  updateWatchProgress(episodeId, 0);

  // lưu theo chu kỳ + khi pause/ended/timeupdate (throttle)
  const INTERVAL_MS = 10000;

  const onTimeUpdate = () => {
    const now = Date.now();
    if (now - lastSentAt >= INTERVAL_MS && !player.paused && player.readyState >= 2) {
      updateWatchProgress(episodeId, player.currentTime);
      lastSentAt = now;
    }
  };

  const onPause = () => updateWatchProgress(episodeId, player.currentTime);
  const onEnded = () => {
    updateWatchProgress(episodeId, player.duration || player.currentTime);
    if (saveInterval) clearInterval(saveInterval);
    player.removeEventListener('timeupdate', onTimeUpdate);
    player.removeEventListener('pause', onPause);
    player.removeEventListener('ended', onEnded);
  };

  player.addEventListener('timeupdate', onTimeUpdate);
  player.addEventListener('pause', onPause, { once: false });
  player.addEventListener('ended', onEnded, { once: true });

  saveInterval = setInterval(() => {
    if (!player.paused && player.readyState >= 2) {
      updateWatchProgress(episodeId, player.currentTime);
    }
  }, INTERVAL_MS);
}

// ===== Main: khởi tạo và gắn cho các nút tập =====
document.addEventListener("DOMContentLoaded", async function () {
  const section = document.getElementById("videoSection");
  const player  = document.getElementById("myVideo");
  if (!player) {
    console.error("Khong tim thay #myVideo");
    return;
  }

  // Nếu đã có data-* trên thẻ video, cấu hình phát sẵn
  const initialEpisodeId = player.getAttribute("data-episode-id");
  const initialSrc       = player.getAttribute("data-video-src");
  const resumeSeconds    = parseFloat(player.getAttribute("data-resume-position") || "0");

  if (initialEpisodeId && initialSrc) {
    player.src = initialSrc;
    player.load();
    player.addEventListener('loadedmetadata', () => {
      if (resumeSeconds > 0 && resumeSeconds < (player.duration || Infinity)) {
        player.currentTime = resumeSeconds;
      }
    }, { once: true });
    try { await player.play(); } catch(_) {}
    startProgressTracking(initialEpisodeId, player);
    if (section && section.style.display === "none") section.style.display = "";
  }

  // Gắn cho các nút tập
  document.querySelectorAll(".episode-button").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault?.();

      const episodeId = btn.getAttribute("data-episode-id"); // bắt buộc id thật
      const src = btn.getAttribute("data-src");
      if (!episodeId || !src) {
        console.warn("Thieu data-episode-id hoac data-src tren nut tap");
        return;
      }

      // cập nhật player + bật player section nếu đang ẩn
      player.src = src;
      player.load();
      try { await player.play(); } catch(_) {}

      if (section && section.style.display === "none") section.style.display = "";

      // Bắt đầu tracking cho tập mới
      startProgressTracking(episodeId, player);
    });
  });
});





