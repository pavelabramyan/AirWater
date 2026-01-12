# 📝 РУКОВОДСТВО ПО ЗАПОЛНЕНИЮ ТЕКСТОВ

## Общая статистика
- **Всего текстов:** 3724
- **Заполнено:** 276 (7.4%)
- **Нужно заполнить:** 3448

## Оптимальный размер порции: 20-30 текстов

---

# 📋 НУМЕРОВАННЫЙ СПИСОК ПОРЦИЙ

## БЛОК A: СИНАСТРИЯ — БЫСТРЫЕ (46 текстов)

### A1. Синастрия: Уровни совместимости (6 текстов)
```
Таблица: synastry_levels
Поле: description

Заполнить:
- ideal (90-100%) — "Идеальная пара"
- excellent (75-89%) — "Отличная совместимость"  
- good (60-74%) — "Хорошая совместимость"
- average (45-59%) — "Средняя совместимость"
- difficult (30-44%) — "Сложные отношения"
- very_difficult (0-29%) — "Очень сложные отношения"
```

### A2. Синастрия: Рекомендации (15 текстов)
```
Таблица: synastry_recommendations
Поле: recommendation

Сильные стороны (5):
- moon_venus_positive
- sun_sun_positive
- venus_mars_positive
- mercury_mercury_positive
- jupiter_positive

Слабые стороны (5):
- saturn_negative
- mars_negative
- moon_saturn_negative
- sun_saturn_negative
- uranus_negative

Советы (5):
- communication_issues
- trust_issues
- passion_issues
- stability_issues
- growth_together
```

### A3. Синастрия: Сферы совместимости (25 текстов)
```
Таблица: synastry_spheres
Поле: text

5 сфер × 5 уровней:

Сферы:
- romance (Романтика и страсть)
- communication (Общение и понимание)
- home (Быт и семья)
- finances (Финансы и ценности)
- goals (Общие цели)

Уровни для каждой сферы:
- excellent, good, average, difficult, very_difficult
```

---

## БЛОК B: НАТАЛ — АСПЕКТЫ (270 текстов, 12 порций по ~22)

```
Таблица: natal_aspects
Поле: text
Формат: planet1 + planet2 + aspect (6 типов аспектов)
```

### B1. Sun-Moon, Sun-Mercury (12 текстов)
```
Sun-Moon: Conjunction, Opposition, Trine, Square, Sextile, Quincunx
Sun-Mercury: Conjunction, Opposition, Trine, Square, Sextile, Quincunx
```

### B2. Sun-Venus, Sun-Mars (12 текстов)
```
Sun-Venus: 6 аспектов
Sun-Mars: 6 аспектов
```

### B3. Sun-Jupiter, Sun-Saturn (12 текстов)
```
Sun-Jupiter: 6 аспектов
Sun-Saturn: 6 аспектов
```

### B4. Sun-Uranus, Sun-Neptune, Sun-Pluto (18 текстов)
```
Sun-Uranus: 6 аспектов
Sun-Neptune: 6 аспектов
Sun-Pluto: 6 аспектов
```

### B5. Moon-Mercury, Moon-Venus (12 текстов)
```
Moon-Mercury: 6 аспектов
Moon-Venus: 6 аспектов
```

### B6. Moon-Mars, Moon-Jupiter (12 текстов)
```
Moon-Mars: 6 аспектов
Moon-Jupiter: 6 аспектов
```

### B7. Moon-Saturn, Moon-Uranus (12 текстов)
```
Moon-Saturn: 6 аспектов
Moon-Uranus: 6 аспектов
```

### B8. Moon-Neptune, Moon-Pluto (12 текстов)
```
Moon-Neptune: 6 аспектов
Moon-Pluto: 6 аспектов
```

### B9. Mercury-Venus, Mercury-Mars, Mercury-Jupiter (18 текстов)
```
Mercury-Venus: 6 аспектов
Mercury-Mars: 6 аспектов
Mercury-Jupiter: 6 аспектов
```

### B10. Mercury-Saturn/Uranus/Neptune/Pluto (24 текста)
```
Mercury-Saturn: 6 аспектов
Mercury-Uranus: 6 аспектов
Mercury-Neptune: 6 аспектов
Mercury-Pluto: 6 аспектов
```

### B11. Venus-Mars/Jupiter/Saturn/Uranus/Neptune/Pluto (36 текстов, разбить на 2)
```
B11a: Venus-Mars, Venus-Jupiter, Venus-Saturn (18)
B11b: Venus-Uranus, Venus-Neptune, Venus-Pluto (18)
```

### B12. Mars-Jupiter/Saturn/Uranus/Neptune/Pluto (30 текстов)
```
Mars-Jupiter: 6
Mars-Saturn: 6
Mars-Uranus: 6
Mars-Neptune: 6
Mars-Pluto: 6
```

### B13. Jupiter-Saturn/Uranus/Neptune/Pluto (24 текста)
```
Jupiter-Saturn: 6
Jupiter-Uranus: 6
Jupiter-Neptune: 6
Jupiter-Pluto: 6
```

### B14. Saturn-Uranus/Neptune/Pluto + внешние (24 текста)
```
Saturn-Uranus: 6
Saturn-Neptune: 6
Saturn-Pluto: 6
Uranus-Neptune: 6
```

### B15. Uranus-Pluto, Neptune-Pluto (12 текстов)
```
Uranus-Pluto: 6
Neptune-Pluto: 6
```

---

## БЛОК C: ТРАНЗИТ — ПЛАНЕТЫ В ДОМАХ (120 текстов, 5 порций по 24)

```
Таблица: transit_planets_houses
Поле: text
Формат: Транзитная планета проходит через N-й натальный дом
```

### C1. Транзит Sun, Moon в 12 домах (24 текста)
```
Sun в домах 1-12
Moon в домах 1-12
```

### C2. Транзит Mercury, Venus в 12 домах (24 текста)
```
Mercury в домах 1-12
Venus в домах 1-12
```

### C3. Транзит Mars, Jupiter в 12 домах (24 текста)
```
Mars в домах 1-12
Jupiter в домах 1-12
```

### C4. Транзит Saturn, Uranus в 12 домах (24 текста)
```
Saturn в домах 1-12
Uranus в домах 1-12
```

### C5. Транзит Neptune, Pluto в 12 домах (24 текста)
```
Neptune в домах 1-12
Pluto в домах 1-12
```

---

## БЛОК D: ТРАНЗИТ — АСПЕКТЫ К НАТАЛУ (600 текстов, 25 порций по 24)

```
Таблица: transit_aspects
Поле: text
Формат: Транзитная планета X в аспекте Y к натальной планете Z
```

### D1-D4. Транзит Sun ко всем натальным (60 текстов = 4 порции)
```
D1: Tr.Sun → Nat.Sun/Moon/Mercury/Venus (24)
D2: Tr.Sun → Nat.Mars/Jupiter/Saturn/Uranus (24)
D3: Tr.Sun → Nat.Neptune/Pluto (12)
```

### D4-D6. Транзит Moon (60 текстов)
```
D4: Tr.Moon → Nat.Sun/Moon/Mercury/Venus (24)
D5: Tr.Moon → Nat.Mars/Jupiter/Saturn/Uranus (24)
D6: Tr.Moon → Nat.Neptune/Pluto (12)
```

### D7-D9. Транзит Mercury (60 текстов)
```
D7: Tr.Mercury → Nat.Sun/Moon/Mercury/Venus (24)
D8: Tr.Mercury → Nat.Mars/Jupiter/Saturn/Uranus (24)
D9: Tr.Mercury → Nat.Neptune/Pluto (12)
```

### D10-D12. Транзит Venus (60 текстов)
```
D10: Tr.Venus → Nat.Sun/Moon/Mercury/Venus (24)
D11: Tr.Venus → Nat.Mars/Jupiter/Saturn/Uranus (24)
D12: Tr.Venus → Nat.Neptune/Pluto (12)
```

### D13-D15. Транзит Mars (60 текстов)
```
D13: Tr.Mars → Nat.Sun/Moon/Mercury/Venus (24)
D14: Tr.Mars → Nat.Mars/Jupiter/Saturn/Uranus (24)
D15: Tr.Mars → Nat.Neptune/Pluto (12)
```

### D16-D18. Транзит Jupiter (60 текстов)
```
D16: Tr.Jupiter → Nat.Sun/Moon/Mercury/Venus (24)
D17: Tr.Jupiter → Nat.Mars/Jupiter/Saturn/Uranus (24)
D18: Tr.Jupiter → Nat.Neptune/Pluto (12)
```

### D19-D21. Транзит Saturn (60 текстов)
```
D19: Tr.Saturn → Nat.Sun/Moon/Mercury/Venus (24)
D20: Tr.Saturn → Nat.Mars/Jupiter/Saturn/Uranus (24)
D21: Tr.Saturn → Nat.Neptune/Pluto (12)
```

### D22-D24. Транзит Uranus (60 текстов)
```
D22: Tr.Uranus → Nat.Sun/Moon/Mercury/Venus (24)
D23: Tr.Uranus → Nat.Mars/Jupiter/Saturn/Uranus (24)
D24: Tr.Uranus → Nat.Neptune/Pluto (12)
```

### D25-D27. Транзит Neptune (60 текстов)
```
D25: Tr.Neptune → Nat.Sun/Moon/Mercury/Venus (24)
D26: Tr.Neptune → Nat.Mars/Jupiter/Saturn/Uranus (24)
D27: Tr.Neptune → Nat.Neptune/Pluto (12)
```

### D28-D30. Транзит Pluto (60 текстов)
```
D28: Tr.Pluto → Nat.Sun/Moon/Mercury/Venus (24)
D29: Tr.Pluto → Nat.Mars/Jupiter/Saturn/Uranus (24)
D30: Tr.Pluto → Nat.Neptune/Pluto (12)
```

---

## БЛОК E: СОЛЯР — ПЛАНЕТЫ В ЗНАКАХ (120 текстов, 5 порций по 24)

```
Таблица: solar_planets_signs
Поле: text
Контекст: "В этом году планета X в знаке Y означает..."
```

### E1. Соляр Sun, Moon в 12 знаках (24 текста)
### E2. Соляр Mercury, Venus в 12 знаках (24 текста)
### E3. Соляр Mars, Jupiter в 12 знаках (24 текста)
### E4. Соляр Saturn, Uranus в 12 знаках (24 текста)
### E5. Соляр Neptune, Pluto в 12 знаках (24 текста)

---

## БЛОК F: СОЛЯР — ПЛАНЕТЫ В ДОМАХ (120 текстов, 5 порций по 24)

```
Таблица: solar_planets_houses
Поле: text
Контекст: "Соляр планета X в N-м доме — тема года..."
```

### F1. Соляр Sun, Moon в 12 домах (24 текста)
### F2. Соляр Mercury, Venus в 12 домах (24 текста)
### F3. Соляр Mars, Jupiter в 12 домах (24 текста)
### F4. Соляр Saturn, Uranus в 12 домах (24 текста)
### F5. Соляр Neptune, Pluto в 12 домах (24 текста)

---

## БЛОК G: СОЛЯР — АСПЕКТЫ К НАТАЛУ (600 текстов, 25 порций по 24)

```
Таблица: solar_aspects
Поле: text
Структура аналогична блоку D (транзиты)
```

### G1-G30. Аналогично D1-D30, но контекст "в этом году"

---

## БЛОК H: ЛУНАР — ПЛАНЕТЫ В ЗНАКАХ (120 текстов, 5 порций по 24)

```
Таблица: lunar_planets_signs
Поле: text
Контекст: "В этом месяце планета X в знаке Y..."
```

### H1-H5. Аналогично E1-E5, но контекст "в этом месяце"

---

## БЛОК I: ЛУНАР — ПЛАНЕТЫ В ДОМАХ (120 текстов, 5 порций по 24)

```
Таблица: lunar_planets_houses
Поле: text
Контекст: "Лунар планета X в N-м доме — тема месяца..."
```

### I1-I5. Аналогично F1-F5, но контекст "в этом месяце"

---

## БЛОК J: ЛУНАР — АСПЕКТЫ К НАТАЛУ (600 текстов, 25 порций по 24)

```
Таблица: lunar_aspects
Поле: text
Контекст: "В этом месяце аспект X..."
```

### J1-J30. Аналогично D1-D30, но контекст "в этом месяце"

---

## БЛОК K: СИНАСТРИЯ — АСПЕКТЫ (600 текстов, 25 порций по 24)

```
Таблица: synastry_aspects
Поле: text
Контекст: "Ваша планета X в аспекте Y к планете Z партнёра..."
```

### K1-K30. Структура как D1-D30, но контекст отношений

---

## БЛОК L: СИНАСТРИЯ — ПЛАНЕТЫ В ДОМАХ ПАРТНЁРА (120 текстов, 5 порций)

```
Таблица: synastry_planets_houses
Поле: text
Контекст: "Ваша планета X попадает в N-й дом партнёра..."
```

### L1. Sun, Moon в 12 домах партнёра (24 текста)
### L2. Mercury, Venus в 12 домах партнёра (24 текста)
### L3. Mars, Jupiter в 12 домах партнёра (24 текста)
### L4. Saturn, Uranus в 12 домах партнёра (24 текста)
### L5. Neptune, Pluto в 12 домах партнёра (24 текста)

---

# 📊 СВОДНАЯ ТАБЛИЦА ПОРЦИЙ

| Блок | Категория | Порций | Текстов | Приоритет |
|------|-----------|--------|---------|-----------|
| A | Синастрия: быстрые | 3 | 46 | 🔴 1 |
| B | Натал: аспекты | 15 | 270 | 🔴 1 |
| C | Транзит: дома | 5 | 120 | 🟡 2 |
| D | Транзит: аспекты | 30 | 600 | 🟡 2 |
| E | Соляр: знаки | 5 | 120 | 🟢 3 |
| F | Соляр: дома | 5 | 120 | 🟢 3 |
| G | Соляр: аспекты | 30 | 600 | 🟢 3 |
| H | Лунар: знаки | 5 | 120 | 🟢 3 |
| I | Лунар: дома | 5 | 120 | 🟢 3 |
| J | Лунар: аспекты | 30 | 600 | 🟢 3 |
| K | Синастрия: аспекты | 30 | 600 | 🔴 1 |
| L | Синастрия: дома | 5 | 120 | 🔴 1 |

**ИТОГО: ~168 порций по ~20-24 текста**

---

# 🎯 РЕКОМЕНДУЕМЫЙ ПОРЯДОК

1. **A1-A3** — Синастрия быстрые (46 текстов) — 30 мин
2. **B1-B15** — Натал аспекты (270 текстов) — 2 часа
3. **K1-K30** — Синастрия аспекты (600 текстов) — 4 часа
4. **L1-L5** — Синастрия дома (120 текстов) — 1 час
5. **C1-C5** — Транзит дома (120 текстов) — 1 час
6. **D1-D30** — Транзит аспекты (600 текстов) — 4 часа
7. **E1-F5** — Соляр знаки+дома (240 текстов) — 2 часа
8. **G1-G30** — Соляр аспекты (600 текстов) — 4 часа
9. **H1-I5** — Лунар знаки+дома (240 текстов) — 2 часа
10. **J1-J30** — Лунар аспекты (600 текстов) — 4 часа

---

# 📝 ПРИМЕР КОМАНДЫ ДЛЯ GPT 5.2

```
Заполни порцию B1 (Натал: аспекты Sun-Moon, Sun-Mercury).

12 текстов:
- Sun-Moon: Conjunction, Opposition, Trine, Square, Sextile, Quincunx
- Sun-Mercury: Conjunction, Opposition, Trine, Square, Sextile, Quincunx

Формат ответа JSON:
[
  {"planet1": "Sun", "planet2": "Moon", "aspect": "Conjunction", "text": "..."},
  ...
]

Длина каждого текста: 150-250 слов.
Контекст: натальная карта (характер человека).
```

---

*Документ создан: 14.12.2024*

