#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Пересобирает mo_sx_1ha.html: мобильная вёрстка, карточки вместо широкой таблицы."""

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
    ckad = extract("CKAD", text)
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
    .legend {{
      position: absolute; left: 10px; bottom: 10px; z-index: 500;
      display: flex; gap: 8px; flex-wrap: wrap;
      background: rgba(255,255,255,.92); padding: 6px 8px; border-radius: 8px;
      font-size: 11px; color: #333; box-shadow: 0 1px 4px rgba(0,0,0,.12);
    }}
    .legend-item {{ display: flex; align-items: center; gap: 6px; }}
    .swatch {{ width: 16px; height: 10px; background: rgba(255,208,0,.75); border: 2px solid #c49200; }}
    .swatch-ckad {{ width: 18px; height: 0; border-top: 4px solid #ff4d00; }}
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
    .stats {{ color: var(--muted); font-size: 13px; margin-bottom: 8px; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0; }}
    .chip {{
      background: #efe8d8; border-radius: 999px; padding: 5px 8px;
      font-size: 12px; color: #2a2618;
    }}
    .rows {{ display: grid; gap: 8px; }}
    .row .k {{ display: block; color: var(--muted); font-size: 11px; margin-bottom: 2px; }}
    .row .v {{ font-size: 13px; }}
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
    .popup {{ max-width: 240px; }}
    .popup .cad {{ font-weight: 700; }}
    .leaflet-control-attribution {{ font-size: 10px; }}
    @media (min-width: 900px) {{
      header {{ padding: 12px 18px; }}
      h1 {{ font-size: 20px; }}
      .layout {{ flex-direction: row; }}
      .map-col {{ flex: 1; min-width: 0; display: flex; flex-direction: column; }}
      #map {{ flex: 1; height: auto; min-height: 0; }}
      .side {{
        width: min(420px, 40vw); border-left: 1px solid var(--line);
        padding: 12px 14px 18px;
      }}
    }}
  </style>
</head>
<body>
  <div class="app">
    <header>
      <h1>Земли СХ от 1 га — Московская область</h1>
      <p class="meta">215 участков · 3 114,87 га · газ, свет, дороги, вода, почва, ИЖС (ориентир, не ТУ)</p>
      <input id="q" type="search" placeholder="Поиск по адресу или кадастровому номеру" enterkeyhint="search">
    </header>
    <div class="layout">
      <div class="map-col">
        <div id="map"></div>
        <div class="legend">
          <span class="legend-item"><span class="swatch"></span> Земли СХ</span>
          <span class="legend-item"><span class="swatch-ckad"></span> ЦКАД</span>
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
    const CKAD = {ckad};

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
    function fmtRub(v) {{
      if (v == null) return "нет данных";
      return v.toLocaleString("ru-RU", {{ maximumFractionDigits: 0 }}) + " ₽";
    }}
    function esc(s) {{
      return String(s ?? "").replace(/[&<>"]/g, (ch) => ({{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }}[ch]));
    }}
    function popupHtml(p) {{
      return `<div class="popup"><div class="cad">${{esc(p.cad)}}</div>` +
        `<div>${{esc(p.address)}}</div>` +
        `<div>${{fmtHa(p.ha)}} · газ ${{esc(p.gas_km)}} · свет ${{esc(p.elec_km)}}</div></div>`;
    }}
    function fillDetail(p) {{
      const box = document.getElementById("detail");
      if (!box || !p) return;
      box.classList.remove("empty");
      box.innerHTML =
        `<h2>${{esc(p.cad)}}</h2>` +
        `<p class="addr">${{esc(p.address)}}</p>` +
        `<div class="stats">${{fmtHa(p.ha)}} · ${{fmtRub(p.cost)}} · КП ${{esc(p.kp_score)}} · ${{esc(p.kp_reco)}}</div>` +
        `<div class="chips">` +
          `<span class="chip">Газ ${{esc(p.gas_km)}}</span>` +
          `<span class="chip">Свет ${{esc(p.elec_km)}}</span>` +
          `<span class="chip">${{esc(p.fed_name)}} ${{esc(p.fed_km)}}</span>` +
        `</div>` +
        `<div class="rows">` +
          `<div class="row"><span class="k">Газ</span><div class="v">${{esc(p.gas_ok)}}. ${{esc(p.gas_name)}}. ${{esc(p.gas_volume)}}</div></div>` +
          `<div class="row"><span class="k">Электричество</span><div class="v">${{esc(p.elec_ok)}}. ${{esc(p.elec_name)}}. ${{esc(p.elec_volume)}}</div></div>` +
          `<div class="row"><span class="k">Дорога</span><div class="v">${{esc(p.road_name)}}, ${{esc(p.road_km)}}</div></div>` +
          `<div class="row"><span class="k">Федеральная трасса</span><div class="v">${{esc(p.fed_name)}}, ${{esc(p.fed_km)}}</div></div>` +
          `<div class="row"><span class="k">Водоём</span><div class="v">на участке ${{esc(p.water_on)}}; ${{esc(p.water_type)}}, ${{esc(p.water_km)}}, ${{esc(p.water_size)}}</div></div>` +
          `<div class="row"><span class="k">Водоснабжение</span><div class="v">${{esc(p.water_supply)}}</div></div>` +
          `<div class="row"><span class="k">Почва</span><div class="v">${{esc(p.soil)}}</div></div>` +
          `<div class="row"><span class="k">Перевод в ИЖС</span><div class="v">${{esc(p.izhs)}}</div></div>` +
          `<div class="row"><span class="k">Программа КП</span><div class="v">${{esc(p.program)}}</div></div>` +
        `</div>`;
      box.scrollIntoView({{ behavior: "smooth", block: "nearest" }});
    }}
    function itemHtml(p, i) {{
      return `<button type="button" class="item" data-i="${{i}}">` +
        `<div class="cad">${{esc(p.cad)}}</div>` +
        `<div class="addr">${{esc(p.address)}}</div>` +
        `<div class="chips">` +
          `<span class="chip">${{fmtHa(p.ha)}}</span>` +
          `<span class="chip">газ ${{esc(p.gas_km)}}</span>` +
          `<span class="chip">свет ${{esc(p.elec_km)}}</span>` +
          `<span class="chip">КП ${{esc(p.kp_score)}}</span>` +
        `</div></button>`;
    }}

    const map = L.map("map", {{ renderer: L.canvas({{ padding: 0.5 }}), zoomControl: false }}).setView([55.6, 37.4], 8);
    L.control.zoom({{ position: "topright" }}).addTo(map);
    L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}", {{
      maxZoom: 19, attribution: "Tiles © Esri"
    }}).addTo(map);
    L.tileLayer("https://{{s}}.basemaps.cartocdn.com/dark_only_labels/{{z}}/{{x}}/{{y}}{{r}}.png", {{
      maxZoom: 19, attribution: "© CARTO"
    }}).addTo(map);

    const ckadSvg = L.svg({{ padding: 0.5 }});
    const ckadCasing = L.geoJSON(CKAD, {{
      renderer: ckadSvg,
      style: {{ color: "#7A1F00", weight: 8, opacity: 0.95, lineJoin: "round", lineCap: "round" }}
    }}).addTo(map);
    const ckadLine = L.geoJSON(CKAD, {{
      renderer: ckadSvg,
      style: {{ color: "#FF4D00", weight: 4, opacity: 1, lineJoin: "round", lineCap: "round" }}
    }}).addTo(map);
    ckadLine.bindPopup("ЦКАД · A-113");

    const layers = [];
    const dots = [];
    const dotsLayer = L.layerGroup();
    const geo = L.geoJSON(DATA, {{
      style: () => parcelStyle(false),
      onEachFeature: (feature, lyr) => {{
        const i = layers.length;
        lyr.bindPopup(popupHtml(feature.properties));
        lyr.on("click", () => highlight(i, false));
        layers.push(lyr);
        const c = lyr.getBounds().getCenter();
        const dot = L.circleMarker(c, {{
          radius: 7, color: "#5C4300", weight: 2, fillColor: "#FFD000", fillOpacity: 0.95
        }});
        dot.bindPopup(popupHtml(feature.properties));
        dot.on("click", () => highlight(i, false));
        dots.push(dot);
      }}
    }}).addTo(map);

    const list = document.getElementById("list");
    list.innerHTML = DATA.features.map((f, i) => itemHtml(f.properties, i)).join("");
    const rows = [...list.querySelectorAll(".item")];

    function syncDots() {{
      const showDots = map.getZoom() < 11;
      if (showDots && !map.hasLayer(dotsLayer)) dotsLayer.addTo(map);
      if (!showDots && map.hasLayer(dotsLayer)) map.removeLayer(dotsLayer);
    }}
    function restyleAll() {{
      layers.forEach((lyr, i) => lyr.setStyle(parcelStyle(i === active)));
      syncDots();
    }}
    let active = -1;
    map.on("zoomend", restyleAll);
    map.fitBounds(geo.getBounds().extend(ckadLine.getBounds()), {{ padding: [24, 24] }});
    ckadCasing.bringToFront();
    ckadLine.bringToFront();

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
    dots.forEach((d) => d.addTo(dotsLayer));
    syncDots();
    const resize = () => {{ map.invalidateSize(); restyleAll(); }};
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
