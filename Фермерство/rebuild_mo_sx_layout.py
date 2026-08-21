#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Пересобирает mo_sx_1ha.html: чипы, кадастр, слои 2ГИС / Яндекс / Google."""

from __future__ import annotations

import re
from pathlib import Path

SRC = Path(__file__).with_name("mo_sx_1ha.html")


def extract(name: str, text: str) -> str:
    m = re.search(rf"const {name} = (\{{.*?\}});\n", text, re.S)
    if not m:
        raise SystemExit(f"{name} not found")
    return m.group(1)


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    data = extract("DATA", text)
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#f4f1ea">
  <title>Карта земель СХ от 1 га — Московская область</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <style>
    :root {{
      color-scheme: light;
      --bg: #f4f1ea;
      --panel: #ffffff;
      --line: #d8d2c6;
      --text: #1c1a16;
      --muted: #6b655c;
      --gold: #d4a200;
      --pad: max(12px, env(safe-area-inset-left));
    }}
    * {{ box-sizing: border-box; }}
    html, body {{
      margin: 0; height: 100%; background: var(--bg); color: var(--text);
      font: 15px/1.4 -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;
    }}
    body {{ overflow: hidden; }}
    .app {{
      height: 100dvh; display: flex; flex-direction: column;
      padding-top: env(safe-area-inset-top);
    }}
    header {{
      flex: 0 0 auto; padding: 10px var(--pad) 10px;
      border-bottom: 1px solid var(--line); background: #fff;
    }}
    h1 {{ font-size: 17px; margin: 0 0 2px; }}
    .meta {{ margin: 0 0 8px; color: var(--muted); font-size: 12px; }}
    #q {{
      width: 100%; padding: 11px 12px; border: 1px solid #c9c3b6;
      border-radius: 10px; background: #fff; color: var(--text); font-size: 16px;
    }}
    .layout {{ flex: 1; min-height: 0; display: flex; flex-direction: column; }}
    .map-col {{ flex: 0 0 auto; position: relative; }}
    #map {{ height: 42dvh; min-height: 220px; background: #e8e4da; }}
    .basemaps {{
      position: absolute; top: 10px; left: 10px; z-index: 500;
      display: flex; flex-wrap: wrap; gap: 4px; max-width: calc(100% - 68px);
    }}
    .basemaps button {{
      appearance: none; border: 1px solid #c9c3b6; background: rgba(255,255,255,.94);
      border-radius: 999px; padding: 6px 10px; font: 12px/1.2 inherit; color: #1c1a16;
      cursor: pointer; box-shadow: 0 1px 4px rgba(0,0,0,.1);
    }}
    .basemaps button.on {{ background: #fff6d6; border-color: var(--gold); font-weight: 700; }}
    .legend {{
      position: absolute; left: 10px; bottom: 10px; z-index: 500;
      display: flex; gap: 8px; flex-wrap: wrap;
      background: rgba(255,255,255,.92); padding: 6px 8px; border-radius: 8px;
      font-size: 11px; color: #333; box-shadow: 0 1px 4px rgba(0,0,0,.12);
    }}
    .legend-item {{ display: flex; align-items: center; gap: 6px; }}
    .swatch {{ width: 16px; height: 10px; background: rgba(255,208,0,.75); border: 2px solid #c49200; }}
    .side {{
      flex: 1; min-height: 0; overflow: auto; -webkit-overflow-scrolling: touch;
      padding: 10px var(--pad) calc(16px + env(safe-area-inset-bottom));
      background: var(--bg);
    }}
    .card, .item {{
      background: var(--panel); border: 1px solid var(--line); border-radius: 12px;
      padding: 12px;
    }}
    .card {{ margin-bottom: 10px; }}
    .card.empty {{ color: var(--muted); }}
    .card h2 {{ margin: 0 0 4px; font-size: 16px; }}
    .card .addr {{ color: #3a3732; margin: 0 0 8px; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0 0; }}
    .chip {{
      display: inline-flex; align-items: center; gap: 5px;
      background: #efe8d8; border-radius: 999px; padding: 5px 9px;
      font-size: 12px; color: #2a2618; max-width: 100%;
    }}
    .chip i {{ font-style: normal; opacity: .72; font-size: 11px; }}
    .chip.money {{ background: #e4eedc; }}
    .chip.gas {{ background: #f3e4d4; }}
    .chip.elec {{ background: #e4e8f6; }}
    .chip.road {{ background: #ece6dc; }}
    .chip.fed {{ background: #f6e4d8; }}
    .chip.water {{ background: #dceef4; }}
    .chip.soil {{ background: #e8e2d0; }}
    .chip.kp {{ background: #efe4c8; }}
    .chip.izhs {{ background: #f3e0dc; }}
    .notes {{ display: grid; gap: 8px; margin-top: 10px; }}
    .note .k {{ display: block; color: var(--muted); font-size: 11px; margin-bottom: 2px; }}
    .note .v {{ font-size: 13px; }}
    .list {{ display: flex; flex-direction: column; gap: 8px; }}
    .item {{
      cursor: pointer; width: 100%; text-align: left; color: inherit;
      font: inherit; appearance: none; -webkit-appearance: none;
    }}
    .item.active {{ border-color: var(--gold); background: #fff6d6; }}
    .item .cad {{ font-weight: 700; font-size: 14px; }}
    .item .addr {{
      color: var(--muted); font-size: 13px; margin: 4px 0 6px;
      display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
    }}
    .leaflet-popup-content {{ color: #111; margin: 10px 12px; }}
    .popup {{ max-width: 260px; }}
    .popup .cad {{ font-weight: 700; }}
    .popup .chips {{ margin-top: 8px; }}
    .ext {{ margin: 8px 0 0; font-size: 13px; }}
    .ext a {{ color: #1a5fb4; }}
    .leaflet-control-attribution {{ font-size: 10px; }}
    @media (min-width: 900px) {{
      header {{ padding: 12px 18px; }}
      h1 {{ font-size: 20px; }}
      .layout {{ flex-direction: row; }}
      .map-col {{ flex: 1; min-width: 0; display: flex; flex-direction: column; }}
      #map {{ flex: 1; height: auto; min-height: 0; }}
      .side {{
        width: min(440px, 42vw); border-left: 1px solid var(--line);
        padding: 12px 14px 18px;
      }}
    }}
  </style>
</head>
<body>
  <div class="app">
    <header>
      <h1>Земли СХ от 1 га — Московская область</h1>
      <p class="meta">215 участков · 3 114,87 га · газ, свет, дороги, вода, почва, кадастр, ИЖС (ориентир, не ТУ)</p>
      <input id="q" type="search" placeholder="Поиск по адресу или кадастровому номеру" enterkeyhint="search">
    </header>
    <div class="layout">
      <div class="map-col">
        <div id="map"></div>
        <div class="basemaps" id="basemaps"></div>
        <div class="legend">
          <span class="legend-item"><span class="swatch"></span> Земли СХ</span>
        </div>
      </div>
      <aside class="side">
        <div id="detail" class="card empty">Нажмите участок на карте или в списке</div>
        <div id="list" class="list"></div>
      </aside>
    </div>
  </div>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    const DATA = {data};

    function parcelStyle(active) {{
      const z = map ? map.getZoom() : 8;
      if (active) {{
        return {{ color: "#FFB000", weight: z < 10 ? 7 : 4, opacity: 1, fillColor: "#FFD000", fillOpacity: z < 10 ? 0.85 : 0.62 }};
      }}
      return {{
        color: z < 10 ? "#C49200" : "#E0A800",
        weight: z < 8 ? 7 : z < 10 ? 5 : z < 13 ? 3.5 : 3,
        opacity: 1, fillColor: "#FFD000", fillOpacity: z < 10 ? 0.78 : 0.5
      }};
    }}
    function fmtHa(ha) {{
      return ha.toLocaleString("ru-RU", {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }}) + " га";
    }}
    function fmtMoney(v, suffix) {{
      if (v == null || !isFinite(v)) return null;
      const n = Number(v);
      if (n >= 1e6) return (n / 1e6).toLocaleString("ru-RU", {{ maximumFractionDigits: 1 }}) + " млн ₽" + (suffix || "");
      if (n >= 1e3) return (n / 1e3).toLocaleString("ru-RU", {{ maximumFractionDigits: 0 }}) + " тыс. ₽" + (suffix || "");
      return n.toLocaleString("ru-RU", {{ maximumFractionDigits: 0 }}) + " ₽" + (suffix || "");
    }}
    function fmtCost(v) {{ return fmtMoney(v) || "н/д"; }}
    function fmtCostFull(v) {{
      if (v == null) return "кадастровая стоимость не указана";
      return Number(v).toLocaleString("ru-RU", {{ maximumFractionDigits: 0 }}) + " ₽";
    }}
    function fmtCostHa(cost, ha) {{
      if (cost == null || !ha) return "н/д";
      return fmtMoney(cost / ha) || "н/д";
    }}
    function esc(s) {{
      return String(s ?? "").replace(/[&<>"]/g, (ch) => ({{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }}[ch]));
    }}
    function izhsChip(p) {{
      const m = /Сложность:\\s*([^.,]+)/.exec(p.izhs || "");
      return "ИЖС: " + (m ? m[1].trim() : "нужен перевод");
    }}
    function waterChip(p) {{
      if (p.water_on === "да") return "водоём на участке, " + (p.water_type || "есть") + (p.water_size ? ", " + p.water_size : "");
      return (p.water_type || "водоём") + " " + (p.water_km || "");
    }}
    function chip(cls, icon, text, title) {{
      return `<span class="chip ${{cls}}"${{title ? ` title="${{esc(title)}}"` : ""}}><i>${{esc(icon)}}</i>${{esc(text)}}</span>`;
    }}
    function chipsHtml(p, kind) {{
      const extra = kind !== "list";
      const out = [
        chip("area", "га", fmtHa(p.ha).replace(" га", "")),
        chip("money", "кадастр", fmtCost(p.cost), fmtCostFull(p.cost)),
        chip("money", "₽/га", fmtCostHa(p.cost, p.ha)),
        chip("gas", "газ", p.gas_km),
        chip("elec", "свет", p.elec_km),
        chip("road", "дорога", p.road_km),
        chip("fed", "трасса", ((p.fed_name || "") + " " + (p.fed_km || "")).trim()),
        chip("water", "вода", waterChip(p)),
        chip("soil", "почва", kind === "list" ? String(p.soil || "").split(";")[0] : p.soil),
        chip("kp", "КП", String(p.kp_score) + (p.kp_reco ? " · " + p.kp_reco : "")),
      ];
      if (extra) {{
        out.push(
          chip("gas", "подкл. газа", p.gas_ok),
          chip("elec", "подкл. света", p.elec_ok),
          chip("road", "какая дорога", p.road_name),
          chip("water", "водоснабжение", p.water_supply),
          chip("izhs", "ИЖС", izhsChip(p).replace(/^ИЖС:\\s*/, ""))
        );
      }}
      return `<div class="chips">${{out.join("")}}</div>`;
    }}
    function popupHtml(p) {{
      return `<div class="popup"><div class="cad">${{esc(p.cad)}}</div>` +
        `<div>${{esc(p.address)}}</div>` +
        chipsHtml(p, "list") + `</div>`;
    }}
    function fillDetail(p) {{
      const box = document.getElementById("detail");
      if (!box || !p) return;
      box.classList.remove("empty");
      box.innerHTML =
        `<h2>${{esc(p.cad)}}</h2>` +
        `<p class="addr">${{esc(p.address)}}</p>` +
        chipsHtml(p, "detail") +
        `<p class="ext"><a href="https://nspd.gov.ru/map?query=${{encodeURIComponent(p.cad)}}" target="_blank" rel="noopener">НСПД</a> · ` +
          `<a href="https://map.ru/pkk?search=${{encodeURIComponent(p.cad)}}" target="_blank" rel="noopener">map.ru</a></p>` +
        `<div class="notes">` +
          `<div class="note"><span class="k">Газ</span><div class="v">${{esc(p.gas_ok)}}. ${{esc(p.gas_name)}}. ${{esc(p.gas_volume)}}</div></div>` +
          `<div class="note"><span class="k">Электричество</span><div class="v">${{esc(p.elec_ok)}}. ${{esc(p.elec_name)}}. ${{esc(p.elec_volume)}}</div></div>` +
          `<div class="note"><span class="k">Перевод в ИЖС</span><div class="v">${{esc(p.izhs)}}</div></div>` +
          `<div class="note"><span class="k">Программа КП</span><div class="v">${{esc(p.program)}}</div></div>` +
        `</div>`;
      box.scrollIntoView({{ behavior: "smooth", block: "nearest" }});
    }}
    function itemHtml(p, i) {{
      return `<button type="button" class="item" data-i="${{i}}">` +
        `<div class="cad">${{esc(p.cad)}}</div>` +
        `<div class="addr">${{esc(p.address)}}</div>` +
        chipsHtml(p, "list") + `</button>`;
    }}

    const CRS3395 = L.extend({{}}, L.CRS.Earth, {{
      code: "EPSG:3395",
      projection: L.Projection.Mercator,
      transformation: (function () {{
        const scale = 0.5 / (Math.PI * L.Projection.Mercator.R);
        return L.transformation(scale, 0.5, -scale, 0.5);
      }})()
    }});
    function featureCenter(feature) {{
      const acc = [];
      (function walk(c) {{
        if (typeof c[0] === "number") acc.push(c);
        else c.forEach(walk);
      }})(feature.geometry.coordinates);
      return [acc.reduce((s, p) => s + p[1], 0) / acc.length, acc.reduce((s, p) => s + p[0], 0) / acc.length];
    }}
    function makeTiles(name) {{
      if (name === "sat") {{
        return [
          L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}", {{
            maxZoom: 19, attribution: "Tiles © Esri"
          }}),
          L.tileLayer("https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{{z}}/{{x}}/{{y}}{{r}}.png", {{
            maxZoom: 19, attribution: "© CARTO"
          }})
        ];
      }}
      if (name === "twogis") {{
        return [L.tileLayer("https://tile{{s}}.maps.2gis.com/tiles?x={{x}}&y={{y}}&z={{z}}", {{
          subdomains: "0123", maxZoom: 18, attribution: "© 2ГИС"
        }})];
      }}
      if (name === "yandex") {{
        return [L.tileLayer("https://core-renderer-tiles.maps.yandex.net/tiles?l=map&x={{x}}&y={{y}}&z={{z}}&scale=1&lang=ru_RU", {{
          maxZoom: 19, attribution: "© Яндекс"
        }})];
      }}
      if (name === "google") {{
        return [L.tileLayer("https://mt{{s}}.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}", {{
          subdomains: "0123", maxZoom: 20, attribution: "© Google"
        }})];
      }}
      return [L.tileLayer("https://{{s}}.tile.opentopomap.org/{{z}}/{{x}}/{{y}}.png", {{
        subdomains: "abc", maxZoom: 17, attribution: "© OpenStreetMap, © OpenTopoMap (CC-BY-SA)"
      }})];
    }}

    let map, geo, dotsLayer, currentBase = [], currentBaseName = "";
    const layers = [];
    const dots = [];
    let active = -1;

    function attachParcels() {{
      layers.splice(0, layers.length);
      dots.splice(0, dots.length);
      dotsLayer = L.layerGroup();
      geo = L.geoJSON(DATA, {{
        style: () => parcelStyle(false),
        onEachFeature: (feature, lyr) => {{
          const i = layers.length;
          lyr.bindPopup(popupHtml(feature.properties));
          lyr.on("click", () => highlight(i, false));
          layers.push(lyr);
          const dot = L.circleMarker(featureCenter(feature), {{
            radius: 7, color: "#5C4300", weight: 2, fillColor: "#FFD000", fillOpacity: 0.95
          }});
          dot.bindPopup(popupHtml(feature.properties));
          dot.on("click", () => highlight(i, false));
          dots.push(dot);
        }}
      }}).addTo(map);
      dots.forEach((d) => d.addTo(dotsLayer));
    }}
    function syncDots() {{
      if (!map) return;
      const showDots = map.getZoom() < 11;
      if (showDots && !map.hasLayer(dotsLayer)) dotsLayer.addTo(map);
      if (!showDots && map.hasLayer(dotsLayer)) map.removeLayer(dotsLayer);
    }}
    function restyleAll() {{
      layers.forEach((lyr, i) => lyr.setStyle(parcelStyle(i === active)));
      syncDots();
    }}
    function createMap(name, view) {{
      if (map) {{
        map.remove();
        map = null;
      }}
      map = L.map("map", {{
        crs: name === "yandex" ? CRS3395 : L.CRS.EPSG3857,
        renderer: L.canvas({{ padding: 0.5 }}),
        zoomControl: false
      }});
      L.control.zoom({{ position: "topright" }}).addTo(map);
      currentBase = makeTiles(name);
      currentBase.forEach((lyr) => lyr.addTo(map));
      attachParcels();
      map.on("zoomend", restyleAll);
      if (view) map.setView(view.center, view.zoom);
      else map.fitBounds(geo.getBounds(), {{ padding: [24, 24] }});
      currentBaseName = name;
      document.querySelectorAll(".basemaps button").forEach((b) => b.classList.toggle("on", b.dataset.base === name));
      syncDots();
      setTimeout(() => map.invalidateSize(), 50);
    }}
    function setBase(name) {{
      const rebuild = !map || (name === "yandex") !== (currentBaseName === "yandex");
      if (rebuild) {{
        const view = map ? {{ center: map.getCenter(), zoom: map.getZoom() }} : null;
        createMap(name, view);
        if (active >= 0) highlight(active, false);
        return;
      }}
      currentBase.forEach((lyr) => map.removeLayer(lyr));
      currentBase = makeTiles(name);
      currentBase.forEach((lyr) => lyr.addTo(map));
      currentBaseName = name;
      document.querySelectorAll(".basemaps button").forEach((b) => b.classList.toggle("on", b.dataset.base === name));
      geo.bringToFront();
    }}
    const baseBox = document.getElementById("basemaps");
    [
      ["yandex", "Яндекс"],
      ["sat", "Спутник"],
      ["twogis", "2ГИС"],
      ["google", "Google"],
      ["relief", "Рельеф"]
    ].forEach(([id, label]) => {{
      const b = document.createElement("button");
      b.type = "button";
      b.dataset.base = id;
      b.textContent = label;
      b.addEventListener("click", () => setBase(id));
      baseBox.appendChild(b);
    }});
    createMap("yandex");

    const list = document.getElementById("list");
    list.innerHTML = DATA.features.map((f, i) => itemHtml(f.properties, i)).join("");
    const rows = [...list.querySelectorAll(".item")];

    const q = document.getElementById("q");
    function highlight(i, fly) {{
      if (active >= 0 && layers[active]) layers[active].setStyle(parcelStyle(false));
      active = i;
      rows.forEach((r) => r.classList.remove("active"));
      if (i >= 0 && layers[i]) {{
        layers[i].setStyle(parcelStyle(true));
        layers[i].bringToFront();
        rows[i].classList.add("active");
        fillDetail(DATA.features[i].properties);
        rows[i].scrollIntoView({{ behavior: "smooth", block: "nearest" }});
        if (fly) {{
          map.fitBounds(layers[i].getBounds(), {{ padding: [40, 40], maxZoom: 15 }});
          layers[i].openPopup();
        }}
      }}
    }}
    function applyFilter() {{
      const s = q.value.trim().toLowerCase();
      const visible = [];
      DATA.features.forEach((f, i) => {{
        const p = f.properties;
        const ok = !s || p.address.toLowerCase().includes(s) || p.cad.toLowerCase().includes(s);
        rows[i].style.display = ok ? "" : "none";
        if (ok) {{
          if (!geo.hasLayer(layers[i])) geo.addLayer(layers[i]);
          if (!dotsLayer.hasLayer(dots[i])) dotsLayer.addLayer(dots[i]);
          visible.push(layers[i]);
        }} else {{
          if (geo.hasLayer(layers[i])) geo.removeLayer(layers[i]);
          if (dotsLayer.hasLayer(dots[i])) dotsLayer.removeLayer(dots[i]);
        }}
      }});
      if (visible.length) {{
        map.fitBounds(L.featureGroup(visible).getBounds(), {{ padding: [24, 24], maxZoom: 12 }});
      }}
    }}
    q.addEventListener("input", applyFilter);
    rows.forEach((el, i) => el.addEventListener("click", () => highlight(i, true)));
    const resize = () => {{ if (map) {{ map.invalidateSize(); restyleAll(); }} }};
    window.addEventListener("resize", resize);
    setTimeout(resize, 200);
  </script>
</body>
</html>
"""
    SRC.write_text(html, encoding="utf-8")
    print("rewrote", SRC, "bytes", SRC.stat().st_size)


if __name__ == "__main__":
    main()
