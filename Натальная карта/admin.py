"""Админ-панель для управления текстами — расширенная версия"""
import base64
import hmac
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3
from pathlib import Path

app = FastAPI(title="Natal Admin", docs_url=None, redoc_url=None, openapi_url=None)
DB_PATH = Path(__file__).parent / 'data' / 'texts.db'

ADMIN_USER = "admin"
ADMIN_PASS = "astro2025"

CATEGORIES = [
    # НАТАЛ
    ('natal_planets_signs', 'Натал: Планеты в знаках', ['planet', 'sign'], 'text'),
    ('natal_planets_houses', 'Натал: Планеты в домах', ['planet', 'house'], 'text'),
    ('natal_aspects', 'Натал: Аспекты', ['planet1', 'planet2', 'aspect'], 'text'),
    # ТРАНЗИТ
    ('transit_aspects', 'Транзит: Аспекты к наталу', ['transit_planet', 'natal_planet', 'aspect'], 'text'),
    ('transit_planets_houses', 'Транзит: Планеты в домах', ['planet', 'house'], 'text'),
    # СОЛЯР
    ('solar_planets_signs', 'Соляр: Планеты в знаках', ['planet', 'sign'], 'text'),
    ('solar_planets_houses', 'Соляр: Планеты в домах', ['planet', 'house'], 'text'),
    ('solar_aspects', 'Соляр: Аспекты к наталу', ['solar_planet', 'natal_planet', 'aspect'], 'text'),
    # ЛУНАР
    ('lunar_planets_signs', 'Лунар: Планеты в знаках', ['planet', 'sign'], 'text'),
    ('lunar_planets_houses', 'Лунар: Планеты в домах', ['planet', 'house'], 'text'),
    ('lunar_aspects', 'Лунар: Аспекты к наталу', ['lunar_planet', 'natal_planet', 'aspect'], 'text'),
    # СИНАСТРИЯ
    ('synastry_aspects', 'Синастрия: Расшифровки аспектов', ['planet1', 'planet2', 'aspect'], 'text'),
    ('synastry_planets_houses', 'Синастрия: Планеты в домах партнёра', ['planet', 'house'], 'text'),
    ('synastry_spheres', 'Синастрия: Сферы совместимости', ['sphere', 'level'], 'text'),
    ('synastry_levels', 'Синастрия: Уровни совместимости', ['level', 'title'], 'description'),
    ('synastry_recommendations', 'Синастрия: Рекомендации', ['category', 'condition'], 'recommendation'),
]

def get_db():
    return sqlite3.connect(DB_PATH)

def _unauthorized():
    raise HTTPException(
        status_code=401,
        detail="Unauthorized",
        headers={"WWW-Authenticate": 'Basic realm="Natal Admin"'}
    )

def require_basic_auth(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Basic "):
        _unauthorized()
    try:
        raw = auth.split(" ", 1)[1].strip()
        decoded = base64.b64decode(raw).decode("utf-8")
        username, password = decoded.split(":", 1)
    except Exception:
        _unauthorized()
    if not (hmac.compare_digest(username, ADMIN_USER) and hmac.compare_digest(password, ADMIN_PASS)):
        _unauthorized()
    return True

def get_stats():
    conn = get_db()
    cur = conn.cursor()
    stats = []
    for table, name, _, text_col in CATEGORIES:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        total = cur.fetchone()[0]
        cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {text_col} IS NOT NULL AND length({text_col}) > 10")
        filled = cur.fetchone()[0]
        stats.append((table, name, total, filled, total - filled))
    conn.close()
    return stats

@app.get("/", response_class=HTMLResponse)
async def root(_auth: bool = Depends(require_basic_auth)):
    return RedirectResponse("/admin", status_code=302)

@app.get("/admin", response_class=HTMLResponse)
async def index(_auth: bool = Depends(require_basic_auth)):
    stats = get_stats()
    total_all = sum(s[2] for s in stats)
    filled_all = sum(s[3] for s in stats)
    
    rows = ""
    for i, (table, name, total, filled, empty) in enumerate(stats, 1):
        pct = filled/total*100 if total > 0 else 0
        color = "#4caf50" if pct == 100 else "#ffc107" if pct > 0 else "#f44336"
        rows += f"""<tr>
            <td>{i}</td>
            <td><a href="/admin/edit/{table}">{name}</a></td>
            <td>{total}</td>
            <td style="color:{color}">{filled}</td>
            <td>{empty}</td>
            <td>
                <div style="background:#333;border-radius:4px;overflow:hidden;height:20px;width:100px">
                    <div style="background:{color};height:100%;width:{pct}%"></div>
                </div>
            </td>
            <td>{pct:.0f}%</td>
        </tr>"""
    
    return f"""<!DOCTYPE html>
<html><head>
    <meta charset="utf-8">
    <title>Админка текстов</title>
    <style>
        body {{ background:#000; color:#fff; font-family:Inter,sans-serif; padding:40px; }}
        h1 {{ color:#bf5af2; }}
        table {{ width:100%; border-collapse:collapse; margin:20px 0; }}
        th, td {{ padding:12px; text-align:left; border-bottom:1px solid #333; }}
        th {{ background:#1a1a1a; color:#bf5af2; }}
        a {{ color:#0a84ff; text-decoration:none; }}
        a:hover {{ text-decoration:underline; }}
        .summary {{ background:#1a1a1a; padding:20px; border-radius:12px; margin:20px 0; }}
    </style>
</head><body>
    <h1>📊 Админка текстов</h1>
    
    <div class="summary">
        <h2>Общая статистика</h2>
        <p>Всего текстов: <b>{total_all}</b></p>
        <p>Заполнено: <b style="color:#4caf50">{filled_all}</b> ({filled_all/total_all*100:.1f}%)</p>
        <p>Пусто: <b style="color:#f44336">{total_all - filled_all}</b></p>
    </div>
    
    <table>
        <tr><th>№</th><th>Категория</th><th>Всего</th><th>Есть</th><th>Нет</th><th>Прогресс</th><th>%</th></tr>
        {rows}
    </table>
</body></html>"""

@app.get("/admin/edit/{table}", response_class=HTMLResponse)
async def edit_category(table: str, page: int = 1, filter: str = "all", _auth: bool = Depends(require_basic_auth)):
    cat = next((c for c in CATEGORIES if c[0] == table), None)
    if not cat:
        return "Категория не найдена"
    
    table_name, name, columns, text_col = cat
    per_page = 50
    offset = (page - 1) * per_page
    
    conn = get_db()
    cur = conn.cursor()
    
    # Фильтр
    where = ""
    if filter == "empty":
        where = f"WHERE {text_col} IS NULL OR length({text_col}) <= 10"
    elif filter == "filled":
        where = f"WHERE {text_col} IS NOT NULL AND length({text_col}) > 10"
    
    cur.execute(f"SELECT COUNT(*) FROM {table} {where}")
    total = cur.fetchone()[0]
    
    cur.execute(f"SELECT * FROM {table} {where} LIMIT {per_page} OFFSET {offset}")
    rows = cur.fetchall()
    col_names = [d[0] for d in cur.description]
    conn.close()
    
    total_pages = (total + per_page - 1) // per_page
    
    table_html = ""
    for row in rows:
        row_dict = dict(zip(col_names, row))
        keys = " | ".join(str(row_dict.get(c, "")) for c in columns)
        text = row_dict.get(text_col, "") or ""
        text_preview = text[:100] + "..." if len(text) > 100 else text
        has_text = len(text) > 10
        table_html += f"""<tr>
            <td>{row_dict['id']}</td>
            <td>{keys}</td>
            <td style="color:{'#4caf50' if has_text else '#f44336'}">{"✓" if has_text else "✗"}</td>
            <td style="max-width:400px;overflow:hidden;text-overflow:ellipsis">{text_preview}</td>
            <td><a href="/admin/edit/{table}/{row_dict['id']}">✏️</a></td>
        </tr>"""
    
    # Пагинация
    pagination = ""
    for p in range(1, total_pages + 1):
        if p == page:
            pagination += f"<span style='padding:5px 10px;background:#bf5af2;border-radius:4px'>{p}</span> "
        else:
            pagination += f"<a href='/admin/edit/{table}?page={p}&filter={filter}' style='padding:5px 10px'>{p}</a> "
    
    return f"""<!DOCTYPE html>
<html><head>
    <meta charset="utf-8">
    <title>{name}</title>
    <style>
        body {{ background:#000; color:#fff; font-family:Inter,sans-serif; padding:40px; }}
        h1 {{ color:#bf5af2; }}
        table {{ width:100%; border-collapse:collapse; margin:20px 0; }}
        th, td {{ padding:10px; text-align:left; border-bottom:1px solid #333; }}
        th {{ background:#1a1a1a; color:#bf5af2; }}
        a {{ color:#0a84ff; text-decoration:none; }}
        .filters {{ margin:20px 0; }}
        .filters a {{ padding:8px 16px; background:#1a1a1a; border-radius:8px; margin-right:10px; }}
        .filters a.active {{ background:#bf5af2; }}
        .pagination {{ margin:20px 0; }}
    </style>
</head><body>
    <a href="/admin">← Назад</a>
    <h1>{name}</h1>
    
    <div class="filters">
        <a href="/admin/edit/{table}?filter=all" class="{'active' if filter=='all' else ''}">Все ({total})</a>
        <a href="/admin/edit/{table}?filter=empty" class="{'active' if filter=='empty' else ''}">Пустые</a>
        <a href="/admin/edit/{table}?filter=filled" class="{'active' if filter=='filled' else ''}">Заполненные</a>
    </div>
    
    <table>
        <tr><th>ID</th><th>Ключ</th><th>Статус</th><th>Текст</th><th></th></tr>
        {table_html}
    </table>
    
    <div class="pagination">{pagination}</div>
</body></html>"""

@app.get("/admin/edit/{table}/{id}", response_class=HTMLResponse)
async def edit_item(table: str, id: int, _auth: bool = Depends(require_basic_auth)):
    cat = next((c for c in CATEGORIES if c[0] == table), None)
    if not cat:
        return "Категория не найдена"
    
    table_name, name, columns, text_col = cat
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table} WHERE id = ?", (id,))
    row = cur.fetchone()
    col_names = [d[0] for d in cur.description]
    conn.close()
    
    if not row:
        return "Запись не найдена"
    
    row_dict = dict(zip(col_names, row))
    text = row_dict.get(text_col, "") or ""
    
    return f"""<!DOCTYPE html>
<html><head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Редактирование</title>
    <style>
        body {{ background:#000; color:#fff; font-family:Inter,sans-serif; padding:40px; }}
        h1 {{ color:#bf5af2; }}
        textarea {{ width:100%; height:300px; background:#1a1a1a; color:#fff; border:1px solid #333; border-radius:8px; padding:15px; font-size:14px; line-height:1.6; resize:vertical; }}
        textarea:focus {{ border-color:#bf5af2; outline:none; box-shadow:0 0 0 3px rgba(191,90,242,0.2); }}
        button {{ background:#bf5af2; color:#fff; border:none; padding:15px 30px; border-radius:8px; cursor:pointer; font-size:16px; transition:all 0.2s; }}
        button:hover {{ opacity:0.9; transform:translateY(-1px); }}
        .info {{ background:#1a1a1a; padding:15px; border-radius:8px; margin:20px 0; }}
        .save-status {{ display:inline-flex; align-items:center; gap:8px; margin-left:15px; font-size:14px; transition:opacity 0.3s; }}
        .save-status.saving {{ color:#ffd700; }}
        .save-status.saved {{ color:#4caf50; }}
        .save-status.error {{ color:#ff5555; }}
        .save-status.unsaved {{ color:#ff9800; }}
        .toolbar {{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-top:15px; }}
        .restore-btn {{ background:#333; font-size:13px; padding:10px 16px; }}
        .char-count {{ color:#666; font-size:12px; margin-top:5px; }}
    </style>
</head><body>
    <a href="/admin/edit/{table}">← Назад к списку</a>
    <h1>Редактирование</h1>
    
    <div class="info">
        {' | '.join(f'<b>{{k}}:</b> {{v}}' for k, v in row_dict.items() if k not in ['id', text_col])}
    </div>
    
    <form method="post" id="editForm" onsubmit="return handleSubmit()">
        <textarea name="text" id="textArea" oninput="onTextChange()">{text}</textarea>
        <div class="char-count"><span id="charCount">{len(text)}</span> символов</div>
        <div class="toolbar">
            <button type="submit" id="saveBtn">💾 Сохранить</button>
            <span class="save-status" id="saveStatus"></span>
            <button type="button" class="restore-btn" onclick="restoreFromLocal()" id="restoreBtn" style="display:none">🔄 Восстановить черновик</button>
        </div>
    </form>
    
    <script>
        const storageKey = 'admin_text_{table}_{id}';
        const textarea = document.getElementById('textArea');
        const statusEl = document.getElementById('saveStatus');
        const charCount = document.getElementById('charCount');
        const restoreBtn = document.getElementById('restoreBtn');
        let saveTimer = null;
        let isDirty = false;
        let originalText = textarea.value;
        
        // Check for saved draft
        (function() {{
            const saved = localStorage.getItem(storageKey);
            if (saved && saved !== textarea.value && saved.length > 0) {{
                restoreBtn.style.display = 'inline-block';
            }}
        }})();
        
        function onTextChange() {{
            isDirty = true;
            charCount.textContent = textarea.value.length;
            
            // Save to localStorage immediately
            localStorage.setItem(storageKey, textarea.value);
            
            // Show unsaved indicator
            statusEl.className = 'save-status unsaved';
            statusEl.textContent = '● Не сохранено';
            
            // Debounced auto-save (3 seconds)
            clearTimeout(saveTimer);
            saveTimer = setTimeout(autoSave, 3000);
        }}
        
        async function autoSave() {{
            if (!isDirty) return;
            
            statusEl.className = 'save-status saving';
            statusEl.textContent = '⏳ Сохранение...';
            
            try {{
                const formData = new FormData();
                formData.append('text', textarea.value);
                
                const resp = await fetch(window.location.href, {{
                    method: 'POST',
                    body: formData,
                    redirect: 'manual'
                }});
                
                if (resp.status === 303 || resp.ok) {{
                    isDirty = false;
                    originalText = textarea.value;
                    statusEl.className = 'save-status saved';
                    statusEl.textContent = '✓ Сохранено';
                    localStorage.removeItem(storageKey);
                    setTimeout(() => {{ if (!isDirty) statusEl.textContent = ''; }}, 3000);
                }} else {{
                    throw new Error('Server error');
                }}
            }} catch(e) {{
                statusEl.className = 'save-status error';
                statusEl.textContent = '⚠ Ошибка сохранения';
            }}
        }}
        
        function restoreFromLocal() {{
            const saved = localStorage.getItem(storageKey);
            if (saved) {{
                textarea.value = saved;
                charCount.textContent = saved.length;
                isDirty = true;
                statusEl.className = 'save-status unsaved';
                statusEl.textContent = '● Черновик восстановлен';
                restoreBtn.style.display = 'none';
            }}
        }}
        
        function handleSubmit() {{
            // Clear auto-save timer
            clearTimeout(saveTimer);
            localStorage.removeItem(storageKey);
            return true;
        }}
        
        // Warn before leaving with unsaved changes
        window.addEventListener('beforeunload', function(e) {{
            if (isDirty) {{
                e.preventDefault();
                e.returnValue = 'Есть несохранённые изменения. Вы уверены?';
            }}
        }});
        
        // Prevent accidental scroll on mobile touching textarea
        textarea.addEventListener('touchstart', function(e) {{
            e.stopPropagation();
        }}, {{ passive: true }});
    </script>
</body></html>"""

@app.post("/admin/edit/{table}/{id}")
async def save_item(table: str, id: int, text: str = Form(...), _auth: bool = Depends(require_basic_auth)):
    cat = next((c for c in CATEGORIES if c[0] == table), None)
    if not cat:
        return "Категория не найдена"
    table_name, name, columns, text_col = cat
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"UPDATE {table} SET {text_col} = ? WHERE id = ?", (text, id))
    conn.commit()
    conn.close()
    return RedirectResponse(f"/admin/edit/{table}", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
