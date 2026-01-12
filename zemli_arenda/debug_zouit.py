import requests
import urllib3
import json

urllib3.disable_warnings()

# Квартал в Аргаяшском районе
quarter = "74:02:0201042"

url = "https://nspd.gov.ru/api/geoportal/v2/search/geoportal"
params = {
    "thematicSearchId": 10, # 10 - ЗОУИТ
    "query": quarter, 
    "CRS": "EPSG:4326"
}
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://nspd.gov.ru/",
}

print(f"Checking ZOUIT (Type 10) for {quarter}...")
try:
    resp = requests.get(url, params=params, headers=headers, verify=False)
    data = resp.json()
    features = data.get("data", {}).get("features", [])
    print(f"Found {len(features)} ZOUITs.")
    for f in features:
        props = f.get("properties", {})
        print(f"ZOUIT: {props.get('label')} - {props.get('readable_address')}")
except Exception as e:
    print(f"Error: {e}")









