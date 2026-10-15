/* Загрузчик стран и областей. Цифры лежат в data/countries.js и data/regions/{ISO}.js */
window.AWC_REGIONS = window.AWC_REGIONS || {};

function awcCountries() {
    return window.AWC_COUNTRIES || [];
}

function awcCountry(iso) {
    return awcCountries().find(c => c.iso === iso) || null;
}

function awcPlaceName(row, lang, countryLang) {
    if (!row) return '';
    if (lang === 'zh') return row.zh || row.en;
    if (lang === 'ru' || lang === 'es' || lang === 'en') return row[lang] || row.en;
    if (countryLang && lang === countryLang) return row.native || row.en;
    return row.en;
}

function loadRegions(iso) {
    return new Promise((resolve) => {
        if (!iso) {
            resolve([]);
            return;
        }
        if (window.AWC_REGIONS[iso]) {
            resolve(window.AWC_REGIONS[iso]);
            return;
        }
        const script = document.createElement('script');
        script.src = 'data/regions/' + iso + '.js';
        script.onload = () => resolve(window.AWC_REGIONS[iso] || []);
        script.onerror = () => resolve([]);
        document.head.appendChild(script);
    });
}

function getLocationsData() {
    const out = {};
    awcCountries().forEach(country => {
        const regions = {};
        (window.AWC_REGIONS[country.iso] || []).forEach(region => {
            regions[region.iso] = {
                humidity: region.humidity,
                coords: [region.lat, region.lng],
                waterPriceUsd1L: country.water,
                region
            };
        });
        out[country.iso] = {
            coords: [country.lat, country.lng],
            regions,
            country
        };
    });
    return out;
}

function renderCalcSource() {
    const el = document.getElementById('calcSource');
    if (!el) return;
    const place = window.AWC_PLACE;
    const src = window.AWC_SOURCES || {};
    const lang = window.currentLang || 'ru';
    if (!place) {
        const empty = {
            ru: 'Выберите страну и регион. Цифры появятся вместе с источником.',
            en: 'Choose a country and a region. Figures appear with their source.',
            zh: '请选择国家和地区。数字会和来源一起出现。',
            es: 'Elija un país y una región. Las cifras aparecen con su fuente.'
        };
        el.textContent = empty[lang] || empty.en;
        return;
    }
    const flags = place.flags || {};
    const bits = [
        src.humidity,
        (flags.water ? 'Water price is the median of the same world region: ' : '') + (src.water || ''),
        (flags.elec ? 'Electricity price is the median of the same world region: ' : '') + (src.elec || ''),
        (flags.tax ? 'Tax rate is the median of the same world region: ' : '') + (src.tax || ''),
        (flags.wage ? 'Wage is the median of the same world region: ' : '') + (src.wage || '')
    ].filter(Boolean);
    el.textContent = bits.join(' ');
}

window.loadRegions = loadRegions;
window.awcCountry = awcCountry;
window.awcPlaceName = awcPlaceName;
window.renderCalcSource = renderCalcSource;
