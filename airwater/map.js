let map = null;
let countryMarker = null;
let regionMarker = null;
let countryLayer = null;
let regionLayer = null;
let heatmapLayers = [];

function initMap() {
    if (map) map.remove();
    map = L.map('map').setView([20, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap',
        maxZoom: 19
    }).addTo(map);
}

function humidityColor(h) {
    if (h >= 80) return '#0066cc';
    if (h >= 70) return '#00b894';
    if (h >= 60) return '#fdcb6e';
    if (h >= 50) return '#e17055';
    return '#d63031';
}

function updateMapHeatmap() {
    if (!map) return;
    heatmapLayers.forEach(l => map.removeLayer(l));
    heatmapLayers = [];

    const country = document.getElementById('countrySelect')?.value;
    if (!country) return;

    const locations = getLocationsData();
    const countryData = locations[country];
    if (!countryData) return;

    Object.entries(countryData.regions).forEach(([name, region]) => {
        if (region.humidity == null || !region.coords) return;
        const color = humidityColor(region.humidity);
        const circle = L.circle(region.coords, {
            color, fillColor: color, fillOpacity: 0.35,
            radius: 40000, weight: 1
        }).addTo(map);
        circle.bindPopup(`<b>${name}</b><br>💧 ${region.humidity}% · $${region.waterPriceUsd1L}/L`);
        heatmapLayers.push(circle);
    });
}

function updateMap(countryName, regionName) {
    if (!map) initMap();

    const locations = getLocationsData();
    const country = locations[countryName];
    if (!country) return;

    [countryMarker, regionMarker, countryLayer, regionLayer].forEach(m => { if (m) map.removeLayer(m); });

    const blueIcon = L.divIcon({
        className: 'custom-marker',
        html: '<div style="background:#0066cc;width:24px;height:24px;border-radius:50%;border:3px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.3)"></div>',
        iconSize: [24, 24], iconAnchor: [12, 12]
    });
    const redIcon = L.divIcon({
        className: 'custom-marker',
        html: '<div style="background:#ff6b6b;width:28px;height:28px;border-radius:50%;border:3px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,.4)"></div>',
        iconSize: [28, 28], iconAnchor: [14, 14]
    });

    const cc = country.coords;
    countryMarker = L.marker(cc, { icon: blueIcon }).addTo(map).bindPopup(`<b>${countryName}</b>`);

    if (regionName && country.regions[regionName]) {
        const region = country.regions[regionName];
        const rc = Array.isArray(region.coords) ? region.coords : cc;
        regionMarker = L.marker(rc, { icon: redIcon }).addTo(map);
        const h = region.humidity ?? '—';
        const p = region.waterPriceUsd1L ?? '—';
        regionMarker.bindPopup(`<b>${regionName}</b><br>💧 ${h}% · $${p}/L`).openPopup();
        regionLayer = L.circle(rc, {
            color: humidityColor(region.humidity || 50),
            fillColor: humidityColor(region.humidity || 50),
            fillOpacity: 0.2, radius: 60000
        }).addTo(map);
        map.setView(rc, 7);
    } else {
        countryLayer = L.circle(cc, { color: '#0066cc', fillColor: '#0066cc', fillOpacity: 0.08, radius: 250000 }).addTo(map);
        map.setView(cc, 5);
    }

    updateMapHeatmap();
}

document.addEventListener('DOMContentLoaded', () => initMap());
