import os
import datetime
import random
import time
import base64
from flask import Flask, render_template_string, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# --- 01. SİSTEM YAPILANDIRMASI ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ggi-ultra-v18-fixed-scroll'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ggi_v18_final.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- 02. VERİTABANI MODELLERİ (SATIR ARTIRICI YAPI) ---
class SystemUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    access_level = db.Column(db.String(20), default="LEVEL_A")
    score = db.Column(db.Integer, default=10000)
    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200))
    ip_addr = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# --- 03. 100 ÜLKE ANALİZİ (MEGA VERİ SETİ) ---
STRATEGIC_INTEL = {
    "TÜRKİYE": "[KOZMİK SEVİYE]\nANALİZ: Bölgesel Güç Projeksiyonu.\n- İHA/SİHA: Dünya lideri otonom sistemler.\n- HAVA SAVUNMA: Çelik Kubbe (SİPER-2, HİSAR-U).\n- DENİZ: TCG Anadolu ve TF-2000 projesi.\n- SİBER: Milli Muharip İşlemci ve Kuantum Kripto.\n- UZAY: Yerli roket motoru ve ay görevi faz-1.",
    "ABD": "[TOP SECRET]\nANALİZ: Küresel Dominans.\n- NÜKLEER: 11 Uçak gemisi, Trident-II füzeleri.\n- SİBER: NSA küresel dinleme ve sıfır-gün açıkları.\n- EKONOMİ: Rezerv para birimi manipülasyonu.\n- TEKNOLOJİ: Starlink v3 ve Mars kolonizasyon hazırlığı.",
    "RUSYA": "[SIGMA-9]\nANALİZ: Stratejik Caydırıcılık.\n- FÜZE: Zircon (Mach 9), Avangard.\n- ENERJİ: Gazprom üzerinden jeopolitik baskı.\n- SİBER: GRU siber harp ve dezenformasyon ağları.\n- ARKTİK: Buzkıran filosu ve Kuzey Deniz yolu kontrolü.",
    "ÇİN": "[RED-DRAGON]\nANALİZ: Ekonomik Hegemonya.\n- ÜRETİM: Dünyanın sanayi motoru.\n- TEKNOLOJİ: 6G ve Kuantum haberleşme uyduları.\n- DONANMA: Tip 004 nükleer uçak gemisi projesi.\n- SOSYAL: Yapay zeka destekli gözetim toplumu.",
    "İNGİLTERE": "[MI6-ALPHA]\nANALİZ: Finansal İstihbarat.\n- SİBER: GCHQ veri toplama merkezleri.\n- DONANMA: Astute sınıfı nükleer denizaltılar.\n- DİPLOMASİ: Commonwealth üzerinden yumuşak güç.",
    "ALMANYA": "[BND-SECURE]\nANALİZ: Endüstriyel Savunma.\n- TANK: Panther KF51 ve Leopard 2A8.\n- SİBER: Endüstri 4.0 güvenlik protokolleri.\n- EKONOMİ: AB'nin lokomotif gücü.",
    "FRANSA": "[DGSE-X]\nANALİZ: Nükleer Bağımsızlık.\n- HAVA: Rafale F5 ve nEUROn SİHA.\n- NÜKLEER: M51 balistik füzeleri.\n- UZAY: Ariane 6 roket sistemleri.",
    "İSRAİL": "[MOSSAD-GOLD]\nANALİZ: Tekno-Askeri Üstünlük.\n- SAVUNMA: Demir Işın (Lazer savunma).\n- SİBER: Unit 8200 ve Pegasus II sistemleri.\n- İSTİHBARAT: Küresel HUMINT ve sızma kabiliyeti."
}

# Kodun satır sayısını ve çeşitliliğini artırmak için diğer ülkeler (100'e tamamlanır)
OTHER_COUNTRIES = ["JAPONYA", "HİNDİSTAN", "GÜNEY KORE", "İRAN", "PAKİSTAN", "BREZİLYA", "KANADA", "AVUSTRALYA", "İTALYA", "POLONYA", "MISIR", "AZERBAYCAN", "KATAR", "UKRAYNA", "YUNANİSTAN", "İSPANYA", "NORVEÇ", "İSVEÇ", "HOLLANDA", "İSVİÇRE", "BELÇİKA", "AVUSTURYA", "MEKSİKA", "ARJANTİN", "VİETNAM", "ENDONEZYA", "GÜNEY AFRİKA", "SUUDİ ARABİSTAN", "BAE", "KAZAKİSTAN", "ÖZBEKİSTAN", "MACARİSTAN", "ROMANYA", "SIRBİSTAN", "PORTEKİZ", "FİNLANDİYA", "DANİMARKA", "SİNGAPUR", "MALEZYA", "TAYLAND", "CEZAYİR", "FAS", "IRAK", "LÜBNAN", "ÜRDÜN", "KUVEYT", "UMMAN", "BAHREYN", "AFGANİSTAN", "GÜRCİSTAN", "ERMENİSTAN", "İZLANDA", "YENİ ZELANDA", "KIBRIS", "SUDAN", "ETİYOPYA", "KÜBA", "VENEZUELA", "ŞİLİ", "KOLOMBİYA", "NİJERYA", "KENYA", "LÜKSEMBURG", "FİLİPİNLER", "BANGLADEŞ", "TAYVAN", "PERU", "İRLANDA", "ÇEK CUMHURİYETİ", "SLOVAKYA", "SLOVENYA", "MAKEDONYA", "ARNAVUTLUK", "BOSNA HERSEK", "HIRVATİSTAN", "ESTONYA", "LETONYA", "LİTVANYA", "BEYAZ RUSYA", "MOLDOVA", "MOĞOLİSTAN", "BOLİVYA", "PARAGUAY", "URUGUAY", "PANAMA", "KOSTA RİKA", "VİETNAM", "KAMBOÇYA", "LAOS", "MYANMAR", "SENEGAL", "GANA", "FİLDİŞİ SAHİLİ"]

for c in OTHER_COUNTRIES:
    if c not in STRATEGIC_INTEL:
        STRATEGIC_INTEL[c] = f"[DOSYA KODU: {c[:3]}-2025]\n- Stratejik Puan: {random.randint(40, 95)}/100\n- Siber Güvenlik Seviyesi: {random.choice(['ALPHA', 'BETA', 'GAMMA'])}\n- Analiz: Bölgesel veri paketleri inceleniyor. Kritik altyapı takibi aktif."

ALL_DATA = [{"n": f"{k} STRATEJİK ANALİZİ", "i": v} for k, v in STRATEGIC_INTEL.items()]

# --- 04. SİBER ARAYÜZ (HTML/CSS/JS) ---
UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GGİ_SUPREME_OS_v18_FIXED</title>
    <style>
        :root { --b: #00f2ff; --g: #39ff14; --r: #ff0055; --bg: #010203; --p: rgba(10, 25, 45, 0.9); }
        * { box-sizing: border-box; }
        
        body, html { 
            margin: 0; padding: 0; background: var(--bg); color: #fff; 
            font-family: 'Courier New', monospace; height: 100vh; width: 100vw;
            overflow: hidden; /* Ana scrollu kapatıyoruz ki iç paneller kaysın */
        }

        #matrix { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; opacity: 0.15; }

        .os-wrapper { 
            display: flex; flex-direction: column; height: 100vh; width: 100vw;
        }

        header { 
            height: 60px; border-bottom: 2px solid var(--b); 
            display: flex; align-items: center; justify-content: space-between; 
            padding: 0 20px; background: #000; flex-shrink: 0;
            box-shadow: 0 0 20px var(--b); z-index: 10;
        }

        main { 
            flex: 1; /* Kalan alanı kapla */
            display: grid; grid-template-columns: 320px 1fr 350px; 
            gap: 10px; padding: 10px; 
            min-height: 0; /* Flexbox içinde scroll için kritik */
        }

        @media (max-width: 1100px) {
            main { display: block; overflow-y: auto; }
            .panel { height: 600px !important; margin-bottom: 20px; }
        }

        .panel { 
            background: var(--p); border: 1px solid #1a2a3a; 
            display: flex; flex-direction: column; 
            height: 100%; /* Parent'ın (main) boyuna eşitlen */
            min-height: 0; /* İçerik taşmasını engelle */
            border-radius: 4px;
        }

        .panel-h { 
            background: #0a111a; padding: 12px; color: var(--b); 
            font-size: 13px; font-weight: bold; border-bottom: 1px solid #1a2a3a;
            flex-shrink: 0;
        }

        /* KAYDIRMA ÇÖZÜMÜ: Burası artık kesinlikle çalışacak */
        .scroll-area { 
            flex: 1; 
            overflow-y: auto; /* Kaydırmayı aktifleştir */
            padding: 15px; 
            position: relative;
            scrollbar-width: thin; scrollbar-color: var(--b) transparent;
        }

        .scroll-area::-webkit-scrollbar { width: 4px; }
        .scroll-area::-webkit-scrollbar-thumb { background: var(--b); }

        .card { 
            background: rgba(5, 10, 15, 0.8); border: 1px solid #112233; 
            margin-bottom: 12px; padding: 15px; cursor: pointer; transition: 0.2s;
        }
        .card:hover { border-color: var(--b); background: #0a1b2a; }

        .intel-box { 
            display: none; color: var(--g); font-size: 12px; 
            white-space: pre-wrap; margin-top: 15px; 
            border-top: 1px dashed #224466; padding-top: 10px;
        }

        /* Stats & Tools */
        .stat-row { margin-bottom: 15px; }
        .stat-bar { height: 4px; background: #111; border: 1px solid #222; margin-top: 5px; }
        .stat-fill { height: 100%; background: var(--b); width: 50%; transition: 1s; }
        
        .term-input-box {
            background: #000; border-top: 1px solid #1a2a3a;
            padding: 8px; display: flex; align-items: center; flex-shrink: 0;
        }
        #term-cmd { 
            background: transparent; border: none; color: #fff; width: 100%;
            font-family: 'Courier New'; outline: none; margin-left: 5px;
        }

        .log { font-size: 10px; margin-bottom: 5px; color: var(--g); border-left: 2px solid var(--g); padding-left: 5px; }
        .cursor { animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="os-wrapper">
        <header>
            <div style="font-size: 20px; color: var(--b); font-weight: bold;">GGİ_SUPREME_v18_CORE</div>
            <div id="clock" style="color: var(--b);">00:00:00</div>
        </header>

        <main>
            <div class="panel">
                <div class="panel-h">SYSTEM_RESOURCES</div>
                <div class="scroll-area">
                    <div class="stat-row">
                        <div style="font-size:10px;">CPU_FREQUENCY</div>
                        <div class="stat-bar"><div class="stat-fill" id="cpu-fill"></div></div>
                    </div>
                    <div class="stat-row">
                        <div style="font-size:10px;">UPLINK_STABILITY</div>
                        <div class="stat-bar"><div class="stat-fill" style="width:85%; background:var(--g);"></div></div>
                    </div>
                    <div style="margin-top:20px; font-size:11px; color:var(--b);">ACTIVE_SESSIONS:</div>
                    <div style="font-size:10px; color:var(--g); margin-top:5px;">> ADMİN_EGE (UID: 001)</div>
                    <div style="font-size:10px; color:#444;">> GUEST_SESSION (BLOCKED)</div>
                </div>
                <div class="term-input-box">
                    <span style="color:var(--g);">#</span>
                    <input type="text" id="term-cmd" placeholder="cmd...">
                </div>
            </div>

            <div class="panel">
                <div class="panel-h">GLOBAL_INTEL_ARCHIVE [100_UNITS]</div>
                <div class="scroll-area" id="main-scroll-box">
                    {% for item in data %}
                    <div class="card" onclick="openD(this, {{loop.index}})">
                        <div style="color: var(--b); font-weight: bold; font-size:12px;">[DECRYPTED] {{ item.n }}</div>
                        <div class="intel-box" id="box-{{loop.index}}" data-raw="{{ item.i }}"></div>
                    </div>
                    {% endfor %}
                    <div style="height: 40px;"></div> </div>
            </div>

            <div class="panel">
                <div class="panel-h">LIVE_LOG_STREAM</div>
                <div class="scroll-area" id="log-container">
                    <div class="log">> OS_KERNEL_READY</div>
                    <div class="log">> SQLITE_DB_CONNECTED</div>
                    <div class="log">> HANDSHAKE_IP: {{ user_ip }}</div>
                </div>
            </div>
        </main>
    </div>

    <script>
        // Matrix Background
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const letters = "01010101010101010101010101010101";
        const fontSize = 14; const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);
        function drawMatrix() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.05)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#0F0"; ctx.font = fontSize + "px monospace";
            for (let i = 0; i < drops.length; i++) {
                const text = letters.charAt(Math.floor(Math.random() * letters.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(drawMatrix, 35);

        // Clock
        setInterval(() => { document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }, 1000);

        // Data Opener (Typewriter)
        function openD(card, id) {
            const box = document.getElementById('box-' + id);
            if(box.style.display === 'block') { box.style.display = 'none'; return; }
            box.style.display = 'block';
            if(box.innerHTML === "") {
                const raw = box.getAttribute('data-raw');
                let i = 0;
                function type() {
                    if (i < raw.length) {
                        box.innerHTML += raw.charAt(i); i++;
                        setTimeout(type, 3);
                    }
                }
                type();
            }
        }

        // Stats Simulation
        setInterval(() => {
            document.getElementById('cpu-fill').style.width = Math.floor(Math.random() * 70 + 10) + "%";
        }, 2000);

        // Auto-scroll logs
        function addLog(msg) {
            const container = document.getElementById('log-container');
            const div = document.createElement('div');
            div.className = 'log';
            div.innerText = "> " + msg + " [" + Math.random().toString(16).slice(2,6).toUpperCase() + "]";
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
            if(container.childNodes.length > 40) container.removeChild(container.firstChild);
        }
        setInterval(() => addLog("SIGNAL_SYNC"), 5000);
    </script>
</body>
</html>
"""

# --- 05. ROUTER VE ÇALIŞTIRICI ---
@app.route('/')
def index():
    with app.app_context():
        db.create_all()
        if not SystemUser.query.filter_by(username="ADMİN_EGE").first():
            db.session.add(SystemUser(
                username="ADMİN_EGE", 
                password=generate_password_hash("supreme2025"),
                score=99999
            ))
            db.session.commit()
    return render_template_string(UI_TEMPLATE, data=ALL_DATA, user_ip=request.remote_addr)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
