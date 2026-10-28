/* ═══════════════════════════════════════════════════════════════
   Physics Teacher Portfolio — Main JavaScript
   ═══════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
  // ── Particle Background ──
  initParticles();

  // ── Navbar Scroll Effect ──
  initNavbar();

  // ── Mobile Menu ──
  initMobileMenu();

  // ── Counter Animation ──
  initCounters();

  // ── Testimonials Slider ──
  initTestimonials();

  // ── Scroll Reveal ──
  initScrollReveal();

  // ── Contact Form ──
  initContactForm();

  // ── Active Nav Highlighting ──
  initActiveNav();
});

/* ────────────────────────────────────────────
   Particle Background
   ──────────────────────────────────────────── */
function initParticles() {
  const canvas = document.getElementById('particles-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let particles = [];
  const PARTICLE_COUNT = 60;
  const MAX_DISTANCE = 120;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  class Particle {
    constructor() {
      this.reset();
    }
    reset() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.vx = (Math.random() - 0.5) * 0.4;
      this.vy = (Math.random() - 0.5) * 0.4;
      this.radius = Math.random() * 2 + 0.5;
      this.opacity = Math.random() * 0.5 + 0.1;
      // Cyan or indigo
      this.color = Math.random() > 0.5 ? '56,189,248' : '129,140,248';
    }
    update() {
      this.x += this.vx;
      this.y += this.vy;
      if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
      if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.color}, ${this.opacity})`;
      ctx.fill();
    }
  }

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push(new Particle());
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(p => {
      p.update();
      p.draw();
    });

    // Draw connections
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < MAX_DISTANCE) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          const opacity = (1 - dist / MAX_DISTANCE) * 0.15;
          ctx.strokeStyle = `rgba(56,189,248,${opacity})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }

    requestAnimationFrame(animate);
  }
  animate();
}

/* ────────────────────────────────────────────
   Navbar Scroll
   ──────────────────────────────────────────── */
function initNavbar() {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;

  const onScroll = () => {
    if (window.scrollY > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/* ────────────────────────────────────────────
   Mobile Menu
   ──────────────────────────────────────────── */
function initMobileMenu() {
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('nav-links');
  if (!hamburger || !navLinks) return;

  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    navLinks.classList.toggle('open');
  });

  // Close menu on link click
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('open');
      navLinks.classList.remove('open');
    });
  });
}

/* ────────────────────────────────────────────
   Counter Animation
   ──────────────────────────────────────────── */
function initCounters() {
  const counters = document.querySelectorAll('.stat-num');
  if (!counters.length) return;

  let animated = false;

  function animateCounters() {
    if (animated) return;
    const triggerBottom = window.innerHeight * 0.85;

    counters.forEach(counter => {
      const rect = counter.getBoundingClientRect();
      if (rect.top < triggerBottom) {
        animated = true;
        const target = parseFloat(counter.dataset.target) || 0;
        const decimals = parseInt(counter.dataset.decimals) || 0;
        const prefix = counter.dataset.prefix || '';
        const suffix = counter.dataset.suffix || '';
        const duration = 2000;
        const startTime = performance.now();

        function step(now) {
          const elapsed = now - startTime;
          const progress = Math.min(elapsed / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          const currentVal = (target * eased).toFixed(decimals);
          counter.textContent = `${prefix}${Number(currentVal).toLocaleString()}${suffix}`;
          if (progress < 1) {
            requestAnimationFrame(step);
          } else {
            counter.textContent = `${prefix}${target.toLocaleString()}${suffix}`;
          }
        }
        requestAnimationFrame(step);
      }
    });
  }

  window.addEventListener('scroll', animateCounters, { passive: true });
  animateCounters(); // initial check
}

/* ────────────────────────────────────────────
   Testimonials Slider
   ──────────────────────────────────────────── */
function initTestimonials() {
  const cards = document.querySelectorAll('.testimonial-card');
  const dotsContainer = document.getElementById('test-dots');
  const prevBtn = document.getElementById('test-prev');
  const nextBtn = document.getElementById('test-next');
  if (!cards.length || !dotsContainer) return;

  let current = 0;

  // Create dots
  cards.forEach((_, i) => {
    const dot = document.createElement('span');
    dot.classList.add('dot');
    if (i === 0) dot.classList.add('active');
    dot.addEventListener('click', () => goTo(i));
    dotsContainer.appendChild(dot);
  });

  function goTo(index) {
    cards[current].classList.remove('active');
    dotsContainer.children[current].classList.remove('active');
    current = index;
    cards[current].classList.add('active');
    dotsContainer.children[current].classList.add('active');
  }

  prevBtn.addEventListener('click', () => {
    goTo((current - 1 + cards.length) % cards.length);
  });
  nextBtn.addEventListener('click', () => {
    goTo((current + 1) % cards.length);
  });

  // Auto-advance every 6 seconds
  setInterval(() => {
    goTo((current + 1) % cards.length);
  }, 6000);
}

/* ────────────────────────────────────────────
   Scroll Reveal
   ──────────────────────────────────────────── */
function initScrollReveal() {
  // Add .reveal class to animatable elements
  const selectors = [
    '.about-text', '.detail-card',
    '.phil-card', '.philosophy-quote',
    '.subject-card',
    '.timeline-item',
    '.research-card',
    '.skill-category-card',
    '.achievement-card',
    '.resource-card',
    '.interest-chip',
    '.contact-info', '.contact-form'
  ];

  selectors.forEach(sel => {
    document.querySelectorAll(sel).forEach((el, i) => {
      el.classList.add('reveal');
      el.style.transitionDelay = `${i * 80}ms`;
    });
  });

  function checkReveal() {
    const reveals = document.querySelectorAll('.reveal');
    const triggerBottom = window.innerHeight * 0.88;

    reveals.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < triggerBottom) {
        el.classList.add('visible');
      }
    });
  }

  window.addEventListener('scroll', checkReveal, { passive: true });
  checkReveal(); // initial check
}

/* ────────────────────────────────────────────
   Contact Form
   ──────────────────────────────────────────── */
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.textContent;
    btn.textContent = 'Sending…';
    btn.disabled = true;

    // Simulate sending
    setTimeout(() => {
      btn.textContent = '✓ Message Sent!';
      btn.style.background = 'linear-gradient(135deg, #34d399, #059669)';
      form.reset();

      setTimeout(() => {
        btn.textContent = originalText;
        btn.style.background = '';
        btn.disabled = false;
      }, 3000);
    }, 1500);
  });
}

/* ────────────────────────────────────────────
   Active Nav Link Highlighting
   ──────────────────────────────────────────── */
function initActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');

  function onScroll() {
    let scrollY = window.scrollY + 120;

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollY >= top && scrollY < top + height) {
        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          }
        });
      }
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
}
