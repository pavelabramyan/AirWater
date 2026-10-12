#!/usr/bin/env python3
"""Спутниковые виды участка 71:16:040403:1018 с контуром кадастра."""
from __future__ import annotations

import math
import ssl
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "фото"
OUT.mkdir(parents=True, exist_ok=True)

POLY = [
    (53.85282559, 36.82597201),
    (53.85238180, 36.82608991),
    (53.85242359, 36.82654018),
    (53.85286738, 36.82642228),
]
CENT = (53.85262459, 36.82625610)
CAD = "71:16:040403:1018"

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def deg2num(lat: float, lon: float, zoom: int) -> tuple[float, float]:
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = (lon + 180.0) / 360.0 * n
    ytile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    return xtile, ytile


def tile_url(source: str, z: int, x: int, y: int) -> str:
    if source == "google":
        return f"https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
    if source == "esri":
        return f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    if source == "streets":
        return f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
    if source == "yandex":
        return f"https://sat01.maps.yandex.net/tiles?l=sat&v=3.1546.0&x={x}&y={y}&z={z}&scale=1&lang=ru_RU"
    if source == "osm":
        return f"https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png"
    raise ValueError(source)


def fetch_tile(source: str, z: int, x: int, y: int) -> Image.Image:
    cache = OUT / "_tiles" / source / str(z)
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / f"{x}_{y}.jpg"
    if not path.exists() or path.stat().st_size < 200:
        url = tile_url(source, z, x, y)
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
            path.write_bytes(r.read())
    return Image.open(path).convert("RGB")


def stitch(source: str, lat: float, lon: float, zoom: int, half: int = 2) -> tuple[Image.Image, float, float, int]:
    cx, cy = deg2num(lat, lon, zoom)
    x0 = int(cx) - half
    y0 = int(cy) - half
    size = 256
    canvas = Image.new("RGB", (size * (2 * half + 1), size * (2 * half + 1)))
    for iy in range(2 * half + 1):
        for ix in range(2 * half + 1):
            tile = fetch_tile(source, zoom, x0 + ix, y0 + iy)
            canvas.paste(tile, (ix * size, iy * size))
    return canvas, x0, y0, size


def latlon_to_px(lat: float, lon: float, zoom: int, x0: float, y0: float, size: int) -> tuple[int, int]:
    x, y = deg2num(lat, lon, zoom)
    return int((x - x0) * size), int((y - y0) * size)


def annotate(img: Image.Image, zoom: int, x0: float, y0: float, size: int, title: str) -> Image.Image:
    draw = ImageDraw.Draw(img, "RGBA")
    pts = [latlon_to_px(lat, lon, zoom, x0, y0, size) for lat, lon in POLY]
    draw.polygon(pts, fill=(255, 40, 40, 70))
    draw.line(pts + [pts[0]], fill=(255, 30, 30, 230), width=4)
    for p in pts:
        r = 5
        draw.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=(255, 255, 255, 240), outline=(200, 0, 0, 255))
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 28)
        small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
    except Exception:
        font = ImageFont.load_default()
        small = font
    bar_h = 86
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, img.width, bar_h), fill=(0, 0, 0, 170))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    d2 = ImageDraw.Draw(img)
    d2.text((16, 10), title, fill="white", font=font)
    d2.text((16, 48), f"{CAD}  ·  контур по НСПД  ·  снимок со спутника, не наземное фото", fill="white", font=small)
    return img.convert("RGB")


def crop_around(img: Image.Image, cx: int, cy: int, w: int, h: int) -> Image.Image:
    left = max(0, cx - w // 2)
    top = max(0, cy - h // 2)
    right = min(img.width, left + w)
    bottom = min(img.height, top + h)
    left = max(0, right - w)
    top = max(0, bottom - h)
    return img.crop((left, top, right, bottom))


def save(name: str, img: Image.Image) -> None:
    path = OUT / name
    img.save(path, quality=92)
    print("saved", path.name, img.size)


def make_view(source: str, lat: float, lon: float, zoom: int, half: int, title: str, name: str, crop: tuple[int, int] | None = None) -> None:
    canvas, x0, y0, size = stitch(source, lat, lon, zoom, half=half)
    canvas = annotate(canvas, zoom, x0, y0, size, title)
    if crop:
        px, py = latlon_to_px(lat, lon, zoom, x0, y0, size)
        canvas = crop_around(canvas, px, py, crop[0], crop[1])
    save(name, canvas)


def main() -> None:
    make_view("google", CENT[0], CENT[1], 20, 2, "Сверху, близко — спутник Google", "01-sverhu-blizko-google.jpg", (1100, 900))
    make_view("yandex", CENT[0], CENT[1], 18, 2, "Сверху, близко — спутник Яндекс", "02-sverhu-blizko-yandex.jpg", (1400, 1000))
    make_view("esri", CENT[0], CENT[1], 18, 2, "Сверху, близко — спутник ESRI", "03-sverhu-blizko-esri.jpg", (1400, 1000))
    dlat = 0.00045
    dlon = 0.00070
    make_view("google", CENT[0] + dlat, CENT[1], 18, 2, "Взгляд с севера", "04-vid-s-severa.jpg", (1400, 1000))
    make_view("google", CENT[0] - dlat, CENT[1], 18, 2, "Взгляд с юга", "05-vid-s-yuga.jpg", (1400, 1000))
    make_view("google", CENT[0], CENT[1] - dlon, 18, 2, "Взгляд с запада", "06-vid-s-zapada.jpg", (1400, 1000))
    make_view("google", CENT[0], CENT[1] + dlon, 18, 2, "Взгляд с востока", "07-vid-s-vostoka.jpg", (1400, 1000))
    make_view("google", CENT[0], CENT[1], 16, 2, "Село Рылево, участок отмечен", "08-selo-obzor.jpg", (1600, 1100))
    make_view("streets", CENT[0], CENT[1], 16, 2, "Схема дорог", "09-shema-dorog.jpg", (1600, 1100))
    make_view("google", CENT[0], CENT[1], 14, 2, "Окрестности: Рылево и район", "10-okrestnosti.jpg", (1600, 1100))
    print("done")


if __name__ == "__main__":
    main()
