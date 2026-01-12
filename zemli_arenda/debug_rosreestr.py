import requests
import json
import urllib3

urllib3.disable_warnings()

quarter = "74:19:1106002"
url = "https://nspd.gov.ru/api/geoportal/v2/search/geoportal"
params = {
    "thematicSearchId": 1,
    "query": quarter,
    "CRS": "EPSG:4326"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://nspd.gov.ru/",
}

try:
    resp = requests.get(url, params=params, headers=headers, verify=False)
    data = resp.json()
    features = data.get("data", {}).get("features", [])
    print(f"Found {len(features)} features.")
    if features:
        print("Sample Feature keys:", features[0].keys())
        print("Sample Feature Properties:", json.dumps(features[0].get("properties", {}), indent=2, ensure_ascii=False))
        print("Sample Feature Geometry Type:", features[0].get("geometry", {}).get("type"))
except Exception as e:
    print(f"Error: {e}")









