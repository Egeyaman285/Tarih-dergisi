import os
import datetime
import random
import time
import math
import base64
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# === GENİŞLETİLMİŞ STRATEJİK VERİLER ===
STRATEGIC_INTEL = {
    "TÜRKİYE": "🇹🇷 [KOZMİK]\n▸ Savunma: İHA/SİHA Global Lider.\n▸ Teknoloji: KAAN 5. Nesil Aktif.\n▸ Siber: AZRA Kuantum İşlemci.\n▸ Uzay: Ay Görevi 2026 Faz-1.\n▸ Doktrin: Mavi Vatan 2.0.",
    "ABD": "🇺🇸 [TOP SECRET]\n▸ Güç: 11 Uçak Gemisi Grubu.\n▸ Siber: NSA PRISM Küresel Ağ.\n▸ Uzay: Space Force Starshield.\n▸ Nükleer: Minuteman III Modernize.\n▸ Ekonomi: SWIFT Kontrol Sistemi.",
    "RUSYA": "🇷🇺 [SIGMA-9]\n▸ Füze: Zircon Mach 9 Operasyonel.\n▸ Nükleer: 5977 Stratejik Başlık.\n▸ Arktik: Yeni Nesil Buzkıran Filosu.\n▸ Tank: T-14 Armata Otonom Sistem.\n▸ Doktrin: Gerasimov Hibrit Savaş.",
    "ÇİN": "🇨🇳 [RED-DRAGON]\n▸ Donanma: Tip 004 Nükleer Taşıyıcı.\n▸ Teknoloji: 6G ve Kuantum Uydu.\n▸ Uzay: Tiangong İstasyonu Genişleme.\n▸ Ekonomi: Dijital Yuan Hegemonyası.\n▸ Askeri: 2 Milyon Aktif Personel."
}

# === GİZLİ ÜLKELER VE BAYRAKLAR (100 ÜLKE İÇİN ÖRNEK VERİ SETİ) ===
COUNTRIES_META = [
    ("ALMANYA", "🇩🇪"), ("İNGİLTERE", "🇬🇧"), ("FRANSA", "🇫🇷"), ("İSRAİL", "🇮🇱"), ("JAPONYA", "🇯🇵"),
    ("HİNDİSTAN", "🇮🇳"), ("GÜNEY KORE", "🇰🇷"), ("AZERBAYCAN", "🇦🇿"), ("PAKİSTAN", "🇵🇰"), ("İRAN", "🇮🇷"),
    ("MISIR", "🇪🇬"), ("BREZİLYA", "🇧🇷"), ("KANADA", "🇨🇦"), ("UKRAYNA", "🇺🇦"), ("İSPANYA", "🇪🇸")
]

SECRET_DB = {}
for name, flag in COUNTRIES_META:
    SECRET_DB[name] = {
        "flag": flag,
        "intel": [
            f"Tehdit Seviyesi: %{random.randint(40,99)}",
            f"Gizli Teknoloji: {random.choice(['Kuantum Silahı', 'Plazma Kalkanı', 'Siber Virüs'])}",
            f"Doktrin: {random.choice(['Yıldırım Baskını', 'Asimetrik Felç', 'Tam Blokaj'])}",
            f"İstihbarat Durumu: {random.choice(['Sızıldı', 'Kritik Gözlem', 'Bilinmiyor'])}",
            f"Operasyonel Statü: {random.choice(['Aktif', 'Beklemede', 'Yüksek Alarm'])}"
        ]
    }

# === UI TEMPLATE (TÜM ÖZELLİKLER DAHİL) ===
UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>GGI_OS_v2.1.6</title>
    <style>
        :root{--b:#00f2ff;--g:#39ff14;--r:#f05;--bg:#010203;--p:rgba(10,25,45,0.95)}
        *{box-sizing:border-box;margin:0;padding:0;font-family:'Courier New',monospace}
        body{background:var(--bg);color:#fff;height:100vh;overflow:hidden;font-size:13px}
        
        /* Animasyonlar */
        @keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}}
        @keyframes shake{0%{transform:translate(0)}25%{transform:translate(-2px,2px)}50%{transform:translate(2px,-2px)}100%{transform:translate(0)}}
        .nuke-icon{display:inline-block;animation:blink 1s infinite, shake 0.2s infinite;color:var(--r)}

        header{height:50px;border-bottom:1px solid var(--b);display:flex;align-items:center;justify-content:space-between;padding:0 20px;background:#000;box-shadow:0 0 15px var(--b)}
        main{display:flex;height:calc(100vh - 50px);padding:10px;gap:10px}
        
        .panel{border:1px solid #224466;background:var(--p);display:flex;flex-direction:column;overflow:hidden}
        .panel-h{background:#0a111a;padding:10px;color:var(--b);font-size:12px;border-bottom:1px solid #224466;font-weight:bold}
        .scroll{flex:1;overflow-y:auto;padding:10px;scrollbar-width:thin;scrollbar-color:var(--b) transparent}
        
        .card{background:rgba(0,0,0,0.4);border:1px solid #112233;margin-bottom:8px;padding:12px;cursor:pointer;transition:0.2s}
        .card:hover{border-color:var(--b);box-shadow:inset 0 0 10px var(--b)}
        .intel-box{color:var(--g);font-size:11px;white-space:pre-wrap;margin-top:8px;display:none;line-height:1.5}

        #term-panel{flex:0 0 350px}
        #term-out{font-size:12px;color:var(--g)}
        .cmd-line{display:flex;padding:10px;background:#050a10;border-top:1px solid #224466;align-items:center}
        input{background:transparent;border:none;color:var(--g);flex:1;outline:none;font-size:14px}

        /* Gizli Ekran */
        #secret-screen{position:fixed;top:0;left:0;width:100%;height:100%;background:#000;z-index:9999;display:none;flex-direction:column;padding:30px;overflow-y:auto}
        .secret-header{font-size:24px;color:var(--r);margin-bottom:30px;border-bottom:2px solid var(--r);padding-bottom:10px}
        .secret-item{margin-bottom:25px;border-left:3px solid var(--r);padding-left:15px;opacity:0}
        .typewriter{overflow:hidden;border-right: .15em solid orange;white-space: nowrap;animation: typing 1s steps(40, end), blink-caret .75s step-end infinite;}

        @keyframes typing { from { width: 0 } to { width: 100% } }
    </style>
</head>
<body>
    <audio id="snd-cmd"><source src="https://www.soundjay.com/communication/sounds/typewriter-key-1.mp3" type="audio/mpeg"></audio>
    <audio id="snd-alarm"><source src="https://www.soundjay.com/mechanical/sounds/alarm-clock-01.mp3" type="audio/mpeg"></audio>

    <header>
        <div>GGI_SUPREME_OS v2.1.6</div>
        <div id="clock">00:00:00</div>
    </header>

    <main>
        <div class="panel" style="flex:1">
            <div class="panel-h">STRATEJİK ANALİZ MERKEZİ</div>
            <div class="scroll">
                {% for country, info in data.items() %}
                <div class="card" onclick="toggleIntel(this)">
                    <strong>{{ country }}</strong>
                    <div class="intel-box">{{ info }}</div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="panel" id="term-panel">
            <div class="panel-h">TERMİNAL</div>
            <div class="scroll" id="term-out">Sistem aktif. Giriş bekleniyor...</div>
            <div class="cmd-line">
                <span style="color:var(--g);margin-right:5px">></span>
                <input type="text" id="term-cmd" autofocus autocomplete="off">
            </div>
        </div>
    </main>

    <div id="secret-screen">
        <div class="secret-header">GGİ SECRET FİLEST <span class="nuke-icon">☢</span></div>
        <div id="secret-content"></div>
        <button onclick="closeSecret()" style="background:var(--r);color:#fff;border:none;padding:10px;cursor:pointer;margin-top:20px">SİSTEMDEN ÇIK</button>
    </div>

    <script>
        const secretData = {{ secret_db|tojson }};
        const cmdInput = document.getElementById('term-cmd');
        const termOut = document.getElementById('term-out');
        const sndCmd = document.getElementById('snd-cmd');
        const sndAlarm = document.getElementById('snd-alarm');

        function toggleIntel(el) {
            const box = el.querySelector('.intel-box');
            box.style.display = box.style.display === 'block' ? 'none' : 'block';
            sndCmd.play();
        }

        function typeWriter(text, element, speed = 30) {
            let i = 0;
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                }
            }
            type();
        }

        cmdInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const cmd = this.value.toLowerCase().trim();
                termOut.innerHTML += `<div style="color:#fff">> ${cmd}</div>`;
                sndCmd.play();

                if (cmd === '78921secretfiles') {
                    openSecret();
                } else if (cmd === 'status') {
                    termOut.innerHTML += `<div>Sistem Kararlı. CPU:%12. Bağlantı: Şifreli.</div>`;
                } else if (cmd === 'clear') {
                    termOut.innerHTML = 'Terminal temizlendi.';
                } else {
                    termOut.innerHTML += `<div style="color:var(--r)">Hatalı komut: ${cmd}</div>`;
                }
                
                this.value = '';
                termOut.scrollTop = termOut.scrollHeight;
            }
        });

        function openSecret() {
            sndAlarm.play();
            document.getElementById('secret-screen').style.display = 'flex';
            const container = document.getElementById('secret-content');
            container.innerHTML = '';
            
            Object.entries(secretData).forEach(([country, data], index) => {
                const item = document.createElement('div');
                item.className = 'secret-item';
                item.style.animation = `blink 2s forwards`;
                item.style.opacity = 1;
                
                container.appendChild(item);
                
                const title = `${data.flag} ${country} DOSYASI\\n`;
                const details = data.intel.join('\\n');
                
                typeWriter(title + details, item, 20);
            });
        }

        function closeSecret() {
            document.getElementById('secret-screen').style.display = 'none';
            sndAlarm.pause();
        }

        setInterval(() => {
            document.getElementById('clock').innerText = new Date().toLocaleTimeString();
        }, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(UI_TEMPLATE, data=STRATEGIC_INTEL, secret_db=SECRET_DB)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
