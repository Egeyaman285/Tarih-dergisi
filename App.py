from flask import Flask, render_template_string, abort, request, redirect, session
import random
import os

app = Flask(__name__)
app.secret_key = 'VAKIF_GIZLI_ANAHTAR_2026'

# --- VERİ TABANI (SINIFLARA GÖRE AYRILMIŞ) ---
scp_database = []
# Sınıfları seviyelerle eşleştiriyoruz
LEVEL_MAP = {
    1: "safe",
    2: "euclid",
    3: "keter",
    4: "thaumiel",
    5: "apollyon"
}

def create_scp_report(id_num, cls):
    return f"""[GÜVENLİK PROTOKOLÜ AKTİF]
DOSYA NO: SCP-{id_num}
NESNE SINIFI: {cls.upper()}
-----------------------------------------
ÖZEL MUHAFAZA PROSEDÜRLERİ:
Bu varlık {cls.upper()} sınıfı kriterlerine göre muhafaza edilmektedir. 
Yetkisiz erişim durumunda imha protokolü devreye girer.
[VERİ SİLİNDİ]
-----------------------------------------
AÇIKLAMA:
SCP-{id_num}, Vakıf tarafından kontrol altına alınmış anomalik bir varlıktır.
...
[RAPORUN SONU]"""

# 350 SCP oluştur ve her birini doğru seviyeye/sınıfa ata
for i in range(1, 351):
    id_num = str(1000 + i)
    lvl = (i % 5) + 1  # 1'den 5'e kadar seviye atar
    cls = LEVEL_MAP[lvl] # Seviyeye göre sınıfı zorunlu kılar
    scp_database.append({
        "id": id_num, 
        "cls": cls, 
        "name": f"Varlık #{id_num}",
        "desc": create_scp_report(id_num, cls),
        "level": lvl
    })

SEVİYE_SIFRELERI = {
    "1": "ERISIM-KABUL-S1",
    "2": "ANOMALI-YAKIN-TAKIP",
    "3": "KONSANTRE-KORKU-99",
    "4": "GOZETMEN-YETKISI-ALFA",
    "5": "DUNYA-SONU-PROTOKOLU"
}

# --- TASARIM (DEV LOGO VE FİLTRELEME) ---
HTML_BASE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>SCP-NET TERMINAL</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root { --amber: #ffb000; --bg: #050505; }
        body { 
            background-color: var(--bg); 
            color: var(--amber); 
            font-family: 'Courier New', monospace; 
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden;
        }

        /* DEV SCP LOGOSU - ARKA PLAN */
        .background-logo {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 70vw;
            height: 70vw;
            background-image: url('https://upload.wikimedia.org/wikipedia/commons/e/ec/SCP_Foundation_logo.svg');
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            opacity: 0.15; /* Görünürlüğü artırıldı */
            filter: sepia(1) saturate(3);
            z-index: 0;
            pointer-events: none;
        }

        .terminal-container { 
            position: relative;
            z-index: 10; /* İçeriği logonun önüne taşır */
            border: 2px solid var(--amber); 
            background: rgba(0, 0, 0, 0.8);
            box-shadow: 0 0 30px rgba(255, 176, 0, 0.2);
            padding: 40px;
            margin-top: 50px;
        }

        .btn-custom { 
            background: transparent; border: 1px solid var(--amber); color: var(--amber); 
            padding: 15px; margin: 10px; text-transform: uppercase; display: block;
            text-align: center; text-decoration: none; transition: 0.3s;
        }
        .btn-custom:hover { background: var(--amber); color: #000; }
        
        .typewriter { white-space: pre-wrap; border-left: 2px solid var(--amber); padding-left: 20px; }
    </style>
</head>
<body>
    <div class="background-logo"></div>
    <div class="container">
        <div class="terminal-container">
            <div class="text-center mb-4">
                <img src="https://upload.wikimedia.org/wikipedia/commons/e/ec/SCP_Foundation_logo.svg" style="width:80px; filter:sepia(1);">
                <h1 class="mt-2">VAKIF VERİ TABANI</h1>
                <p>[SİSTEM DURUMU: AKTİF]</p>
            </div>
            {{ content | safe }}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    content = """
    <div class="row">
        <div class="col-md-4"><a href="/login/1" class="btn-custom">SEVİYE 1 (SAFE)</a></div>
        <div class="col-md-4"><a href="/login/2" class="btn-custom">SEVİYE 2 (EUCLID)</a></div>
        <div class="col-md-4"><a href="/login/3" class="btn-custom">SEVİYE 3 (KETER)</a></div>
        <div class="col-md-4"><a href="/login/4" class="btn-custom">SEVİYE 4 (THAUMIEL)</a></div>
        <div class="col-md-4"><a href="/login/5" class="btn-custom">SEVİYE 5 (APOLLYON)</a></div>
    </div>"""
    return render_template_string(HTML_BASE, content=content)

@app.route('/login/<int:level>')
def login_page(level):
    content = f"""
    <div class="text-center p-4">
        <h2 class="text-danger">GÜVENLİK KONTROLÜ - SEVİYE {level}</h2>
        <form action="/verify" method="post" class="mt-4">
            <input type="hidden" name="level" value="{level}">
            <input type="text" name="pwd" class="form-control bg-dark text-warning border-warning text-center mx-auto" style="max-width:300px" autocomplete="off" autofocus>
            <button type="submit" class="btn-custom mt-3 mx-auto" style="width:200px">GİRİŞ</button>
        </form>
    </div>"""
    return render_template_string(HTML_BASE, content=content)

@app.route('/verify', methods=['POST'])
def verify():
    lvl = request.form.get('level')
    pwd = request.form.get('pwd')
    if SEVİYE_SIFRELERI.get(lvl) == pwd:
        session['auth_lvl'] = int(lvl)
        return redirect(f'/archive/{lvl}')
    return "<h1>ERİŞİM REDDEDİLDİ</h1><a href='/'>GERİ</a>"

@app.route('/archive/<int:level>')
def archive(level):
    if session.get('auth_lvl', 0) < level: return redirect('/')
    # KRİTİK DÜZELTME: Sadece o seviyeye ait sınıfı getir
    target_class = LEVEL_MAP[level]
    filtered = [s for s in scp_database if s['cls'] == target_class]
    
    list_html = f"<h3>{target_class.upper()} SINIFI ARŞİVİ</h3><hr><div class='row'>"
    for scp in filtered:
        list_html += f"<div class='col-md-3'><a href='/view/{scp['id']}' class='btn-custom' style='font-size:11px'>SCP-{scp['id']}</a></div>"
    list_html += "</div><a href='/' class='btn-custom mt-4' style='width:150px'>ÇIKIŞ</a>"
    return render_template_string(HTML_BASE, content=list_html)

@app.route('/view/<scp_id>')
def view(scp_id):
    scp = next((s for s in scp_database if s['id'] == scp_id), None)
    if not scp or session.get('auth_lvl', 0) < scp['level']: return redirect('/')
    content = f"<h2>DOSYA: SCP-{scp['id']}</h2><div class='typewriter'>{scp['desc']}</div><br><button onclick='history.back()' class='btn-custom' style='width:150px'>GERİ</button>"
    return render_template_string(HTML_BASE, content=content)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
