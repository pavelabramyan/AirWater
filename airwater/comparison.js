const COMPARE_LOCATIONS = {
    ru: [
        { id: 'uae',    label: '🇦🇪 ОАЭ (Дубай)',     country: 'ОАЭ', region: 'Дубай' },
        { id: 'moscow', label: '🇷🇺 Москва',          country: 'Россия', region: 'Москва' },
        { id: 'sochi',  label: '🇷🇺 Сочи',            country: 'Россия', region: 'Сочи' },
        { id: 'bali',   label: '🇮🇩 Бали',            country: 'Индонезия', region: 'Бали' }
    ],
    en: [
        { id: 'uae',    label: '🇦🇪 UAE (Dubai)',     country: 'United Arab Emirates', region: 'Dubai' },
        { id: 'moscow', label: '🇷🇺 Moscow',          country: 'Russia', region: 'Moscow' },
        { id: 'sochi',  label: '🇷🇺 Sochi',           country: 'Russia', region: 'Sochi' },
        { id: 'bali',   label: '🇮🇩 Bali',            country: 'Indonesia', region: 'Bali' }
    ],
    zh: [
        { id: 'uae',    label: '🇦🇪 阿联酋（迪拜）',   country: '阿联酋', region: '迪拜' },
        { id: 'moscow', label: '🇷🇺 莫斯科',          country: '俄罗斯', region: '莫斯科' },
        { id: 'sochi',  label: '🇷🇺 索契',            country: '俄罗斯', region: '索契' },
        { id: 'bali',   label: '🇮🇩 巴厘岛',          country: '印度尼西亚', region: '巴厘岛' }
    ],
    es: [
        { id: 'uae',    label: '🇦🇪 EAU (Dubái)',     country: 'Emiratos Árabes Unidos', region: 'Dubái' },
        { id: 'moscow', label: '🇷🇺 Moscú',           country: 'Rusia', region: 'Moscú' },
        { id: 'sochi',  label: '🇷🇺 Sochi',           country: 'Rusia', region: 'Sochi' },
        { id: 'bali',   label: '🇮🇩 Bali',            country: 'Indonesia', region: 'Bali' }
    ]
};

function getCompareLocations() {
    const lang = window.currentLang || 'ru';
    return COMPARE_LOCATIONS[lang] || COMPARE_LOCATIONS.ru;
}

function computeLocationMetrics(country, region) {
    const locations = getLocationsData();
    const countryData = locations[country];
    if (!countryData?.regions[region]) return null;

    const r = countryData.regions[region];
    const params = getCalculatorParams();
    return computeMetrics({
        ...params,
        humidity: r.humidity,
        pricePerLiter: r.waterPriceUsd1L ?? params.pricePerLiter,
        operatingCostsPercent: COUNTRY_OPERATING_COSTS[country] || params.operatingCostsPercent
    });
}

function updateComparison() {
    const grid = document.getElementById('comparisonGrid');
    if (!grid) return;

    const locs = getCompareLocations();
    const lang = window.currentLang || 'ru';
    const labels = {
        roi: { ru: 'ROI', en: 'ROI', zh: 'ROI', es: 'ROI' },
        payback: { ru: 'Окупаемость', en: 'Payback', zh: '回收期', es: 'Recuperación' },
        profit: { ru: 'Прибыль/год', en: 'Profit/yr', zh: '年利润', es: 'Beneficio/año' },
        prod: { ru: 'л/сут', en: 'L/day', zh: '升/天', es: 'L/día' }
    };
    const L = (k) => labels[k][lang] || labels[k].en;

    grid.innerHTML = locs.map(loc => {
        const m = computeLocationMetrics(loc.country, loc.region);
        if (!m) return `<div class="compare-card"><h4>${loc.label}</h4><p>—</p></div>`;

        let payback = '—';
        if (m.paybackYears !== Infinity && m.paybackYears > 0) {
            payback = m.paybackYears < 1
                ? Math.round(m.paybackYears * 12) + ' ' + getMonthsText()
                : formatNumber(m.paybackYears) + ' ' + getYearsText();
        }

        const best = loc.id === 'bali';
        return `
        <div class="compare-card ${best ? 'compare-card--best' : ''}">
            <h4>${loc.label}</h4>
            ${best ? '<span class="compare-badge">★ Top</span>' : ''}
            <div class="compare-roi">${formatNumber(m.roiPercent)}%</div>
            <div class="compare-stats">
                <div><span>${L('payback')}</span><strong>${payback}</strong></div>
                <div><span>${L('profit')}</span><strong>${formatCurrency(m.avgInvestorProfit)}</strong></div>
                <div><span>${L('prod')}</span><strong>${formatNumber(m.dailyProduction)}</strong></div>
            </div>
            <button class="compare-select-btn" data-country="${loc.country}" data-region="${loc.region}">${lang === 'ru' ? 'Выбрать' : lang === 'zh' ? '选择' : lang === 'es' ? 'Elegir' : 'Select'}</button>
        </div>`;
    }).join('');

    grid.querySelectorAll('.compare-select-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const cs = document.getElementById('countrySelect');
            const rs = document.getElementById('regionSelect');
            if (!cs) return;
            cs.value = btn.dataset.country;
            cs.dispatchEvent(new Event('change'));
            setTimeout(() => {
                if (rs) { rs.value = btn.dataset.region; rs.dispatchEvent(new Event('change')); }
                document.getElementById('calculator')?.scrollIntoView({ behavior: 'smooth' });
            }, 50);
        });
    });
}

function updateHeroFromCalculator(m, params) {
    const heroDynamic = document.getElementById('heroDynamic');
    if (!heroDynamic) return;

    const country = document.getElementById('countrySelect')?.value;
    const region = document.getElementById('regionSelect')?.value;
    if (!country || !region) {
        heroDynamic.classList.remove('visible');
        return;
    }

    heroDynamic.classList.add('visible');
    const lang = window.currentLang || 'ru';
    const texts = {
        ru: `Ваш расчёт: ${region} · ROI ${formatNumber(m.roiPercent)}% · окупаемость ${m.paybackYears < 1 ? Math.round(m.paybackYears*12)+' мес.' : formatNumber(m.paybackYears)+' лет'}`,
        en: `Your estimate: ${region} · ROI ${formatNumber(m.roiPercent)}% · payback ${m.paybackYears < 1 ? Math.round(m.paybackYears*12)+' mo.' : formatNumber(m.paybackYears)+' yrs'}`,
        zh: `您的估算：${region} · ROI ${formatNumber(m.roiPercent)}% · 回收期 ${m.paybackYears < 1 ? Math.round(m.paybackYears*12)+' 月' : formatNumber(m.paybackYears)+' 年'}`,
        es: `Su cálculo: ${region} · ROI ${formatNumber(m.roiPercent)}% · recuperación ${m.paybackYears < 1 ? Math.round(m.paybackYears*12)+' mes.' : formatNumber(m.paybackYears)+' años'}`
    };
    heroDynamic.textContent = texts[lang] || texts.en;

    const statNums = document.querySelectorAll('.hero-stats .stat-number');
    if (statNums[0]) statNums[0].textContent = formatNumber(m.dailyProduction);
    if (statNums[1]) statNums[1].textContent = formatNumber(m.roiPercent) + '%';
    if (statNums[2]) statNums[2].textContent = m.paybackYears < 1 ? Math.round(m.paybackYears*12) + (lang==='ru'?' мес.':' mo.') : formatNumber(m.paybackYears) + (lang==='ru'?' лет':' yrs');
}

document.addEventListener('DOMContentLoaded', () => updateComparison());
