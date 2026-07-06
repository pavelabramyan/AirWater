// Smooth scrolling, form, animations
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href'))?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (navbar) navbar.style.boxShadow = window.pageYOffset > 100 ? '0 4px 16px rgba(0,0,0,.12)' : '0 2px 8px rgba(0,0,0,.08)';
    });

    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const snap = window.getCalculatorSnapshot?.() || {};
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                investmentInterest: document.getElementById('investmentInterest').value,
                message: document.getElementById('message').value,
                calculator: snap
            };

            const btn = contactForm.querySelector('button[type=submit]');
            const origText = btn.textContent;
            btn.disabled = true;
            btn.textContent = '...';

            try {
                await submitForm(formData);
                showFormToast(getSuccessMessage());
                contactForm.reset();
            } catch (err) {
                showFormToast(getErrorMessage() + ' ' + err.message, true);
            } finally {
                btn.disabled = false;
                btn.textContent = origText;
            }
        });
    }

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.about-card, .advantage-item, .result-card, .trust-card, .bali-stat, .compare-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

function formatSnapshotText(snap) {
    return [
        `📍 ${snap.country || '—'} / ${snap.region || '—'}`,
        `⚙️ ${snap.capacity || '—'} л/сут × ${snap.units || 1} шт.`,
        `💰 $${snap.investment?.toLocaleString() || '—'}`,
        `💧 Влажность: ${snap.humidity ?? '—'}% → ${snap.dailyProduction ?? '—'} л/сут`,
        `📊 ROI: ${snap.roi?.toFixed?.(1) || '—'}% | NPV: $${Math.round(snap.npv || 0).toLocaleString()}`,
        `⏱ Окупаемость: ${snap.payback?.toFixed?.(1) || '—'} лет`,
        `📈 IRR: ${snap.irr?.toFixed?.(1) || '—'}%`
    ].join('\n');
}

async function submitForm(data) {
    const snap = data.calculator;
    const calcBlock = formatSnapshotText(snap);
    const text = [
        '🆕 Заявка AquaFuture',
        '',
        `👤 ${data.name}`,
        `📧 ${data.email}`,
        `📱 ${data.phone}`,
        `💵 Интерес: $${data.investmentInterest || '—'}`,
        '',
        '📊 Параметры калькулятора:',
        calcBlock,
        '',
        `💬 ${data.message || '—'}`
    ].join('\n');

    const cfg = typeof AWC_CONFIG !== 'undefined' ? AWC_CONFIG : {};

    if (cfg.webhookUrl) {
        const res = await fetch(cfg.webhookUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...data, text, calcBlock })
        });
        if (!res.ok) throw new Error('Webhook error');
        return;
    }

    if (cfg.telegramBotToken && cfg.telegramBotToken !== 'YOUR_BOT_TOKEN' &&
        cfg.telegramChatId && cfg.telegramChatId !== 'YOUR_CHAT_ID') {
        const url = `https://api.telegram.org/bot${cfg.telegramBotToken}/sendMessage`;
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: cfg.telegramChatId, text, parse_mode: 'HTML' })
        });
        const json = await res.json();
        if (!json.ok) throw new Error(json.description || 'Telegram error');
        return;
    }

    // Fallback: clipboard + console
    console.log('Form submission:', data, text);
    try {
        await navigator.clipboard.writeText(text);
    } catch (_) {}
    // Show data in hidden field for user awareness
    const hidden = document.getElementById('calcSnapshotField');
    if (hidden) hidden.value = calcBlock;
}

function showFormToast(msg, isError) {
    let toast = document.getElementById('formToast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'formToast';
        toast.className = 'form-toast';
        document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.className = 'form-toast' + (isError ? ' form-toast--error' : ' form-toast--success');
    toast.classList.add('visible');
    setTimeout(() => toast.classList.remove('visible'), 5000);
}

function getSuccessMessage() {
    const lang = window.currentLang || 'ru';
    const cfg = typeof AWC_CONFIG !== 'undefined' ? AWC_CONFIG : {};
    const hasBackend = (cfg.telegramBotToken && cfg.telegramBotToken !== 'YOUR_BOT_TOKEN') || cfg.webhookUrl;
    const msgs = {
        ru: hasBackend ? 'Спасибо! Заявка с параметрами калькулятора отправлена.' : 'Спасибо! Данные скопированы в буфер — отправьте менеджеру.',
        en: hasBackend ? 'Thank you! Application with calculator data sent.' : 'Thank you! Data copied to clipboard — send to manager.',
        zh: hasBackend ? '谢谢！已发送包含计算器数据的申请。' : '谢谢！数据已复制到剪贴板。',
        es: hasBackend ? '¡Gracias! Solicitud con datos del calculador enviada.' : '¡Gracias! Datos copiados al portapapeles.'
    };
    return msgs[lang] || msgs.en;
}

function getErrorMessage() {
    const lang = window.currentLang || 'ru';
    return { ru: 'Ошибка отправки:', en: 'Send error:', zh: '发送错误：', es: 'Error de envío:' }[lang] || 'Error:';
}

window.addEventListener('load', () => {
    document.querySelectorAll('.stat-number').forEach(stat => {
        const v = stat.textContent;
        if (!isNaN(parseInt(v))) animateValue(stat, 0, parseInt(v), 2000);
    });
});

function animateValue(element, start, end, duration) {
    let ts = null;
    const step = (timestamp) => {
        if (!ts) ts = timestamp;
        const p = Math.min((timestamp - ts) / duration, 1);
        element.textContent = Math.floor(p * (end - start) + start);
        if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
}
