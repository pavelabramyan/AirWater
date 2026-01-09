// Производительность → Инвестиции
const PRODUCTION_INVESTMENTS = {
    1000: 150000,   // $150K - реальная калькуляция с резервом 50% и комиссией 20%
    2000: 215000,   // $215K
    3000: 320000,   // $320K
    5000: 470000,   // $470K
    10000: 960000   // $960K
};

// Операционные расходы по странам (% от выручки)
const COUNTRY_OPERATING_COSTS = {
    // Индонезия - дешёвая энергия, низкие зарплаты
    'Индонезия': 60,
    'Indonesia': 60,
    '印度尼西亚': 60,
    'Indonesia': 60,
    // Россия - средние расходы
    'Россия': 75,
    'Russia': 75,
    '俄罗斯': 75,
    'Rusia': 75,
    // ОАЭ - высокая стоимость электроэнергии, низкая влажность
    'ОАЭ': 80,
    'United Arab Emirates': 80,
    '阿联酋': 80,
    'Emiratos Árabes Unidos': 80,
    // Саудовская Аравия - высокая стоимость электроэнергии, низкая влажность
    'Саудовская Аравия': 80,
    'Saudi Arabia': 80,
    '沙特阿拉伯': 80,
    'Arabia Saudí': 80
};
const DEFAULT_OPERATING_COSTS = 75;

let currentHumidity = null;
let currentWaterPrice = null;
let currentBaseProduction = 5000;

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function formatNumber(num) {
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 1
    }).format(num);
}

function getYearsText() {
    const lang = window.currentLang || 'ru';
    const texts = {
        ru: 'лет',
        en: 'years',
        zh: '年',
        es: 'años'
    };
    return texts[lang] || texts.en;
}

function getMonthsText() {
    const lang = window.currentLang || 'ru';
    const texts = {
        ru: 'мес.',
        en: 'mo.',
        zh: '月',
        es: 'meses'
    };
    return texts[lang] || texts.en;
}

function calculateROI() {
    // Получаем значения из формы
    const investment = parseFloat(document.getElementById('investmentAmount').value) || 500000;
    const pricePerLiter = parseFloat(document.getElementById('pricePerLiter').value) || 0.50;
    const operatingCostsPercent = parseFloat(document.getElementById('operatingCosts').value) || 75;
    const investorSharePercent = parseFloat(document.getElementById('investorShare').value) || 50;
    const period = parseFloat(document.getElementById('period').value) || 5;
    
    // Базовое производство из выбранной мощности
    const productionCapacity = document.getElementById('productionCapacity');
    const baseProduction = productionCapacity ? parseInt(productionCapacity.value) : 5000;
    currentBaseProduction = baseProduction;
    
    // Скорректированное производство по влажности
    let dailyProduction = baseProduction;
    if (currentHumidity !== null && currentHumidity > 0) {
        dailyProduction = baseProduction * (currentHumidity / 100);
    }
    
    // Обновляем отображение производства
    const productionInput = document.getElementById('dailyProduction');
    if (productionInput) {
        productionInput.value = Math.round(dailyProduction);
    }
    
    // Годовые показатели (общие по проекту)
    const daysPerYear = 365;
    const annualProduction = dailyProduction * daysPerYear;
    const annualRevenue = annualProduction * pricePerLiter;
    const operatingCosts = annualRevenue * (operatingCostsPercent / 100);
    const totalAnnualProfit = annualRevenue - operatingCosts;
    
    // Прибыль инвестора (его доля от общей прибыли)
    const investorAnnualProfit = totalAnnualProfit * (investorSharePercent / 100);
    
    // ROI и окупаемость для инвестора
    const roiPercent = investment > 0 ? (investorAnnualProfit / investment) * 100 : 0;
    const paybackYears = investorAnnualProfit > 0 ? investment / investorAnnualProfit : Infinity;
    
    // Прибыль инвестора за период
    const totalProfit = investorAnnualProfit * period;
    
    // Точка безубыточности для инвестора (литры и дни)
    let breakevenLiters = Infinity;
    let breakevenDays = Infinity;
    if (pricePerLiter > 0 && operatingCostsPercent < 100 && investorSharePercent > 0) {
        // Прибыль инвестора с литра = (цена - опер.расходы) * доля инвестора
        const investorProfitPerLiter = pricePerLiter * (1 - operatingCostsPercent / 100) * (investorSharePercent / 100);
        breakevenLiters = investment / investorProfitPerLiter;
        breakevenDays = dailyProduction > 0 ? breakevenLiters / dailyProduction : Infinity;
    }
    
    // Обновляем UI
    const roiEl = document.getElementById('roi');
    const revenueEl = document.getElementById('annualRevenue');
    const profitEl = document.getElementById('annualProfit');
    const paybackEl = document.getElementById('paybackPeriod');
    const totalEl = document.getElementById('totalProfit');
    
    if (roiEl) roiEl.textContent = formatNumber(roiPercent) + '%';
    if (revenueEl) revenueEl.textContent = formatCurrency(annualRevenue);
    if (profitEl) profitEl.textContent = formatCurrency(investorAnnualProfit);
    
    if (paybackEl) {
        if (paybackYears === Infinity || paybackYears < 0) {
            paybackEl.textContent = '—';
        } else if (paybackYears < 1) {
            const months = Math.round(paybackYears * 12);
            paybackEl.textContent = months + ' ' + getMonthsText();
        } else {
            paybackEl.textContent = formatNumber(paybackYears) + ' ' + getYearsText();
        }
    }
    
    if (totalEl) totalEl.textContent = formatCurrency(totalProfit);
    
    // Обновляем график (для инвестора)
    if (typeof updateBreakevenChart === 'function') {
        updateBreakevenChart(investment, investorAnnualProfit, period, breakevenDays);
    }
}

function setHumidity(humidity) {
    currentHumidity = humidity;
    const humidityDisplay = document.getElementById('humidityDisplay');
    if (humidityDisplay) {
        humidityDisplay.value = humidity !== null ? humidity + '%' : '—';
    }
    calculateROI();
}

function setWaterPrice(price) {
    currentWaterPrice = price;
    const priceInput = document.getElementById('pricePerLiter');
    if (priceInput && price !== null) {
        priceInput.value = price;
    }
    calculateROI();
}

function setOperatingCostsByCountry(countryName) {
    const operatingCostsInput = document.getElementById('operatingCosts');
    if (operatingCostsInput && countryName) {
        const costs = COUNTRY_OPERATING_COSTS[countryName] || DEFAULT_OPERATING_COSTS;
        operatingCostsInput.value = costs;
    }
}

function updateInvestmentFromCapacity() {
    const capacitySelect = document.getElementById('productionCapacity');
    const investmentInput = document.getElementById('investmentAmount');
    
    if (capacitySelect && investmentInput) {
        const capacity = parseInt(capacitySelect.value);
        const investment = PRODUCTION_INVESTMENTS[capacity] || 500000;
        investmentInput.value = investment;
    }
    calculateROI();
}

// Инициализация выпадающих списков стран и регионов
function initLocationSelects() {
    const countrySelect = document.getElementById('countrySelect');
    const regionSelect = document.getElementById('regionSelect');
    
    if (!countrySelect || !regionSelect) return;
    
    const locations = getLocationsData();
    
    // Заполняем список стран
    Object.keys(locations).sort().forEach(countryName => {
        const option = document.createElement('option');
        option.value = countryName;
        option.textContent = countryName;
        countrySelect.appendChild(option);
    });
    
    // Обработчик смены страны
    countrySelect.addEventListener('change', function() {
        const selectedCountry = this.value;
        const selectRegionText = getSelectRegionText();
        regionSelect.innerHTML = `<option value="">${selectRegionText}</option>`;
        regionSelect.disabled = !selectedCountry;
        
        if (selectedCountry && locations[selectedCountry]) {
            const country = locations[selectedCountry];
            Object.keys(country.regions).sort().forEach(regionName => {
                const region = country.regions[regionName];
                const option = document.createElement('option');
                option.value = regionName;
                const humidityText = (region && region.humidity !== null && region.humidity !== undefined)
                    ? `${region.humidity}%`
                    : '—';
                option.textContent = `${regionName} (${humidityText})`;
                regionSelect.appendChild(option);
            });
            
            // Обновляем карту
            if (typeof updateMap === 'function') {
                updateMap(selectedCountry, null);
            }
            
            // Устанавливаем операционные расходы по стране
            setOperatingCostsByCountry(selectedCountry);
        } else {
            if (typeof initMap === 'function') {
                initMap();
            }
        }
        
        // Сбрасываем влажность и цену
        setHumidity(null);
        setWaterPrice(null);
    });
    
    // Обработчик смены региона
    regionSelect.addEventListener('change', function() {
        const selectedCountry = countrySelect.value;
        const selectedRegion = this.value;
        
        if (selectedCountry && selectedRegion && locations[selectedCountry]) {
            const region = locations[selectedCountry].regions[selectedRegion];
            if (region) {
                // Устанавливаем влажность
                setHumidity((region.humidity !== null && region.humidity !== undefined) ? region.humidity : null);
                
                // Устанавливаем цену воды
                if (region.waterPriceUsd1L !== null && region.waterPriceUsd1L !== undefined) {
                    setWaterPrice(region.waterPriceUsd1L);
                }
                
                // Обновляем карту
                if (typeof updateMap === 'function') {
                    updateMap(selectedCountry, selectedRegion);
                }
            }
        } else {
            setHumidity(null);
            setWaterPrice(null);
        }
    });
}

function getSelectRegionText() {
    const lang = window.currentLang || 'ru';
    const texts = {
        ru: 'Выберите регион',
        en: 'Select region',
        zh: '选择地区',
        es: 'Seleccione región'
    };
    return texts[lang] || texts.ru;
}

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    // Инициализация списков локаций
    initLocationSelects();
    
    // Обработчик смены производительности
    const capacitySelect = document.getElementById('productionCapacity');
    if (capacitySelect) {
        capacitySelect.addEventListener('change', updateInvestmentFromCapacity);
    }
    
    // Обработчики для всех полей ввода
    const inputs = [
        'investmentAmount',
        'pricePerLiter',
        'operatingCosts',
        'investorShare',
        'period'
    ];
    
    inputs.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', calculateROI);
            element.addEventListener('change', calculateROI);
        }
    });
    
    // Устанавливаем начальные инвестиции по выбранной производительности
    updateInvestmentFromCapacity();
    
    // Начальный расчёт
    calculateROI();
});
