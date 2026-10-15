#!/usr/bin/env python3
"""Собирает страны, области и экономику калькулятора из открытых источников."""
import json
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = Path("/tmp/awc-world")
DATA = ROOT / "data"
REGIONS = DATA / "regions"
CACHE = DATA / "humidity_cache.json"
EXTRA_ISO = {"VA", "MC", "PS", "TW", "XK"}

ALIASES = {
    "united states of america": "united states",
    "usa": "united states",
    "u s a": "united states",
    "uk": "united kingdom",
    "uae": "united arab emirates",
    "russian federation": "russia",
    "republic of korea": "south korea",
    "korea, republic of": "south korea",
    "viet nam": "vietnam",
    "czechia": "czech republic",
    "türkiye": "turkey",
    "turkey": "turkey",
    "iran (islamic republic of)": "iran",
    "syrian arab republic": "syria",
    "laos": "lao people's democratic republic",
    "bolivia (plurinational state of)": "bolivia",
    "venezuela (bolivarian republic of)": "venezuela",
    "tanzania, united republic of": "tanzania",
    "moldova, republic of": "moldova",
    "palestine, state of": "palestine",
    "palestinian territory occupied": "palestine",
    "vatican city state (holy see)": "vatican",
    "holy see": "vatican",
    "congo, democratic republic of the": "democratic republic of the congo",
    "congo, republic of the": "republic of the congo",
    "brunei darussalam": "brunei",
    "cape verde": "cabo verde",
    "swaziland": "eswatini",
    "macedonia": "north macedonia",
}


def norm(name):
    s = (name or "").lower().replace("&", "and")
    s = re.sub(r"\(.*?\)", "", s)
    s = s.replace(",", " ")
    s = re.sub(r"[^a-z\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return ALIASES.get(s, s)


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_tax():
    text = load_json(RAW / "wiki-tax.json")["parse"]["wikitext"]["*"]
    out = {}
    for m in re.finditer(r"\{\{flagcountry\|([^}<]+)\}\}", text):
        chunk = text[m.end() : m.end() + 240]
        rate = re.search(r"([0-9]+(?:\.[0-9]+)?)%", chunk)
        if rate:
            out[norm(m.group(1))] = float(rate.group(1))
    return out


def parse_electricity():
    html = (RAW / "gpp.html").read_text(encoding="utf-8", errors="ignore")
    out = {}
    for name, household, business in re.findall(
        r'href="/([^"/]+)/electricity_prices/"[^>]*>([^<]+)</a></td>\s*<td>([0-9.]*)',
        html,
    ):
        # second price is business when present in the next cell
        pass
    for m in re.finditer(
        r'href="/[^"/]+/electricity_prices/"[^>]*>([^<]+)</a></td>\s*<td>([0-9.]*)</td>\s*<td>([0-9.]*)</td>',
        html,
    ):
        country, household, business = m.group(1), m.group(2), m.group(3)
        price = business or household
        if price:
            out[norm(country)] = float(price)
    return out


def parse_water():
    html = (RAW / "water.html").read_text(encoding="utf-8", errors="ignore")
    out = {}
    for name, price in re.findall(r"\['([^']+)',\s*([0-9.]+)\]", html):
        out[norm(name)] = round(float(price) / 1.5, 3)
    return out


def parse_wage():
    text = load_json(RAW / "wiki-wage.json")["parse"]["wikitext"]["*"]
    out = {}
    for m in re.finditer(r"List of minimum wages by country/Row\|([^|]+)\|", text):
        country = m.group(1).strip()
        chunk = text[m.start() : m.start() + 900]
        nums = [float(x.replace(",", "")) for x in re.findall(r"US\$\]*\]*\s*([0-9][0-9,]*(?:\.[0-9]+)?)", chunk)]
        nums = [n for n in nums if 0 < n < 20000]
        if not nums:
            continue
        monthly = []
        for n in nums:
            monthly.append(round(n * 173, 0) if n < 40 else n)
        out[norm(country)] = sorted(monthly)[len(monthly) // 2]
    return out


def lang_map():
    mapping = {}
    for line in (RAW / "lang3.csv").read_text(encoding="utf-8").splitlines()[1:]:
        parts = [p.strip().strip('"') for p in line.split(",")]
        if len(parts) >= 2 and parts[1]:
            mapping[parts[0]] = parts[1]
    mapping.update({
        "ind": "id", "fra": "fr", "deu": "de", "spa": "es", "rus": "ru", "eng": "en",
        "por": "pt", "zho": "zh", "ara": "ar", "fas": "fa", "per": "fa", "swa": "sw",
        "msa": "ms", "nld": "nl", "ita": "it", "jpn": "ja", "kor": "ko", "hin": "hi",
        "tur": "tr", "ukr": "uk", "pol": "pl", "vie": "vi", "tha": "th", "ell": "el",
        "heb": "he", "urd": "ur", "ben": "bn", "tam": "ta", "amh": "am", "nep": "ne",
        "sin": "si", "mya": "my", "khm": "km", "lao": "lo", "kat": "ka", "hye": "hy",
        "aze": "az", "kaz": "kk", "uzb": "uz", "kir": "ky", "tgk": "tg", "tuk": "tk",
        "mon": "mn", "bos": "bs", "hrv": "hr", "srp": "sr", "slv": "sl", "slk": "sk",
        "ces": "cs", "bul": "bg", "ron": "ro", "hun": "hu", "fin": "fi", "swe": "sv",
        "nor": "no", "dan": "da", "isl": "is", "gle": "ga", "lit": "lt", "lav": "lv",
        "est": "et", "sqi": "sq", "mkd": "mk", "bel": "be", "som": "so", "afr": "af",
        "mlt": "mt", "ltz": "lb", "div": "dv", "dzo": "dz", "tir": "ti", "kin": "rw",
        "run": "rn", "nya": "ny", "sag": "sg", "lin": "ln", "kon": "kg", "lua": "lu",
        "her": "hz", "ndo": "ng", "tso": "ts", "ssw": "ss", "ven": "ve", "nbl": "nr",
        "nso": "nso", "tsn": "tn", "xho": "xh", "zul": "zu", "sot": "st",
    })
    return mapping


def fetch_humidity(lat, lon):
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}&start_date=2022-01-01&end_date=2022-12-31"
        "&daily=relative_humidity_2m_mean"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "AWC-calculator/1.0"})
    with urllib.request.urlopen(req, timeout=40) as resp:
        data = json.loads(resp.read().decode())
    vals = [v for v in data["daily"]["relative_humidity_2m_mean"] if v is not None]
    if not vals:
        raise RuntimeError("empty")
    return round(sum(vals) / len(vals))


def main():
    countries_raw = load_json(RAW / "countries.json")
    states_raw = load_json(RAW / "states.json")
    mledoze = load_json(RAW / "mledoze.json")
    by_iso = {c["cca2"]: c for c in mledoze}
    dr = {c["iso2"]: c for c in countries_raw}
    codes_3 = lang_map()
    tax = parse_tax()
    elec = parse_electricity()
    water = parse_water()
    wage = parse_wage()

    chosen = []
    for iso, meta in by_iso.items():
        if meta.get("unMember") or iso in EXTRA_ISO:
            if iso in dr:
                chosen.append(iso)
    print("countries", len(chosen))

    states_by = {}
    for row in states_raw:
        states_by.setdefault(row["country_code"], []).append(row)

    def first_level(iso):
        rows = states_by.get(iso, [])
        level1 = [r for r in rows if str(r.get("level")) == "1"]
        if level1:
            if iso == "US":
                level1 = [r for r in level1 if r.get("type") in ("state", "district", "outlying area")]
            return level1
        loose = [r for r in rows if not r.get("parent_id") and "military" not in (r.get("type") or "")]
        return loose

    points = {}
    country_objs = []
    region_objs = {}
    missing = {"tax": [], "elec": [], "water": [], "wage": []}

    def pick(table, *names, default=None, bucket=None):
        for name in names:
            key = norm(name)
            if key in table:
                return table[key], False
        if bucket is not None:
            return None, True
        return default, True

    # continent medians filled after first pass of known values
    for iso in chosen:
        d = dr[iso]
        m = by_iso[iso]
        names = [d["name"], m["name"]["common"], m["name"]["official"]]
        t, t_miss = pick(tax, *names)
        e, e_miss = pick(elec, *names)
        w, w_miss = pick(water, *names)
        g, g_miss = pick(wage, *names)
        if t_miss:
            missing["tax"].append(d["name"])
        if e_miss:
            missing["elec"].append(d["name"])
        if w_miss:
            missing["water"].append(d["name"])
        if g_miss:
            missing["wage"].append(d["name"])
        langs = list((m.get("languages") or {"eng": "English"}).keys())
        alpha3 = langs[0]
        lang = codes_3.get(alpha3, alpha3[:2])
        tr = m.get("translations") or {}
        country_objs.append({
            "iso": iso,
            "en": m["name"]["common"],
            "ru": (tr.get("rus") or {}).get("common") or d["translations"].get("ru") or m["name"]["common"],
            "es": (tr.get("spa") or {}).get("common") or d["translations"].get("es") or m["name"]["common"],
            "zh": (tr.get("zho") or {}).get("common") or d["translations"].get("zh-CN") or m["name"]["common"],
            "native": d.get("native") or m["name"]["common"],
            "lang": lang,
            "lat": float(d["latitude"]),
            "lng": float(d["longitude"]),
            "region": d.get("region") or "",
            "tax": t,
            "elec": e,
            "water": w,
            "wage": g,
            "flags": {"tax": t_miss, "elec": e_miss, "water": w_miss, "wage": g_miss},
        })
        regs = []
        for row in first_level(iso):
            try:
                lat = round(float(row["latitude"]), 1)
                lon = round(float(row["longitude"]), 1)
            except (TypeError, ValueError):
                continue
            trs = row.get("translations") or {}
            regs.append({
                "iso": row.get("iso3166_2") or f"{iso}-{row['id']}",
                "en": row["name"],
                "ru": trs.get("ru") or row["name"],
                "es": trs.get("es") or row["name"],
                "zh": trs.get("zh-CN") or row["name"],
                "native": row.get("native") or row["name"],
                "lat": lat,
                "lng": lon,
            })
            points[(lat, lon)] = None
        if not regs:
            lat = round(float(d["latitude"]), 1)
            lon = round(float(d["longitude"]), 1)
            regs.append({
                "iso": iso,
                "en": m["name"]["common"],
                "ru": country_objs[-1]["ru"],
                "es": country_objs[-1]["es"],
                "zh": country_objs[-1]["zh"],
                "native": country_objs[-1]["native"],
                "lat": lat,
                "lng": lon,
            })
            points[(lat, lon)] = None
        region_objs[iso] = regs

    def median(vals):
        vals = sorted(v for v in vals if v is not None)
        if not vals:
            return None
        return vals[len(vals) // 2]

    by_region = {}
    for c in country_objs:
        by_region.setdefault(c["region"], []).append(c)
    for field in ("tax", "elec", "water", "wage"):
        for group in by_region.values():
            med = median([c[field] for c in group if not c["flags"][field]])
            if med is None:
                med = median([c[field] for c in country_objs if not c["flags"][field]])
            for c in group:
                if c["flags"][field]:
                    c[field] = med

    cache = {}
    if CACHE.exists():
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
    measured = {k: v for k, v in cache.items() if v is not None}

    def nearest(lat, lon):
        best = None
        best_d = 99
        for key, val in measured.items():
            plat, plon = map(float, key.split(","))
            dist = abs(plat - lat) + abs(plon - lon)
            if dist < best_d:
                best_d = dist
                best = val
        return best if best_d <= 80 else None

    borrowed = 0
    for lat, lon in list(points):
        key = f"{lat},{lon}"
        if cache.get(key) is None:
            near = nearest(lat, lon)
            if near is not None:
                cache[key] = near
                borrowed += 1
    print("humidity borrowed from nearby Open-Meteo points", borrowed, flush=True)
    todo = [p for p in points if cache.get(f"{p[0]},{p[1]}") is None]
    print("humidity points", len(points), "todo", len(todo), flush=True)

    def job(pt):
        lat, lon = pt
        key = f"{lat},{lon}"
        last = None
        for attempt in range(4):
            try:
                time.sleep(0.15)
                return key, fetch_humidity(lat, lon)
            except Exception as exc:
                last = exc
                time.sleep(1.5 * (attempt + 1))
        print("fail", key, last)
        return key, None

    done = 0
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(job, pt) for pt in todo]
        for fut in as_completed(futures):
            key, val = fut.result()
            cache[key] = val
            done += 1
            if done % 100 == 0:
                CACHE.parent.mkdir(parents=True, exist_ok=True)
                CACHE.write_text(json.dumps(cache), encoding="utf-8")
                print("humidity", done, "/", len(todo))
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache), encoding="utf-8")

    REGIONS.mkdir(parents=True, exist_ok=True)
    for old in REGIONS.glob("*.js"):
        old.unlink()

    for c in country_objs:
        hums = []
        for r in region_objs[c["iso"]]:
            h = cache.get(f"{r['lat']},{r['lng']}")
            r["humidity"] = h
            if h is not None:
                hums.append(h)
        fill = median(hums)
        for r in region_objs[c["iso"]]:
            if r["humidity"] is None:
                r["humidity"] = fill
                r["humidityFill"] = True
        payload = []
        for r in region_objs[c["iso"]]:
            payload.append({
                "iso": r["iso"], "en": r["en"], "ru": r["ru"], "es": r["es"], "zh": r["zh"],
                "native": r["native"], "lat": r["lat"], "lng": r["lng"], "humidity": r["humidity"],
            })
        js = "window.AWC_REGIONS=window.AWC_REGIONS||{};window.AWC_REGIONS[" + json.dumps(c["iso"]) + "]=" + json.dumps(payload, ensure_ascii=False) + ";\n"
        (REGIONS / f"{c['iso']}.js").write_text(js, encoding="utf-8")

    (DATA / "countries.js").write_text(
        "window.AWC_COUNTRIES=" + json.dumps(country_objs, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    sources = {
        "humidity": "Open-Meteo archive, ERA5, mean daily relative humidity for 2022 at the region coordinate rounded to 0.1 degree. If that point was rate-limited, the nearest measured point within 4 degrees is used. https://open-meteo.com/",
        "water": "Numbeo, markets, price of a 1.5 liter bottle, archived 2024, divided by 1.5. https://www.numbeo.com/cost-of-living/country_price_rankings?itemId=13",
        "elec": "GlobalPetrolPrices, average business electricity price, period 2023-2026, USD per kWh. https://www.globalpetrolprices.com/electricity_prices/",
        "tax": "Wikipedia, List of countries by tax rates, corporate column. https://en.wikipedia.org/wiki/List_of_countries_by_tax_rates",
        "wage": "Wikipedia, List of countries by minimum wage, monthly USD cited in the country row. https://en.wikipedia.org/wiki/List_of_countries_by_minimum_wage",
        "note": "If a country has no row in a source, the value is the median of countries in the same world region and the card says so.",
    }
    (DATA / "sources.js").write_text(
        "window.AWC_SOURCES=" + json.dumps(sources, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print("wrote", len(country_objs), "countries", sum(len(v) for v in region_objs.values()), "regions")
    print("missing before median", {k: len(v) for k, v in missing.items()})
    for iso in ("ID", "US", "RU", "IR"):
        c = next(x for x in country_objs if x["iso"] == iso)
        print(iso, c["en"], "tax", c["tax"], "elec", c["elec"], "water", c["water"], "wage", c["wage"], "regions", len(region_objs[iso]), "flags", c["flags"])


if __name__ == "__main__":
    main()
