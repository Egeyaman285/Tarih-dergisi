from flask import Flask, render_template_string, abort, request, redirect, session

app = Flask(__name__)
app.secret_key = 'vakif_gizli_anahtar'

# --- 350 SCP VERİ HAVUZU (15+ SATIR DETAYLI) ---
def generate_desc(id_num, cls):
    return f"""[ERİŞİM KAYDI ONAYLANDI]
NESNE NO: SCP-{id_num}
SINIFLANDIRMA: {cls.upper()}
MUHAFAZA PROSEDÜRLERİ:
Nesne, Bölge-19 bünyesinde bulunan ve her yönden en az 5 metre kalınlığında güçlendirilmiş beton duvarlarla çevrili bir hücrede tutulmalıdır. Hücre içerisindeki hava basıncı sürekli olarak kontrol edilmeli ve herhangi bir sapma durumunda tesis alarmı seviye 3'e yükseltilmelidir. Yetkili personel içeri girmeden önce en az iki (2) güvenlik görevlisi kapıda hazır beklemelidir. İçerideki tüm faaliyetler 7/24 yüksek çözünürlüklü termal kameralarla izlenmelidir.

AÇIKLAMA:
SCP-{id_num}, yapılan radyometrik testlere göre yaklaşık 450 yaşında olduğu tahmin edilen, kökeni tam olarak saptanamamış bir anomalidir. Nesnenin çevresinde sürekli olarak düşük frekanslı bir elektromanyetik dalgalanma gözlemlenmiştir. Bu dalgalanmalar, yakın mesafedeki biyolojik organizmaların sinir sistemi üzerinde doğrudan etki ederek halüsinasyonlara, aşırı öfke nöbetlerine veya geçici hafıza kaybına neden olmaktadır. Yapılan son deneylerde (Bkz: Deney Kaydı {id_num}-A), nesnenin kendi kendine yer değiştirebildiği ve gözlemlenmediği anlarda fiziksel formunu kurbanının en büyük korkusuna dönüştürebildiği saptanmıştır. Bu durum, personelin nesneyle olan temasını minimuma indirmesini zorunlu kılmaktadır. Olası bir muhafaza ihlali durumunda, 'Kilit-Altı' protokolü devreye sokulmalı ve bölge imha birimleri tarafından mühürlenmelidir.
[VERİLERİN DEVAMI İÇİN YETKİ SEVİYESİ ARTTIRILMALIDIR]"""

scp_database = []
all_classes = ["safe", "euclid", "keter", "thaumiel", "apollyon", "archon"]
for i in range(350):
    id_num = str(1000 + i)
    cls = all_classes[i % len(all_classes)]
    scp_database.append({
        "id": id_num, "cls": cls, "name": f"Anomalik Kayıt #{id_num}",
        "desc": generate_desc(id_num, cls),
        "level": (i % 5) + 1 # 1'den 5'e kadar seviyeler
    })

# Şifre Eşleşmeleri
PASSWORDS = {
    "1": "SCP-123",
    "2": "VAKIF-2026",
    "3": "KETER-ALARM",
    "4": "GIZLI-PROJE",
    "5": "DUNYANIN-SONU"
}

# --- ARAYÜZ ---
HTML_BASE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>SCP FOUNDATION SECURITY TERMINAL</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root { --amber: #ffb000; --bg: #020202; }
        body { background: var(--bg); color: var(--amber); font-family: 'Courier New', monospace; overflow-x: hidden; }
        .scanline { width: 100%; height: 2px; background: rgba(255,176,0,0.03); position: fixed; top: 0; animation: scan 10s linear infinite; pointer-events: none; }
        @keyframes scan { from { top: 0; } to { top: 100%; } }
        
        .terminal-container { border: 2px solid var(--amber); margin-top: 30px; padding: 40px; position: relative; background: rgba(0,0,0,0.8); }
        
        /* LOGO ARKADA */
        .header-logo-container { position: relative; text-align: center; margin-bottom: 50px; }
        .bg-logo { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 150px; opacity: 0.2; z-index: 1; }
        .header-title { position: relative; z-index: 2; font-size: 4rem; font-weight: 900; letter-spacing: 10px; }

        .btn-gate { background: transparent; border: 1px solid var(--amber); color: var(--amber); border-radius: 0; transition: 0.3s; margin: 10px; padding: 20px; }
        .btn-gate:hover { background: var(--amber); color: black; box-shadow: 0 0 20px var(--amber); }
        .typewriter { white-space: pre-wrap; line-height: 1.5; font-size: 1.1rem; }
    </style>
</head>
<body>
    <div class="scanline"></div>
    <div class="container terminal-container">
        <div class="header-logo-container">
            <img src="https://upload.wikimedia.org/wikipedia/commons/e/ec/SCP_Foundation_logo.svg" class="bg-logo">
            <h1 class="header-title">SCP DATABASE</h1>
        </div>
        {{ content | safe }}
    </div>
</body>
</html>
"""

INDEX_CONTENT = """
<div class="text-center">
    <h3>ERİŞİM SEVİYESİ SEÇİNİZ</h3>
    <hr style="border-color: var(--amber)">
    <div class="row">
        {% for lvl in range(1, 6) %}
        <div class="col-md-4">
            <form action="/auth" method="post">
                <input type="hidden" name="level" value="{{ lvl }}">
                <button type="submit" class="btn-gate w-100">SEVİYE {{ lvl }} GİRİŞİ</button>
            </form>
        </div>
        {% endfor %}
    </div>
</div>
"""

AUTH_CONTENT = """
<div class="text-center py-5">
    <h2 class="text-danger">GÜVENLİK KONTROLÜ: SEVİYE {{ level }}</h2>
    <p>Lütfen bu yetki seviyesi için atanmış olan güvenlik anahtarını giriniz.</p>
    <form action="/verify" method="post" class="mt-4">
        <input type="hidden" name="level" value="{{ level }}">
        <input type="password" name="password" class="form-control bg-dark text-warning border-warning text-center mx-auto" style="max-width: 300px;" autofocus>
        <button type="submit" class="btn-gate mt-3">DOĞRULA</button>
    </form>
</div>
"""

@app.route('/')
def index():
    return render_template_string(HTML_BASE, content=INDEX_CONTENT)

@app.route('/auth', methods=['POST'])
def auth():
    level = request.form.get('level')
    return render_template_string(HTML_BASE, content=render_template_string(AUTH_CONTENT, level=level))

@app.route('/verify', methods=['POST'])
def verify():
    level = request.form.get('level')
    password = request.form.get('password')
    if PASSWORDS.get(level) == password:
        session['access_level'] = int(level)
        return redirect(f'/list/{level}')
    return "<h1>ERİŞİM REDDEDİLDİ: HATALI ŞİFRE!</h1><a href='/'>Geri Dön</a>"

@app.route('/list/<int:level>')
def list_scps(level):
    if session.get('access_level', 0) < level:
        return redirect('/')
    filtered = [s for s in scp_database if s['level'] == level]
    
    list_html = f"<h3>SEVİYE {level} ARŞİVİ</h3><hr><div class='row'>"
    for scp in filtered:
        list_html += f"<div class='col-md-3'><a href='/scp/{scp['id']}' class='btn-gate w-100'>SCP-{scp['id']}</a></div>"
    list_html += "</div><a href='/' class='btn-gate mt-4'>ANA MENÜ</a>"
    
    return render_template_string(HTML_BASE, content=list_html)

@app.route('/scp/<scp_id>')
def detail(scp_id):
    scp = next((s for s in scp_database if s['id'] == scp_id), None)
    if not scp or session.get('access_level', 0) < scp['level']:
        return "<h1>ERİŞİM YETKİSİ YETERSİZ!</h1>"
    
    content = f"""
    <div class='p-3 border border-warning'>
        <h2 class='text-danger'>DOKÜMAN: SCP-{scp['id']}</h2>
        <p><strong>GÜVENLİK DÜZEYİ:</strong> SEVİYE {scp['level']}</p>
        <hr style='border-color: var(--amber)'>
        <div class='typewriter'>{scp['desc']}</div>
        <button onclick='history.back()' class='btn-gate mt-5'>DOSYAYI KAPAT</button>
    </div>
    """
    return render_template_string(HTML_BASE, content=content)

if __name__ == "__main__":
    app.run(debug=True)
