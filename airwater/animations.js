/* AquaFuture motion layer — CSS + rAF + IntersectionObserver */
(function () {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const RESULT_IDS = ['roi', 'npv', 'irr', 'ebitda', 'annualRevenue', 'annualProfit', 'paybackPeriod', 'totalProfit'];

    function prefersReduce() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    function parseNumeric(text) {
        if (!text || text === '—' || text === '-') return null;
        const cleaned = String(text).replace(/[^0-9.,\-]/g, '').replace(/,/g, '');
        const n = parseFloat(cleaned);
        return Number.isFinite(n) ? n : null;
    }

    function isNegativeMetric(text) {
        const t = String(text || '').trim();
        if (!t || t === '—') return false;
        return /^-/.test(t.replace(/\s/g, '')) || /\(\s*-/.test(t);
    }

    function animateValue(el, start, end, duration, formatter) {
        if (prefersReduce() || !el) {
            if (el && formatter) el.textContent = formatter(end);
            return;
        }
        let startTs = null;
        const step = (ts) => {
            if (!startTs) startTs = ts;
            const p = Math.min((ts - startTs) / duration, 1);
            const eased = 1 - Math.pow(1 - p, 3);
            const val = start + (end - start) * eased;
            el.textContent = formatter ? formatter(val) : String(Math.round(val));
            if (p < 1) requestAnimationFrame(step);
            else el.textContent = formatter ? formatter(end) : String(Math.round(end));
        };
        requestAnimationFrame(step);
    }

    /* ── Hero particles (canvas, <5KB logic) ── */
    function initHeroParticles() {
        const canvas = document.getElementById('heroParticles');
        if (!canvas || prefersReduce()) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let w = 0, h = 0, raf = 0;
        const drops = [];
        const COUNT = Math.min(48, Math.floor((window.innerWidth * window.innerHeight) / 28000) + 18);

        function resize() {
            const rect = canvas.parentElement.getBoundingClientRect();
            w = canvas.width = Math.floor(rect.width * devicePixelRatio);
            h = canvas.height = Math.floor(rect.height * devicePixelRatio);
            canvas.style.width = rect.width + 'px';
            canvas.style.height = rect.height + 'px';
        }

        function spawn(i) {
            drops[i] = {
                x: Math.random() * w,
                y: Math.random() * h,
                r: (1 + Math.random() * 2.2) * devicePixelRatio,
                vy: (0.15 + Math.random() * 0.45) * devicePixelRatio,
                vx: (Math.random() - 0.5) * 0.2 * devicePixelRatio,
                a: 0.18 + Math.random() * 0.35
            };
        }

        function tick() {
            ctx.clearRect(0, 0, w, h);
            for (let i = 0; i < drops.length; i++) {
                const d = drops[i];
                d.y += d.vy;
                d.x += d.vx + Math.sin((d.y + i * 12) * 0.002) * 0.15;
                if (d.y > h + 10) spawn(i);
                ctx.beginPath();
                ctx.fillStyle = `rgba(11, 107, 203, ${d.a})`;
                ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
                ctx.fill();
            }
            raf = requestAnimationFrame(tick);
        }

        resize();
        for (let i = 0; i < COUNT; i++) spawn(i);
        tick();
        window.addEventListener('resize', () => {
            cancelAnimationFrame(raf);
            resize();
            for (let i = 0; i < COUNT; i++) spawn(i);
            tick();
        }, { passive: true });
    }

    /* ── Reveal on scroll ── */
    function initReveal() {
        const nodes = document.querySelectorAll(
            '.reveal, .about-card, .trust-card, .advantage-item, .bali-stat, .compare-card, .result-card, .breakdown-item, .timeline-item'
        );
        nodes.forEach((el) => {
            if (!el.classList.contains('reveal') && !el.classList.contains('breakdown-item') && !el.classList.contains('timeline-item')) {
                el.classList.add('reveal');
            }
        });

        if (prefersReduce()) {
            document.querySelectorAll('.reveal, .breakdown-item, .timeline-item').forEach((el) => {
                el.classList.add('is-visible');
                if (el.classList.contains('timeline-item')) el.classList.add('is-active');
            });
            return;
        }

        const io = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                const el = entry.target;
                const delay = Number(el.dataset.revealDelay || 0);
                setTimeout(() => {
                    el.classList.add('is-visible');
                    if (el.classList.contains('timeline-item')) el.classList.add('is-active');
                }, delay);
                io.unobserve(el);
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

        document.querySelectorAll('.reveal, .breakdown-item, .timeline-item').forEach((el, i) => {
            if (el.parentElement && el.parentElement.classList.contains('about-grid')) {
                el.dataset.revealDelay = String((i % 4) * 70);
            } else if (el.parentElement && (el.parentElement.classList.contains('trust-grid') || el.parentElement.classList.contains('bali-stats'))) {
                el.dataset.revealDelay = String((i % 6) * 60);
            }
            io.observe(el);
        });
    }

    /* ── Roadmap progress line ── */
    function initTimelineProgress() {
        const timeline = document.getElementById('roadmapTimeline');
        const bar = document.getElementById('timelineProgress');
        if (!timeline || !bar || prefersReduce()) return;

        const items = [...timeline.querySelectorAll('.timeline-item')];
        function update() {
            const rect = timeline.getBoundingClientRect();
            const view = window.innerHeight * 0.55;
            let progress = 0;
            if (rect.top < view && rect.bottom > 0) {
                const total = rect.height;
                const scrolled = Math.min(Math.max(view - rect.top, 0), total);
                progress = scrolled / total;
            }
            bar.style.height = Math.max(0, Math.min(1, progress)) * (timeline.offsetHeight - 40) + 'px';
            items.forEach((item) => {
                const r = item.getBoundingClientRect();
                if (r.top < view) item.classList.add('is-active');
            });
        }
        window.addEventListener('scroll', update, { passive: true });
        update();
    }

    /* ── Calc result semantics + count-up via MutationObserver ── */
    function applyMetricSemantics(el) {
        if (!el) return;
        const card = el.closest('.result-card');
        if (!card) return;
        card.classList.toggle('is-negative', isNegativeMetric(el.textContent));
    }

    function flashResult(el) {
        if (!el || prefersReduce()) return;
        el.animate(
            [{ transform: 'scale(1)' }, { transform: 'scale(1.04)' }, { transform: 'scale(1)' }],
            { duration: 320, easing: 'cubic-bezier(0.22, 1, 0.36, 1)' }
        );
    }

    function initResultObserver() {
        RESULT_IDS.forEach((id) => {
            const el = document.getElementById(id);
            if (!el) return;
            let last = el.textContent;
            const mo = new MutationObserver(() => {
                const next = el.textContent;
                if (next === last) return;
                const prevNum = parseNumeric(last);
                const nextNum = parseNumeric(next);
                const suffix = String(next).replace(/^[\s$€₽\-0-9.,]+/, '') || (String(next).includes('%') ? '%' : '');
                const prefix = String(next).trim().startsWith('$') ? '$' : '';
                last = next;
                applyMetricSemantics(el);
                flashResult(el);

                if (nextNum !== null && prevNum !== null && !prefersReduce() && Math.abs(nextNum - prevNum) > 0.001) {
                    const decimals = String(next).includes('.') ? 1 : 0;
                    animateValue(el, prevNum, nextNum, 650, (v) => {
                        const abs = Math.abs(v);
                        let body;
                        if (prefix === '$') {
                            body = Math.round(v).toLocaleString('en-US');
                            return (v < 0 ? '-$' : '$') + Math.abs(Math.round(v)).toLocaleString('en-US');
                        }
                        body = decimals ? v.toFixed(1) : Math.round(v).toLocaleString('en-US');
                        if (String(next).includes('%')) return body + '%';
                        return body + (suffix && !suffix.includes('%') ? (String(next).match(/\s+.+$/)?.[0] || '') : '');
                    });
                    // After animation, restore exact formatted string from calculator
                    setTimeout(() => { el.textContent = next; last = next; applyMetricSemantics(el); }, 680);
                }
            });
            mo.observe(el, { characterData: true, childList: true, subtree: true });
            applyMetricSemantics(el);
        });
    }

    function onCalcUpdate() {
        RESULT_IDS.forEach((id) => applyMetricSemantics(document.getElementById(id)));
    }

    /* ── Sticky mobile CTA ── */
    function initStickyCta() {
        const cta = document.getElementById('mobileStickyCta');
        const heroCta = document.querySelector('.hero .cta-button');
        const contact = document.getElementById('contact');
        if (!cta || !heroCta) return;

        const io = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                const heroVisible = entry.target === heroCta.closest('.hero') && entry.isIntersecting;
                const contactVisible = entry.target === contact && entry.isIntersecting;
                if (entry.target.classList?.contains('hero') || entry.target === document.getElementById('top')) {
                    cta.classList.toggle('is-visible', !entry.isIntersecting && window.innerWidth < 640);
                }
                if (entry.target === contact) {
                    if (entry.isIntersecting) cta.classList.remove('is-visible');
                }
            });
        }, { threshold: 0.15 });

        const hero = document.getElementById('top');
        if (hero) io.observe(hero);
        if (contact) io.observe(contact);

        window.addEventListener('resize', () => {
            if (window.innerWidth >= 640) cta.classList.remove('is-visible');
        }, { passive: true });
    }

    /* ── Nav burger ── */
    function initMobileNav() {
        const burger = document.getElementById('navBurger');
        const drawer = document.getElementById('navDrawer');
        const backdrop = document.getElementById('navDrawerBackdrop');
        const navbar = document.getElementById('navbar');
        if (!burger || !drawer) return;

        function setOpen(open) {
            burger.setAttribute('aria-expanded', open ? 'true' : 'false');
            drawer.classList.toggle('is-open', open);
            if (open) {
                drawer.hidden = false;
                document.body.classList.add('nav-locked');
            } else {
                document.body.classList.remove('nav-locked');
                setTimeout(() => {
                    if (!drawer.classList.contains('is-open')) drawer.hidden = true;
                }, 420);
            }
        }

        burger.addEventListener('click', () => {
            setOpen(burger.getAttribute('aria-expanded') !== 'true');
        });
        backdrop?.addEventListener('click', () => setOpen(false));
        drawer.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setOpen(false)));

        window.addEventListener('scroll', () => {
            navbar?.classList.toggle('is-scrolled', window.scrollY > 24);
        }, { passive: true });
    }

    function wrapCalculateROI() {
        if (typeof window.calculateROI !== 'function') return;
        const orig = window.calculateROI;
        window.calculateROI = function wrappedCalculateROI() {
            const result = orig.apply(this, arguments);
            onCalcUpdate();
            return result;
        };
    }

    function wrapComparison() {
        if (typeof window.updateComparison !== 'function') return;
        const orig = window.updateComparison;
        window.updateComparison = function wrappedUpdateComparison() {
            const result = orig.apply(this, arguments);
            document.querySelectorAll('#comparisonGrid .compare-card').forEach((el, i) => {
                el.classList.add('reveal', 'is-visible');
                el.style.transitionDelay = (i * 60) + 'ms';
            });
            return result;
        };
    }

    function init() {
        initMobileNav();
        initHeroParticles();
        initReveal();
        initTimelineProgress();
        initResultObserver();
        initStickyCta();
        wrapCalculateROI();
        wrapComparison();
    }

    window.AWCAnimate = { onCalcUpdate, animateValue, prefersReduce };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
