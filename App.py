import os
import datetime
import random
import time
import json
import base64
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# --- SİSTEM ÇEKİRDEK YAPILANDIRMASI ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ggi-ultra-v12-vortex-888-omega-access-granted'

# Veritabanı dosya yolu
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'ggi_v12.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# --- VERİTABANI MODELLERİ (GENİŞLETİLMİŞ) ---
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)
    access_level = db.Column(db.String(30), default="LEVEL_A_SUPREME")
    last_action = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class SystemVisit(db.Model):
    __tablename__ = 'system_visits'
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50))
    agent = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class GlobalAlert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    risk_level = db.Column(db.Integer) # 1-10
    description = db.Column(db.String(500))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- DEVASA STRATEJİK ANALİZ MOTORU (HER ÜLKE 40+ SATIR) ---
def get_mega_intelligence_report(name):
    unique_id = base64.b16encode(name.encode()).decode()[:10]
    return f"""
[ERİŞİM SEVİYESİ: KOZMIK-TOP-SECRET]
DOSYA REF: GGİ-INTEL-{unique_id}
HEDEF BİRİM: {name} FEDERASYONU / DEVLETİ
----------------------------------------------------------------------
01. ASKERİ DOKTRİN VE CAYDIRICILIK ANALİZİ:
- {name} savunma doktrini, 'Hibrit Savaş' ve 'Alan Engelleme' (A2/AD) üzerine kuruludur.
- Toplam Tank Kuvveti: 5,450 (Aktif Koruma Sistemleri ile donatılmış).
- Toplam Hava Gücü: 1,200+ (5. Nesil savaş uçakları ağırlıklı).
- Nükleer Kapasite: 'Aktif Caydırıcılık' kapsamında 24/7 hazır bekletilmektedir.
- Füze Envanteri: Hipersonik (Mach 7+) vuruş yeteneği onaylanmıştır.
- Özel Operasyon Birimleri: 'Siyah Müfreze' seviyesinde 12 tabur mevcuttur.
- Deniz Savunması: Otonom denizaltı dronları ve sonar engelleme ağları.
- Lojistik: 48 saatlik genel seferberlik protokolü 'Alpha-Ready' modundadır.

02. SİBER KAPASİTE VE ELEKTRONİK HARP (EW):
- Milli Güvenlik Duvarı: 256 katmanlı kuantum-kripto şifreleme.
- Ofansif Siber Güç: Dakikada 10Tbps veri manipülasyon kapasitesi.
- EMP Dayanıklılığı: Tüm askeri donanım Faraday kafesiyle izole edilmiştir.
- Yapay Zeka Komuta Zinciri: Karar alma mekanizması %85 AI desteklidir.
- İstihbarat Ağı: Küresel fiber optik kablo hatlarına fiziksel erişim.
- Uydu Karartma: Alçak yörünge uydularını lazerle etkisiz hale getirme yeteneği.
- Veri Merkezleri: 300 metre yer altında, sismik izolatörlü tesisler.

03. EKONOMİK MANİPÜLASYON VE KAYNAK YÖNETİMİ:
- Stratejik Rezervler: 20 yıllık nadir toprak elementleri stoku.
- Enerji Portföyü: Toryum tabanlı yeni nesil reaktörler operasyoneldir.
- Gıda Güvenliği: Dikey tarım ve genetik tohum bankası tam kapasite çalışmaktadır.
- Finansal Siber Savunma: Swift dışı blokzincir tabanlı ödeme sistemi.
- Dış Ticaret Dengesi: Teknoloji ihracatı, hammadde ithalatını domine etmektedir.
- Milli Para Birimi: %100 dijital ve izlenebilir 'Vortex' altyapısına geçti.

04. GELECEK PROJEKSİYONU (2025-2050):
- 2026: Yapay zeka kontrollü ilk insansız hava tümeni kurulumu.
- 2030: Uzay madenciliği kapsamında asteroid yakalama görevi.
- 2035: İnsan beyni ve makine arayüzü (BCI) ile askeri yönetim.
- 2040: Sınırsız temiz enerji sağlayan füzyon reaktörlerinin yaygınlaşması.
- 2050: Mars kolonisi üzerinde egemenlik iddiası ve askeri üs planı.

KAYIT DURUMU: ANALİZ TAMAMLANDI. BU VERİLER DİNAMİKTİR.
----------------------------------------------------------------------
"""

# Ülke Veri Seti (Genişletilmiş)
country_names = ["TÜRKİYE", "ABD", "RUSYA", "ÇİN", "İNGİLTERE", "FRANSA", "ALMANYA", "JAPONYA", "HİNDİSTAN", "GÜNEY KORE", 
                "İSRAİL", "İRAN", "BREZİLYA", "KANADA", "AVUSTRALYA", "İTALYA", "POLONYA", "MISIR", "AZERBAYCAN", "PAKİSTAN", 
                "NORVEÇ", "İSVEÇ", "KATAR", "SUUDİ ARABİSTAN", "İSPANYA", "HOLLANDA", "İSVİÇRE", "VİETNAM", "ENDONEZYA", 
                "TAYLAND", "MEKSİKA", "ARJANTİN", "YUNANİSTAN", "UKRAYNA", "GÜNEY AFRİKA"]

COUNTRIES_DATA = [{"n": f"{name} STRATEJİK İSTİHBARAT DOSYASI", "info": get_mega_intelligence_report(name)} for name in country_names]

# --- SİBER TERMİNAL ARAYÜZÜ (HTML5/CSS3/JS) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GGİ_COMMAND_CENTER_v12</title>
    <style>
        :root {
            --blue: #00f2ff;
            --green: #39ff14;
            --red: #ff0055;
            --bg: #010203;
            --glass: rgba(10, 25, 45, 0.9);
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        
        body, html { 
            height: 100%; width: 100%; margin: 0; 
            background: var(--bg); color: #fff;
            font-family: 'Courier New', monospace;
            overflow: hidden; /* Scroll sorunu panel içinde çözülecek */
        }

        /* Ana Konteynır */
        .os-wrapper {
            display: flex;
            flex-direction: column;
            height: 100vh;
            width: 100vw;
        }

        /* Header Üst Panel */
        .top-nav {
            height: 55px;
            background: #000;
            border-bottom: 2px solid var(--blue);
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
            box-shadow: 0 0 20px var(--blue);
            z-index: 100;
        }

        /* Grid Sistemi */
        .main-layout {
            flex: 1;
            display: grid;
            grid-template-columns: 360px 1fr 380px;
            gap: 12px;
            padding: 12px;
            overflow: hidden;
        }

        /* Mobilde Grid Değişimi */
        @media (max-width: 1100px) {
            .main-layout {
                grid-template-columns: 1fr;
                grid-template-rows: auto 1fr auto;
                overflow-y: auto;
            }
            body { overflow: auto; }
        }

        /* Panel Tasarımı */
        .terminal-panel {
            background: var(--glass);
            border: 1px solid #1a2a3a;
            display: flex;
            flex-direction: column;
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }

        .panel-header {
            background: #0a111a;
            padding: 12px;
            font-size: 13px;
            color: var(--blue);
            border-bottom: 1px solid #1a2a3a;
            font-weight: bold;
            text-transform: uppercase;
        }

        .panel-scroll {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
            scrollbar-width: thin;
            scrollbar-color: var(--blue) transparent;
        }

        .panel-scroll::-webkit-scrollbar { width: 5px; }
        .panel-scroll::-webkit-scrollbar-thumb { background: var(--blue); }

        /* Ülke Kartları */
        .intel-card {
            background: #050a0f;
            border: 1px solid #112233;
            margin-bottom: 12px;
            padding: 18px;
            cursor: pointer;
            transition: 0.3s;
        }
        .intel-card:hover { 
            border-color: var(--blue); 
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
            background: #0a1b2a;
        }
        
        .intel-content {
            display: none;
            color: var(--green);
            font-size: 12px;
            white-space: pre-wrap;
            margin-top: 15px;
            border-top: 1px dashed #224466;
            padding-top: 12px;
            line-height: 1.6;
        }

        /* Hesap Makinesi (PRO) */
        .calc-ui {
            background: #000;
            border: 1px solid var(--blue);
            padding: 10px;
            border-radius: 4px;
        }
        #calc-display {
            width: 100%;
            background: #050505;
            border: 1px solid var(--blue);
            color: var(--green);
            padding: 15px;
            text-align: right;
            font-size: 24px;
            margin-bottom: 12px;
            box-sizing: border-box;
        }
        .calc-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
        }
        .calc-grid button {
            background: #111;
            border: 1px solid #333;
            color: #fff;
            padding: 18px 0;
            cursor: pointer;
            font-family: 'Courier New';
            transition: 0.2s;
        }
        .calc-grid button:hover { background: var(--blue); color: #000; }

        /* Canlı Loglar */
        .log-entry { font-size: 11px; margin-bottom: 5px; opacity: 0.8; }
        .cursor { display: inline-block; width: 8px; height: 16px; background: var(--green); animation: blink 0.8s infinite; vertical-align: middle; }
        @keyframes blink { 50% { opacity: 0; } }

        /* Tehdit Matrisi */
        .threat-meter {
            height: 10px;
            background: #111;
            border: 1px solid #333;
            margin: 10px 0;
            position: relative;
        }
        .threat-fill { height: 100%; background: var(--red); width: 45%; box-shadow: 0 0 10px var(--red); }

    </style>
</head>
<body>

    <audio id="click-fx" src="https://www.soundjay.com/buttons/button-50.mp3"></audio>

    <div class="os-wrapper">
        <header class="top-nav">
            <div style="font-size: 20px; color: var(--blue); font-weight: bold; letter-spacing: 2px;">GGİ_COMMAND_OS_v12</div>
            <div id="live-clock" style="color: var(--blue); font-size: 16px;">00:00:00</div>
        </header>

        <main class="main-layout">
            <section class="terminal-panel">
                <div class="panel-header">CORE_RESOURCES & TOOLS</div>
                <div class="panel-scroll">
                    <div class="calc-ui">
                        <input type="text" id="calc-display" value="0" readonly>
                        <div class="calc-grid">
                            <button onclick="key('7')">7</button><button onclick="key('8')">8</button><button onclick="key('9')">9</button><button onclick="key('/')">/</button>
                            <button onclick="key('4')">4</button><button onclick="key('5')">5</button><button onclick="key('6')">6</button><button onclick="key('*')">*</button>
                            <button onclick="key('1')">1</button><button onclick="key('2')">2</button><button onclick="key('3')">3</button><button onclick="key('-')">-</button>
                            <button onclick="cls()">C</button><button onclick="key('0')">0</button><button onclick="exe()">=</button><button onclick="key('+')">+</button>
                        </div>
                    </div>

                    <div style="margin-top: 30px;">
                        <p style="color: var(--blue); font-size: 12px;">GLOBAL_THREAT_LEVEL</p>
                        <div class="threat-meter"><div class="threat-fill" id="threat-bar"></div></div>
                        <p id="threat-status" style="color: var(--red); font-size: 11px;">DEFCON 3: ELEVATED RISK</p>
                    </div>

                    <div style="margin-top: 30px;">
                        <p style="color: var(--blue); font-size: 12px; border-bottom: 1px solid #224466;">ACTIVE_OPERATORS</p>
                        {% for u in users %}
                        <div style="display: flex; justify-content: space-between; font-size: 11px; padding: 6px 0;">
                            <span>{{ u.username }}</span>
                            <span style="color: var(--green);">{{ u.score }} PX</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </section>

            <section class="terminal-panel">
                <div class="panel-header">GLOBAL_STRATEGIC_INTELLIGENCE (CLICK_TO_DECRYPT)</div>
                <div class="panel-scroll" id="archive-container">
                    {% for item in data %}
                    <div class="intel-card" onclick="openIntelligence(this, {{loop.index}})">
                        <div style="color: var(--blue); font-size: 15px; font-weight: bold;">[SECURE] {{ item.n }}</div>
                        <div class="intel-content" id="report-{{loop.index}}" data-raw="{{ item.info }}"></div>
                    </div>
                    {% endfor %}
                </div>
            </section>

            <section class="terminal-panel">
                <div class="panel-header">ENCRYPTED_SYSTEM_LOGS</div>
                <div class="panel-scroll" id="log-box" style="background: #000;">
                    <div class="log-entry" style="color: var(--green); font-weight: bold;">> KERNEL_LOAD_SUCCESSFUL...</div>
                    <div class="log-entry" style="color: var(--blue);">> OPERATOR_IP: {{ user_ip }}</div>
                </div>
            </section>
        </main>
    </div>

    <script>
        // Saat Fonksiyonu
        setInterval(() => {
            document.getElementById('live-clock').innerText = new Date().toLocaleTimeString();
        }, 1000);

        // Gelişmiş Hesap Makinesi
        let display = document.getElementById('calc-display');
        function key(v) { if(display.value=='0' || display.value=='ERROR') display.value=v; else display.value+=v; }
        function cls() { display.value='0'; }
        function exe() { try { display.value = eval(display.value); } catch { display.value='ERROR'; } }

        // DAKTİLO VE İSTİHBARAT ÇÖZÜMLEME
        function openIntelligence(card, id) {
            document.getElementById('click-fx').play();
            const content = document.getElementById('report-' + id);
            
            if(content.style.display === 'block') {
                content.style.display = 'none';
                return;
            }

            // Diğer açık olanları kapat (Opsiyonel: ekranı temiz tutar)
            // document.querySelectorAll('.intel-content').forEach(el => el.style.display = 'none');

            content.style.display = 'block';
            
            if(content.innerHTML === "") {
                const rawText = content.getAttribute('data-raw');
                let i = 0;
                content.innerHTML = '<span id="typing-'+id+'"></span><span class="cursor"></span>';
                const target = document.getElementById('typing-'+id);

                function startTyping() {
                    if (i < rawText.length) {
                        target.innerHTML += rawText.charAt(i);
                        i++;
                        // Otomatik kaydır
                        card.parentElement.scrollTop = card.offsetTop - 20;
                        setTimeout(startTyping, 4); // Yüksek hızda akış
                    }
                }
                startTyping();
            }
        }

        // Dinamik Tehdit Seviyesi
        setInterval(() => {
            let val = Math.floor(Math.random() * 40) + 40;
            document.getElementById('threat-bar').style.width = val + "%";
            if(val > 70) {
                document.getElementById('threat-status').innerText = "DEFCON 2: CRITICAL ALERT";
                document.getElementById('threat-status').style.color = "var(--red)";
            } else {
                document.getElementById('threat-status').innerText = "DEFCON 3: ELEVATED RISK";
                document.getElementById('threat-status').style.color = "orange";
            }
        }, 4000);

        // Canlı Log Akışı (Multifont & Random)
        const logMsgs = [
            "> UYDU_VERİ_PAKETİ_ALINDI", "> SİBER_SALDIRI_ENGELLEME_PASİF", "> PROTOKOL_X_YÜKLENİYOR",
            "> VERİ_TABANI_ERİŞİM_İZNİ", "> ŞİFRELEME_ANAHTARI_GÜNCELLENDİ", "> OMEGA_SEKTÖR_İZLENİYOR",
            "> KRİTİK_HATA_0x44_GİDERİLDİ", "> YENİ_BAĞLANTI_İSTEĞİ_ONAYLANDI"
        ];
        const logFonts = ['Courier New', 'monospace', 'Impact', 'Arial', 'Verdana'];

        setInterval(() => {
            const box = document.getElementById('log-box');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.style.fontFamily = logFonts[Math.floor(Math.random()*logFonts.length)];
            entry.style.color = Math.random() > 0.85 ? 'var(--red)' : 'var(--green)';
            entry.innerText = logMsgs[Math.floor(Math.random()*logMsgs.length)] + " [" + Math.random().toString(16).slice(2,6).toUpperCase() + "]";
            box.appendChild(entry);
            box.scrollTop = box.scrollHeight;
            if(box.childNodes.length > 50) box.removeChild(box.firstChild);
        }, 1800);

    </script>
</body>
</html>
"""

# --- ROUTERLAR VE VERİ KONTROLLERİ ---
@app.route('/')
def index():
    db.create_all()
    # Eğer kullanıcı yoksa test operatörleri oluştur
    if not User.query.first():
        o1 = User(username="SUPREME_COMMANDER", score=12500, access_level="ADMİN")
        o2 = User(username="GGI_OPERATOR_01", score=8900, access_level="STAFF")
        db.session.add_all([o1, o2])
        db.session.commit()
        
    u_ip = request.remote_addr
    # Ziyaret kaydı
    try:
        v = SystemVisit(ip_address=u_ip, agent=request.user_agent.string)
        db.session.add(v)
        db.session.commit()
    except:
        db.session.rollback()

    operators = User.query.order_by(User.score.desc()).all()
    return render_template_string(HTML_TEMPLATE, data=COUNTRIES_DATA, users=operators, user_ip=u_ip)

@app.route('/health')
def health():
    return jsonify({"status": "online", "system": "GGI_V12", "load": "stable"})

# --- SİSTEMİ BAŞLAT ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # Port yapılandırması (Render/Heroku uyumlu)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
