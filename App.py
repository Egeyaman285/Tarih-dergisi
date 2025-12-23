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
app.config['SECRET_KEY'] = 'ggi-ultra-v18-omega-access-999'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ggi_v18_supreme.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- 02. VERİTABANI MODELLERİ ---
class SystemUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    access_level = db.Column(db.String(20), default="LEVEL_A")
    score = db.Column(db.Integer, default=10000)

class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# --- 03. 100 ÜLKE ANALİZİ (DEVSAL VERİ BLOĞU) ---
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

# 100 ÜLKE İÇİN RANDOM EKLEMELER (KODU ŞİŞİRİCİ)
OTHER_COUNTRIES = [
    "JAPONYA", "HİNDİSTAN", "GÜNEY KORE", "İRAN", "PAKİSTAN", "BREZİLYA", "KANADA", "AVUSTRALYA", "İTALYA", "POLONYA",
    "MISIR", "AZERBAYCAN", "KATAR", "UKRAYNA", "YUNANİSTAN", "İSPANYA", "NORVEÇ", "İSVEÇ", "HOLLANDA", "İSVİÇRE",
    "BELÇİKA", "AVUSTURYA", "MEKSİKA", "ARJANTİN", "VİETNAM", "ENDONEZYA", "GÜNEY AFRİKA", "SUUDİ ARABİSTAN", "BAE", "KAZAKİSTAN",
    "ÖZBEKİSTAN", "MACARİSTAN", "ROMANYA", "SIRBİSTAN", "PORTEKİZ", "FİNLANDİYA", "DANİMARKA", "SİNGAPUR", "MALEZYA", "TAYLAND",
    "CEZAYİR", "FAS", "IRAK", "LÜBNAN", "ÜRDÜN", "KUVEYT", "UMMAN", "BAHREYN", "AFGANİSTAN", "GÜRCİSTAN", "ERMENİSTAN", "İZLANDA",
    "YENİ ZELANDA", "KIBRIS", "SUDAN", "ETİYOPYA", "KÜBA", "VENEZUELA", "ŞİLİ", "KOLOMBİYA", "NİJERYA", "KENYA", "LÜKSEMBURG",
    "FİLİPİNLER", "BANGLADEŞ", "TAYVAN", "PERU", "İRLANDA", "ÇEK CUMHURİYETİ", "SLOVAKYA", "SLOVENYA", "MAKEDONYA", "ARNAVUTLUK",
    "BOSNA HERSEK", "HIRVATİSTAN", "ESTONYA", "LETONYA", "LİTVANYA", "BEYAZ RUSYA", "MOLDOVA", "MOĞOLİSTAN", "BOLİVYA", "PARAGUAY",
    "URUGUAY", "PANAMA", "KOSTA RİKA", "VİETNAM", "KAMBOÇYA", "LAOS", "MYANMAR", "SENEGAL", "GANA", "FİLDİŞİ SAHİLİ"
]

for c in OTHER_COUNTRIES:
    if c not in STRATEGIC_INTEL:
        STRATEGIC_INTEL[c] = f"[STATUS: {c}-2025]\n- Stratejik Puan: {random.randint(40, 95)}/100\n- Siber Güvenlik: {random.choice(['Yüksek', 'Kritik', 'Stabil'])}\n- Not: Askeri modernizasyon süreci takip ediliyor."

ALL_DATA = [{"n": f"{k} DOSYASI", "i": v} for k, v in STRATEGIC_INTEL.items()]

# --- 04. SİBER ARAYÜZ (HTML5 / CSS3 / JS) ---
UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GGİ_SUPREME_OS_v18</title>
    <style>
        :root { --b: #00f2ff; --g: #39ff14; --r: #ff0055; --bg: #010203; }
        * { box-sizing: border-box; }
        
        body, html { 
            margin: 0; padding: 0; background: var(--bg); color: #fff; 
            font-family: 'Courier New', monospace; height: 100%; width: 100%;
            overflow: hidden;
        }

        /* Matrix Rain Simülasyonu */
        #matrix { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; opacity: 0.15; }

        .os-wrapper { display: flex; flex-direction: column; height: 100vh; position: relative; z-index: 1; }

        header { 
            height: 65px; border-bottom: 3px solid var(--b); 
            display: flex; align-items: center; justify-content: space-between; 
            padding: 0 30px; background: rgba(0,0,0,0.85); flex-shrink: 0;
            box-shadow: 0 0 25px var(--b);
        }

        main { 
            flex: 1; display: grid; grid-template-columns: 350px 1fr 380px; 
            gap: 12px; padding: 12px; overflow: hidden; 
        }

        @media (max-width: 1200px) {
            main { display: block; overflow-y: auto; }
            .panel { margin-bottom: 20px; height: 500px !important; }
        }

        .panel { 
            background: rgba(10, 25, 45, 0.9); border: 2px solid #1a2a3a; 
            display: flex; flex-direction: column; height: 100%;
            border-radius: 5px; box-shadow: inset 0 0 15px #000;
        }

        .panel-h { 
            background: #0a111a; padding: 15px; color: var(--b); 
            font-size: 14px; font-weight: bold; border-bottom: 2px solid #1a2a3a;
            display: flex; justify-content: space-between;
        }

        /* SCROLL ÇÖZÜMÜ */
        .scroll-area { 
            flex: 1; overflow-y: scroll; padding: 18px; 
            scrollbar-width: thin; scrollbar-color: var(--b) transparent;
        }

        .scroll-area::-webkit-scrollbar { width: 6px; }
        .scroll-area::-webkit-scrollbar-thumb { background: var(--b); border-radius: 10px; }

        .card { 
            background: rgba(5, 10, 15, 0.8); border: 1px solid #112233; 
            margin-bottom: 15px; padding: 18px; cursor: pointer; transition: 0.3s;
            position: relative; overflow: hidden;
        }
        .card:hover { border-color: var(--b); box-shadow: 0 0 20px rgba(0,242,255,0.25); background: #0a1b2a; }
        .card::before { content: ''; position: absolute; left: 0; top: 0; width: 3px; height: 100%; background: var(--b); }

        .intel-box { 
            display: none; color: var(--g); font-size: 13px; 
            white-space: pre-wrap; margin-top: 20px; 
            border-top: 1px dashed #224466; padding-top: 15px;
            animation: fadeIn 0.5s;
        }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* TERMINAL KOMUT SATIRI */
        .term-input-box {
            background: #000; border-top: 2px solid #1a2a3a;
            padding: 10px; display: flex; align-items: center;
        }
        .term-input-box span { color: var(--g); margin-right: 10px; }
        #term-cmd { 
            background: transparent; border: none; color: #fff; width: 100%;
            font-family: 'Courier New'; outline: none; font-size: 14px;
        }

        /* HARDWARE MONITOR */
        .stat-row { margin-bottom: 12px; }
        .stat-label { font-size: 11px; color: var(--b); margin-bottom: 5px; }
        .stat-bar { height: 6px; background: #111; border-radius: 3px; overflow: hidden; border: 1px solid #222; }
        .stat-fill { height: 100%; background: var(--b); width: 0%; transition: 0.5s; }

        .log { font-size: 11px; margin-bottom: 6px; line-height: 1.4; color: var(--g); }
        .log.err { color: var(--r); }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>

    <div class="os-wrapper">
        <header>
            <div style="font-size: 24px; color: var(--b); font-weight: bold; text-shadow: 0 0 10px var(--b);">
                GGİ_DEEP_STATE_OS_v18
            </div>
            <div id="clock" style="color: var(--b); font-size: 18px;">00:00:00</div>
        </header>

        <main>
            <div class="panel">
                <div class="panel-h">SYSTEM_MONITOR <span>[STABLE]</span></div>
                <div class="scroll-area">
                    <div class="stat-row">
                        <div class="stat-label">CPU_USAGE</div>
                        <div class="stat-bar"><div class="stat-fill" id="cpu-bar" style="width: 42%;"></div></div>
                    </div>
                    <div class="stat-row">
                        <div class="stat-label">RAM_CORE_INDEX</div>
                        <div class="stat-bar"><div class="stat-fill" id="ram-bar" style="width: 68%; background: var(--g);"></div></div>
                    </div>
                    <div class="stat-row">
                        <div class="stat-label">ENCRYPTION_LOAD</div>
                        <div class="stat-bar"><div class="stat-fill" id="net-bar" style="width: 25%; background: var(--r);"></div></div>
                    </div>
                    
                    <div style="margin-top: 40px;">
                        <div class="panel-h" style="padding-left:0; border-bottom:1px solid #224466;">ACTIVE_OPERATORS</div>
                        <div id="op-list" style="padding-top:15px; font-size: 12px;">
                            <div style="color: var(--g);">[ADMİN] EGE - ONLINE</div>
                            <div style="color: #666; margin-top:5px;">[AI_AGENT] GEMINI - SYNCING...</div>
                        </div>
                    </div>
                </div>
                <div class="term-input-box">
                    <span>root@ggi_os:~$</span>
                    <input type="text" id="term-cmd" placeholder="Komut yazın (help, scan, clear)...">
                </div>
            </div>

            <div class="panel">
                <div class="panel-h">GLOBAL_STRATEGIC_DATABASE [100_NODES]</div>
                <div class="scroll-area" id="main-scroll">
                    {% for item in data %}
                    <div class="card" onclick="openD(this, {{loop.index}})">
                        <div style="color: var(--b); font-weight: bold; letter-spacing: 1px;">
                            <span style="opacity: 0.5;">#{{loop.index}}</span> [SECURE] {{ item.n }}
                        </div>
                        <div class="intel-box" id="box-{{loop.index}}" data-raw="{{ item.i }}"></div>
                    </div>
                    {% endfor %}
                    <div style="height: 60px;"></div>
                </div>
            </div>

            <div class="panel">
                <div class="panel-h">ENCRYPTED_LOG_STREAM <span>[LIVE]</span></div>
                <div class="scroll-area" id="l-box">
                    <div class="log">> BOOT_SEQUENCE_INITIATED...</div>
                    <div class="log">> LOADING_COUNTRY_DATABASE_100...</div>
                    <div class="log">> SİSTEM_AKTİF. IP: {{ user_ip }}</div>
                </div>
            </div>
        </main>
    </div>

    <script>
        // Matrix Rain
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()*&^";
        const fontSize = 16;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);

        function drawMatrix() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#0F0";
            ctx.font = fontSize + "px arial";
            for (let i = 0; i < drops.length; i++) {
                const text = letters.charAt(Math.floor(Math.random() * letters.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(drawMatrix, 33);

        // Saat
        setInterval(() => { document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }, 1000);

        // Daktilo ve Kaydırma Fix
        function openD(card, id) {
            const box = document.getElementById('box-' + id);
            if(box.style.display === 'block') { box.style.display = 'none'; return; }
            box.style.display = 'block';
            if(box.innerHTML === "") {
                const raw = box.getAttribute('data-raw');
                let i = 0;
                function type() {
                    if (i < raw.length) {
                        box.innerHTML += raw.charAt(i);
                        i++;
                        setTimeout(type, 4);
                    }
                }
                type();
            }
        }

        // Hardware Simülasyonu
        setInterval(() => {
            document.getElementById('cpu-bar').style.width = (Math.random() * 60 + 20) + "%";
            document.getElementById('net-bar').style.width = (Math.random() * 90) + "%";
        }, 3000);

        // Terminal Komutları
        document.getElementById('term-cmd').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const cmd = this.value.toLowerCase();
                const lb = document.getElementById('l-box');
                const line = document.createElement('div');
                line.className = 'log';
                
                if(cmd === 'help') line.innerText = "> Komutlar: scan, clear, hack, status";
                else if(cmd === 'scan') line.innerText = "> Port taraması yapılıyor... Tüm portlar güvenli.";
                else if(cmd === 'clear') { lb.innerHTML = ''; line.innerText = "> Konsol temizlendi."; }
                else if(cmd === 'status') line.innerText = "> GGİ_OS v18: Sistemler %100 kapasite çalışıyor.";
                else line.innerText = "> Geçersiz komut: " + cmd;
                
                lb.appendChild(line);
                this.value = '';
                lb.scrollTop = lb.scrollHeight;
            }
        });

        // Canlı Loglar
        const logs = ["> PAKET_ALINDI", "> SİBER_TEHDİT_ENGELLENDİ", "> UYDU_SENKRON_TAMAM", "> VERİ_TABANI_GÜNCELLENDİ"];
        setInterval(() => {
            const lb = document.getElementById('l-box');
            const l = document.createElement('div');
            l.className = 'log';
            l.innerText = logs[Math.floor(Math.random()*logs.length)] + " [" + Math.random().toString(16).slice(2,8) + "]";
            lb.appendChild(l);
            lb.scrollTop = lb.scrollHeight;
            if(lb.childNodes.length > 50) lb.removeChild(lb.firstChild);
        }, 4000);
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
