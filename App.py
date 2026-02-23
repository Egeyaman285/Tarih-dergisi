from flask import Flask, render_template_string, abort

app = Flask(__name__)

# --- 350 SCP VERİ HAVUZU & EKSTRA SINIFLAR ---
scp_database = [
    {"id": "173", "cls": "euclid", "name": "Heykel", "desc": "SCP-173, beton ve inşaat demirinden yapılmış canlı bir heykeldir. Doğrudan göz teması kesildiği anda inanılmaz bir hızla hareket eder ve kurbanlarının boynunu kırar. Odasına giren personelin birbirini 'şimdi göz kırpıyorum' diyerek uyarması hayati önem taşır. Sürekli olarak yerlere kan ve dışkı karışımı bir madde salgıladığı için odası düzenli temizlenmelidir."},
    {"id": "096", "cls": "euclid", "name": "Utangaç Adam", "desc": "SCP-096, yaklaşık 2.38 metre boyunda bir insansı yaratıktır. Normalde uysaldır ancak birisi yüzüne baktığında kontrolden çıkar. Yüzünü gören kişiyi hedef alır ve dünyanın neresinde olursa olsun onu bulur. Hiçbir fiziksel engel SCP-096'yı hedefine ulaşmaktan alıkoyamaz. Öfke nöbeti bittikten sonra tekrar uysal haline döner."},
    {"id": "682", "cls": "keter", "name": "Zor Ölür Sürüngen", "desc": "Bilinmeyen bir kökene sahip, devasa ve sürüngen benzeri bir yaratıktır. Tüm yaşam formlarına karşı aşırı nefret duyar ve çok yüksek zekaya sahiptir. İnanılmaz bir rejenerasyon yeteneği vardır; asit havuzunda bile hayatta kalabilir. Vakfın en çok imha etmeye çalıştığı ancak her seferinde başarısız olduğu bir varlıktır."},
    {"id": "3000", "cls": "thaumiel", "name": "Anantashesha", "desc": "Bengal Körfezi'nin dibinde bulunan devasa bir su yılanıdır. Vakıf tarafından hafıza silici (amnestics) üretimi için kullanılmaktadır. Varlığı çok gizlidir ve sadece Seviye 5 personelin erişimine açıktır. Zihinsel etkileri nedeniyle personelin yaklaşması yasaktır."},
    {"id": "3999", "cls": "apollyon", "name": "Beni Çıldırtan Şey", "desc": "Gerçekliği büken, kontrol edilemez ve dünyayı yok etme potansiyeline sahip bir varlıktır. Muhafaza edilmesi imkansızdır. Tüm gerçeklik üzerinde tam kontrole sahiptir. Vakfın elindeki en tehlikeli ve açıklanamaz fenomenlerden biridir."},
    {"id": "4444", "cls": "archon", "name": "Bush v. Gore", "desc": "Muhafaza edilmesi durumunda insanlık tarihinin akışını bozacak, bu yüzden bilerek serbest bırakılan bir anomalidir. Siyasi figürlerle ve seçim süreçleriyle bağlantılıdır. Müdahale edilmesi yıkıcı sonuçlar doğurabilir."}
]

# 350 SCP'ye tamamla
all_classes = ["safe", "euclid", "keter", "thaumiel", "apollyon", "archon"]
for i in range(len(scp_database), 350):
    id_num = str(1000 + i)
    cls = all_classes[i % len(all_classes)]
    scp_database.append({
        "id": id_num, "cls": cls, "name": f"Gizli Dosya #{id_num}",
        "desc": f"ERİŞİM REDDEDİLDİ... Şaka şaka.\nBu nesne {cls.upper()} sınıflandırmasındadır.\nVakıf mühendisleri tarafından özel olarak izlenmektedir.\nİçerisinde yüksek miktarda Radyo-Anomalik enerji barındırır.\nPersonelin 3 metreden fazla yaklaşması durumunda zihin koruma kaskı takması zorunludur.\nDosya son güncelleme: 2026-02-23."
    })

# --- GELİŞMİŞ TERMİNAL ARAYÜZÜ ---
HTML_BASE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>SCP FOUNDATION | DEEP WEB TERMINAL</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root { --amber: #ffb000; --bg: #030303; --safe: #00ff41; --euclid: #f1c40f; --keter: #ff3e3e; --thaumiel: #3498db; --apollyon: #9b59b6; --archon: #e67e22; }
        body { background: var(--bg); color: var(--amber); font-family: 'Courier New', monospace; min-height: 100vh; position: relative; }
        
        /* ARKA PLAN LOGO */
        .scp-logo-bg {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 80vh; height: 80vh; background: url('https://upload.wikimedia.org/wikipedia/commons/e/ec/SCP_Foundation_logo.svg') no-repeat center;
            opacity: 0.07; filter: sepia(1) saturate(5) hue-rotate(5deg); pointer-events: none; z-index: -1;
        }

        .terminal { border: 1px solid var(--amber); box-shadow: 0 0 20px rgba(255,176,0,0.15); padding: 30px; margin-top: 20px; background: rgba(3,3,3,0.9); }
        .typewriter { overflow: hidden; white-space: pre-wrap; }
        
        /* SINIF RENKLERİ */
        .safe { color: var(--safe); } .euclid { color: var(--euclid); } .keter { color: var(--keter); }
        .thaumiel { color: var(--thaumiel); } .apollyon { color: var(--apollyon); } .archon { color: var(--archon); }

        .btn-scp { background: transparent; border: 1px solid var(--amber); color: var(--amber); border-radius: 0; margin: 5px; transition: 0.3s; }
        .btn-scp:hover { background: var(--amber); color: #000; box-shadow: 0 0 15px var(--amber); }
        
        .scanline { width: 100%; height: 3px; background: rgba(255, 176, 0, 0.05); position: fixed; top: 0; left: 0; animation: scan 6s linear infinite; pointer-events: none; }
        @keyframes scan { from { top: 0; } to { top: 100%; } }
    </style>
</head>
<body>
    <div class="scp-logo-bg"></div>
    <div class="scanline"></div>
    <div class="container terminal">
        <header class="mb-4 border-bottom border-secondary d-flex justify-content-between">
            <span>[DB_SÜRÜM: 3.5.0] [STATÜ: AKTİF]</span>
            <nav>
                <a href="/" class="btn-scp btn btn-sm">ANA MENÜ</a>
                <a href="/ayarlar" class="btn-scp btn btn-sm">AYARLAR</a>
            </nav>
        </header>
        {{ content | safe }}
    </div>

    <script>
        function typeWriter(el, speed = 20) {
            const text = el.innerText; el.innerText = '';
            let i = 0;
            function type() { if (i < text.length) { el.innerHTML += text.charAt(i); i++; setTimeout(type, speed); } }
            type();
        }
        document.querySelectorAll('.typewriter').forEach(el => typeWriter(el));
    </script>
</body>
</html>
"""

INDEX_CONTENT = """
<div class="text-center py-5">
    <h1 class="display-1 fw-bold">SCP DATABASE</h1>
    <p class="lead">SECURE. CONTAIN. PROTECT.</p>
    <hr>
    <div class="row g-3 mt-4">
        <div class="col-md-4"><a href="/sinif/safe" class="btn btn-scp w-100 py-3">SAFE</a></div>
        <div class="col-md-4"><a href="/sinif/euclid" class="btn btn-scp w-100 py-3">EUCLID</a></div>
        <div class="col-md-4"><a href="/sinif/keter" class="btn btn-scp w-100 py-3">KETER</a></div>
        <div class="col-md-4"><a href="/sinif/thaumiel" class="btn btn-scp w-100 py-3 text-info">THAUMIEL</a></div>
        <div class="col-md-4"><a href="/sinif/apollyon" class="btn btn-scp w-100 py-3 text-warning">APOLLYON</a></div>
        <div class="col-md-4"><a href="/sinif/archon" class="btn btn-scp w-100 py-3 text-danger">ARCHON</a></div>
    </div>
</div>
"""

LIST_CONTENT = """
<h2 class="mb-4">Sorgu: {{ cls.upper() }} SINIFI (350 Kayıt Mevcut)</h2>
<div class="row row-cols-1 row-cols-md-4 g-2">
    {% for scp in scps %}
    <div class="col">
        <div class="p-2 border border-secondary">
            <span class="{{ scp.cls }}">SCP-{{ scp.id }}</span>
            <br><a href="/scp/{{ scp.id }}" class="text-white small">[DETAY]</a>
        </div>
    </div>
    {% endfor %}
</div>
"""

DETAIL_CONTENT = """
<div class="p-4">
    <h1 class="{{ scp.cls }}">SCP-{{ scp.id }}</h1>
    <h3 class="text-muted">NESNE SINIFI: <span class="{{ scp.cls }}">{{ scp.cls.upper() }}</span></h3>
    <hr>
    <div class="typewriter fs-5" style="line-height: 1.8;">{{ scp.desc }}</div>
    <hr>
    <button onclick="history.back()" class="btn-scp btn mt-4">Geri Dön</button>
</div>
"""

SETTINGS_CONTENT = """
<h3>SİSTEM YAPILANDIRMASI</h3>
<hr>
<div class="fs-5">
    <p>> Arka Plan Logosu: [AKTİF]</p>
    <p>> Veri Tabanı Boyutu: [350 NESNE]</p>
    <p>> Terminal Rengi: [AMBER STANDART]</p>
    <div class="mt-4">
        <button class="btn-scp" onclick="document.body.style.color='#00ff41'">YEŞİL TERMİNAL</button>
        <button class="btn-scp" onclick="document.body.style.color='#ffb000'">AMBER TERMİNAL</button>
    </div>
</div>
"""

@app.route('/')
def index(): return render_template_string(HTML_BASE, content=INDEX_CONTENT)

@app.route('/sinif/<cls>')
def list_scps(cls):
    filtered = [s for s in scp_database if s['cls'] == cls.lower()]
    return render_template_string(HTML_BASE, content=render_template_string(LIST_CONTENT, scps=filtered, cls=cls))

@app.route('/scp/<scp_id>')
def detail(scp_id):
    scp = next((s for s in scp_database if s['id'] == scp_id), None)
    if not scp: abort(404)
    return render_template_string(HTML_BASE, content=render_template_string(DETAIL_CONTENT, scp=scp))

@app.route('/ayarlar')
def settings(): return render_template_string(HTML_BASE, content=SETTINGS_CONTENT)

if __name__ == "__main__":
    app.run(debug=True)
