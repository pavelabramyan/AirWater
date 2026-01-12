#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Автозаполнение порций текстов через GPT 5.2 (OpenAI API)

- Очередь порций хранится в SQLite: data/texts.db, таблица fill_queue
- Скрипт берёт следующую порцию, просит модель вернуть СТРОГО JSON, пишет в БД

ENV:
- OPENAI_API_KEY (обязательно)
- OPENAI_MODEL (по умолчанию: gpt-5.2)
- OPENAI_API_URL (по умолчанию: https://api.openai.com/v1/chat/completions)

Запуск:
- 1 порция:   python3 scripts/fill_texts_queue.py --once
- цикл:       python3 scripts/fill_texts_queue.py --loop
- dry-run:    python3 scripts/fill_texts_queue.py --once --dry-run
"""

import argparse
import json
import os
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

DB_PATH = Path(__file__).resolve().parents[1] / 'data' / 'texts.db'
DEFAULT_MODEL = os.getenv('OPENAI_MODEL', 'gpt-5.2')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '').strip()
OPENAI_API_URL = os.getenv('OPENAI_API_URL', 'https://api.openai.com/v1/chat/completions').strip()

PLANETS = ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']
SIGNS_RU = ['Овен','Телец','Близнецы','Рак','Лев','Дева','Весы','Скорпион','Стрелец','Козерог','Водолей','Рыбы']
ASPECTS = ['Conjunction','Opposition','Trine','Square','Sextile','Quincunx']
HOUSES = list(range(1, 13))

ASPECTS_RU = {
    'Conjunction': 'Соединение',
    'Opposition': 'Оппозиция',
    'Trine': 'Тригон',
    'Square': 'Квадрат',
    'Sextile': 'Секстиль',
    'Quincunx': 'Квинконс',
}

BASE_SYSTEM = (
    "Ты — профессиональный астролог-практик с 20-летним опытом. "
    "Пиши уникальные, конкретные, практичные интерпретации без воды. "
    "Не повторяйся."
)

BASE_RULES = (
    "Требования к каждому тексту:
"
    "- 150–250 слов
"
    "- Начни с ключевой мысли
"
    "- Дай 2–3 конкретных проявления
"
    "- Заверши практическим советом/ориентиром
"
    "- Контекст важен: натал (характер), транзит (сейчас), соляр (в этом году), лунар (в этом месяце), синастрия (между вами)
"
    "- Верни СТРОГО JSON без markdown и без комментариев
"
)


@dataclass
class Portion:
    code: str
    title: str
    table: str
    text_col: str
    key_cols: Tuple[str, ...]
    context: str
    selector: Dict[str, Any]


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def ensure_queue_schema(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fill_queue (
            id INTEGER PRIMARY KEY,
            code TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            table_name TEXT NOT NULL,
            text_col TEXT NOT NULL,
            key_cols TEXT NOT NULL,
            context TEXT NOT NULL,
            selector_json TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at INTEGER NOT NULL,
            started_at INTEGER,
            finished_at INTEGER,
            last_error TEXT,
            last_response_json TEXT
        )
    """)
    conn.commit()


def portion_definitions() -> List[Portion]:
    portions: List[Portion] = []

    # A1-A3
    portions.append(Portion(
        'A1', 'Синастрия: уровни совместимости (6)',
        'synastry_levels', 'description', ('level',), 'synastry_levels',
        {'levels': ['ideal','excellent','good','average','difficult','very_difficult']}
    ))
    portions.append(Portion(
        'A2', 'Синастрия: рекомендации (15)',
        'synastry_recommendations', 'recommendation', ('category','condition'), 'synastry_recommendations', {}
    ))
    portions.append(Portion(
        'A3', 'Синастрия: сферы (25)',
        'synastry_spheres', 'text', ('sphere','level'), 'synastry_spheres', {}
    ))

    # Натал аспекты: B1..B15
    def add_pair_block(code: str, pairs: List[Tuple[str, str]]):
        portions.append(Portion(
            code,
            'Натал: аспекты ' + ', '.join([f'{a}-{b}' for a, b in pairs]) + f' ({len(pairs) * len(ASPECTS)})',
            'natal_aspects', 'text', ('planet1','planet2','aspect'), 'natal_aspects',
            {'pairs': pairs, 'aspects': ASPECTS}
        ))

    add_pair_block('B1', [('Sun','Moon'), ('Sun','Mercury')])
    add_pair_block('B2', [('Sun','Venus'), ('Sun','Mars')])
    add_pair_block('B3', [('Sun','Jupiter'), ('Sun','Saturn')])
    add_pair_block('B4', [('Sun','Uranus'), ('Sun','Neptune'), ('Sun','Pluto')])
    add_pair_block('B5', [('Moon','Mercury'), ('Moon','Venus')])
    add_pair_block('B6', [('Moon','Mars'), ('Moon','Jupiter')])
    add_pair_block('B7', [('Moon','Saturn'), ('Moon','Uranus')])
    add_pair_block('B8', [('Moon','Neptune'), ('Moon','Pluto')])
    add_pair_block('B9', [('Mercury','Venus'), ('Mercury','Mars'), ('Mercury','Jupiter')])
    add_pair_block('B10', [('Mercury','Saturn'), ('Mercury','Uranus'), ('Mercury','Neptune'), ('Mercury','Pluto')])
    add_pair_block('B11a', [('Venus','Mars'), ('Venus','Jupiter'), ('Venus','Saturn')])
    add_pair_block('B11b', [('Venus','Uranus'), ('Venus','Neptune'), ('Venus','Pluto')])
    add_pair_block('B12', [('Mars','Jupiter'), ('Mars','Saturn'), ('Mars','Uranus'), ('Mars','Neptune'), ('Mars','Pluto')])
    add_pair_block('B13', [('Jupiter','Saturn'), ('Jupiter','Uranus'), ('Jupiter','Neptune'), ('Jupiter','Pluto')])
    add_pair_block('B14', [('Saturn','Uranus'), ('Saturn','Neptune'), ('Saturn','Pluto'), ('Uranus','Neptune')])
    add_pair_block('B15', [('Uranus','Pluto'), ('Neptune','Pluto')])

    # Транзит: планеты в домах (C1..C5)
    for code, pls in [
        ('C1',['Sun','Moon']),
        ('C2',['Mercury','Venus']),
        ('C3',['Mars','Jupiter']),
        ('C4',['Saturn','Uranus']),
        ('C5',['Neptune','Pluto']),
    ]:
        portions.append(Portion(
            code,
            f'Транзиты: планеты в домах {", ".join(pls)} (24)',
            'transit_planets_houses', 'text', ('planet','house'), 'transit_planets_houses',
            {'planets': pls, 'houses': HOUSES}
        ))

    # Чанки натальных планет для аспектов (4+4+2)
    chunks = [
        ['Sun','Moon','Mercury','Venus'],
        ['Mars','Jupiter','Saturn','Uranus'],
        ['Neptune','Pluto'],
    ]

    # Транзиты: аспекты к наталу (D1..D30)
    d = 1
    for tp in PLANETS:
        for chunk in chunks:
            portions.append(Portion(
                f'D{d}',
                f'Транзиты: {tp} к наталу ({len(chunk) * 6})',
                'transit_aspects', 'text', ('transit_planet','natal_planet','aspect'), 'transit_aspects',
                {'transit_planet': tp, 'natal_planets': chunk, 'aspects': ASPECTS}
            ))
            d += 1

    # Соляр/Лунар: планеты в знаках/домах
    def add_sign(prefix: str, table: str, title: str):
        for idx, pls in [(1,['Sun','Moon']),(2,['Mercury','Venus']),(3,['Mars','Jupiter']),(4,['Saturn','Uranus']),(5,['Neptune','Pluto'])]:
            portions.append(Portion(
                f'{prefix}{idx}',
                f'{title}: планеты в знаках {", ".join(pls)} (24)',
                table, 'text', ('planet','sign'), table,
                {'planets': pls, 'signs': SIGNS_RU}
            ))

    def add_house(prefix: str, table: str, title: str):
        for idx, pls in [(1,['Sun','Moon']),(2,['Mercury','Venus']),(3,['Mars','Jupiter']),(4,['Saturn','Uranus']),(5,['Neptune','Pluto'])]:
            portions.append(Portion(
                f'{prefix}{idx}',
                f'{title}: планеты в домах {", ".join(pls)} (24)',
                table, 'text', ('planet','house'), table,
                {'planets': pls, 'houses': HOUSES}
            ))

    add_sign('E', 'solar_planets_signs', 'Соляр')
    add_house('F', 'solar_planets_houses', 'Соляр')
    add_sign('H', 'lunar_planets_signs', 'Лунар')
    add_house('I', 'lunar_planets_houses', 'Лунар')

    # Соляр/Лунар: аспекты к наталу (G/J) — 30 порций
    def add_cross(prefix: str, table: str, outer_col: str, title: str):
        n = 1
        for op in PLANETS:
            for chunk in chunks:
                sel = {outer_col: op, 'natal_planets': chunk, 'aspects': ASPECTS}
                portions.append(Portion(
                    f'{prefix}{n}',
                    f'{title}: {op} к наталу ({len(chunk) * 6})',
                    table, 'text', (outer_col,'natal_planet','aspect'), table,
                    sel
                ))
                n += 1

    add_cross('G', 'solar_aspects', 'solar_planet', 'Соляр')
    add_cross('J', 'lunar_aspects', 'lunar_planet', 'Лунар')

    # Синастрия: аспекты (K1..K30)
    k = 1
    for p1 in PLANETS:
        for chunk in chunks:
            portions.append(Portion(
                f'K{k}',
                f'Синастрия: {p1} к планетам партнёра ({len(chunk) * 6})',
                'synastry_aspects', 'text', ('planet1','planet2','aspect'), 'synastry_aspects',
                {'planet1': p1, 'planet2_list': chunk, 'aspects': ASPECTS}
            ))
            k += 1

    # Синастрия: планеты в домах партнёра (L1..L5)
    for code, pls in [
        ('L1',['Sun','Moon']),
        ('L2',['Mercury','Venus']),
        ('L3',['Mars','Jupiter']),
        ('L4',['Saturn','Uranus']),
        ('L5',['Neptune','Pluto']),
    ]:
        portions.append(Portion(
            code,
            f'Синастрия: планеты в домах партнёра {", ".join(pls)} (24)',
            'synastry_planets_houses', 'text', ('planet','house'), 'synastry_planets_houses',
            {'planets': pls, 'houses': HOUSES}
        ))

    return portions


def seed_queue(conn: sqlite3.Connection) -> None:
    ensure_queue_schema(conn)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM fill_queue')
    if cur.fetchone()[0] > 0:
        return

    now = int(time.time())
    for p in portion_definitions():
        cur.execute(
            """
            INSERT OR IGNORE INTO fill_queue
            (code, title, table_name, text_col, key_cols, context, selector_json, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
            """,
            (
                p.code,
                p.title,
                p.table,
                p.text_col,
                json.dumps(list(p.key_cols), ensure_ascii=False),
                p.context,
                json.dumps(p.selector, ensure_ascii=False),
                now,
            )
        )
    conn.commit()


def fetch_next_portion(conn: sqlite3.Connection) -> Optional[sqlite3.Row]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM fill_queue WHERE status='pending' ORDER BY id ASC LIMIT 1")
    return cur.fetchone()


def mark_started(conn: sqlite3.Connection, qid: int) -> None:
    cur = conn.cursor()
    cur.execute("UPDATE fill_queue SET status='running', started_at=?, last_error=NULL WHERE id=?", (int(time.time()), qid))
    conn.commit()


def mark_done(conn: sqlite3.Connection, qid: int, response_text: str) -> None:
    cur = conn.cursor()
    cur.execute(
        "UPDATE fill_queue SET status='done', finished_at=?, last_response_json=? WHERE id=?",
        (int(time.time()), response_text[:200000], qid)
    )
    conn.commit()


def mark_error(conn: sqlite3.Connection, qid: int, err: str) -> None:
    cur = conn.cursor()
    cur.execute("UPDATE fill_queue SET status='pending', last_error=? WHERE id=?", (err[:2000], qid))
    conn.commit()


def select_items(conn: sqlite3.Connection, table: str, text_col: str, key_cols: List[str], selector: Dict[str, Any]) -> List[Dict[str, Any]]:
    cur = conn.cursor()
    where = f"({text_col} IS NULL OR length({text_col}) <= 10)"
    params: List[Any] = []

    if table == 'natal_aspects':
        pairs = selector['pairs']
        aspects = selector['aspects']
        pair_where = []
        for p1, p2 in pairs:
            pair_where.append('(planet1=? AND planet2=?)')
            params.extend([p1, p2])
        where += ' AND (' + ' OR '.join(pair_where) + ')'
        where += ' AND aspect IN (' + ','.join(['?'] * len(aspects)) + ')'
        params.extend(aspects)

    elif table == 'transit_aspects':
        where += ' AND transit_planet=?'
        params.append(selector['transit_planet'])
        nps = selector['natal_planets']
        where += ' AND natal_planet IN (' + ','.join(['?'] * len(nps)) + ')'
        params.extend(nps)
        aspects = selector['aspects']
        where += ' AND aspect IN (' + ','.join(['?'] * len(aspects)) + ')'
        params.extend(aspects)

    elif table == 'solar_aspects':
        where += ' AND solar_planet=?'
        params.append(selector['solar_planet'])
        nps = selector['natal_planets']
        where += ' AND natal_planet IN (' + ','.join(['?'] * len(nps)) + ')'
        params.extend(nps)
        aspects = selector['aspects']
        where += ' AND aspect IN (' + ','.join(['?'] * len(aspects)) + ')'
        params.extend(aspects)

    elif table == 'lunar_aspects':
        where += ' AND lunar_planet=?'
        params.append(selector['lunar_planet'])
        nps = selector['natal_planets']
        where += ' AND natal_planet IN (' + ','.join(['?'] * len(nps)) + ')'
        params.extend(nps)
        aspects = selector['aspects']
        where += ' AND aspect IN (' + ','.join(['?'] * len(aspects)) + ')'
        params.extend(aspects)

    elif table == 'synastry_aspects':
        where += ' AND planet1=?'
        params.append(selector['planet1'])
        p2s = selector['planet2_list']
        where += ' AND planet2 IN (' + ','.join(['?'] * len(p2s)) + ')'
        params.extend(p2s)
        aspects = selector['aspects']
        where += ' AND aspect IN (' + ','.join(['?'] * len(aspects)) + ')'
        params.extend(aspects)

    elif table in ('transit_planets_houses','solar_planets_houses','lunar_planets_houses','synastry_planets_houses'):
        planets = selector['planets']
        houses = selector['houses']
        where += ' AND planet IN (' + ','.join(['?'] * len(planets)) + ')'
        params.extend(planets)
        where += ' AND house IN (' + ','.join(['?'] * len(houses)) + ')'
        params.extend(houses)

    elif table in ('solar_planets_signs','lunar_planets_signs'):
        planets = selector['planets']
        signs = selector['signs']
        where += ' AND planet IN (' + ','.join(['?'] * len(planets)) + ')'
        params.extend(planets)
        where += ' AND sign IN (' + ','.join(['?'] * len(signs)) + ')'
        params.extend(signs)

    elif table == 'synastry_levels':
        levels = selector['levels']
        where += ' AND level IN (' + ','.join(['?'] * len(levels)) + ')'
        params.extend(levels)

    sql = f"SELECT {', '.join(key_cols)} FROM {table} WHERE {where} ORDER BY id ASC"
    cur.execute(sql, params)
    return [dict(r) for r in cur.fetchall()]


def build_prompt(portion: sqlite3.Row, items: List[Dict[str, Any]]) -> Tuple[str, str]:
    ctx_key = portion['context']

    if ctx_key == 'natal_aspects':
        ctx = 'Контекст: НАТАЛ (черты личности и устойчивые паттерны).'
    elif ctx_key == 'transit_aspects':
        ctx = 'Контекст: ТРАНЗИТЫ (сейчас/в ближайшие недели).'
    elif ctx_key == 'solar_aspects':
        ctx = 'Контекст: СОЛЯР (в этом году).'
    elif ctx_key == 'lunar_aspects':
        ctx = 'Контекст: ЛУНАР (в этом месяце).'
    elif ctx_key == 'synastry_aspects':
        ctx = 'Контекст: СИНАСТРИЯ (между вами/в отношениях).'
    elif ctx_key == 'solar_planets_signs':
        ctx = 'Контекст: СОЛЯР (в этом году — планета в знаке).'
    elif ctx_key == 'lunar_planets_signs':
        ctx = 'Контекст: ЛУНАР (в этом месяце — планета в знаке).'
    elif ctx_key == 'transit_planets_houses':
        ctx = 'Контекст: ТРАНЗИТЫ (планета проходит по натальному дому сейчас).'
    elif ctx_key == 'synastry_levels':
        ctx = 'Контекст: СИНАСТРИЯ (общий уровень пары).'
    elif ctx_key == 'synastry_spheres':
        ctx = 'Контекст: СИНАСТРИЯ (сферы отношений).'
    elif ctx_key == 'synastry_recommendations':
        ctx = 'Контекст: СИНАСТРИЯ (рекомендации/советы).'
    else:
        ctx = f'Контекст: {ctx_key}.'

    system = BASE_SYSTEM + "
" + BASE_RULES
    user = (
        f"ЗАДАНИЕ {portion['code']}: {portion['title']}
"
        f"{ctx}

"
        f"Справочник аспектов: {json.dumps(ASPECTS_RU, ensure_ascii=False)}
"
        f"Планеты: {', '.join(PLANETS)}
"
        f"Знаки (RU): {', '.join(SIGNS_RU)}

"
        f"Сгенерируй {len(items)} текстов.
"
        f"Верни СТРОГО JSON массив объектов. Каждый объект должен содержать ВСЕ ключи из входного списка + поле 'text'.

"
        f"Входной список объектов (нужно заполнить поле text):
{json.dumps(items, ensure_ascii=False)}
"
    )
    return system, user


def call_openai(system: str, user: str, model: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY не задан')
    headers = {'Authorization': f'Bearer {OPENAI_API_KEY}', 'Content-Type': 'application/json'}
    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': user},
        ],
        'temperature': 0.7,
    }
    r = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=300)
    r.raise_for_status()
    data = r.json()
    return data['choices'][0]['message']['content']


def extract_json_array(text: str) -> List[Dict[str, Any]]:
    s = (text or '').strip()
    start = s.find('[')
    end = s.rfind(']')
    if start == -1 or end == -1 or end <= start:
        raise ValueError('Не найден JSON массив в ответе')
    raw = s[start:end + 1]
    arr = json.loads(raw)
    if not isinstance(arr, list):
        raise ValueError('JSON не массив')
    return arr


def apply_updates(conn: sqlite3.Connection, table: str, text_col: str, key_cols: List[str], rows: List[Dict[str, Any]]) -> int:
    cur = conn.cursor()
    updated = 0
    for obj in rows:
        text = (obj.get('text') or '').strip()
        if len(text) <= 10:
            continue
        where = ' AND '.join([f"{c}=?" for c in key_cols])
        sql = f"UPDATE {table} SET {text_col}=? WHERE {where}"
        params = [text] + [obj.get(c) for c in key_cols]
        cur.execute(sql, params)
        updated += cur.rowcount
    conn.commit()
    return updated


def run_once(dry_run: bool = False) -> int:
    conn = db()
    try:
        ensure_queue_schema(conn)
        seed_queue(conn)
        portion = fetch_next_portion(conn)
        if not portion:
            print('Очередь пустая: все порции выполнены')
            return 0

        qid = int(portion['id'])
        mark_started(conn, qid)

        key_cols = json.loads(portion['key_cols'])
        selector = json.loads(portion['selector_json'])
        items = select_items(conn, portion['table_name'], portion['text_col'], key_cols, selector)

        if not items:
            mark_done(conn, qid, json.dumps({'skipped': True, 'reason': 'no empty items'}, ensure_ascii=False))
            print(f"{portion['code']}: нечего заполнять — DONE")
            return 1

        system, user = build_prompt(portion, items)
        print(f"
=== NEXT: {portion['code']} | {portion['title']} ===")
        print(f"Table: {portion['table_name']} | Items: {len(items)}")

        if dry_run:
            print('
--- USER (начало) ---
' + user[:2000])
            mark_done(conn, qid, json.dumps({'dry_run': True}, ensure_ascii=False))
            print(f"{portion['code']}: DRY-RUN DONE")
            return 1

        raw = call_openai(system, user, DEFAULT_MODEL)
        arr = extract_json_array(raw)

        for obj in arr:
            for c in key_cols:
                if c not in obj:
                    raise ValueError(f"В ответе нет ключа {c}")

        updated = apply_updates(conn, portion['table_name'], portion['text_col'], key_cols, arr)
        mark_done(conn, qid, raw)
        print(f"{portion['code']}: DONE, updated={updated}")
        return 1

    except Exception as e:
        try:
            if 'portion' in locals() and locals().get('portion') is not None:
                mark_error(conn, int(locals()['portion']['id']), str(e))
        except Exception:
            pass
        print(f"ERROR: {e}")
        return 2
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--loop', action='store_true')
    parser.add_argument('--sleep', type=int, default=3)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if not args.once and not args.loop:
        args.once = True

    if args.once:
        raise SystemExit(run_once(dry_run=args.dry_run))

    while True:
        rc = run_once(dry_run=args.dry_run)
        if rc == 0:
            break
        time.sleep(max(1, args.sleep))


# --- недостающие функции очереди ---

def mark_error(conn: sqlite3.Connection, qid: int, err: str) -> None:
    cur = conn.cursor()
    cur.execute("UPDATE fill_queue SET status='pending', last_error=? WHERE id=?", (err[:2000], qid))
    conn.commit()


def mark_done(conn: sqlite3.Connection, qid: int, response_text: str) -> None:
    cur = conn.cursor()
    cur.execute(
        "UPDATE fill_queue SET status='done', finished_at=?, last_response_json=? WHERE id=?",
        (int(time.time()), response_text[:200000], qid)
    )
    conn.commit()


def fetch_next_portion(conn: sqlite3.Connection) -> Optional[sqlite3.Row]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM fill_queue WHERE status='pending' ORDER BY id ASC LIMIT 1")
    return cur.fetchone()


def mark_started(conn: sqlite3.Connection, qid: int) -> None:
    cur = conn.cursor()
    cur.execute("UPDATE fill_queue SET status='running', started_at=?, last_error=NULL WHERE id=?", (int(time.time()), qid))
    conn.commit()


if __name__ == '__main__':
    main()
