const COMPARE_LOCATIONS = [
    { id: 'uae', iso: 'AE', region: 'AE-DU', flag: '🇦🇪' },
    { id: 'moscow', iso: 'RU', region: 'RU-MOW', flag: '🇷🇺' },
    { id: 'krasnodar', iso: 'RU', region: 'RU-KDA', flag: '🇷🇺' },
    { id: 'bali', iso: 'ID', region: 'ID-BA', flag: '🇮🇩' }
];

function getCompareLocations() {
    const lang = window.currentLang || 'ru';
    return COMPARE_LOCATIONS.map(item => {
        const country = awcCountry(item.iso);
        const region = (window.AWC_REGIONS[item.iso] || []).find(r => r.iso === item.region);
        const place = region ? awcPlaceName(region, lang, country?.lang) : item.region;
        return { ...item, country: item.iso, label: `${item.flag} ${place}` };
    });
}

function computeLocationMetrics(iso, regionIso) {
    const country = awcCountry(iso);
    const region = (window.AWC_REGIONS[iso] || []).find(r => r.iso === regionIso);
    if (!country || !region) return null;
    const params = getCalculatorParams();
    return computeMetrics({
        ...params,
        humidity: region.humidity,
        pricePerLiter: country.water ?? params.pricePerLiter,
        electricityCost: country.elec,
        taxRate: country.tax / 100,
        monthlyWage: country.wage
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
            loadRegions(btn.dataset.country).then(() => {
                fillRegionSelect(btn.dataset.country);
                if (rs) { rs.value = btn.dataset.region; rs.dispatchEvent(new Event('change')); }
                document.getElementById('calculator')?.scrollIntoView({ behavior: 'smooth' });
            });
        });
    });
}

function updateHeroFromCalculator(m, params) {
    const heroDynamic = document.getElementById('heroDynamic');
    if (!heroDynamic) return;

    const country = awcCountry(document.getElementById('countrySelect')?.value);
    const regionIso = document.getElementById('regionSelect')?.value;
    const region = (window.AWC_REGIONS[country?.iso] || []).find(r => r.iso === regionIso);
    if (!country || !region) {
        heroDynamic.classList.remove('visible');
        return;
    }

    heroDynamic.classList.add('visible');
    const lang = window.currentLang || 'ru';
    const place = awcPlaceName(region, lang, country.lang);
    const texts = {
        ru: `Ваш расчёт: ${place} · ROI ${formatNumber(m.roiPercent)}% · окупаемость ${m.paybackYears < 1 ? Math.round(m.paybackYears*12)+' мес.' : formatNumber(m.paybackYears)+' лет'}`,
        en: `Your estimate: ${place} · ROI ${formatNumber(m.roiPercent)}% · payback ${m.paybackYears < 1 ? Math.round(m.paybackYears*12)+' mo.' : formatNumber(m.paybackYears)+' yrs'}`,
        zh: `您的估算：${place} · ROI ${formatNumber(m.roiPercent)}% · 回收期 ${m.paybackYears < 1 ? Math.round(m.paybackYears*12)+' 月' : formatNumber(m.paybackYears)+' 年'}`,
        es: `Su cálculo: ${place} · ROI ${formatNumber(m.roiPercent)}% · recuperación ${m.paybackYears < 1 ? Math.round(m.paybackYears*12)+' mes.' : formatNumber(m.paybackYears)+' años'}`
    };
    heroDynamic.textContent = texts[lang] || texts.en;

    const statNums = document.querySelectorAll('.hero-stats .stat-number');
    if (statNums[0]) statNums[0].textContent = formatNumber(m.dailyProduction);
    if (statNums[1]) statNums[1].textContent = formatNumber(m.roiPercent) + '%';
    if (statNums[2]) statNums[2].textContent = m.paybackYears < 1 ? Math.round(m.paybackYears*12) + (lang==='ru'?' мес.':' mo.') : formatNumber(m.paybackYears) + (lang==='ru'?' лет':' yrs');
}

document.addEventListener('DOMContentLoaded', () => {
    Promise.all(['AE', 'RU', 'ID', 'US', 'IR'].map(loadRegions)).then(() => updateComparison());
});
