#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для просмотра структуры ответа API
"""

import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_URL = "https://nspd.gov.ru/api/registers-manager/v2/registers/46504?page=1&count=10"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'application/json',
    'Referer': 'https://nspd.gov.ru/land-nspd/land-building?mode=table',
    'Origin': 'https://nspd.gov.ru'
}

response = requests.post(API_URL, headers=headers, json={}, timeout=30, verify=False)

if response.status_code == 200:
    data = response.json()
    
    # Сохраняем в файл
    with open('api_response_sample.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ Ответ сохранен в api_response_sample.json")
    print(f"\nКлючи верхнего уровня: {list(data.keys())}")
    
    if 'data' in data:
        print(f"\nТип 'data': {type(data['data'])}")
        if isinstance(data['data'], list) and len(data['data']) > 0:
            print(f"Первая запись в 'data': {data['data'][0]}")
    
    if 'header' in data:
        print(f"\nЗаголовки колонок:")
        for h in data['header']:
            print(f"  - {h.get('key')}: {h.get('name')}")
else:
    print(f"❌ Ошибка: {response.status_code}")


