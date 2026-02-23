from flask import Flask, render_template_string, abort, request, redirect, session
import random
import os

app = Flask(__name__)
app.secret_key = 'VAKIF_GIZLI_ANAHTAR_2026'

# --- VERİ TABANI (DETAYLANDIRILMIŞ 15+ SATIR RAPORLAR) ---
LEVEL_MAP = {1: "safe", 2: "euclid", 3: "keter", 4: "thaumiel", 5: "apollyon"}

def create_scp_report(id_num, cls):
    return f"""[GÜVENLİK PROTOKOLÜ: KATMAN-4 AKTİF]
DOSYA NO: SCP-{id_num}
NESNE SINIFI: {cls.upper()}
KONTROL DURUMU: TAM MUHAFAZA

ÖZEL MUHAFAZA PROSEDÜRLERİ:
1. Nesne, Site-19 bünyesinde bulunan ve [VERİ SİLİNDİ] alaşımıyla güçlendirilmiş 
   standart bir yüksek güvenlik hücresinde tutulmalıdır.
2. Hücre içerisindeki sıcaklık sabit 18°C derecede tutulmalı, sapmalar durumunda 
   Otomatik Soğutma Protokolü (OSP-7) devreye girmelidir.
3. Deneyler sırasında personelin yanında en az bir (1) silahlı güvenlik görevlisi 
   bulunması ve görsel kayıt cihazlarının aktif olması zorunludur.
4. Nesne ile doğrudan temas, sadece Seviye 3 üstü yetkiye sahip personelin 
   yazılı onayı ile D-Sınıfı denekler üzerinden gerçekleştirilebilir.
5. Hücreye girişlerde 'Hava Kilidi Beta' sistemi kullanılmalı, çıkışta personel 
   zorunlu radyasyon ve biyolojik taramadan geçirilmelidir.
6. Herhangi bir enerji kesintisi durumunda, yedek jeneratörler nesnenin 
   elektromanyetik kalkanını ayakta tutmak için önceliklendirilmelidir.

AÇIKLAMA:
SCP-{id_num}, ilk olarak 20██ yılında [SANSÜRLENDİ] bölgesindeki bir kazı 
çalışması sırasında, yerin 50 metre altında keşfedilmiştir. 
Varlığın moleküler yapısı, bilinen organik ve inorganik maddelerin bir karışımı 
gibi görünse de, periyodik tablodaki hiçbir elementle tam uyuşmamaktadır.
Yapılan spektral analizler (Bkz: Ek Belge-09), nesnenin çevresindeki 
gerçeklik dokusunu mikro ölçekte bükebildiğini kanıtlamıştır.
Özneler, SCP-{id_num} ile aynı odada kaldıklarında düşük frekanslı bir 
vızıltı duyduklarını ve [REDACTED] gördüklerini rapor etmişlerdir.
Dr. ██████'in yürüttüğü son testler, nesnenin aslında bir tür 
boyutlararası 'çapa' olabileceği teorisini desteklemektedir.
Eğer muhafaza ihlali gerçekleşirse, etki alanı hızla genişleyerek 
yerel gerçeklik çöküşüne (ZK-Sınıfı Senaryo) neden olabilir.
Personelin bu dosyayı kapattıktan sonra psikolojik destek alması önerilir.

[RAPORUN SONU - VAKIF MÜHÜRÜ ONAYLANDI]"""

scp_database = []
for i in range(1, 351):
    id_num = str(1000 + i)
    lvl = (i % 5) + 1
    cls = LEVEL_MAP[lvl]
    scp_database.append({
        "id": id_num, "cls": cls, "name": f"Varlık #{id_num}",
        "desc": create_scp_report(id_num, cls), "level": lvl
    })

SEVİYE_SIFRELERI = {
    "1": "ERISIM-KABUL-S1", "2": "ANOMALI-YAKIN-TAKIP", "3": "KONSANTRE-KORKU-99",
    "4": "GOZETMEN-YETKISI-ALFA", "5": "DUNYA-SONU-PROTOKOLU"
}

# --- TASARIM (SAHİL ARKA PLANI + ŞEFFAF YEŞİL LOGO + DAKTİLO) ---
HTML_BASE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>SCP TERMINAL v6.0</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root { --neon-green: #39ff14; --amber: #ffb000; --bg-overlay: rgba(0, 5, 0, 0.85); }
        
        body { 
            background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1920&q=80') no-repeat center center fixed;
            background-size: cover;
            color: var(--neon-green); 
            font-family: 'Courier New', monospace; 
            min-height: 100vh; margin: 0; overflow-x: hidden;
        }

        /* ŞEFFAF YEŞİL LOGO KATMANI */
        .scp-overlay-logo {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 60vw; height: 60vw;
            background: url('https://upload.wikimedia.org/wikipedia/commons/e/ec/SCP_Foundation_logo.svg') no-repeat center;
            background-size: contain;
            opacity: 0.12; filter: invert(48%) sepia(79%) saturate(2476%) hue-rotate(86deg) brightness(118%) contrast(119%);
            z-index: 1; pointer-events: none;
        }

        .terminal-container { 
            position: relative; z-index: 10;
            border: 2px solid var(--neon-green); 
            background: var(--bg-overlay);
            box-shadow: 0 0 25px rgba(57, 255, 20, 0.3);
            padding: 40px; margin-top: 50px; border-radius: 5px;
        }

        .btn-custom { 
            background: transparent; border: 1px solid var(--neon-green); color: var(--neon-green); 
            padding: 12px; margin: 8px; text-transform: uppercase; display: block;
            text-align: center; text-decoration: none; transition: 0.3s; font-weight: bold;
        }
        .btn-custom:hover { background: var(--neon-green); color: #000; box-shadow: 0 0 15px var(--neon-green); }
        
        #typewriter-text { white-space: pre-wrap; line-height: 1.6; border-left: 3px solid var(--neon-green); padding-left: 15px; }
        .scanline { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06)); z-index: 100; background-size: 100% 2px, 3px 100%; pointer-events: none; }
    </style>
</head>
<body>
    <div class="scanline"></div>
    <div class="scp-overlay-logo"></div>
    <div class="container">
        <div class="terminal-container">
            <div class="text-center mb-4">
                <h1 style="letter-spacing: 5px; text-shadow: 0 0 10px var(--neon-green);">SCP FOUNDATION ARCHIVE</h1>
                <p>[LOCATION: SITE-19] [STATUS: ENCRYPTED]</p>
            </div>
            <hr style="border-color: var(--neon-green);">
            {{ content | safe }}
        </div>
    </div>

    <script>
        function typeWriter(elementId, text, i = 0) {
            const el = document.getElementById(elementId);
            if (!el) return;
            if (i === 0) el.innerHTML = "";
            if (i < text.length) {
                el.innerHTML += text.charAt(i);
                setTimeout(() => typeWriter(elementId, text, i + 1), 15);
            }
        }
        window.onload = () => {
            const textNode = document.getElementById('raw-text');
            if (textNode) {
                const fullText = textNode.value;
                typeWriter('typewriter-text', fullText);
            }
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    content = """
    <div class="row">
        <div class="col-md-4"><a href="/login/1" class="btn-custom">LVL 1 - SAFE</a></div>
        <div class="col-md-4"><a href="/login/2" class="btn-custom">LVL 2 - EUCLID</a></div>
        <div class="col-md-4"><a href="/login/3" class="btn-custom">LVL 3 - KETER</a></div>
        <div class="col-md-4"><a href="/login/4" class="btn-custom">LVL 4 - THAUMIEL</a></div>
        <div class="col-md-4"><a href="/login/5" class="btn-custom">LVL 5 - APOLLYON</a></div>
    </div>"""
    return render_template_string(HTML_BASE, content=content)

@app.route('/login/<int:level>')
def login_page(level):
    content = f"""
    <div class="text-center">
        <h3 class="text-warning">GÜVENLİK KİMLİK DOĞRULAMA (LEVEL {level})</h3>
        <form action="/verify" method="post" class="mt-4">
            <input type="hidden" name="level" value="{level}">
            <input type="text" name="pwd" class="form-control bg-dark text-success border-success text-center mx-auto" style="max-width:350px; font-size:1.5rem;" autocomplete="off" autofocus>
            <button type="submit" class="btn-custom mt-3 mx-auto" style="width:200px">ERİŞİM İSTE</button>
        </form>
    </div>"""
    return render_template_string(HTML_BASE, content=content)

@app.route('/verify', methods=['POST'])
def verify():
    lvl, pwd = request.form.get('level'), request.form.get('pwd')
    if SEVİYE_SIFRELERI.get(lvl) == pwd:
        session['auth_lvl'] = int(lvl)
        return redirect(f'/archive/{lvl}')
    return "<h1 style='color:red; text-align:center;'>YETKİSİZ ERİŞİM SAPTANDI. GÜVENLİK EKİPLERİ YOLDA.</h1>"

@app.route('/archive/<int:level>')
def archive(level):
    if session.get('auth_lvl', 0) < level: return redirect('/')
    target_class = LEVEL_MAP[level]
    filtered = [s for s in scp_database if s['cls'] == target_class]
    list_html = f"<h3>{target_class.upper()} SINIFI DOSYALARI</h3><div class='row'>"
    for scp in filtered:
        list_html += f"<div class='col-md-3'><a href='/view/{scp['id']}' class='btn-custom' style='font-size:10px'>SCP-{scp['id']}</a></div>"
    list_html += "</div><a href='/' class='btn-custom mt-4' style='width:150px'>ANA MENÜ</a>"
    return render_template_string(HTML_BASE, content=list_html)

@app.route('/view/<scp_id>')
def view(scp_id):
    scp = next((s for s in scp_database if s['id'] == scp_id), None)
    if not scp or session.get('auth_lvl', 0) < scp['level']: return redirect('/')
    content = f"""
    <input type="hidden" id="raw-text" value="{scp['desc']}">
    <h2 class="text-warning">DOSYA: SCP-{scp['id']}</h2>
    <div id="typewriter-text"></div>
    <br><button onclick="history.back()" class="btn-custom" style="width:150px">GERİ</button>
    """
    return render_template_string(HTML_BASE, content=content)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
