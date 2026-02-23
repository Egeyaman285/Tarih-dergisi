from flask import Flask, render_template_string, abort, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'SÜPER_GİZLİ_VAKIF_ANAHTARI_2026'

# --- VERİ TABANI OLUŞTURMA (350 SCP + DETAYLI RAPORLAR) ---
def create_scp_report(id_num, cls):
    # 15+ Satırlık Detaylı Rapor Şablonu
    return f"""[GÜVENLİK PROTOKOLÜ AKTİF]
DOSYA NO: SCP-{id_num}
NESNE SINIFI: {cls.upper()}
ERİŞİM İZNİ: SEVİYE {random.randint(1,5)}

ÖZEL MUHAFAZA PROSEDÜRLERİ:
1. Nesne, her türlü dış müdahaleden arındırılmış, [VERİSİLİNDİ] maddesiyle kaplanmış 10x10x10 metrelik bir odada tutulmalıdır.
2. Odadaki nem oranı %15'in üzerine çıkmamalıdır; aksi takdirde nesne agresifleşmektedir.
3. Deneyler sırasında en az iki (2) Seviye 3 personel odanın dışında hazır bulunmalıdır.
4. Muhafaza ihlali durumunda 'Kod Siyah' protokolü uygulanmalı ve tüm tesis tahliye edilmelidir.
5. Herhangi bir personel nesneyle doğrudan göz teması kurmamalıdır; kuranlar derhal [REDACTED] işlemine tabi tutulmalıdır.
6. Hücrenin temizliği sadece D-Sınıfı personel tarafından, ayda bir kez yapılmalıdır.

AÇIKLAMA:
SCP-{id_num}, ilk olarak 19██ yılında [SANSÜRLENDİ] yakınlarında bir mağarada keşfedilmiştir. 
Fiziksel yapısı itibariyle durağan görünse de, kuantum seviyesinde sürekli bir yer değiştirme sergilemektedir. 
Yapılan testler (Bkz: Ek-4), nesnenin insan bilincine doğrudan sızabildiğini göstermiştir. 
Mağdur olan özneler, nesnenin kendilerine [SANSÜRLENDİ] fısıldadığını iddia etmektedirler.
Nesnenin çevresindeki radyasyon düzeyi, bilinen hiçbir elementle uyuşmamaktadır. 
Dr. ██████ tarafından yürütülen araştırmalar sonucunda, nesnenin aslında bir [REDACTED] olduğu teorisi ortaya atılmıştır.
Bu durum, K-Sınıfı bir dünya sonu senaryosuna yol açabilecek potansiyele sahiptir.
Personelin bu dosyayı okuduktan sonra amneztik (hafıza silici) kullanması tavsiye edilir.

[RAPORUN SONU - YETKİSİZ KOPYALANMASI ÖLÜMLE CEZALANDIRILIR]"""

# 350 SCP'lik Veri Setini Oluştur
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

# Şifre Tanımlamaları
SEVİYE_SIFRELERI = {
    "1": "SCP-SAFE",
    "2": "EUCLID-77",
    "3": "KETER-ALARM",
    "4": "O5-ONLY",
    "5": "PROTOKOL-SİFIR"
}

# --- TASARIM (SCP-001 SANSÜRLÜ RAPOR ARKA PLANI) ---
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

        /* SCP-001 GİZLİ RAPOR ARKA PLANI */
        body::before {
            content: "TOP SECRET - SCP-001 REPORT [REDACTED] [SANSÜRLENDİ] ITEM-001: THE GUARDIAN... [VERİ SİLİNDİ]... PROHIBITED... DEATH PENALTY... NO ACCESS... [REDACTED]";
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
            background: rgba(0, 0, 0, 0.9);
            box-shadow: 0 0 30px rgba(255, 176, 0, 0.2);
            padding: 40px;
            margin-top: 50px;
            position: relative;
        }

        .header-section {
            border-bottom: 2px double var(--amber);
            margin-bottom: 30px;
            padding-bottom: 20px;
            text-align: center;
        }

        .scp-logo {
            width: 120px;
            opacity: 0.3;
            filter: sepia(1) saturate(5);
        }

        .btn-custom {
            background: transparent;
            border: 1px solid var(--amber);
            color: var(--amber);
            padding: 15px;
            margin: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: 0.3s;
            cursor: pointer;
            width: 100%;
        }

        .btn-custom:hover {
            background: var(--amber);
            color: #000;
            box-shadow: 0 0 15px var(--amber);
        }

        .redacted {
            background: #ffb000;
            color: #ffb000;
            padding: 0 5px;
        }

        .typewriter {
            white-space: pre-wrap;
            border-left: 2px solid var(--amber);
            padding-left: 20px;
            margin-top: 20px;
            font-size: 1.1rem;
        }

        .scanline {
            width: 100%;
            height: 4px;
            background: rgba(255, 176, 0, 0.05);
            position: fixed;
            top: 0;
            animation: moveScan 8s linear infinite;
            z-index: 1000;
            pointer-events: none;
        }

        @keyframes moveScan { from { top: 0; } to { top: 100%; } }
    </style>
</head>
<body>
    <div class="scanline"></div>
    <div class="container">
        <div class="terminal-container">
            <div class="header-section">
                <img src="https://upload.wikimedia.org/wikipedia/commons/e/ec/SCP_Foundation_logo.svg" class="scp-logo">
                <h1 class="mt-3">VAKIF VERİ TABANI AĞI</h1>
                <p>[STATÜ: GÜVENLİ BAĞLANTI] [SUNUCU: SITE-19]</p>
            </div>
            {{ content | safe }}
        </div>
    </div>

    <script>
        function runTypewriter() {
            const elements = document.querySelectorAll('.typewriter');
            elements.forEach(el => {
                const text = el.innerText;
                el.innerText = '';
                let i = 0;
                const timer = setInterval(() => {
                    if (i < text.length) {
                        el.innerHTML += text.charAt(i);
                        i++;
                    } else { clearInterval(timer); }
                }, 10);
            });
        }
        window.onload = runTypewriter;
    </script>
</body>
</html>
"""

# --- YOLLAR (ROUTES) ---

@app.route('/')
def index():
    # Ana sayfa: Seviye seçimi
    content = """
    <h3 class="text-center mb-4">ERİŞİM YETKİSİ SEÇİN</h3>
    <div class="row">
        <div class="col-md-4"><a href="/login/1" class="btn-custom btn">SEVİYE 1 (SAFE)</a></div>
        <div class="col-md-4"><a href="/login/2" class="btn-custom btn">SEVİYE 2 (EUCLID)</a></div>
        <div class="col-md-4"><a href="/login/3" class="btn-custom btn">SEVİYE 3 (KETER)</a></div>
        <div class="col-md-4"><a href="/login/4" class="btn-custom btn">SEVİYE 4 (THAUMIEL)</a></div>
        <div class="col-md-4"><a href="/login/5" class="btn-custom btn">SEVİYE 5 (APOLLYON)</a></div>
        <div class="col-md-4"><a href="/ayarlar" class="btn-custom btn">AYARLAR / LOGLAR</a></div>
    </div>
    """
    return render_template_string(HTML_BASE, content=content)

@app.route('/login/<int:level>')
def login_page(level):
    content = f"""
    <div class="text-center p-5">
        <h2 class="text-danger mb-4">DİKKAT! SEVİYE {level} ERİŞİMİ</h2>
        <p>Devam etmek için dijital imza kodunu (şifre) giriniz:</p>
        <form action="/verify" method="post" class="mt-4">
            <input type="hidden" name="level" value="{level}">
            <input type="password" name="pwd" class="form-control bg-dark text-warning border-warning text-center mx-auto" style="max-width:300px" autofocus>
            <button type="submit" class="btn-custom mt-4" style="max-width:200px">GİRİŞ YAP</button>
        </form>
    </div>
    """
    return render_template_string(HTML_BASE, content=content)

@app.route('/verify', methods=['POST'])
def verify():
    lvl = request.form.get('level')
    pwd = request.form.get('pwd')
    
    if SEVİYE_SIFRELERI.get(lvl) == pwd:
        session['auth_lvl'] = int(lvl)
        return redirect(f'/archive/{lvl}')
    else:
        return """<body style="background:#000;color:red;text-align:center;padding-top:100px;font-family:monospace">
                  <h1>ERİŞİM İZNİ REDDEDİLDİ!</h1>
                  <p>GEÇERSİZ KİMLİK BİLGİSİ GİRİLDİ. GÜVENLİK BİRİMLERİ KONUMUNUZA YÖNLENDİRİLDİ.</p>
                  <a href="/" style="color:white">TEKRAR DENE</a></body>"""

@app.route('/archive/<int:level>')
def archive(level):
    if session.get('auth_lvl', 0) < level:
        return redirect('/')
    
    filtered = [s for s in scp_database if s['level'] == level]
    list_html = f"<h3>ARŞİV SEVİYESİ {level} - TOPLAM {len(filtered)} KAYIT</h3><hr>"
    list_html += "<div class='row'>"
    for scp in filtered:
        list_html += f"<div class='col-md-3'><a href='/view/{scp['id']}' class='btn-custom btn' style='font-size:12px'>SCP-{scp['id']}</a></div>"
    list_html += "</div><a href='/' class='btn-custom btn mt-4' style='width:200px'>ÇIKIŞ YAP</a>"
    return render_template_string(HTML_BASE, content=list_html)

@app.route('/view/<scp_id>')
def view(scp_id):
    scp = next((s for s in scp_database if s['id'] == scp_id), None)
    if not scp or session.get('auth_lvl', 0) < scp['level']:
        return redirect('/')
    
    content = f"""
    <div class="p-2">
        <h1 class="text-danger">DOSYA: SCP-{scp['id']}</h1>
        <h4>DURUM: <span class="redacted">[SANSÜRLENDİ]</span></h4>
        <div class="typewriter">{scp['desc']}</div>
        <hr>
        <button onclick="history.back()" class="btn-custom" style="width:200px">GERİ DÖN</button>
    </div>
    """
    return render_template_string(HTML_BASE, content=content)

@app.route('/ayarlar')
def settings():
    content = """
    <h3>SİSTEM TERMİNAL AYARLARI</h3>
    <hr>
    <p>> Arka Plan Dokusu: SCP-001 ONAYLANDI</p>
    <p>> Veri Tabanı Kaydı: 350 Nesne</p>
    <p>> Güvenlik Protokolü: AKTİF</p>
    <p>> Bağlantı Noktası: Render.com Cloud</p>
    <div class="mt-4">
        <p>Sistem Logları:</p>
        <div class="bg-dark p-3 text-secondary small" style="height:150px; overflow-y:scroll">
            [13:48:02] Bağlantı isteği alındı...<br>
            [13:48:05] Seviye 5 protokolü sorgulanıyor...<br>
            [13:48:10] SCP-001 veri sızıntısı engellendi.<br>
            [13:49:01] Kullanıcı kimliği doğrulanamadı...<br>
            [13:49:55] Şifreleme anahtarı güncellendi.
        </div>
    </div>
    <a href="/" class="btn-custom btn mt-4" style="width:200px">GERİ</a>
    """
    return render_template_string(HTML_BASE, content=content)

if __name__ == "__main__":
    app.run(debug=True)
import os

if __name__ == "__main__":
    # Render'ın verdiği portu al, yoksa 5000 kullan
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' dış erişim için ŞARTTIR
    app.run(host='0.0.0.0', port=port)
