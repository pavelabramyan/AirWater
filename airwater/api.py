#!/usr/bin/env python3
"""
AirWater API Backend
Flask сервер для калькулятора ROI
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Данные производительности установок и инвестиций
PRODUCTION_OPTIONS = [
    {"id": 1, "liters_per_day": 1000, "investment_usd": 100000},
    {"id": 2, "liters_per_day": 2000, "investment_usd": 200000},
    {"id": 3, "liters_per_day": 3000, "investment_usd": 300000},
    {"id": 4, "liters_per_day": 5000, "investment_usd": 500000},
    {"id": 5, "liters_per_day": 10000, "investment_usd": 1000000},
]

# Страны и регионы РФ с реальными оценками цен
# Цены в USD за 1 литр бутилированной воды (оценка на основе рыночных данных 2024-2025)
COUNTRIES_DATA = {
    "Россия": {
        "coords": [61.5240, 105.3188],
        "regions": {
            "Москва и Московская область": {"humidity": 75, "coords": [55.7558, 37.6173], "waterPriceUsd1L": 0.70},
            "Санкт-Петербург и Ленинградская область": {"humidity": 78, "coords": [59.9343, 30.3351], "waterPriceUsd1L": 0.65},
            "Краснодарский край": {"humidity": 75, "coords": [45.0355, 38.9753], "waterPriceUsd1L": 0.55},
            "Ростовская область": {"humidity": 60, "coords": [47.2357, 39.7015], "waterPriceUsd1L": 0.50},
            "Республика Крым": {"humidity": 70, "coords": [44.9521, 34.1024], "waterPriceUsd1L": 0.55},
            "Приморский край": {"humidity": 78, "coords": [43.1155, 131.8855], "waterPriceUsd1L": 0.55},
            "Республика Адыгея": {"humidity": 72, "coords": [44.8228, 40.1753], "waterPriceUsd1L": 0.50},
            "Республика Алтай": {"humidity": 60, "coords": [50.7114, 86.8573], "waterPriceUsd1L": 0.45},
            "Республика Башкортостан": {"humidity": 68, "coords": [54.7351, 55.9587], "waterPriceUsd1L": 0.45},
            "Республика Бурятия": {"humidity": 55, "coords": [51.8340, 107.5845], "waterPriceUsd1L": 0.45},
            "Республика Дагестан": {"humidity": 65, "coords": [42.2610, 47.0953], "waterPriceUsd1L": 0.45},
            "Республика Ингушетия": {"humidity": 68, "coords": [43.1651, 44.8109], "waterPriceUsd1L": 0.45},
            "Кабардино-Балкарская Республика": {"humidity": 68, "coords": [43.3932, 43.5628], "waterPriceUsd1L": 0.45},
            "Республика Калмыкия": {"humidity": 50, "coords": [46.2313, 45.3279], "waterPriceUsd1L": 0.45},
            "Карачаево-Черкесская Республика": {"humidity": 70, "coords": [43.7360, 41.7270], "waterPriceUsd1L": 0.45},
            "Республика Карелия": {"humidity": 78, "coords": [63.5569, 33.3606], "waterPriceUsd1L": 0.50},
            "Республика Коми": {"humidity": 75, "coords": [64.0000, 54.0000], "waterPriceUsd1L": 0.50},
            "Республика Марий Эл": {"humidity": 72, "coords": [56.6349, 47.8669], "waterPriceUsd1L": 0.45},
            "Республика Мордовия": {"humidity": 70, "coords": [54.1838, 45.1749], "waterPriceUsd1L": 0.45},
            "Республика Саха (Якутия)": {"humidity": 60, "coords": [66.7613, 124.1238], "waterPriceUsd1L": 0.55},
            "Республика Северная Осетия — Алания": {"humidity": 66, "coords": [43.0205, 44.6819], "waterPriceUsd1L": 0.45},
            "Республика Татарстан": {"humidity": 70, "coords": [55.7963, 49.1088], "waterPriceUsd1L": 0.50},
            "Республика Тыва": {"humidity": 55, "coords": [51.7191, 94.4378], "waterPriceUsd1L": 0.45},
            "Удмуртская Республика": {"humidity": 72, "coords": [57.0000, 53.0000], "waterPriceUsd1L": 0.45},
            "Республика Хакасия": {"humidity": 55, "coords": [53.7219, 91.4422], "waterPriceUsd1L": 0.45},
            "Чеченская Республика": {"humidity": 66, "coords": [43.3976, 45.6985], "waterPriceUsd1L": 0.45},
            "Чувашская Республика": {"humidity": 70, "coords": [55.5000, 47.0000], "waterPriceUsd1L": 0.45},
            "Алтайский край": {"humidity": 60, "coords": [52.6932, 82.6936], "waterPriceUsd1L": 0.45},
            "Красноярский край": {"humidity": 60, "coords": [64.2504, 95.1049], "waterPriceUsd1L": 0.50},
            "Ставропольский край": {"humidity": 68, "coords": [44.6680, 43.5200], "waterPriceUsd1L": 0.50},
            "Хабаровский край": {"humidity": 75, "coords": [50.5888, 135.0000], "waterPriceUsd1L": 0.55},
            "Амурская область": {"humidity": 65, "coords": [52.8000, 128.0000], "waterPriceUsd1L": 0.50},
            "Архангельская область": {"humidity": 78, "coords": [63.0000, 41.0000], "waterPriceUsd1L": 0.50},
            "Астраханская область": {"humidity": 55, "coords": [46.3497, 48.0408], "waterPriceUsd1L": 0.45},
            "Белгородская область": {"humidity": 68, "coords": [50.5997, 36.5986], "waterPriceUsd1L": 0.45},
            "Брянская область": {"humidity": 75, "coords": [53.2635, 34.3717], "waterPriceUsd1L": 0.45},
            "Владимирская область": {"humidity": 72, "coords": [55.9000, 40.4000], "waterPriceUsd1L": 0.50},
            "Волгоградская область": {"humidity": 60, "coords": [49.6000, 44.4000], "waterPriceUsd1L": 0.45},
            "Вологодская область": {"humidity": 78, "coords": [59.2239, 39.8839], "waterPriceUsd1L": 0.50},
            "Воронежская область": {"humidity": 65, "coords": [51.6720, 39.1843], "waterPriceUsd1L": 0.45},
            "Ивановская область": {"humidity": 75, "coords": [57.0000, 41.0000], "waterPriceUsd1L": 0.45},
            "Иркутская область": {"humidity": 60, "coords": [56.0000, 105.0000], "waterPriceUsd1L": 0.50},
            "Калининградская область": {"humidity": 80, "coords": [54.7104, 20.4522], "waterPriceUsd1L": 0.55},
            "Калужская область": {"humidity": 72, "coords": [54.5000, 35.5000], "waterPriceUsd1L": 0.50},
            "Камчатский край": {"humidity": 80, "coords": [56.0000, 159.0000], "waterPriceUsd1L": 0.60},
            "Кемеровская область — Кузбасс": {"humidity": 65, "coords": [54.7500, 87.1361], "waterPriceUsd1L": 0.45},
            "Кировская область": {"humidity": 72, "coords": [58.5000, 50.0000], "waterPriceUsd1L": 0.45},
            "Костромская область": {"humidity": 75, "coords": [58.5500, 43.9500], "waterPriceUsd1L": 0.45},
            "Курганская область": {"humidity": 65, "coords": [55.4530, 65.3419], "waterPriceUsd1L": 0.45},
            "Курская область": {"humidity": 68, "coords": [51.7373, 36.1874], "waterPriceUsd1L": 0.45},
            "Липецкая область": {"humidity": 68, "coords": [52.6031, 39.5708], "waterPriceUsd1L": 0.45},
            "Магаданская область": {"humidity": 78, "coords": [62.0000, 153.0000], "waterPriceUsd1L": 0.60},
            "Мурманская область": {"humidity": 80, "coords": [68.9585, 33.0827], "waterPriceUsd1L": 0.55},
            "Нижегородская область": {"humidity": 70, "coords": [56.3269, 44.0059], "waterPriceUsd1L": 0.50},
            "Новгородская область": {"humidity": 78, "coords": [58.5228, 31.2750], "waterPriceUsd1L": 0.50},
            "Новосибирская область": {"humidity": 60, "coords": [55.0084, 82.9357], "waterPriceUsd1L": 0.50},
            "Омская область": {"humidity": 60, "coords": [54.9924, 73.3686], "waterPriceUsd1L": 0.45},
            "Оренбургская область": {"humidity": 60, "coords": [51.7727, 55.0988], "waterPriceUsd1L": 0.45},
            "Орловская область": {"humidity": 72, "coords": [52.9700, 36.0600], "waterPriceUsd1L": 0.45},
            "Пензенская область": {"humidity": 68, "coords": [53.1949, 45.0183], "waterPriceUsd1L": 0.45},
            "Пермский край": {"humidity": 72, "coords": [58.0000, 56.3167], "waterPriceUsd1L": 0.50},
            "Псковская область": {"humidity": 78, "coords": [57.8192, 28.3319], "waterPriceUsd1L": 0.50},
            "Рязанская область": {"humidity": 72, "coords": [54.6269, 39.6916], "waterPriceUsd1L": 0.45},
            "Самарская область": {"humidity": 65, "coords": [53.2038, 50.1606], "waterPriceUsd1L": 0.50},
            "Саратовская область": {"humidity": 60, "coords": [51.5336, 46.0342], "waterPriceUsd1L": 0.45},
            "Сахалинская область": {"humidity": 85, "coords": [50.6942, 142.9506], "waterPriceUsd1L": 0.60},
            "Свердловская область": {"humidity": 65, "coords": [56.8389, 60.6057], "waterPriceUsd1L": 0.50},
            "Смоленская область": {"humidity": 75, "coords": [54.7826, 32.0453], "waterPriceUsd1L": 0.45},
            "Тамбовская область": {"humidity": 65, "coords": [52.7212, 41.4523], "waterPriceUsd1L": 0.45},
            "Тверская область": {"humidity": 75, "coords": [56.8587, 35.9176], "waterPriceUsd1L": 0.50},
            "Томская область": {"humidity": 70, "coords": [58.5966, 70.0000], "waterPriceUsd1L": 0.50},
            "Тульская область": {"humidity": 70, "coords": [54.1931, 37.6173], "waterPriceUsd1L": 0.50},
            "Тюменская область": {"humidity": 70, "coords": [57.1553, 68.4305], "waterPriceUsd1L": 0.50},
            "Ульяновская область": {"humidity": 65, "coords": [54.3167, 48.4000], "waterPriceUsd1L": 0.45},
            "Челябинская область": {"humidity": 65, "coords": [55.1599, 61.4026], "waterPriceUsd1L": 0.50},
            "Забайкальский край": {"humidity": 55, "coords": [52.0000, 115.0000], "waterPriceUsd1L": 0.50},
            "Ярославская область": {"humidity": 75, "coords": [57.6261, 39.8845], "waterPriceUsd1L": 0.50},
            "Еврейская автономная область": {"humidity": 70, "coords": [48.8000, 132.9500], "waterPriceUsd1L": 0.50},
            "Ненецкий автономный округ": {"humidity": 80, "coords": [68.0000, 53.0000], "waterPriceUsd1L": 0.60},
            "Ханты-Мансийский автономный округ — Югра": {"humidity": 75, "coords": [61.0000, 69.0000], "waterPriceUsd1L": 0.55},
            "Чукотский автономный округ": {"humidity": 78, "coords": [66.0000, 169.0000], "waterPriceUsd1L": 0.65},
            "Ямало-Ненецкий автономный округ": {"humidity": 78, "coords": [66.5000, 70.0000], "waterPriceUsd1L": 0.60},
        }
    }
}


@app.route('/api/production-options', methods=['GET'])
def get_production_options():
    """Возвращает варианты производительности установок"""
    return jsonify(PRODUCTION_OPTIONS)


@app.route('/api/countries', methods=['GET'])
def get_countries():
    """Возвращает список стран"""
    countries = []
    for name, data in COUNTRIES_DATA.items():
        countries.append({
            "name": name,
            "coords": data["coords"],
            "regions_count": len(data["regions"])
        })
    return jsonify(countries)


@app.route('/api/regions/<country>', methods=['GET'])
def get_regions(country):
    """Возвращает регионы страны"""
    if country not in COUNTRIES_DATA:
        return jsonify({"error": "Country not found"}), 404
    
    regions = []
    for name, data in COUNTRIES_DATA[country]["regions"].items():
        regions.append({
            "name": name,
            "humidity": data["humidity"],
            "coords": data["coords"],
            "waterPriceUsd1L": data["waterPriceUsd1L"]
        })
    return jsonify(regions)


@app.route('/api/region/<country>/<region>', methods=['GET'])
def get_region(country, region):
    """Возвращает данные региона"""
    if country not in COUNTRIES_DATA:
        return jsonify({"error": "Country not found"}), 404
    if region not in COUNTRIES_DATA[country]["regions"]:
        return jsonify({"error": "Region not found"}), 404
    
    data = COUNTRIES_DATA[country]["regions"][region]
    return jsonify({
        "name": region,
        "country": country,
        "humidity": data["humidity"],
        "coords": data["coords"],
        "waterPriceUsd1L": data["waterPriceUsd1L"]
    })


@app.route('/api/calculate', methods=['POST'])
def calculate_roi():
    """Расчёт ROI"""
    data = request.json
    
    investment = data.get('investment', 500000)
    daily_production = data.get('dailyProduction', 5000)
    price_per_liter = data.get('pricePerLiter', 0.50)
    operating_costs_percent = data.get('operatingCostsPercent', 75)
    period = data.get('period', 5)
    humidity = data.get('humidity', 70)
    
    # Корректировка производства по влажности
    adjusted_production = daily_production * (humidity / 100)
    
    # Годовые показатели
    annual_production = adjusted_production * 365
    annual_revenue = annual_production * price_per_liter
    operating_costs = annual_revenue * (operating_costs_percent / 100)
    annual_profit = annual_revenue - operating_costs
    
    # ROI и окупаемость
    roi_percent = (annual_profit / investment) * 100 if investment > 0 else 0
    payback_years = investment / annual_profit if annual_profit > 0 else float('inf')
    
    # Общая прибыль за период
    total_profit = annual_profit * period
    
    # Точка безубыточности (в литрах)
    if price_per_liter > 0:
        breakeven_liters = investment / (price_per_liter * (1 - operating_costs_percent / 100))
        breakeven_days = breakeven_liters / adjusted_production if adjusted_production > 0 else float('inf')
    else:
        breakeven_liters = float('inf')
        breakeven_days = float('inf')
    
    return jsonify({
        "investment": investment,
        "adjustedDailyProduction": round(adjusted_production, 0),
        "annualProduction": round(annual_production, 0),
        "annualRevenue": round(annual_revenue, 2),
        "operatingCosts": round(operating_costs, 2),
        "annualProfit": round(annual_profit, 2),
        "roiPercent": round(roi_percent, 1),
        "paybackYears": round(payback_years, 2) if payback_years != float('inf') else None,
        "totalProfit": round(total_profit, 2),
        "breakevenLiters": round(breakeven_liters, 0) if breakeven_liters != float('inf') else None,
        "breakevenDays": round(breakeven_days, 0) if breakeven_days != float('inf') else None
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
