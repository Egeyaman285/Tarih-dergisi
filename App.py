from flask import Flask, render_template_string, abort

app = Flask(__name__)

# --- 150 SCP VERİ HAVUZU (Örnekler ve Dinamik Üretim) ---
scp_database = [
    {"id": "173", "cls": "euclid", "name": "Heykel", "desc": "SCP-173, beton ve inşaat demirinden yapılmış, Krylon marka sprey boya izleri taşıyan canlı bir heykeldir. Doğrudan göz teması kesildiği anda inanılmaz bir hızla hareket eder ve kurbanlarının boynunu kırar. Odasına giren personelin birbirini 'şimdi göz kırpıyorum' diyerek uyarması hayati önem taşır. Sürekli olarak yerlere kan ve dışkı karışımı bir madde salgıladığı için odası düzenli temizlenmelidir. Eğer gözünüzü bir saniye bile kırparsanız, SCP-173 sizinle olan mesafeyi anında kapatacaktır."},
    {"id": "096", "cls": "euclid", "name": "Utangaç Adam", "desc": "SCP-096, yaklaşık 2.38 metre boyunda, kas kütlesi çok az olan insansı bir yaratıktır. Normalde uysaldır ancak birisi yüzüne baktığında (fotoğraf dahil) kontrolden çıkar. Yüzünü gören kişiyi hedef alır ve dünyanın neresinde olursa olsun onu bulup yok eder. Hiçbir fiziksel engel veya silahlı saldırı SCP-096'yı hedefine ulaşmaktan alıkoyamaz. Öfke nöbeti bittikten sonra tekrar uysal haline döner ve yüzünü kapatarak ağlamaya başlar."},
    {"id": "682", "cls": "keter", "name": "Zor Ölür Sürüngen", "desc": "Bilinmeyen bir kökene sahip, devasa ve sürüngen benzeri bir yaratıktır. Tüm yaşam formlarına karşı aşırı nefret duyar ve çok yüksek zekaya sahiptir. İnanılmaz bir rejenerasyon yeteneği vardır; asit havuzunda bile hayatta kalabilir. Vakfın en çok imha etmeye çalıştığı ancak her seferinde başarısız olduğu bir varlıktır. Vücut kütlesini ve formunu aldığı hasara göre hızla adapte edebilir ve değiştirebilir."},
]

# 150 SCP'ye tamamla
for i in range(len(scp_database), 150):
    id_num = str(100 + i)
    cls = "safe" if i % 3 == 0 else "euclid" if i % 3 == 1 else "keter"
    scp_database.append({
        "id": id_num, "cls": cls, "name": f"Gözlem Kaydı #{id_num}",
        "desc": f"DOKÜMAN GİZLİLİK DERECESİ: SEVİYE 4\nBu nesne {cls.upper()} sınıflandırmasına dahil edilmiştir.\nBölge 19 içerisinde özel elektromanyetik kilitlerle muhafaza edilmektedir.\nDeney protokolü 12-B gereği, deneklerin nesneyle teması kesinlikle yasaktır.\nHerhangi bir sızıntı durumunda tesis 'Omega-7' protokolüne göre karantinaya alınacaktır.\nBu dosya otomatik olarak güncellenmektedir."
    })

# --- MODERN TERMİNAL ARAYÜZÜ (HTML & CSS & JS) ---
HTML_BASE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>SCP FOUNDATION | SECURE ACCESS</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root { --term-green: #00ff41; --term-bg: #050505; --term-red: #ff3e3e; --term-orange: #ffb000; }
        body { background: var(--term-bg); color: var(--term-green); font-family: 'Courier New', Courier, monospace; overflow-x: hidden; }
        .terminal-border { border: 2px solid var(--term-green); box-shadow: 0 0 15px rgba(0,255,65,0.2); padding: 20px; margin-top: 20px; min-height: 80vh; }
        .scanline { width: 100%; height: 2px; background: rgba(0, 255, 65, 0.1); position: fixed; top: 0; left: 0; pointer-events: none; animation: scan 8s linear infinite; }
        @keyframes scan { from { top: 0; } to { top: 100%; } }
        .typewriter { overflow: hidden; white-space: pre-wrap; display: inline-block; }
        .safe { color: var(--term-green); } .euclid { color: var(--term-orange); } .keter { color: var(--term-red); }
        .btn-term { background: transparent; border: 1px solid var(--term-green); color: var(--term-green); border-radius: 0; transition: 0.3s; margin: 5px; }
        .btn-term:hover { background: var(--term-green); color: black; box-shadow: 0 0 10px var(--term-green); }
        .nav-link { color: var(--term-green) !important; text-decoration: underline; }
        hr { border-color: var(--term-green); opacity: 0.5; }
    </style>
</head>
<body>
    <div class="scanline"></div>
    <div class="container terminal-border">
        <header class="d-flex justify-content-between align-items-center mb-4">
            <div>[SİSTEM: BAĞLI] [YETKİ: SEVİYE 4]</div>
            <div>
                <a href="/" class="btn-term btn btn-sm">ANA DİZİN</a>
                <a href="/ayarlar" class="btn-term btn btn-sm">AYARLAR</a>
            </div>
        </header>
        {{ content | safe }}
    </div>

    <script>
        function typeEffect(element, speed) {
            let text = element.innerHTML;
            element.innerHTML = "";
            let i = 0;
            let timer = setInterval(function() {
                if (i < text.length) {
                    element.append(text.charAt(i));
                    i++;
                } else { clearInterval(timer); }
            }, speed);
        }
        document.querySelectorAll('.typewriter').forEach(el => typeEffect(el, 15));
    </script>
</body>
</html>
"""

INDEX_CONTENT = """
<div class="text-center py-5">
    <h1 class="display-3 mb-0">SCP VAKFI</h1>
    <p class="mb-5 text-uppercase">Güvence Altına Al, Muhafaza Et, Koru</p>
    <div class="row g-4 mt-4">
        <div class="col-md-4"><a href="/sinif/safe" class="btn btn-term w-100 py-4">>> SAFE DOSYALARI</a></div>
        <div class="col-md-4"><a href="/sinif/euclid" class="btn btn-term w-100 py-4">>> EUCLID DOSYALARI</a></div>
        <div class="col-md-4"><a href="/sinif/keter" class="btn btn-term w-100 py-4">>> KETER DOSYALARI</a></div>
    </div>
</div>
"""

LIST_CONTENT = """
<h3>Sorgu Sonucu: {{ cls.upper() }} SINIFI NESNELER</h3>
<hr>
<div class="row row-cols-1 row-cols-md-3 g-3 mt-3">
    {% for scp in scps %}
    <div class="col">
        <div class="p-2 border border-secondary">
            <span class="{{ scp.cls }}">SCP-{{ scp.id }}</span> | {{ scp.name }}
            <br>
            <a href="/scp/{{ scp.id }}" class="nav-link small mt-2 d-inline-block">[DOSYAYI AÇ]</a>
        </div>
    </div>
    {% endfor %}
</div>
"""

DETAIL_CONTENT = """
<div class="scp-report">
    <h2 class="{{ scp.cls }}">NESNE NO: SCP-{{ scp.id }}</h2>
    <h4>SINIF: <span class="{{ scp.cls }}">{{ scp.cls.upper() }}</span></h4>
    <hr>
    <div class="row">
        <div class="col-md-12">
            <p class="typewriter text-start fs-5" style="line-height: 1.6;">{{ scp.desc }}</p>
        </div>
    </div>
    <hr>
    <button onclick="history.back()" class="btn-term btn mt-3">KAPAT</button>
</div>
"""

SETTINGS_CONTENT = """
<h3>SİSTEM AYARLARI</h3>
<hr>
<div class="mt-4">
    <p>Görünüm Modu: [KLASİK TERMİNAL]</p>
    <p>Yazı Tipi: [MONOSPACE CRT]</p>
    <p>Protokol: [SCPNET V2.0.26]</p>
    <div class="mt-4">
        <button class="btn-term" onclick="document.body.style.color='#ffb000'">AMBER MODU</button>
        <button class="btn-term" onclick="document.body.style.color='#00ff41'">YEŞİL MODU</button>
        <button class="btn-term" onclick="location.reload()">SİSTEMİ SIFIRLA</button>
    </div>
</div>
"""

# --- ROUTES ---

@app.route('/')
def index():
    return render_template_string(HTML_BASE, content=INDEX_CONTENT)

@app.route('/sinif/<cls>')
def list_scps(cls):
    filtered = [s for s in scp_database if s['cls'] == cls.lower()]
    content = render_template_string(LIST_CONTENT, scps=filtered, cls=cls)
    return render_template_string(HTML_BASE, content=content)

@app.route('/scp/<scp_id>')
def detail(scp_id):
    scp = next((s for s in scp_database if s['id'] == scp_id), None)
    if not scp: abort(404)
    content = render_template_string(DETAIL_CONTENT, scp=scp)
    return render_template_string(HTML_BASE, content=content)

@app.route('/ayarlar')
def settings():
    return render_template_string(HTML_BASE, content=SETTINGS_CONTENT)

if __name__ == "__main__":
    app.run(debug=True)
