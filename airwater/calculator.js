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
    conservative: { priceMult: 0.85, extraRevenueCost: 0.08, labelKey: 'calculator.scenario.conservative' },
    base:         { priceMult: 1.0,  extraRevenueCost: 0,    labelKey: 'calculator.scenario.base' },
    optimistic:   { priceMult: 1.10, extraRevenueCost: 0,    labelKey: 'calculator.scenario.optimistic' }
};

// Паспорт установки в бизнес-плане: 5 000 л/сут при 80% влажности, 65 кВт.
const RATED_HUMIDITY = 80;
const KWH_PER_LITER = (65 * 24) / 5000;
// Тара $0,03/л вместо $800/мес из сметы: на 3 900 л/сут это было бы $0,007/л, бутылка 0,5–5 л столько не стоит.
const PACKAGING_USD_PER_LITER = 0.03;
// Верх вилки зарплат из плана ($350+$600+$300) + аренда $400 + логистика $500 + сервис $400 + прочее $300.
const FIXED_MONTHLY_PER_UNIT = 1250 + 400 + 500 + 400 + 300;
// Оборудование, доставка и монтаж $212 600 из $470 000, срок 8 лет. Резерв и комиссия не амортизируются.
const DEPRECIABLE_SHARE = 212600 / 470000;
const DEPRECIATION_YEARS = 8;
const CORPORATE_TAX = 0.22;

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
    // Паспорт уже задан при 80% влажности. При 78% это 4 875 л/сут, не 78% от паспорта.
    const factor = Math.min(1, humidity / RATED_HUMIDITY);
    return Math.round(baseCapacity * factor);
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
            ru: `${formatNumber(baseCapacity)} л/сут при 80% → ${formatNumber(dailyProduction)} л/сут при ${pct}%`,
            en: `${formatNumber(baseCapacity)} L/day at 80% → ${formatNumber(dailyProduction)} L/day at ${pct}%`,
            zh: `${formatNumber(baseCapacity)} 升/天（80%湿度）→ ${formatNumber(dailyProduction)} 升/天（${pct}%）`,
            es: `${formatNumber(baseCapacity)} L/día al 80% → ${formatNumber(dailyProduction)} L/día al ${pct}%`
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
    const effectiveUtil = utilization;
    const electricityRate = Number.isFinite(electricityCost) ? electricityCost : 0.09;

    const nominalDaily = humidityToProduction(baseCapacity, humidity);
    const dailyProduction = Math.round(nominalDaily * (effectiveUtil / 100));
    const totalInvestment = investment * unitCount;
    const daysPerYear = 365;
    const annualDepreciation = totalInvestment * DEPRECIABLE_SHARE / DEPRECIATION_YEARS;

    let totalRevenue = 0, totalOpex = 0, totalNet = 0, totalProfit = 0;
    const cashFlows = [-totalInvestment];
    let cumulative = -totalInvestment;

    for (let y = 1; y <= period; y++) {
        const inflMult = Math.pow(1 + priceInflation / 100, y - 1);
        const yearPrice = effectivePrice * inflMult;

        let yearDailyProd = dailyProduction;
        if (y === 1 && rampUpMonths > 0) {
            const rampFactor = Math.max(0.3, 1 - rampUpMonths / 24);
            yearDailyProd = Math.round(dailyProduction * rampFactor);
        }

        const annualProduction = yearDailyProd * daysPerYear * unitCount;
        const annualRevenue = annualProduction * yearPrice;
        const electricity = annualProduction * KWH_PER_LITER * electricityRate;
        const packaging = annualProduction * PACKAGING_USD_PER_LITER;
        const fixed = FIXED_MONTHLY_PER_UNIT * 12 * unitCount;
        const extra = annualRevenue * (scen.extraRevenueCost || 0);
        const cashOpex = electricity + packaging + fixed + extra;
        const ebit = annualRevenue - cashOpex - annualDepreciation;
        const tax = Math.max(0, ebit) * CORPORATE_TAX;
        const netProfit = ebit - tax;
        const investorProfit = netProfit * (investorSharePercent / 100);

        totalRevenue += annualRevenue;
        totalOpex += cashOpex;
        totalNet += netProfit;
        totalProfit += investorProfit;
        cashFlows.push(investorProfit);
        cumulative += investorProfit;
    }

    const avgAnnualRevenue = totalRevenue / period;
    const avgInvestorProfit = totalProfit / period;
    const avgCashOpex = totalOpex / period;
    const avgNetProfit = totalNet / period;
    const roiPercent = totalInvestment > 0 ? (avgInvestorProfit / totalInvestment) * 100 : 0;
    const paybackYears = avgInvestorProfit > 0 ? totalInvestment / avgInvestorProfit : Infinity;
    const ebitdaMargin = avgAnnualRevenue > 0 ? ((avgAnnualRevenue - avgCashOpex) / avgAnnualRevenue) * 100 : 0;
    const netMargin = avgAnnualRevenue > 0 ? (avgNetProfit / avgAnnualRevenue) * 100 : 0;
    const effectiveOpex = avgAnnualRevenue > 0 ? (avgCashOpex / avgAnnualRevenue) * 100 : 0;

    const npv = calcNPV(cashFlows, 0.12);
    const irr = calcIRR(cashFlows);

    let breakevenDays = Infinity;
    const yearProd = dailyProduction * daysPerYear * unitCount;
    const yearRevenue = yearProd * effectivePrice;
    const yearCash = yearProd * KWH_PER_LITER * electricityRate + yearProd * PACKAGING_USD_PER_LITER + FIXED_MONTHLY_PER_UNIT * 12 * unitCount;
    const contributionPerLiter = effectivePrice - KWH_PER_LITER * electricityRate - PACKAGING_USD_PER_LITER;
    if (contributionPerLiter > 0) {
        const fixedAndCapital = FIXED_MONTHLY_PER_UNIT * 12 * unitCount + annualDepreciation;
        breakevenDays = (fixedAndCapital / contributionPerLiter) / (dailyProduction * unitCount || 1);
    }

    return {
        dailyProduction, nominalDaily, effectivePrice, effectiveOpex, effectiveUtil,
        totalInvestment, avgAnnualRevenue, avgInvestorProfit, roiPercent, paybackYears,
        totalProfit, npv, irr, ebitdaMargin, netMargin, avgCashOpex, breakevenDays, cashFlows, cumulative,
        yearRevenue, yearCash
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

function numOr(raw, fallback) {
    const n = parseFloat(raw);
    return Number.isFinite(n) ? n : fallback;
}

function getCalculatorParams() {
    const capacitySelect = document.getElementById('productionCapacity');
    const baseCapacity = capacitySelect ? parseInt(capacitySelect.value) : 5000;
    return {
        investment: numOr(document.getElementById('investmentAmount')?.value, 470000),
        pricePerLiter: numOr(document.getElementById('pricePerLiter')?.value, 0.5),
        operatingCostsPercent: numOr(document.getElementById('operatingCosts')?.value, 75),
        investorSharePercent: numOr(document.getElementById('investorShare')?.value, 50),
        period: numOr(document.getElementById('period')?.value, 5),
        baseCapacity,
        humidity: currentHumidity,
        utilization: numOr(document.getElementById('capacityUtilization')?.value, 100),
        unitCount: parseInt(document.getElementById('unitCount')?.value, 10) || 1,
        rampUpMonths: numOr(document.getElementById('rampUpMonths')?.value, 0),
        priceInflation: numOr(document.getElementById('priceInflation')?.value, 0),
        electricityCost: numOr(document.getElementById('electricityCost')?.value, 0.09),
        scenario: currentScenario
    };
}

function calculateROI() {
    const params = getCalculatorParams();
    currentBaseProduction = params.baseCapacity;
    const m = computeMetrics(params);

    const prodInput = document.getElementById('dailyProduction');
    if (prodInput) prodInput.value = m.dailyProduction;

    updateHumidityVisual(params.baseCapacity * params.unitCount, currentHumidity, m.nominalDaily * params.unitCount);

    const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    set('roi', formatNumber(m.roiPercent) + '%');
    set('annualRevenue', formatCurrency(m.avgAnnualRevenue));
    set('annualProfit', formatCurrency(m.avgInvestorProfit));
    set('totalProfit', formatCurrency(m.totalProfit));
    set('npv', formatCurrency(m.npv));
    set('irr', formatNumber(m.irr) + '%');
    set('ebitda', formatNumber(m.netMargin) + '%');
    const opexEl = document.getElementById('operatingCosts');
    if (opexEl) opexEl.value = formatNumber(m.effectiveOpex);

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
