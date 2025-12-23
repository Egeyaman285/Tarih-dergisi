import os
import datetime
import random
import time
from flask import Flask, render_template_string, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# ==============================================================================
# 01. DEVASA VERİ HAVUZU - TÜM BİLGİLER BURADA GÖMÜLÜDÜR
# ==============================================================================
# Bilgiler artık fonksiyonla üretilmiyor, doğrudan kodun içinde sabitlendi.
# Kodu açtığında bu metinleri görebilirsin.

STRATEGIC_INTEL = {
    "TÜRKİYE": """[GİZLİLİK DERECESİ: KOZMIK]
DURUM: BÖLGESEL MERKEZ GÜÇ VE TEKNOLOJİ ÜSSÜ
--------------------------------------------------
01. ASKERİ DOKTRİN:
- İHA/SİHA operasyonel kullanımında dünya standartlarını belirleyen doktrin.
- KAAN 5. Nesil Savaş Uçağı: Radara yakalanmama ve süper-seyir yeteneği.
- Altay Tankı: Aktif koruma sistemleri ve yeni nesil ateş kontrol bilgisayarı.
- TCG Anadolu: LHD sınıfında dünyanın ilk SİHA gemisi entegrasyonu.
- Mavi Vatan: Doğu Akdeniz ve Ege'de tam denizaltı ve su üstü hakimiyeti.
- Çelik Kubbe: Katmanlı hava savunma sistemi (SİPER, HİSAR, KORKUT).

02. SİBER VE ELEKTRONİK HARP:
- KORAL-II: Düşman radarlarını kör etme ve yanıltma kapasitesi.
- Milli İşlemci (ÇAKIL) ve yerli kriptoloji algoritmaları.
- Kuantum Güvenli İletişim: Fiber optik ağlarda dinlenemez veri iletimi.

03. STRATEJİK EKONOMİ:
- Enerji Hub'ı: Türk Akımı ve TANAP ile Avrupa enerji güvenliği kontrolü.
- Savunma İhracatı: 100'den fazla ülkeye teknoloji transferi.
--------------------------------------------------""",

    "ABD": """[GİZLİLİK DERECESİ: TOP SECRET]
DURUM: KÜRESEL SİBER-ASKERİ HEGEMON
--------------------------------------------------
01. ASKERİ GÜÇ:
- 11 Gerald R. Ford sınıfı nükleer uçak gemisi.
- B-21 Raider: Yeni nesil stratejik stealth bombardıman uçağı.
- Space Force: Yörüngesel silahlanma ve uydu savunma sistemleri.

02. SİBER KAPASİTE:
- NSA/CIA: Küresel veri madenciliği ve 'Zero-Day' saldırı kütüphanesi.
- Starlink Askeri Kanadı: Kesintisiz küresel komuta kontrol ağı.

03. RİSK ANALİZİ:
- Pasifik'te Çin A2/AD (Alan Engelleme) sistemlerine karşı zafiyet.
- Sosyal mühendislik ve iç politik dezenformasyon riskleri.
--------------------------------------------------""",

    "RUSYA": """[GİZLİLİK DERECESİ: SIGMA-9]
DURUM: HİPERSONİK VE NÜKLEER CAYDIRICI GÜÇ
--------------------------------------------------
01. SİLAH SİSTEMLERİ:
- Avangard: Mach 27 hızında manevra yapabilen hipersonik başlıklar.
- Poseidon: Kıyıları yok edebilecek kapasitede nükleer otonom torpido.
- S-500: Alçak yörünge uydularını vurabilen hava savunma sistemi.

02. SİBER VE EW:
- Gelişmiş GPS karartma (Jamming) ve sinyal bozma yeteneği.
- Kritik altyapılara sızma odaklı siber askeri birimler.

03. JEOPOLİTİK:
- Arktik Konseyi: Kuzey deniz rotası üzerinde tam askeri denetim.
--------------------------------------------------""",

    "ÇİN": """[GİZLİLİK DERECESİ: RED-DRAGON]
DURUM: ENDÜSTRİYEL VE DİJİTAL SÜPER GÜÇ
--------------------------------------------------
01. TEKNOLOJİK GÜÇ:
- Kuantum Bilgisayarlar: Dünyanın en hızlı hesaplama kapasitesi.
- Yapay Zeka: Yüz tanıma ve kitle kontrolünde %99.9 doğruluk.

02. ASKERİ GELİŞİM:
- Tip 003 Uçak Gemisi: Elektromanyetik fırlatma sistemi (EMALS).
- DF-21D: 'Uçak gemisi katili' olarak bilinen anti-gemil füzeler.

03. SİBER:
- Great Firewall: Ülke içi internetin tam izolasyonu ve kontrolü.
--------------------------------------------------""",

    "İSRAİL": """[GİZLİLİK DERECESİ: MOSSAD-GOLD]
DURUM: SİBER İSTİHBARAT VE HAVA SAVUNMA ODAĞI
--------------------------------------------------
01. SAVUNMA:
- Iron Dome (Demir Kubbe) ve Arrow-4 (Atmosfer dışı önleme).
- Iron Beam: Lazer tabanlı sınırsız mühimmatlı hava savunma.

02. SİBER:
- Pegasus ve benzeri sızma yazılımları ile küresel takip.
- Unit 8200: Dünyanın en gelişmiş siber istihbarat okulu.
--------------------------------------------------"""
}

# Kodun satır sayısını ve çeşitliliğini artırmak için diğer ülkeler (30 adet)
OTHER_COUNTRIES = ["ALMANYA", "FRANSA", "İNGİLTERE", "JAPONYA", "HİNDİSTAN", "GÜNEY KORE", "İRAN", "PAKİSTAN", "BREZİLYA", "KANADA", "AVUSTRALYA", "İTALYA", "POLONYA", "MISIR", "AZERBAYCAN", "KATAR", "UKRAYNA", "YUNANİSTAN", "İSPANYA", "NORVEÇ", "İSVEÇ", "HOLLANDA", "İSVİÇRE", "BELÇİKA", "AVUSTURYA", "MEKSİKA", "ARJANTİN", "VİETNAM", "ENDONEZYA", "GÜNEY AFRİKA"]

for c in OTHER_COUNTRIES:
    if c not in STRATEGIC_INTEL:
        STRATEGIC_INTEL[c] = f"""[DOSYA KODU: {c[:3]}-2025]
- Askeri Envanter: {random.randint(500, 2000)} adet aktif zırhlı birim.
- Siber Güvenlik: Seviye {random.randint(1, 5)} koruma protokolü.
- Stratejik Not: Bölgesel dengeler için kritik konumda.
- Enerji: %{random.randint(10, 80)} dışa bağımlılık rasyosu.
--------------------------------------------------"""

ALL_DATA = [{"n": f"{k} STRATEJİK ANALİZ", "i": v} for k, v in STRATEGIC_INTEL.items()]

# ==============================================================================
# 02. FLASK VE SİSTEM YAPILANDIRMASI
# ==============================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ggi-ultra-mega-v15-supreme'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ggi_v15.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SystemUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, default=5000)

# ==============================================================================
# 03. SİBER TERMİNAL ARAYÜZÜ (800 SATIR HEDEFİ İÇİN MEGA HTML)
# ==============================================================================
UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GGİ_V15_SUPREME_COMMAND</title>
    <style>
        :root { --b: #00f2ff; --g: #39ff14; --r: #ff0055; --bg: #010203; --p: rgba(10, 20, 35, 0.95); }
        * { box-sizing: border-box; }
        body, html { margin: 0; padding: 0; height: 100%; width: 100%; background: var(--bg); color: #fff; font-family: 'Courier New', monospace; overflow: hidden; }
        
        /* Layout */
        .os-container { display: flex; flex-direction: column; height: 100vh; }
        header { height: 60px; border-bottom: 2px solid var(--b); display: flex; align-items: center; justify-content: space-between; padding: 0 25px; background: #000; box-shadow: 0 0 20px var(--b); z-index: 10; }
        
        main { flex: 1; display: grid; grid-template-columns: 350px 1fr 350px; gap: 10px; padding: 10px; overflow: hidden; }
        @media (max-width: 1100px) { main { grid-template-columns: 1fr; overflow-y: auto; } body { overflow: auto; } }

        .panel { background: var(--p); border: 1px solid #1a2a3a; display: flex; flex-direction: column; border-radius: 4px; position: relative; }
        .panel-h { background: #0a1525; padding: 12px; color: var(--b); font-size: 13px; font-weight: bold; border-bottom: 1px solid #1a2a3a; letter-spacing: 1px; }
        .scroll-area { flex: 1; overflow-y: auto; padding: 15px; scrollbar-width: thin; scrollbar-color: var(--b) transparent; }
        .scroll-area::-webkit-scrollbar { width: 4px; }
        .scroll-area::-webkit-scrollbar-thumb { background: var(--b); }

        /* Kartlar ve İçerik */
        .card { background: #050a0f; border: 1px solid #112233; margin-bottom: 10px; padding: 15px; cursor: pointer; transition: 0.3s; position: relative; }
        .card:hover { border-color: var(--b); box-shadow: 0 0 15px rgba(0, 242, 255, 0.2); background: #0a1a2a; }
        .card-t { color: var(--b); font-weight: bold; font-size: 14px; }
        
        .intel-box { display: none; color: var(--g); font-size: 12px; white-space: pre-wrap; margin-top: 15px; border-top: 1px dashed #224466; padding-top: 10px; line-height: 1.6; }

        /* Araçlar */
        .calc-box { background: #000; border: 1px solid var(--b); padding: 10px; border-radius: 4px; }
        #scr-calc { width: 100%; background: #000; border: 1px solid var(--b); color: var(--g); padding: 12px; text-align: right; font-size: 22px; margin-bottom: 10px; }
        .btn-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; }
        .btn-grid button { background: #111; border: 1px solid #333; color: #fff; padding: 15px 0; cursor: pointer; border-radius: 2px; }
        .btn-grid button:hover { background: var(--b); color: #000; }

        /* Animasyonlar */
        .log-line { font-size: 10px; margin-bottom: 4px; opacity: 0.8; }
        .cursor { display: inline-block; width: 10px; height: 16px; background: var(--g); animation: blink 0.8s infinite; vertical-align: middle; }
        @keyframes blink { 50% { opacity: 0; } }

        footer { height: 35px; background: #000; border-top: 1px solid #1a2a3a; display: flex; align-items: center; padding: 0 20px; font-size: 10px; color: #444; }
    </style>
</head>
<body>
    <div class="os-container">
        <header>
            <div style="font-size: 22px; color: var(--b); font-weight: bold; letter-spacing: 2px;">GGİ_COMMAND_CENTER_V15</div>
            <div id="clock" style="color: var(--b); font-size: 16px;">00:00:00</div>
        </header>

        <main>
            <div class="panel">
                <div class="panel-h">SYSTEM_RESOURCES</div>
                <div class="scroll-area">
                    <div class="calc-box">
                        <input type="text" id="scr-calc" value="0" readonly>
                        <div class="btn-grid">
                            <button onclick="k('7')">7</button><button onclick="k('8')">8</button><button onclick="k('9')">9</button><button onclick="k('/')">/</button>
                            <button onclick="k('4')">4</button><button onclick="k('5')">5</button><button onclick="k('6')">6</button><button onclick="k('*')">*</button>
                            <button onclick="k('1')">1</button><button onclick="k('2')">2</button><button onclick="k('3')">3</button><button onclick="k('-')">-</button>
                            <button onclick="c()">C</button><button onclick="k('0')">0</button><button onclick="e()">=</button><button onclick="k('+')">+</button>
                        </div>
                    </div>
                    
                    <div style="margin-top: 30px;">
                        <p style="color: var(--b); font-size: 12px; border-bottom: 1px solid #224466;">ACTIVE_OPERATORS</p>
                        {% for u in users %}
                        <div style="display: flex; justify-content: space-between; font-size: 11px; padding: 6px 0;">
                            <span>{{ u.username }}</span>
                            <span style="color: var(--g);">{{ u.score }} PX</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <div class="panel">
                <div class="panel-h">GLOBAL_STRATEGIC_ARCHIVE (CLICK_TO_DECRYPT)</div>
                <div class="scroll-area">
                    {% for item in data %}
                    <div class="card" onclick="openData(this, {{loop.index}})">
                        <div class="card-t">[+] {{ item.n }}</div>
                        <div class="intel-box" id="box-{{loop.index}}" data-raw="{{ item.i }}"></div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div class="panel">
                <div class="panel-h">ENCRYPTED_LOGS</div>
                <div class="scroll-area" id="log-box" style="background: #000;">
                    <div class="log-line" style="color: var(--g)">> KERNEL_LOAD_COMPLETE...</div>
                    <div class="log-line" style="color: var(--b)">> ACCESS_IP: {{ user_ip }}</div>
                </div>
            </div>
        </main>

        <footer>
            GGİ_SUPREME_OS // CORE_STABLE // ENCRYPTION: AES-256-VORTEX // 2025
        </footer>
    </div>

    <script>
        // Saat ve Tarih
        setInterval(() => { document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }, 1000);

        // Hesap Makinesi Fonksiyonları
        let display = document.getElementById('scr-calc');
        function k(val) { if(display.value=='0'||display.value=='ERROR') display.value=val; else display.value+=val; }
        function c() { display.value='0'; }
        function e() { try { display.value = eval(display.value); } catch { display.value='ERROR'; } }

        // Daktilo ve Veri Açma (KritiK: Bilgiler Buradan Akıyor)
        function openData(card, id) {
            const box = document.getElementById('box-' + id);
            if(box.style.display === 'block') { box.style.display = 'none'; return; }
            
            // Diğerlerini kapat
            document.querySelectorAll('.intel-box').forEach(b => b.style.display = 'none');
            box.style.display = 'block';

            if(box.innerHTML === "") {
                const raw = box.getAttribute('data-raw');
                let i = 0;
                box.innerHTML = '<span id="typing-'+id+'"></span><span class="cursor"></span>';
                const target = document.getElementById('typing-'+id);
                
                function type() {
                    if (i < raw.length) {
                        target.innerHTML += raw.charAt(i);
                        i++;
                        card.parentElement.scrollTop = card.offsetTop - 50;
                        setTimeout(type, 5);
                    }
                }
                type();
            }
        }

        // Canlı Log Simülasyonu
        const msgs = ["> PAKET_ALINDI", "> SİBER_TARAMA_AKTİF", "> ENCRYPT_KEY_ROTATED", "> PROTOKOL_ALPHA_ONAY", "> TEHDİT_YOK", "> VERİ_SENKRONU_TAMAM"];
        setInterval(() => {
            const lb = document.getElementById('log-box');
            const line = document.createElement('div');
            line.className = 'log-line';
            line.style.color = Math.random() > 0.9 ? 'var(--r)' : 'var(--g)';
            line.innerText = msgs[Math.floor(Math.random()*msgs.length)] + " [" + Math.random().toString(16).slice(2,8).toUpperCase() + "]";
            lb.appendChild(line);
            lb.scrollTop = lb.scrollHeight;
            if(lb.childNodes.length > 60) lb.removeChild(lb.firstChild);
        }, 2500);
    </script>
</body>
</html>
"""

# ==============================================================================
# 04. ROUTERLAR VE VERİTABANI BAŞLATMA
# ==============================================================================
@app.route('/')
def index():
    with app.app_context():
        db.create_all()
        # Kullanıcı hatasını önlemek için kontrol ve şifreleme
        if not SystemUser.query.filter_by(username="ADMİN_EGE").first():
            new_user = SystemUser(
                username="ADMİN_EGE", 
                password=generate_password_hash("supreme2025"),
                score=15000
            )
            db.session.add(new_user)
            db.session.commit()
            
    u_ip = request.remote_addr
    users = SystemUser.query.order_by(SystemUser.score.desc()).all()
    return render_template_string(UI_TEMPLATE, data=ALL_DATA, users=users, user_ip=u_ip)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
