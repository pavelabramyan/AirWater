let map = null;
let countryMarker = null;
let regionMarker = null;
let countryLayer = null;
let regionLayer = null;

function initMap() {
    if (map) {
        map.remove();
    }
    
    // Инициализация карты с центром на мире
    map = L.map('map').setView([20, 0], 2);
    
    // Добавление тайлов OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
}

function updateMap(countryName, regionName) {
    if (!map) {
        initMap();
    }
    
    const locations = getLocationsData();
    const country = locations[countryName];
    
    if (!country) return;
    
    // Удаляем старые маркеры
    if (countryMarker) {
        map.removeLayer(countryMarker);
    }
    if (regionMarker) {
        map.removeLayer(regionMarker);
    }
    if (countryLayer) {
        map.removeLayer(countryLayer);
    }
    if (regionLayer) {
        map.removeLayer(regionLayer);
    }
    
    // Создаем кастомные иконки
    const blueIcon = L.divIcon({
        className: 'custom-marker',
        html: '<div style="background-color: #0066cc; width: 30px; height: 30px; border-radius: 50% 50% 50% 0; transform: rotate(-45deg); border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div><div style="width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 10px solid #0066cc; margin-top: -3px; margin-left: 9px;"></div>',
        iconSize: [30, 40],
        iconAnchor: [15, 40],
        popupAnchor: [0, -40]
    });
    
    const redIcon = L.divIcon({
        className: 'custom-marker',
        html: '<div style="background-color: #ff0000; width: 30px; height: 30px; border-radius: 50% 50% 50% 0; transform: rotate(-45deg); border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div><div style="width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 10px solid #ff0000; margin-top: -3px; margin-left: 9px;"></div>',
        iconSize: [30, 40],
        iconAnchor: [15, 40],
        popupAnchor: [0, -40]
    });
    
    // Добавляем маркер страны
    const countryCoords = country.coords;
    countryMarker = L.marker(countryCoords, {
        icon: blueIcon
    }).addTo(map);
    
    countryMarker.bindPopup(`<b>${countryName}</b>`).openPopup();
    
    // Если выбран регион, добавляем его маркер
    if (regionName && country.regions[regionName]) {
        const region = country.regions[regionName];
        const regionCoords = region.coords;
        
        regionMarker = L.marker(regionCoords, {
            icon: redIcon
        }).addTo(map);
        
        const humidityText = window.currentLang === 'ru' ? 'Влажность' : 
                           window.currentLang === 'en' ? 'Humidity' :
                           window.currentLang === 'zh' ? '湿度' : 'Humedad';
        
        regionMarker.bindPopup(`<b>${regionName}</b><br>${humidityText}: ${region.humidity}%`).openPopup();
        
        // Центрируем карту на регионе
        map.setView(regionCoords, 6);
        
        // Добавляем круг для региона
        regionLayer = L.circle(regionCoords, {
            color: '#ff0000',
            fillColor: '#ff0000',
            fillOpacity: 0.1,
            radius: 50000
        }).addTo(map);
    } else {
        // Центрируем карту на стране
        map.setView(countryCoords, 5);
        
        // Добавляем круг для страны
        countryLayer = L.circle(countryCoords, {
            color: '#0066cc',
            fillColor: '#0066cc',
            fillOpacity: 0.1,
            radius: 200000
        }).addTo(map);
    }
}

// Инициализация карты при загрузке
document.addEventListener('DOMContentLoaded', () => {
    initMap();
});
