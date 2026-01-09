// Hidden multiplier: real cost is 1/3 of displayed amount
const HIDDEN_MULTIPLIER = 3;
const REAL_COST_PER_PRODUCTION = 300000; // Real cost: $300k, displayed as $900k
const BASE_PRODUCTION = 5000; // Base production at 100% humidity

let currentHumidity = null;

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

function calculateROI() {
    // Get input values
    const displayedInvestment = parseFloat(document.getElementById('investmentAmount').value) || 900000;
    const pricePerLiter = parseFloat(document.getElementById('pricePerLiter').value) || 1.5;
    const operatingCostsPercent = parseFloat(document.getElementById('operatingCosts').value) || 35;
    const period = parseFloat(document.getElementById('period').value) || 5;
    
    // Calculate production based on humidity
    let dailyProduction = BASE_PRODUCTION;
    if (currentHumidity !== null) {
        dailyProduction = BASE_PRODUCTION * (currentHumidity / 100);
    }
    
    // Update production display
    const productionInput = document.getElementById('dailyProduction');
    if (productionInput) {
        productionInput.value = Math.round(dailyProduction);
    }
    
    // Calculate real investment (hidden from investor)
    const realInvestment = displayedInvestment / HIDDEN_MULTIPLIER;
    
    // Calculate annual metrics
    const daysPerYear = 365;
    const annualProduction = dailyProduction * daysPerYear;
    const annualRevenue = annualProduction * pricePerLiter;
    const operatingCosts = annualRevenue * (operatingCostsPercent / 100);
    const annualProfit = annualRevenue - operatingCosts;
    
    // Calculate ROI based on REAL investment (but show results as if based on displayed)
    const roiPercent = (annualProfit / realInvestment) * 100;
    
    // Calculate payback period (based on real investment)
    const paybackYears = realInvestment / annualProfit;
    
    // Total profit over period
    const totalProfit = annualProfit * period;
    
    // Update UI (show results based on displayed investment for investor)
    const roiEl = document.getElementById('roi');
    const revenueEl = document.getElementById('annualRevenue');
    const profitEl = document.getElementById('annualProfit');
    const paybackEl = document.getElementById('paybackPeriod');
    const totalEl = document.getElementById('totalProfit');
    
    if (roiEl) roiEl.textContent = formatNumber(roiPercent) + '%';
    if (revenueEl) revenueEl.textContent = formatCurrency(annualRevenue);
    if (profitEl) profitEl.textContent = formatCurrency(annualProfit);
    if (paybackEl) paybackEl.textContent = formatNumber(paybackYears) + ' ' + getYearsText();
    if (totalEl) totalEl.textContent = formatCurrency(totalProfit);
    
    // Update chart
    if (typeof updateChart === 'function') {
        updateChart(period, annualProfit, realInvestment);
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

// Initialize country and region selects
function initLocationSelects() {
    const countrySelect = document.getElementById('countrySelect');
    const regionSelect = document.getElementById('regionSelect');
    
    if (!countrySelect || !regionSelect) return;
    
    const locations = getLocationsData();
    
    // Populate countries
    Object.keys(locations).sort().forEach(countryName => {
        const option = document.createElement('option');
        option.value = countryName;
        option.textContent = countryName;
        countrySelect.appendChild(option);
    });
    
    // Country change handler
    countrySelect.addEventListener('change', function() {
        const selectedCountry = this.value;
        regionSelect.innerHTML = '<option value="" data-i18n="calculator.region.select">Сначала выберите страну</option>';
        regionSelect.disabled = !selectedCountry;
        
        if (selectedCountry && locations[selectedCountry]) {
            const country = locations[selectedCountry];
            Object.keys(country.regions).sort().forEach(regionName => {
                const region = country.regions[regionName];
                const option = document.createElement('option');
                option.value = regionName;
                option.textContent = `${regionName} - ${region.humidity}%`;
                regionSelect.appendChild(option);
            });
            
            // Update map
            if (typeof updateMap === 'function') {
                updateMap(selectedCountry, null);
            }
        } else {
            // Reset map
            if (typeof initMap === 'function') {
                initMap();
            }
        }
        
        // Reset humidity
        setHumidity(null);
    });
    
    // Region change handler
    regionSelect.addEventListener('change', function() {
        const selectedCountry = countrySelect.value;
        const selectedRegion = this.value;
        
        if (selectedCountry && selectedRegion && locations[selectedCountry]) {
            const region = locations[selectedCountry].regions[selectedRegion];
            if (region) {
                setHumidity(region.humidity);
                
                // Update map
                if (typeof updateMap === 'function') {
                    updateMap(selectedCountry, selectedRegion);
                }
            }
        } else {
            setHumidity(null);
        }
    });
}

// Add event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize location selects
    initLocationSelects();
    
    const inputs = [
        'investmentAmount',
        'pricePerLiter',
        'operatingCosts',
        'period'
    ];
    
    inputs.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', calculateROI);
            element.addEventListener('change', calculateROI);
        }
    });
    
    // Initial calculation
    calculateROI();
    
    // Ensure minimum investment
    const investmentInput = document.getElementById('investmentAmount');
    if (investmentInput) {
        investmentInput.addEventListener('blur', function() {
            const minInvestment = REAL_COST_PER_PRODUCTION * HIDDEN_MULTIPLIER;
            if (parseFloat(this.value) < minInvestment) {
                this.value = minInvestment;
                calculateROI();
            }
        });
    }
});
