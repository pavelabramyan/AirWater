#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Инженерный и природный анализ участков МО под коттеджный посёлок.

Источники: OpenStreetMap (Overpass), ISRIC SoilGrids WRB, уже посчитанный
cottage_settlement_assessments. Это ориентир для отбора, не ТУ и не юрзаключение.
"""

from __future__ import annotations

import json
import math
import os
import re
import sqlite3
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "farmland.db"
CACHE = ROOT / "data_cache" / "infra"
HTML_PATH = ROOT / "mo_sx_1ha.html"
OVERPASS = "https://overpass-api.de/api/interpreter"
SOIL_URL = "https://rest.isric.org/soilgrids/v2.0/classification/query"
UA = "farmland-map/1.0 (pavel@local)"

CELL = 0.20
PAD = 0.06
HIGHWAY_OK = {
    "motorway", "motorway_link", "trunk", "trunk_link", "primary", "primary_link",
    "secondary", "secondary_link", "tertiary", "tertiary_link", "unclassified",
    "residential", "service", "track",
}
FED_RE = re.compile(
    r"(?:^|[\s,;])(?:М|M)-?(?:1|2|3|4|5|7|8|9|10|11)\b|"
    r"(?:А|A)-?(?:104|107|108|113)\b|ЦКАД|МКАД",
    re.I,
)
HW_RU = {
    "motorway": "автомагистраль",
    "trunk": "магистральная дорога",
    "primary": "дорога I класса / региональная",
    "secondary": "областная дорога",
    "tertiary": "районная дорога",
    "unclassified": "местная дорога",
    "residential": "улица / внутрипоселковая",
    "service": "подъезд / служебный проезд",
    "track": "просёлок / полевая",
}
WRB_RU = {
    "Albeluvisols": "дерново-подзолистые (Albeluvisols)",
    "Retisols": "дерново-подзолистые / ретисоли",
    "Podzols": "подзолы",
    "Phaeozems": "серые лесные / файозёмы",
    "Luvisols": "серые лесные (лювисоли)",
    "Chernozems": "чернозёмы",
    "Histosols": "торфяные (гистосоли)",
    "Gleysols": "глеевые",
    "Fluvisols": "аллювиальные (пойменные)",
    "Cambisols": "бурозёмы / камбисоли",
    "Arenosols": "песчаные (ареносоли)",
    "Umbrisols": "умбрисоли",
    "Stagnosols": "стагносоли / поверхностно-оглеенные",
    "Alisols": "алисоли",
    "Lixisols": "ливисоли",
}
FED_QUERIES = [
    "М-1 Беларусь", "М-2 Крым", "М-3 Украина", "М-4 Дон", "М-5 Урал",
    "М-7 Волга", "М-8 Холмогоры", "М-9 Балтия", "М-10 Россия", "М-11 Нева",
    "А-104", "А-107 Московское малое кольцо", "А-108 Большое кольцо",
]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=60)
    conn.row_factory = sqlite3.Row
    return conn


def http_json(url: str, timeout: int = 40) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def overpass(query: str, timeout: int = 50, retries: int = 4) -> list[dict]:
    payload = urllib.parse.urlencode({"data": query}).encode()
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                OVERPASS,
                data=payload,
                headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data.get("elements") or []
        except Exception as exc:
            last = exc
            time.sleep(3 + attempt * 4)
    raise RuntimeError(f"Overpass failed: {last}")


def osm_map(s: float, w: float, n: float, e: float) -> list[dict]:
    dlat, dlon = n - s, e - w
    if dlat > 0.09 or dlon > 0.09 or dlat * dlon > 0.008:
        mid_lat, mid_lon = (s + n) / 2, (w + e) / 2
        out = []
        for box in ((s, w, mid_lat, mid_lon), (s, mid_lon, mid_lat, e), (mid_lat, w, n, mid_lon), (mid_lat, mid_lon, n, e)):
            if box[2] > box[0] and box[3] > box[1]:
                out.extend(osm_map(*box))
        return out
    key = f"osm_{s:.4f}_{w:.4f}_{n:.4f}_{e:.4f}"
    path = CACHE / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    url = f"https://api.openstreetmap.org/api/0.6/map.json?bbox={w:.5f},{s:.5f},{e:.5f},{n:.5f}"
    last = None
    for attempt in range(6):
        try:
            data = http_json(url, timeout=50)
            els = data.get("elements") or []
            path.write_text(json.dumps(els, ensure_ascii=False), encoding="utf-8")
            time.sleep(2.0)
            return els
        except Exception as exc:
            last = exc
            msg = str(exc)
            if "400" in msg and (n - s) > 0.03:
                mid_lat, mid_lon = (s + n) / 2, (w + e) / 2
                out = []
                for box in ((s, w, mid_lat, mid_lon), (s, mid_lon, mid_lat, e), (mid_lat, w, n, mid_lon), (mid_lat, mid_lon, n, e)):
                    out.extend(osm_map(*box))
                return out
            wait = 35 + attempt * 20 if ("509" in msg or "429" in msg) else 3 + attempt * 3
            print(f"     retry {attempt+1} {msg[:80]} sleep {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"OSM map failed {s},{w},{n},{e}: {last}")


def parse_osm_elements(elements: list[dict]) -> list[dict]:
    nodes = {el["id"]: el for el in elements if el.get("type") == "node"}
    out = []
    for el in elements:
        kind = classify_el(el)
        if not kind:
            continue
        item = dict(el)
        item["_kind"] = kind
        if el.get("type") == "way":
            geom = []
            for nid in el.get("nodes") or []:
                node = nodes.get(nid)
                if node and node.get("lat") is not None:
                    geom.append({"lat": node["lat"], "lon": node["lon"]})
            if geom:
                item["geometry"] = geom
                item["center"] = {
                    "lat": sum(p["lat"] for p in geom) / len(geom),
                    "lon": sum(p["lon"] for p in geom) / len(geom),
                }
        elif el.get("lat") is not None:
            item["center"] = {"lat": el["lat"], "lon": el["lon"]}
        out.append(item)
    return out


def cluster_rows(rows: list[sqlite3.Row], radius_km: float = 9.0) -> list[list[sqlite3.Row]]:
    clusters: list[list[sqlite3.Row]] = []
    for row in rows:
        lat, lon = float(row["lat"]), float(row["lon"])
        placed = False
        for cl in clusters:
            clat = sum(float(r["lat"]) for r in cl) / len(cl)
            clon = sum(float(r["lon"]) for r in cl) / len(cl)
            if haversine_m(lat, lon, clat, clon) <= radius_km * 1000:
                cl.append(row)
                placed = True
                break
        if not placed:
            clusters.append([row])
    return clusters


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def point_to_segment_m(lat: float, lon: float, a: tuple[float, float], b: tuple[float, float]) -> float:
    # a,b = (lat, lon); local meters
    mid_lat = math.radians((a[0] + b[0]) / 2 or lat)
    kx = 111320.0 * math.cos(mid_lat)
    ky = 110540.0
    x, y = lon * kx, lat * ky
    x1, y1 = a[1] * kx, a[0] * ky
    x2, y2 = b[1] * kx, b[0] * ky
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(x - x1, y - y1)
    t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))


def dist_to_geom_m(lat: float, lon: float, geom: list[dict] | list[list[float]] | None, center=None) -> float | None:
    if geom:
        pts: list[tuple[float, float]] = []
        for p in geom:
            if isinstance(p, dict):
                pts.append((float(p["lat"]), float(p["lon"])))
            else:
                pts.append((float(p[1]), float(p[0])))
        if len(pts) == 1:
            return haversine_m(lat, lon, pts[0][0], pts[0][1])
        best = min(point_to_segment_m(lat, lon, pts[i], pts[i + 1]) for i in range(len(pts) - 1))
        return best
    if center:
        return haversine_m(lat, lon, float(center[0]), float(center[1]))
    return None


def poly_area_ha(geom: list[dict] | None) -> float | None:
    if not geom or len(geom) < 4:
        return None
    pts = [(float(p["lon"]), float(p["lat"])) for p in geom]
    mid = math.radians(sum(p[1] for p in pts) / len(pts))
    kx = 111320.0 * math.cos(mid)
    ky = 110540.0
    acc = 0.0
    for i in range(len(pts) - 1):
        x1, y1 = pts[i][0] * kx, pts[i][1] * ky
        x2, y2 = pts[i + 1][0] * kx, pts[i + 1][1] * ky
        acc += x1 * y2 - x2 * y1
    return abs(acc) / 2.0 / 10000.0


def line_len_km(geom: list[dict] | None) -> float | None:
    if not geom or len(geom) < 2:
        return None
    total = 0.0
    for i in range(len(geom) - 1):
        total += haversine_m(geom[i]["lat"], geom[i]["lon"], geom[i + 1]["lat"], geom[i + 1]["lon"])
    return total / 1000.0


def fmt_km(meters: float | None) -> str:
    if meters is None:
        return "нет данных"
    if meters < 1000:
        return f"{int(round(meters))} м"
    return f"{meters / 1000:.1f} км".replace(".", ",")


def hw_name(tags: dict) -> str:
    cls = (tags.get("highway") or "").replace("_link", "")
    kind = HW_RU.get(cls, cls or "дорога")
    title = tags.get("name") or tags.get("ref") or ""
    ref = tags.get("ref") or ""
    if title and ref and ref not in title:
        return f"{kind}: {title} ({ref})"
    if title:
        return f"{kind}: {title}"
    if ref:
        return f"{kind}: {ref}"
    return kind


def is_federal(tags: dict) -> bool:
    blob = " ".join(filter(None, [tags.get("ref"), tags.get("name"), tags.get("official_name")]))
    return bool(FED_RE.search(blob)) or (tags.get("highway") in {"motorway", "trunk"} and bool(tags.get("ref")))


def cottage_program(area_ha: float) -> dict:
    lots = max(4, int(round(area_ha * 0.72 / 0.12)))
    k = min(0.65, 0.28 + 0.45 / math.sqrt(lots))
    p_inst = lots * 15
    p_sim = int(round(p_inst * k))
    gas_h = round(lots * 2.8 * 0.40, 1)
    gas_y = lots * 1800
    water_d = round(lots * 0.80, 1)
    return {
        "lots": lots,
        "p_inst_kw": p_inst,
        "p_sim_kw": p_sim,
        "gas_m3h": gas_h,
        "gas_m3y": gas_y,
        "water_m3d": water_d,
        "note": (
            f"ориентир КП: ~{lots} домов (12 соток + дороги), "
            f"электр. {p_inst} кВт заявл. / ~{p_sim} кВт одновр., "
            f"газ ~{gas_h} м³/ч и ~{gas_y:,} м³/год, "
            f"вода ~{water_d} м³/сут".replace(",", " ")
        ),
    }


def verdict(dist_m: float | None, good: float, ok: float, far: float) -> str:
    if dist_m is None:
        return "нет данных — нужна заявка в сеть"
    if dist_m <= good:
        return "скорее да, точка подключения рядом"
    if dist_m <= ok:
        return "возможно, нужна стройка линии/трубы"
    if dist_m <= far:
        return "сложно и дорого, без магистрали не обойтись"
    return "маловероятно без крупной стройки сетей"


def izhs_text(row: sqlite3.Row, city_km: float | None) -> str:
    vri = (row["permitted_use"] or "не указан").strip()
    cat = (row["land_category"] or "земли СХ").strip()
    legal = row["legal_complexity"] or "высокая"
    risk = row["conversion_risk"] or "высокий"
    city = row["nearest_city"] or "город МО"
    bits = [
        f"Сейчас: {cat}, ВРИ «{vri}». Для полноценного КП нужен перевод в земли населённых пунктов и ВРИ ИЖС / малоэтажная жилая застройка (172-ФЗ + генплан/ПЗЗ).",
        f"Сложность: {legal}, риск отказа: {risk}.",
    ]
    if city_km is not None and city_km <= 6:
        bits.append(f"Рядом {city} ({fmt_km(city_km * 1000)}) — шанс включить участок в границы населённого пункта выше, чем у дальнего поля.")
    elif city_km is not None and city_km <= 20:
        bits.append(f"Ближайший рынок — {city} ({fmt_km(city_km * 1000)}): перевод реален только при поддержке администрации и изменении генплана/ПЗЗ.")
    else:
        bits.append(f"Далеко от крупных городов ({city}, {fmt_km((city_km or 0) * 1000)}) — перевод в ИЖС обычно трудный и долгий.")
    if row["lph_or_garden_vri"]:
        bits.append("ВРИ ближе к ЛПХ/саду: жилой дом по 217-ФЗ теоретически проще, но продукт слабее полноценного ИЖС.")
    else:
        bits.append("Базовый путь: диагностика ПЗЗ/ЗОУИТ → ходатайство о смене категории/границ НП → слушания → ЕГРН → ППТ и ТУ на сети. Срок часто 1–3 года.")
    return " ".join(bits)


def ensure_table(cur: sqlite3.Cursor) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS parcel_infra_analysis (
            objdoc_id INTEGER PRIMARY KEY,
            cadastral_number TEXT,
            lots INTEGER,
            program_note TEXT,
            gas_ok TEXT,
            gas_km REAL,
            gas_name TEXT,
            gas_volume TEXT,
            elec_ok TEXT,
            elec_km REAL,
            elec_name TEXT,
            elec_volume TEXT,
            road_km REAL,
            road_name TEXT,
            fed_km REAL,
            fed_name TEXT,
            water_on_site INTEGER,
            water_km REAL,
            water_type TEXT,
            water_size TEXT,
            water_supply TEXT,
            soil_type TEXT,
            izhs TEXT,
            source_note TEXT,
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def load_parcels() -> list[sqlite3.Row]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            p.objdoc_id, p.cadastral_number, p.address, p.area_ha,
            p.permitted_use, p.land_category, p.vri_crop_policy,
            c.legal_complexity, c.conversion_risk, c.nearest_city, c.nearest_city_km,
            c.lph_or_garden_vri, c.has_village_or_settlement,
            m.lat, m.lon
        FROM farmland_parcels p
        JOIN parcel_map_points m ON m.objdoc_id = p.objdoc_id
        LEFT JOIN cottage_settlement_assessments c ON c.objdoc_id = p.objdoc_id
        WHERE p.region_code = '50' AND p.area_ha >= 1
        ORDER BY p.id
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def cell_key(lat: float, lon: float) -> tuple[int, int]:
    return int(math.floor(lat / CELL)), int(math.floor(lon / CELL))


def cell_bbox(key: tuple[int, int]) -> tuple[float, float, float, float]:
    i, j = key
    return i * CELL - PAD, j * CELL - PAD, (i + 1) * CELL + PAD, (j + 1) * CELL + PAD


def classify_el(el: dict) -> str | None:
    tags = el.get("tags") or {}
    if tags.get("substance") == "gas" or (
        tags.get("man_made") == "pipeline" and "газ" in (tags.get("name") or "").lower()
    ):
        return "gas"
    if tags.get("power") in {"line", "minor_line", "substation", "transformer", "portal", "cable"}:
        return "power"
    if tags.get("man_made") in {"water_tower", "water_works", "water_well"} or tags.get("landuse") == "reservoir":
        return "watersupply"
    if tags.get("natural") == "water" or tags.get("water") or tags.get("waterway") in {"river", "stream", "canal", "oxbow"}:
        return "water"
    if tags.get("highway") in HIGHWAY_OK:
        return "road"
    return None


def feature_label(kind: str, tags: dict) -> str:
    name = tags.get("name") or tags.get("ref") or ""
    if kind == "gas":
        return name or "газопровод"
    if kind == "power":
        base = {"line": "ЛЭП", "minor_line": "местная ЛЭП", "substation": "подстанция", "transformer": "ТП"}.get(
            tags.get("power") or "", "электросеть"
        )
        volt = tags.get("voltage")
        extra = f", {int(volt)/1000:.0f} кВ" if volt and str(volt).isdigit() else ""
        return f"{base}{extra}" + (f" «{name}»" if name else "")
    if kind == "water":
        wtype = tags.get("water") or tags.get("waterway") or ("водоём" if tags.get("natural") == "water" else "вода")
        ru = {
            "river": "река", "stream": "ручей", "canal": "канал", "lake": "озеро",
            "pond": "пруд", "reservoir": "водохранилище", "oxbow": "старица",
        }.get(wtype, wtype)
        return f"{ru}" + (f" «{name}»" if name else "")
    if kind == "watersupply":
        return name or tags.get("man_made") or "водоснабжение"
    if kind == "road":
        return hw_name(tags)
    return name or kind


def cache_path(prefix: str, key: tuple[int, int]) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    return CACHE / f"{prefix}_{key[0]}_{key[1]}.json"


def fetch_cell_centers(key: tuple[int, int]) -> list[dict]:
    path = cache_path("center", key)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    s, w, n, e = cell_bbox(key)
    q = f"""[out:json][timeout:35];
(
  way["highway"~"^(motorway|trunk|primary|secondary|tertiary|unclassified|residential|service|track)$"]({s},{w},{n},{e});
  way["power"~"^(line|minor_line|cable)$"]({s},{w},{n},{e});
  node["power"~"^(substation|transformer)$"]({s},{w},{n},{e});
  way["power"="substation"]({s},{w},{n},{e});
  way["man_made"="pipeline"]["substance"="gas"]({s},{w},{n},{e});
  node["man_made"="pipeline"]["substance"="gas"]({s},{w},{n},{e});
  way["natural"="water"]({s},{w},{n},{e});
  way["waterway"~"^(river|stream|canal)$"]({s},{w},{n},{e});
  node["man_made"~"^(water_tower|water_works|water_well)$"]({s},{w},{n},{e});
  way["man_made"~"^(water_tower|water_works)$"]({s},{w},{n},{e});
);
out tags center;
"""
    els = overpass(q, timeout=45)
    path.write_text(json.dumps(els, ensure_ascii=False), encoding="utf-8")
    time.sleep(1.2)
    return els


def fetch_way_geoms(way_ids: list[int]) -> dict[int, list[dict]]:
    out: dict[int, list[dict]] = {}
    uniq = sorted(set(way_ids))
    CACHE.mkdir(parents=True, exist_ok=True)
    for i in range(0, len(uniq), 40):
        chunk = uniq[i : i + 40]
        mark = CACHE / f"geom_{chunk[0]}_{chunk[-1]}_{len(chunk)}.json"
        if mark.exists():
            data = json.loads(mark.read_text(encoding="utf-8"))
        else:
            ids = ",".join(str(x) for x in chunk)
            q = f"[out:json][timeout:35];way(id:{ids});out tags geom;"
            data = overpass(q, timeout=45)
            mark.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            time.sleep(1.0)
        for el in data:
            if el.get("type") == "way" and el.get("geometry"):
                out[int(el["id"])] = el["geometry"]
    return out


def fetch_federal() -> list[dict]:
    path = CACHE / "federal_roads.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    CACHE.mkdir(parents=True, exist_ok=True)
    boxes = [
        (35.8, 56.6, 38.0, 54.8),
        (37.2, 56.6, 40.0, 54.8),
        (35.8, 56.0, 40.0, 55.2),
    ]
    feats: dict[tuple, dict] = {}
    for qname in FED_QUERIES:
        for vb in boxes:
            params = {
                "q": qname,
                "format": "geojson",
                "polygon_geojson": 1,
                "limit": 40,
                "dedupe": 0,
                "countrycodes": "ru",
                "viewbox": ",".join(map(str, vb)),
                "bounded": 1,
            }
            url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(params)
            try:
                data = http_json(url, timeout=25)
            except Exception:
                time.sleep(1.2)
                continue
            for f in data.get("features") or []:
                geom = f.get("geometry") or {}
                if geom.get("type") not in {"LineString", "MultiLineString"}:
                    continue
                oid = (qname, f.get("properties", {}).get("osm_id"))
                feats[oid] = {
                    "name": qname,
                    "display": (f.get("properties") or {}).get("display_name", qname),
                    "geometry": geom,
                }
            time.sleep(1.05)
    rows = list(feats.values())
    # plus local CKAD file if present
    ckad = ROOT / "ckad.geojson"
    if ckad.exists():
        g = json.loads(ckad.read_text(encoding="utf-8"))
        rows.append({"name": "ЦКАД A-113", "display": "ЦКАД (A-113)", "geometry": g.get("geometry")})
    path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    return rows


def fed_dist(lat: float, lon: float, roads: list[dict]) -> tuple[float | None, str]:
    best = None
    name = "нет данных"
    for road in roads:
        geom = road.get("geometry") or {}
        coords = geom.get("coordinates") or []
        lines = coords if geom.get("type") == "MultiLineString" else [coords]
        for line in lines:
            if not line:
                continue
            pts = [(float(p[1]), float(p[0])) for p in line]
            if len(pts) == 1:
                d = haversine_m(lat, lon, pts[0][0], pts[0][1])
            else:
                d = min(point_to_segment_m(lat, lon, pts[i], pts[i + 1]) for i in range(len(pts) - 1))
            if best is None or d < best:
                best = d
                name = road.get("name") or "федеральная трасса"
    return best, name


def soil_hint(lat: float, lon: float) -> str:
    if lat < 54.85:
        return "юг МО: серые лесные / выщелоченные чернозёмы, суглинки"
    if lon >= 38.7:
        return "Мещёра: супеси, пески, местами торфяные"
    if lat >= 56.1:
        return "север МО: дерново-подзолистые, часто супесь"
    return "центр/запад МО: дерново-подзолистые суглинки и супеси"


def fetch_soil(lat: float, lon: float, cache: dict) -> str:
    key = (round(lat, 1), round(lon, 1))
    if key in cache:
        return cache[key]
    path = CACHE / f"soil_{key[0]}_{key[1]}.json"
    data: dict = {}
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        url = SOIL_URL + "?" + urllib.parse.urlencode({"lon": key[1], "lat": key[0], "number_classes": 1})
        try:
            data = http_json(url, timeout=12)
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            time.sleep(0.3)
        except Exception:
            data = {}
    wrb = data.get("wrb_class_name") or ""
    ru = WRB_RU.get(wrb, wrb)
    hint = soil_hint(lat, lon)
    label = f"{ru}; {hint}" if ru else hint
    cache[key] = label
    return label


def nearest_of(lat: float, lon: float, items: list[dict], geoms: dict[int, list[dict]]) -> dict | None:
    ranked = []
    for it in items:
        c = it.get("center")
        if c:
            ranked.append((haversine_m(lat, lon, c["lat"], c["lon"]), it))
        elif it.get("lat") is not None:
            ranked.append((haversine_m(lat, lon, it["lat"], it["lon"]), it))
    ranked.sort(key=lambda x: x[0])
    items = [it for _, it in ranked[:40]]
    best = None
    for it in items:
        eid = it.get("id")
        geom = it.get("geometry") or (geoms.get(eid) if it.get("type") == "way" else None)
        center = None
        if it.get("lat") is not None:
            center = (it["lat"], it["lon"])
        elif it.get("center"):
            center = (it["center"]["lat"], it["center"]["lon"])
        d = dist_to_geom_m(lat, lon, geom, center)
        if d is None:
            continue
        if best is None or d < best["dist"]:
            tags = it.get("tags") or {}
            best = {
                "dist": d,
                "tags": tags,
                "id": eid,
                "geom": geom,
                "name": feature_label(it["_kind"], tags),
                "kind": it["_kind"],
            }
    return best


def overpass_around(kind: str, lat: float, lon: float, radius: int, query_inner: str) -> list[dict]:
    path = CACHE / f"around_{kind}_{round(lat, 3)}_{round(lon, 3)}_{radius}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    q = f"[out:json][timeout:30];({query_inner});out tags geom;"
    try:
        els = overpass(q, timeout=40, retries=3)
    except Exception as exc:
        print("   around fail", kind, exc)
        els = []
    path.write_text(json.dumps(els, ensure_ascii=False), encoding="utf-8")
    time.sleep(1.4)
    return els


def tagged_from_overpass(els: list[dict], kind: str) -> list[dict]:
    out = []
    for el in els:
        item = dict(el)
        item["_kind"] = kind
        if el.get("geometry"):
            item["center"] = {
                "lat": sum(p["lat"] for p in el["geometry"]) / len(el["geometry"]),
                "lon": sum(p["lon"] for p in el["geometry"]) / len(el["geometry"]),
            }
        elif el.get("lat") is not None:
            item["center"] = {"lat": el["lat"], "lon": el["lon"]}
        out.append(item)
    return out


def enrich_networks() -> None:
    """Добирает газ и ЛЭП более широким поиском, не пересчитывая всё заново."""
    rows = load_parcels()
    conn = get_conn()
    cur = conn.cursor()
    ensure_table(cur)
    existing = {r["objdoc_id"]: dict(r) for r in cur.execute("SELECT * FROM parcel_infra_analysis")}
    if len(existing) < 50:
        conn.close()
        print("Сначала нужен полный analyze()")
        return

    gas_clusters = cluster_rows(rows, radius_km=18)
    gas_pool: list[dict] = []
    gas_geoms: dict[int, list[dict]] = {}
    print(f"Газ: кластеров {len(gas_clusters)}")
    for i, cl in enumerate(gas_clusters, 1):
        lat = sum(float(r["lat"]) for r in cl) / len(cl)
        lon = sum(float(r["lon"]) for r in cl) / len(cl)
        inner = (
            f'way["man_made"="pipeline"]["substance"="gas"](around:20000,{lat:.5f},{lon:.5f});'
            f'way["pipeline"="gas"](around:20000,{lat:.5f},{lon:.5f});'
            f'node["name"~"ГРС"](around:20000,{lat:.5f},{lon:.5f});'
        )
        print(f"  газ {i}/{len(gas_clusters)}", flush=True)
        tagged = tagged_from_overpass(overpass_around("gas", lat, lon, 20000, inner), "gas")
        for el in tagged:
            if el.get("geometry"):
                gas_geoms[int(el["id"])] = el["geometry"]
            gas_pool.append(el)
        print(f"    +{len(tagged)}", flush=True)

    miss_elec = [r for r in rows if not existing.get(r["objdoc_id"], {}).get("elec_km")]
    elec_clusters = cluster_rows(miss_elec, radius_km=14) if miss_elec else []
    elec_by_oid: dict[int, list[dict]] = defaultdict(list)
    elec_geoms: dict[int, list[dict]] = {}
    print(f"ЛЭП: без данных {len(miss_elec)}, кластеров {len(elec_clusters)}")
    for i, cl in enumerate(elec_clusters, 1):
        lat = sum(float(r["lat"]) for r in cl) / len(cl)
        lon = sum(float(r["lon"]) for r in cl) / len(cl)
        inner = (
            f'way["power"~"^(line|minor_line)$"](around:12000,{lat:.5f},{lon:.5f});'
            f'node["power"~"^(substation|transformer)$"](around:12000,{lat:.5f},{lon:.5f});'
            f'way["power"="substation"](around:12000,{lat:.5f},{lon:.5f});'
        )
        print(f"  лэп {i}/{len(elec_clusters)}", flush=True)
        tagged = tagged_from_overpass(overpass_around("power", lat, lon, 12000, inner), "power")
        for el in tagged:
            if el.get("geometry"):
                elec_geoms[int(el["id"])] = el["geometry"]
        for r in cl:
            elec_by_oid[int(r["objdoc_id"])].extend(tagged)
        print(f"    +{len(tagged)}", flush=True)

    updated = 0
    for row in rows:
        oid = int(row["objdoc_id"])
        rec = existing.get(oid)
        if not rec:
            continue
        lat, lon = float(row["lat"]), float(row["lon"])
        changed = False
        if rec.get("gas_km") is None and gas_pool:
            hit = nearest_of(lat, lon, gas_pool, gas_geoms)
            if hit:
                rec["gas_km"] = round(hit["dist"] / 1000, 3)
                rec["gas_ok"] = verdict(hit["dist"], 350, 1600, 5000)
                rec["gas_name"] = hit["name"]
                changed = True
        if rec.get("elec_km") is None and elec_by_oid.get(oid):
            hit = nearest_of(lat, lon, elec_by_oid[oid], elec_geoms)
            if hit:
                rec["elec_km"] = round(hit["dist"] / 1000, 3)
                rec["elec_ok"] = verdict(hit["dist"], 400, 2000, 8000)
                rec["elec_name"] = hit["name"]
                changed = True
        if changed:
            cur.execute(
                """
                UPDATE parcel_infra_analysis
                SET gas_ok=?, gas_km=?, gas_name=?, elec_ok=?, elec_km=?, elec_name=?
                WHERE objdoc_id=?
                """,
                (rec["gas_ok"], rec["gas_km"], rec["gas_name"], rec["elec_ok"], rec["elec_km"], rec["elec_name"], oid),
            )
            updated += 1
    conn.commit()
    conn.close()
    print(f"Обновлено участков: {updated}")


def analyze() -> None:
    rows = load_parcels()
    tile = 0.08
    tiles: dict[tuple[int, int], list[int]] = defaultdict(list)
    for row in rows:
        lat, lon = float(row["lat"]), float(row["lon"])
        key = (int(math.floor(lat / tile)), int(math.floor(lon / tile)))
        tiles[key].append(int(row["objdoc_id"]))
    print(f"Участков {len(rows)}, тайлов OSM {len(tiles)}")
    geoms: dict[int, list[dict]] = {}
    tile_els: dict[tuple[int, int], list[dict]] = {}
    CACHE.mkdir(parents=True, exist_ok=True)
    for i, key in enumerate(sorted(tiles), 1):
        s, w = key[0] * tile, key[1] * tile
        n, e = s + tile, w + tile
        print(f"  OSM {i}/{len(tiles)} {s:.3f},{w:.3f}", flush=True)
        try:
            tagged = parse_osm_elements(osm_map(s, w, n, e))
        except Exception as exc:
            print("   fail", exc)
            tagged = []
        tile_els[key] = tagged
        for el in tagged:
            if el.get("geometry"):
                geoms[int(el["id"])] = el["geometry"]
        print(f"    объектов {len(tagged)}", flush=True)

    by_parcel: dict[int, list[dict]] = defaultdict(list)
    seen_pair: set[tuple[int, int]] = set()
    for key, oids in tiles.items():
        for oid in oids:
            for el in tile_els.get(key) or []:
                pair = (oid, int(el["id"]))
                if pair in seen_pair:
                    continue
                seen_pair.add(pair)
                by_parcel[oid].append(el)

    print("Федеральные трассы…", flush=True)
    federal = fetch_federal()
    print(f"  сегментов трасс: {len(federal)}")

    soil_cache: dict = {}
    conn = get_conn()
    cur = conn.cursor()
    ensure_table(cur)
    cur.execute("DELETE FROM parcel_infra_analysis")

    for idx, row in enumerate(rows, 1):
        lat, lon = float(row["lat"]), float(row["lon"])
        tagged = by_parcel.get(row["objdoc_id"]) or []
        by_kind = defaultdict(list)
        for el in tagged:
            by_kind[el["_kind"]].append(el)
        gas = nearest_of(lat, lon, by_kind["gas"], geoms)
        power = nearest_of(lat, lon, by_kind["power"], geoms)
        road = nearest_of(lat, lon, by_kind["road"], geoms)
        water = nearest_of(lat, lon, by_kind["water"], geoms)
        wsup = nearest_of(lat, lon, by_kind["watersupply"], geoms)
        fed_m, fed_name = fed_dist(lat, lon, federal)
        # federal from local OSM roads if closer
        if road and is_federal(road["tags"]):
            if fed_m is None or road["dist"] < fed_m:
                fed_m, fed_name = road["dist"], road["name"]
        else:
            for el in by_kind["road"]:
                if not is_federal(el.get("tags") or {}):
                    continue
                hit = nearest_of(lat, lon, [{**el, "_kind": "road"}], geoms)
                if hit and (fed_m is None or hit["dist"] < fed_m):
                    fed_m, fed_name = hit["dist"], hit["name"]

        prog = cottage_program(float(row["area_ha"] or 0))
        gas_d = gas["dist"] if gas else None
        elec_d = power["dist"] if power else None
        road_d = road["dist"] if road else None
        water_d = water["dist"] if water else None
        wsup_d = wsup["dist"] if wsup else None
        on_site = 1 if water_d is not None and water_d <= 40 else 0
        water_size = "нет данных"
        if water and water.get("geom"):
            tags = water["tags"]
            if tags.get("natural") == "water" or tags.get("water"):
                area = poly_area_ha(water["geom"])
                water_size = f"{area:.2f} га".replace(".", ",") if area else "контур без площади"
            else:
                ln = line_len_km(water["geom"])
                water_size = f"длина фрагмента {ln:.1f} км".replace(".", ",") if ln else "русло без длины"
        if wsup_d is not None and wsup_d <= 1500:
            water_supply = f"централизованно вероятно реально: {wsup['name']} в {fmt_km(wsup_d)}"
        elif water_d is not None and water_d <= 300 and on_site:
            water_supply = "на участке есть водоём — для КП обычно скважины + ЛОС, водоём не питьевой"
        else:
            water_supply = "централи нет рядом; для КП в МО типичны скважины 30–80 м и локальная канализация"

        soil = fetch_soil(lat, lon, soil_cache)
        city_km = float(row["nearest_city_km"]) if row["nearest_city_km"] is not None else None
        gas_place = (row["nearest_city"] or "населённый пункт") + (
            f", {fmt_km(city_km * 1000)}" if city_km is not None else ""
        )
        cur.execute(
            """
            INSERT INTO parcel_infra_analysis (
                objdoc_id, cadastral_number, lots, program_note,
                gas_ok, gas_km, gas_name, gas_volume,
                elec_ok, elec_km, elec_name, elec_volume,
                road_km, road_name, fed_km, fed_name,
                water_on_site, water_km, water_type, water_size, water_supply,
                soil_type, izhs, source_note
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                row["objdoc_id"], row["cadastral_number"], prog["lots"], prog["note"],
                verdict(gas_d, 350, 1600, 5000),
                None if gas_d is None else round(gas_d / 1000, 3),
                (gas["name"] + f"; ближайший город/рынок: {gas_place}") if gas else f"газопровод в выгрузке OSM не найден; ориентир — {gas_place}",
                f"{prog['gas_m3h']} м³/ч · {prog['gas_m3y']} м³/год на {prog['lots']} домов",
                verdict(elec_d, 400, 2000, 8000),
                None if elec_d is None else round(elec_d / 1000, 3),
                power["name"] if power else "ЛЭП/подстанция в выгрузке OSM не найдены",
                f"{prog['p_inst_kw']} кВт заявл. · ~{prog['p_sim_kw']} кВт одновр. на {prog['lots']} домов",
                None if road_d is None else round(road_d / 1000, 3),
                road["name"] if road else "дорога не найдена в OSM",
                None if fed_m is None else round(fed_m / 1000, 3),
                fed_name,
                on_site,
                None if water_d is None else round(water_d / 1000, 3),
                water["name"] if water else "водоём рядом не найден",
                water_size,
                water_supply,
                soil,
                izhs_text(row, city_km),
                "OSM Overpass + Nominatim трассы + ISRIC WRB; не ТУ",
            ),
        )
        if idx % 40 == 0:
            conn.commit()
            print(f"  посчитано {idx}/{len(rows)}", flush=True)
    conn.commit()
    conn.close()
    print("Анализ записан в parcel_infra_analysis")


def km_txt(km: float | None) -> str:
    if km is None:
        return "н/д"
    return fmt_km(km * 1000)


def apply_html() -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT a.*, p.address, p.area_ha, d.cost_value,
               c.cottage_score, c.cottage_recommendation, c.nearest_city, c.nearest_city_km
        FROM parcel_infra_analysis a
        JOIN farmland_parcels p ON p.objdoc_id = a.objdoc_id
        LEFT JOIN farmland_details d ON d.objdoc_id = a.objdoc_id
        LEFT JOIN cottage_settlement_assessments c ON c.objdoc_id = a.objdoc_id
        """
    )
    by_cad = {r["cadastral_number"]: dict(r) for r in cur.fetchall()}
    conn.close()
    html = HTML_PATH.read_text(encoding="utf-8")
    m = re.search(r"const DATA = (\{.*?\});\n    function parcelStyle", html, re.S)
    if not m:
        raise SystemExit("DATA block not found")
    data = json.loads(m.group(1))
    for feat in data["features"]:
        p = feat["properties"]
        a = by_cad.get(p["cad"]) or {}
        p.update(
            {
                "gas_ok": a.get("gas_ok") or "нет данных",
                "gas_km": km_txt(a.get("gas_km")),
                "gas_name": a.get("gas_name") or "",
                "gas_volume": a.get("gas_volume") or "",
                "elec_ok": a.get("elec_ok") or "нет данных",
                "elec_km": km_txt(a.get("elec_km")),
                "elec_name": a.get("elec_name") or "",
                "elec_volume": a.get("elec_volume") or "",
                "road_km": km_txt(a.get("road_km")),
                "road_name": a.get("road_name") or "",
                "fed_km": km_txt(a.get("fed_km")),
                "fed_name": a.get("fed_name") or "",
                "water_on": "да" if a.get("water_on_site") else "нет",
                "water_km": km_txt(a.get("water_km")),
                "water_type": a.get("water_type") or "",
                "water_size": a.get("water_size") or "",
                "water_supply": a.get("water_supply") or "",
                "soil": a.get("soil_type") or "",
                "izhs": a.get("izhs") or "",
                "program": a.get("program_note") or "",
                "kp_score": a.get("cottage_score") if a.get("cottage_score") is not None else "",
                "kp_reco": a.get("cottage_recommendation") or "",
            }
        )
    new_data = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    html = html[: m.start(1)] + new_data + html[m.end(1) :]

    if ".popup .block" not in html:
        html = html.replace(
            "    .popup { min-width: 220px; }",
            "    .popup { min-width: 280px; max-width: 360px; }\n"
            "    .popup .block { margin-top: 8px; font-size: 12px; line-height: 1.35; }\n"
            "    .popup .block b { color: #333; }\n"
            "    td.an { font-size: 12px; line-height: 1.35; color: #e8e8e8; }\n"
            "    #detail { display: none; margin: 0 18px 12px; padding: 12px 14px; background: #1f1f1f;\n"
            "      border: 1px solid #444; border-radius: 8px; font-size: 13px; line-height: 1.45; }\n"
            "    #detail.open { display: block; }\n"
            "    #detail h3 { margin: 0 0 8px; font-size: 15px; }\n"
            "    #detail p { margin: 0 0 6px; color: #ddd; }",
        )
    if "<th>Оценка КП</th>" not in html and "<th>Перевод в ИЖС</th>" in html:
        html = html.replace(
            "            <th>Перевод в ИЖС</th>\n",
            "            <th>Перевод в ИЖС</th>\n            <th>Оценка КП</th>\n",
        )
    if "Оценка КП:" not in html:
        html = html.replace(
            '        `<div class="block"><b>ИЖС:</b> ${p.izhs}</div>` +',
            '        `<div class="block"><b>ИЖС:</b> ${p.izhs}</div>` +\n'
            '        `<div class="block"><b>Оценка КП:</b> ${p.kp_score} · ${p.kp_reco}</div>` +',
        )
    if "<th>Газ</th>" not in html:
        html = html.replace(
            "            <th>Кадастровая стоимость, ₽</th>\n",
            "            <th>Кадастровая стоимость, ₽</th>\n"
            "            <th>Газ</th>\n"
            "            <th>Электричество</th>\n"
            "            <th>Дорога</th>\n"
            "            <th>Федеральная трасса</th>\n"
            "            <th>Водоём</th>\n"
            "            <th>Водоснабжение</th>\n"
            "            <th>Почва</th>\n"
            "            <th>Перевод в ИЖС</th>\n"
            "            <th>Оценка КП</th>\n",
        )
    # rebuild tbody
    tbody = []
    for feat in data["features"]:
        p = feat["properties"]
        cost = "нет данных" if p.get("cost") is None else f"{p['cost']}"
        if p.get("cost") is not None:
            cost = f"{p['cost']:,.2f}".replace(",", " ").replace(".", ",") if isinstance(p["cost"], (int, float)) else str(p["cost"])
        tbody.append(
            "<tr>"
            f"<td>{p.get('address') or ''}</td>"
            f"<td>{p['cad']}</td>"
            f"<td class='num'>{p['ha']}</td>"
            f"<td class='num'>{cost}</td>"
            f"<td class='an'>{p['gas_ok']}<br>{p['gas_km']}<br>{p['gas_volume']}</td>"
            f"<td class='an'>{p['elec_ok']}<br>{p['elec_km']}<br>{p['elec_volume']}</td>"
            f"<td class='an'>{p['road_name']}<br>{p['road_km']}</td>"
            f"<td class='an'>{p['fed_name']}<br>{p['fed_km']}</td>"
            f"<td class='an'>на участке: {p['water_on']}<br>{p['water_type']}, {p['water_km']}<br>{p['water_size']}</td>"
            f"<td class='an'>{p['water_supply']}</td>"
            f"<td class='an'>{p['soil']}</td>"
            f"<td class='an'>{p['izhs']}</td>"
            f"<td class='an'>{p.get('kp_score','')} · {p.get('kp_reco','')}</td>"
            "</tr>"
        )
    html = re.sub(
        r"<tbody id=\"rows\">.*?</tbody>",
        "<tbody id=\"rows\">" + "".join(tbody) + "</tbody>",
        html,
        count=1,
        flags=re.S,
    )
    if 'id="detail"' not in html:
        html = html.replace(
            '    <div class="table-wrap">',
            '    <div id="detail"></div>\n    <div class="table-wrap">',
        )

    old_popup = """    function popupHtml(p) {
      return `<div class="popup"><div class="cad">${p.cad}</div>` +
        `<div class="addr">${p.address}</div>` +
        `<div>${fmtHa(p.ha)} · ${fmtRub(p.cost)}</div></div>`;
    }"""
    new_popup = """    function popupHtml(p) {
      return `<div class="popup"><div class="cad">${p.cad}</div>` +
        `<div class="addr">${p.address}</div>` +
        `<div>${fmtHa(p.ha)} · ${fmtRub(p.cost)}</div>` +
        `<div class="block"><b>Газ:</b> ${p.gas_ok}. ${p.gas_km}. ${p.gas_name}. ${p.gas_volume}</div>` +
        `<div class="block"><b>Электричество:</b> ${p.elec_ok}. ${p.elec_km}. ${p.elec_name}. ${p.elec_volume}</div>` +
        `<div class="block"><b>Дорога:</b> ${p.road_name}, ${p.road_km}</div>` +
        `<div class="block"><b>Федеральная:</b> ${p.fed_name}, ${p.fed_km}</div>` +
        `<div class="block"><b>Водоём:</b> на участке ${p.water_on}; ${p.water_type}, ${p.water_km}, ${p.water_size}</div>` +
        `<div class="block"><b>Водоснабжение:</b> ${p.water_supply}</div>` +
        `<div class="block"><b>Почва:</b> ${p.soil}</div>` +
        `<div class="block"><b>ИЖС:</b> ${p.izhs}</div>` +
        `<div class="block"><b>Оценка КП:</b> ${p.kp_score} · ${p.kp_reco}</div>` +
        `<div class="block">${p.program}</div></div>`;
    }
    function fillDetail(p) {
      const box = document.getElementById("detail");
      if (!box || !p) return;
      box.classList.add("open");
      box.innerHTML = `<h3>${p.cad}</h3>` + popupHtml(p);
    }"""
    if old_popup in html:
        html = html.replace(old_popup, new_popup)
    html = html.replace(
        "        layers[i].openPopup();\n          }\n        }\n      }",
        "        layers[i].openPopup();\n          }\n          fillDetail(DATA.features[i].properties);\n        }\n      }",
    )
    # also fill detail on map click highlight
    html = html.replace(
        "        rows[i].classList.add(\"active\");\n        if (fly) {",
        "        rows[i].classList.add(\"active\");\n        fillDetail(DATA.features[i].properties);\n        if (fly) {",
    )
    HTML_PATH.write_text(html, encoding="utf-8")
    print("HTML обновлён:", HTML_PATH)


if __name__ == "__main__":
    import sys
    if "--html-only" in sys.argv:
        apply_html()
    elif "--enrich" in sys.argv:
        enrich_networks()
        apply_html()
    else:
        analyze()
        apply_html()
