from flask import Flask, render_template_string, abort, request, redirect, session
import random
import os

app = Flask(__name__)
app.secret_key = 'SÜPER_GİZLİ_VAKIF_ANAHTARI_2026'

# --- VERİ TABANI OLUŞTURMA (350 SCP) ---
def create_scp_report(id_num, cls):
    return f"""[GÜVENLİK PROTOKOLÜ AKTİF]
DOSYA NO: SCP-{id_num}
NESNE SINIFI: {cls.upper()}
ERİŞİM İZNİ: SEVİYE {random.randint(1,5)}

ÖZEL MUHAFAZA PROSEDÜRLERİ:
1. Nesne, her türlü dış müdahaleden arındırılmış, [VERİSİLİNDİ] maddesiyle kaplanmış 10x10x10 metrelik bir odada tutulmalıdır.
... (Rapor içeriği devam ediyor) ...
[RAPORUN SONU]"""

scp_database = []
classes = ["safe", "euclid", "keter", "thaumiel", "apollyon", "archon"]
for i in range(1, 351):
    id_num = str(1000 + i)
    cls = classes[i % len(classes)]
    scp_database.append({
        "id": id_num, 
        "cls": cls, 
        "name": f"Anomalik Varlık #{id_num}",
        "desc": create_scp_report(id_num, cls),
        "level": (i % 5) + 1
    })

# --- YENİ ŞİFRE TASARIMLARI (DEĞİŞİKLİK 2) ---
SEVİYE_SIFRELERI = {
    "1": "ERISIM-KABUL-S1",
    "2": "ANOMALI-YAKIN-TAKIP",
    "3": "KONSANTRE-KORKU-99",
    "4": "GOZETMEN-YETKISI-ALFA",
    "5": "DUNYA-SONU-PROTOKOLU"
}

# --- TASARIM (GÜNCELLEMELER YAPILDI) ---
HTML_BASE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>SCP-NET TERMINAL v5.0</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root { --amber: #ffb000; --bg: #050505; --red: #ff3e3e; }
        
        body { 
            background-color: var(--bg); 
            color: var(--amber); 
            font-family: 'Courier New', monospace; 
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }

        /* ARKA PLAN BÜYÜK LOGO (DEĞİŞİKLİK 3) */
        body::after {
            content: "";
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80vh;
            height: 80vh;
            background-image: url('https://upload.wikimedia.org/wikipedia/commons/e/ec/SCP_Foundation_logo.svg');
            background-repeat: no-repeat;
            background-position: center;
            background-size: contain;
            opacity: 0.07; /* Çok hafif görünmesi için */
            filter: sepia(1) saturate(5);
            z-index: -2;
            pointer-events: none;
        }

        body::before {
            content: "TOP SECRET - SCP-001 REPORT [REDACTED] [SANSÜRLENDİ] ITEM-001: THE GUARDIAN... [VERİ SİLİNDİ]...";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            font-size: 14px;
            color: rgba(255, 176, 0, 0.04);
            white-space: pre-wrap;
            padding: 20px;
            z-index: -1;
            line-height: 2;
            pointer-events: none;
        }

        .terminal-container { 
            border: 2px solid var(--amber); 
            background: rgba(0, 0, 0, 0.85); /* Arkadaki logonun hafif görünmesi için opaklık düşürüldü */
            box-shadow: 0 0 30px rgba(255, 176, 0, 0.2);
            padding: 40px;
            margin-top: 50px;
            position: relative;
        }
        
        /* Buton ve diğer stiller aynı bırakıldı... */
        .btn-custom { background: transparent; border: 1px solid var(--amber); color: var(--amber); padding: 15px; margin: 10px; text-transform: uppercase; letter-spacing: 2px; transition: 0.3s; cursor: pointer; width: 100%; text-decoration: none; display: inline-block; text-align: center; }
        .btn-custom:hover { background: var(--amber); color: #000; box-shadow: 0 0 15px var(--amber); }
        .redacted { background: #ffb000; color: #ffb000; padding: 0 5px; }
        .typewriter { white-space: pre-wrap; border-left: 2px solid var(--amber); padding-left: 20px; margin-top: 20px; font-size: 1.1rem; }
        .scanline { width: 100%; height: 4px; background: rgba(255, 176, 0, 0.05); position: fixed; top: 0; animation: moveScan 8s linear infinite; z-index: 1000; pointer-events: none; }
        @keyframes moveScan { from { top: 0; } to { top: 100%; } }
        .scp-logo-small { width: 120px; opacity: 0.5; filter: sepia(1) saturate(5); }
    </style>
</head>
<body>
    <div class="scanline"></div>
    <div class="container">
        <div class="terminal-container">
            <div class="header-section text-center mb-4">
                <img src="https://upload.wikimedia.org/wikipedia/commons/e/ec/SCP_Foundation_logo.svg" class="scp-logo-small">
                <h1 class="mt-3">VAKIF VERİ TABANI AĞI</h1>
                <p>[STATÜ: GÜVENLİ BAĞLANTI] [SUNUCU: SITE-19]</p>
            </div>
            {{ content | safe }}
        </div>
    </div>
</body>
</html>
"""

# --- YOLLAR (ROUTES) ---

@app.route('/')
def index():
    content = """
    <h3 class="text-center mb-4">ERİŞİM YETKİSİ SEÇİN</h3>
    <div class="row">
        <div class="col-md-4"><a href="/login/1" class="btn-custom">SEVİYE 1 (SAFE)</a></div>
        <div class="col-md-4"><a href="/login/2" class="btn-custom">SEVİYE 2 (EUCLID)</a></div>
        <div class="col-md-4"><a href="/login/3" class="btn-custom">SEVİYE 3 (KETER)</a></div>
        <div class="col-md-4"><a href="/login/4" class="btn-custom">SEVİYE 4 (THAUMIEL)</a></div>
        <div class="col-md-4"><a href="/login/5" class="btn-custom">SEVİYE 5 (APOLLYON)</a></div>
        <div class="col-md-4"><a href="/ayarlar" class="btn-custom">AYARLAR / LOGLAR</a></div>
    </div>
    """
    return render_template_string(HTML_BASE, content=content)

@app.route('/login/<int:level>')
def login_page(level):
    # DEĞİŞİKLİK 1: type="text" yapılarak şifrenin görünmesi sağlandı
    content = f"""
    <div class="text-center p-5">
        <h2 class="text-danger mb-4">DİKKAT! SEVİYE {level} ERİŞİMİ</h2>
        <p>Devam etmek için dijital imza kodunu (şifre) giriniz:</p>
        <form action="/verify" method="post" class="mt-4">
            <input type="hidden" name="level" value="{level}">
            <input type="text" name="pwd" class="form-control bg-dark text-warning border-warning text-center mx-auto" 
                   style="max-width:300px; font-size: 1.2rem; letter-spacing: 2px;" autocomplete="off" autofocus>
            <button type="submit" class="btn-custom mt-4" style="max-width:200px">GİRİŞ YAP</button>
        </form>
    </div>
    """
    return render_template_string(HTML_BASE, content=content)

# ... (Verify, Archive, View, Settings fonksiyonları aynı kalmıştır) ...

@app.route('/verify', methods=['POST'])
def verify():
    lvl = request.form.get('level')
    pwd = request.form.get('pwd')
    if SEVİYE_SIFRELERI.get(lvl) == pwd:
        session['auth_lvl'] = int(lvl)
        return redirect(f'/archive/{lvl}')
    else:
        return """<body style="background:#000;color:red;text-align:center;padding-top:100px;font-family:monospace">
                  <h1>ERİŞİM İZNİ REDDEDİLDİ!</h1><a href="/" style="color:white">TEKRAR DENE</a></body>"""

@app.route('/archive/<int:level>')
def archive(level):
    if session.get('auth_lvl', 0) < level: return redirect('/')
    filtered = [s for s in scp_database if s['level'] == level]
    list_html = f"<h3>ARŞİV SEVİYESİ {level}</h3><hr><div class='row'>"
    for scp in filtered:
        list_html += f"<div class='col-md-3'><a href='/view/{scp['id']}' class='btn-custom' style='font-size:12px'>SCP-{scp['id']}</a></div>"
    list_html += "</div><a href='/' class='btn-custom mt-4' style='width:200px'>ÇIKIŞ</a>"
    return render_template_string(HTML_BASE, content=list_html)

@app.route('/view/<scp_id>')
def view(scp_id):
    scp = next((s for s in scp_database if s['id'] == scp_id), None)
    if not scp or session.get('auth_lvl', 0) < scp['level']: return redirect('/')
    content = f"<h1 class='text-danger'>SCP-{scp['id']}</h1><div class='typewriter'>{scp['desc']}</div><button onclick='history.back()' class='btn-custom' style='width:200px'>GERİ</button>"
    return render_template_string(HTML_BASE, content=content)

@app.route('/ayarlar')
def settings():
    content = "<h3>SİSTEM AYARLARI</h3><hr><p>> Logo Durumu: MERKEZİ<br>> Şifre Maskeleme: DEVRE DIŞI</p><a href='/' class='btn-custom' style='width:200px'>GERI</a>"
    return render_template_string(HTML_BASE, content=content)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
