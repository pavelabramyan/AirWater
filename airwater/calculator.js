// Производительность → Инвестиции
const PRODUCTION_INVESTMENTS = {
    1000: 150000,
    2000: 215000,
    3000: 320000,
    5000: 470000,
    10000: 960000
};

const COUNTRY_OPERATING_COSTS = {
    'Индонезия': 60, 'Indonesia': 60, '印度尼西亚': 60,
    'Россия': 75, 'Russia': 75, '俄罗斯': 75, 'Rusia': 75,
    'ОАЭ': 80, 'United Arab Emirates': 80, '阿联酋': 80, 'Emiratos Árabes Unidos': 80,
    'Саудовская Аравия': 80, 'Saudi Arabia': 80, '沙特阿拉伯': 80, 'Arabia Saudí': 80
};
const DEFAULT_OPERATING_COSTS = 75;

const SCENARIOS = {
    conservative: { priceMult: 0.85, opexAdd: 10, utilization: 70, labelKey: 'calculator.scenario.conservative' },
    base:         { priceMult: 1.0,  opexAdd: 0,  utilization: 80, labelKey: 'calculator.scenario.base' },
    optimistic:   { priceMult: 1.10, opexAdd: -10, utilization: 90, labelKey: 'calculator.scenario.optimistic' }
};

let currentHumidity = null;
let currentWaterPrice = null;
let currentBaseProduction = 5000;
let currentScenario = 'base';
let baseOperatingCosts = 75;
let basePricePerLiter = 0.5;
let baseUtilization = 80;

// ─── Форматирование ───────────────────────────────────────────
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(amount);
}
function formatNumber(num) {
    return new Intl.NumberFormat('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 1 }).format(num);
}
function getYearsText() {
    const t = { ru: 'лет', en: 'years', zh: '年', es: 'años' };
    return t[window.currentLang || 'ru'] || t.en;
}
function getMonthsText() {
    const t = { ru: 'мес.', en: 'mo.', zh: '月', es: 'meses' };
    return t[window.currentLang || 'ru'] || t.en;
}

// ─── Влажность → литры ───────────────────────────────────────
function humidityToProduction(baseCapacity, humidity) {
    if (humidity === null || humidity <= 0) return baseCapacity;
    // Эффективность: при 100% влажности = 100%, при 50% = ~75% (не линейно)
    const efficiency = 0.5 + (humidity / 100) * 0.5;
    return Math.round(baseCapacity * efficiency);
}

function updateHumidityVisual(baseCapacity, humidity, dailyProduction) {
    const bar = document.getElementById('humidityBar');
    const marker = document.getElementById('humidityMarker');
    const formula = document.getElementById('humidityFormula');
    const pct = humidity !== null ? humidity : 0;
    if (bar) bar.style.setProperty('--humidity', pct + '%');
    if (marker) marker.style.left = Math.min(98, Math.max(2, pct)) + '%';
    if (formula) {
        const lang = window.currentLang || 'ru';
        const texts = {
            ru: `${formatNumber(baseCapacity)} л/сут (номинал) × ${pct}% влажности → ${formatNumber(dailyProduction)} л/сут`,
            en: `${formatNumber(baseCapacity)} L/day (nominal) × ${pct}% humidity → ${formatNumber(dailyProduction)} L/day`,
            zh: `${formatNumber(baseCapacity)} 升/天（额定）× ${pct}% 湿度 → ${formatNumber(dailyProduction)} 升/天`,
            es: `${formatNumber(baseCapacity)} L/día (nominal) × ${pct}% humedad → ${formatNumber(dailyProduction)} L/día`
        };
        formula.textContent = humidity !== null ? (texts[lang] || texts.en) : '—';
    }
}

// ─── Расчётный движок ─────────────────────────────────────────
function computeMetrics(params) {
    const {
        investment, pricePerLiter, operatingCostsPercent, investorSharePercent,
        period, baseCapacity, humidity, utilization, unitCount,
        rampUpMonths, priceInflation, electricityCost, scenario
    } = params;

    const scen = SCENARIOS[scenario] || SCENARIOS.base;
    const effectivePrice = pricePerLiter * scen.priceMult;
    const effectiveOpex = Math.max(20, Math.min(95, operatingCostsPercent + scen.opexAdd));
    const effectiveUtil = scen.utilization > 0 ? scen.utilization : utilization;

    const nominalDaily = humidityToProduction(baseCapacity, humidity);
    const dailyProduction = Math.round(nominalDaily * (effectiveUtil / 100));
    const totalInvestment = investment * unitCount;

    // Электроэнергия: ~0.5 кВт·ч/л, влияет на opex
    const elecCostAnnual = dailyProduction * 365 * 0.5 * electricityCost * unitCount;
    const daysPerYear = 365;

    let totalRevenue = 0, totalOpex = 0, totalProfit = 0;
    const cashFlows = [-totalInvestment];
    let cumulative = -totalInvestment;

    for (let y = 1; y <= period; y++) {
        const inflMult = Math.pow(1 + priceInflation / 100, y - 1);
        const yearPrice = effectivePrice * inflMult;

        let yearDays = daysPerYear;
        let yearDailyProd = dailyProduction;
        if (y === 1 && rampUpMonths > 0) {
            const rampFactor = Math.max(0.3, 1 - rampUpMonths / 24);
            yearDailyProd = Math.round(dailyProduction * rampFactor);
        }

        const annualProduction = yearDailyProd * yearDays * unitCount;
        const annualRevenue = annualProduction * yearPrice;
        const operatingCosts = annualRevenue * (effectiveOpex / 100) + elecCostAnnual;
        const annualProfit = annualRevenue - operatingCosts;
        const investorProfit = annualProfit * (investorSharePercent / 100);

        totalRevenue += annualRevenue;
        totalOpex += operatingCosts;
        totalProfit += investorProfit;
        cashFlows.push(investorProfit);
        cumulative += investorProfit;
    }

    const avgAnnualRevenue = totalRevenue / period;
    const avgInvestorProfit = totalProfit / period;
    const roiPercent = totalInvestment > 0 ? (avgInvestorProfit / totalInvestment) * 100 : 0;
    const paybackYears = avgInvestorProfit > 0 ? totalInvestment / avgInvestorProfit : Infinity;
    const ebitdaMargin = avgAnnualRevenue > 0 ? ((avgAnnualRevenue - avgAnnualRevenue * effectiveOpex / 100) / avgAnnualRevenue) * 100 : 0;

    const npv = calcNPV(cashFlows, 0.12);
    const irr = calcIRR(cashFlows);

    let breakevenDays = Infinity;
    if (effectivePrice > 0 && effectiveOpex < 100 && investorSharePercent > 0) {
        const profitPerLiter = effectivePrice * (1 - effectiveOpex / 100) * (investorSharePercent / 100);
        const breakevenLiters = totalInvestment / profitPerLiter;
        breakevenDays = dailyProduction > 0 ? breakevenLiters / (dailyProduction * unitCount) : Infinity;
    }

    return {
        dailyProduction, nominalDaily, effectivePrice, effectiveOpex, effectiveUtil,
        totalInvestment, avgAnnualRevenue, avgInvestorProfit, roiPercent, paybackYears,
        totalProfit, npv, irr, ebitdaMargin, breakevenDays, cashFlows, cumulative
    };
}

function calcNPV(cashFlows, rate) {
    return cashFlows.reduce((npv, cf, i) => npv + cf / Math.pow(1 + rate, i), 0);
}

function calcIRR(cashFlows) {
    let rate = 0.1;
    for (let iter = 0; iter < 100; iter++) {
        let npv = 0, dnpv = 0;
        for (let i = 0; i < cashFlows.length; i++) {
            npv += cashFlows[i] / Math.pow(1 + rate, i);
            if (i > 0) dnpv -= i * cashFlows[i] / Math.pow(1 + rate, i + 1);
        }
        if (Math.abs(dnpv) < 1e-10) break;
        const newRate = rate - npv / dnpv;
        if (Math.abs(newRate - rate) < 1e-7) { rate = newRate; break; }
        rate = Math.max(-0.99, Math.min(10, newRate));
    }
    return rate * 100;
}

function getCalculatorParams() {
    const capacitySelect = document.getElementById('productionCapacity');
    const baseCapacity = capacitySelect ? parseInt(capacitySelect.value) : 5000;
    return {
        investment: parseFloat(document.getElementById('investmentAmount')?.value) || 470000,
        pricePerLiter: parseFloat(document.getElementById('pricePerLiter')?.value) || 0.5,
        operatingCostsPercent: parseFloat(document.getElementById('operatingCosts')?.value) || 75,
        investorSharePercent: parseFloat(document.getElementById('investorShare')?.value) || 50,
        period: parseFloat(document.getElementById('period')?.value) || 5,
        baseCapacity,
        humidity: currentHumidity,
        utilization: parseFloat(document.getElementById('capacityUtilization')?.value) || 80,
        unitCount: parseInt(document.getElementById('unitCount')?.value) || 1,
        rampUpMonths: parseInt(document.getElementById('rampUpMonths')?.value) || 3,
        priceInflation: parseFloat(document.getElementById('priceInflation')?.value) || 3,
        electricityCost: parseFloat(document.getElementById('electricityCost')?.value) || 0.12,
        scenario: currentScenario
    };
}

function calculateROI() {
    const params = getCalculatorParams();
    currentBaseProduction = params.baseCapacity;
    const m = computeMetrics(params);

    const prodInput = document.getElementById('dailyProduction');
    if (prodInput) prodInput.value = m.dailyProduction;

    updateHumidityVisual(params.baseCapacity * params.unitCount, currentHumidity, m.dailyProduction);

    const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    set('roi', formatNumber(m.roiPercent) + '%');
    set('annualRevenue', formatCurrency(m.avgAnnualRevenue));
    set('annualProfit', formatCurrency(m.avgInvestorProfit));
    set('totalProfit', formatCurrency(m.totalProfit));
    set('npv', formatCurrency(m.npv));
    set('irr', formatNumber(m.irr) + '%');
    set('ebitda', formatNumber(m.ebitdaMargin) + '%');

    const paybackEl = document.getElementById('paybackPeriod');
    if (paybackEl) {
        if (m.paybackYears === Infinity || m.paybackYears < 0) paybackEl.textContent = '—';
        else if (m.paybackYears < 1) paybackEl.textContent = Math.round(m.paybackYears * 12) + ' ' + getMonthsText();
        else paybackEl.textContent = formatNumber(m.paybackYears) + ' ' + getYearsText();
    }

    // Сценарии — мини-карточки
    ['conservative', 'base', 'optimistic'].forEach(s => {
        const el = document.getElementById('scenarioRoi_' + s);
        if (el) {
            const sm = computeMetrics({ ...params, scenario: s });
            el.textContent = formatNumber(sm.roiPercent) + '%';
        }
    });

    if (typeof updateBreakevenChart === 'function') {
        updateBreakevenChart(m.totalInvestment, m.avgInvestorProfit, params.period, m.breakevenDays);
    }
    if (typeof updateHeroFromCalculator === 'function') updateHeroFromCalculator(m, params);
    if (typeof updateComparison === 'function') updateComparison();
    if (typeof updateMapHeatmap === 'function') updateMapHeatmap();
    window.lastCalculatorSnapshot = buildCalculatorSnapshot(m, params);
}

function buildCalculatorSnapshot(m, params) {
    const country = document.getElementById('countrySelect')?.value || '';
    const region = document.getElementById('regionSelect')?.value || '';
    return {
        country, region,
        scenario: currentScenario,
        capacity: params.baseCapacity,
        units: params.unitCount,
        investment: m.totalInvestment,
        humidity: currentHumidity,
        dailyProduction: m.dailyProduction,
        pricePerLiter: params.pricePerLiter,
        opex: params.operatingCostsPercent,
        investorShare: params.investorSharePercent,
        period: params.period,
        utilization: params.utilization,
        rampUpMonths: params.rampUpMonths,
        priceInflation: params.priceInflation,
        electricityCost: params.electricityCost,
        roi: m.roiPercent,
        payback: m.paybackYears,
        npv: m.npv,
        irr: m.irr,
        annualProfit: m.avgInvestorProfit
    };
}

window.getCalculatorSnapshot = () => window.lastCalculatorSnapshot || buildCalculatorSnapshot({}, getCalculatorParams());

function applyScenario(name) {
    currentScenario = name;
    document.querySelectorAll('.scenario-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.scenario === name);
    });
    calculateROI();
}

function setHumidity(h) {
    currentHumidity = h;
    const el = document.getElementById('humidityDisplay');
    if (el) el.value = h !== null ? h + '%' : '—';
    calculateROI();
}

function setWaterPrice(price) {
    currentWaterPrice = price;
    const el = document.getElementById('pricePerLiter');
    if (el && price !== null) { el.value = price; basePricePerLiter = price; }
    calculateROI();
}

function setOperatingCostsByCountry(countryName) {
    const el = document.getElementById('operatingCosts');
    if (el && countryName) {
        const costs = COUNTRY_OPERATING_COSTS[countryName] || DEFAULT_OPERATING_COSTS;
        el.value = costs;
        baseOperatingCosts = costs;
    }
}

function updateInvestmentFromCapacity() {
    const cap = document.getElementById('productionCapacity');
    const inv = document.getElementById('investmentAmount');
    if (cap && inv) {
        const c = parseInt(cap.value);
        inv.value = PRODUCTION_INVESTMENTS[c] || 470000;
    }
    calculateROI();
}

function initLocationSelects() {
    refreshCountrySelect();
    if (window._locationSelectsInit) return;
    window._locationSelectsInit = true;

    const countrySelect = document.getElementById('countrySelect');
    const regionSelect = document.getElementById('regionSelect');
    if (!countrySelect || !regionSelect) return;

    countrySelect.addEventListener('change', function () {
        const locations = getLocationsData();
        const sel = this.value;
        regionSelect.innerHTML = `<option value="">${getSelectRegionText('region')}</option>`;
        regionSelect.disabled = !sel;
        if (sel && locations[sel]) {
            Object.keys(locations[sel].regions).sort().forEach(rname => {
                const r = locations[sel].regions[rname];
                const opt = document.createElement('option');
                opt.value = rname;
                const ht = r?.humidity != null ? `${r.humidity}%` : '—';
                opt.textContent = `${rname} (${ht})`;
                regionSelect.appendChild(opt);
            });
            setOperatingCostsByCountry(sel);
            if (typeof updateMap === 'function') updateMap(sel, null);
        } else {
            if (typeof initMap === 'function') initMap();
        }
        setHumidity(null);
        setWaterPrice(null);
    });

    regionSelect.addEventListener('change', function () {
        const locations = getLocationsData();
        const sel = countrySelect.value;
        const reg = this.value;
        if (sel && reg && locations[sel]?.regions[reg]) {
            const r = locations[sel].regions[reg];
            setHumidity(r.humidity ?? null);
            if (r.waterPriceUsd1L != null) setWaterPrice(r.waterPriceUsd1L);
            if (typeof updateMap === 'function') updateMap(sel, reg);
        } else {
            setHumidity(null);
            setWaterPrice(null);
        }
    });
}

function refreshCountrySelect() {
    const countrySelect = document.getElementById('countrySelect');
    if (!countrySelect) return;
    const prev = countrySelect.value;
    const locations = getLocationsData();
    countrySelect.innerHTML = `<option value="">${getSelectRegionText('country')}</option>`;
    Object.keys(locations).sort().forEach(name => {
        const opt = document.createElement('option');
        opt.value = name;
        opt.textContent = name;
        countrySelect.appendChild(opt);
    });
    if (prev && locations[prev]) countrySelect.value = prev;
}

function getSelectRegionText(type) {
    const lang = window.currentLang || 'ru';
    const texts = {
        country: { ru: 'Выберите страну', en: 'Select country', zh: '选择国家', es: 'Seleccione país' },
        region:  { ru: 'Выберите регион', en: 'Select region', zh: '选择地区', es: 'Seleccione región' }
    };
    return texts[type][lang] || texts[type].en;
}

function initTooltips() {
    document.querySelectorAll('[data-tooltip]').forEach(el => {
        el.addEventListener('mouseenter', () => showTooltip(el));
        el.addEventListener('mouseleave', hideTooltip);
        el.addEventListener('click', (e) => { e.preventDefault(); showTooltip(el, true); });
    });
}

function showTooltip(el, toggle) {
    hideTooltip();
    const key = el.dataset.tooltip;
    const lang = window.currentLang || 'ru';
    const tips = window.METRIC_TOOLTIPS?.[lang]?.[key] || window.METRIC_TOOLTIPS?.en?.[key] || '';
    if (!tips) return;
    const tip = document.createElement('div');
    tip.className = 'metric-tooltip';
    tip.id = 'activeTooltip';
    tip.textContent = tips;
    document.body.appendChild(tip);
    const rect = el.getBoundingClientRect();
    tip.style.top = (rect.bottom + window.scrollY + 8) + 'px';
    tip.style.left = Math.min(rect.left, window.innerWidth - tip.offsetWidth - 16) + 'px';
    if (toggle) setTimeout(hideTooltip, 4000);
}

function hideTooltip() {
    document.getElementById('activeTooltip')?.remove();
}

document.addEventListener('DOMContentLoaded', () => {
    initLocationSelects();
    initTooltips();

    document.getElementById('productionCapacity')?.addEventListener('change', updateInvestmentFromCapacity);

    ['investmentAmount','pricePerLiter','operatingCosts','investorShare','period',
     'capacityUtilization','unitCount','rampUpMonths','priceInflation','electricityCost'
    ].forEach(id => {
        document.getElementById(id)?.addEventListener('input', calculateROI);
        document.getElementById(id)?.addEventListener('change', calculateROI);
    });

    document.querySelectorAll('.scenario-btn').forEach(btn => {
        btn.addEventListener('click', () => applyScenario(btn.dataset.scenario));
    });

    updateInvestmentFromCapacity();
    calculateROI();
});

window.calculateROI = calculateROI;
window.initLocationSelects = initLocationSelects;
window.refreshCountrySelect = refreshCountrySelect;
window.computeMetrics = computeMetrics;
