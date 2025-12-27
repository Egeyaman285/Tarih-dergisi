import os
import random
import time
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# === 25 ÜLKE ANA LİSTE (5 Satır Bilgi) ===
MAIN_COUNTRIES = {
    "TÜRKİYE": "🇹🇷 KOZMİK SEVİYE\n▸ İHA/SİHA: Global liderlik.\n▸ HAVA: KAAN 5. Nesil entegrasyonu.\n▸ SİBER: AZRA kuantum işlemci.\n▸ DENİZ: Mavi Vatan doktrini.\n▸ UZAY: Yerli roket motoru testi.",
    "ABD": "🇺🇸 TOP SECRET\n▸ NÜKLEER: 11 Uçak gemisi grubu.\n▸ SİBER: NSA küresel veri madenciliği.\n▸ UZAY: Starshield askeri ağ.\n▸ EKONOMİ: Rezerv para kontrolü.\n▸ DOKTRİN: Full-spectrum dominance.",
    "RUSYA": "🇷🇺 SIGMA-9\n▸ FÜZE: Zircon hipersonik füze.\n▸ NÜKLEER: En büyük stratejik arsenal.\n▸ ARKTİK: Yeni nesil askeri üsler.\n▸ SİBER: Fancy Bear operasyonları.\n▸ TANK: T-14 Armata otonom mod.",
    "ÇİN": "🇨🇳 RED-DRAGON\n▸ DONANMA: Tip 004 nükleer gemi.\n▸ TEKNOLOJİ: 6G ve kuantum uydu.\n▸ EKONOMİ: Kuşak Yol inisiyatifi.\n▸ J-20: 5. Nesil geniş filo.\n▸ UZAY: Tiangong istasyon genişlemesi.",
    "AZERBAYCAN": "🇦🇿 KASPIAN-ALPHA\n▸ SAVUNMA: Modern SİHA doktrini.\n▸ ENERJİ: TANAP stratejik hat.\n▸ ASKERİ: Türk ordusu modeli entegrasyon.\n▸ SİBER: Kritik altyapı koruma.\n▸ DOKTRİN: Tek millet, iki devlet."
}
# (Not: Diğer 20 ülke verisi SECRET_DB üzerinden veya benzer şekilde genişletilebilir)

# === GİZLİ VERİTABANI (100 ÜLKE) ===
SECRET_DB = {}
EQ_DB = {} # Deprem veritabanı
countries_list = ["ALMANYA", "İNGİLTERE", "FRANSA", "İSRAİL", "JAPONYA", "G.KORE", "POLONYA", "PAKİSTAN", "İRAN", "MISIR", "BREZİLYA", "İSPANYA", "İTALYA", "YUNANİSTAN", "UKRAYNA", "HİNDİSTAN", "İSVEÇ", "NORVEÇ", "KANADA", "AVUSTRALYA"]

for c in countries_list:
    SECRET_DB[c] = {
        "flag": "🌐",
        "intel": [f"Tehdit: %{random.randint(50,99)}", "Teknoloji: Kuantum", "Statü: Aktif", "Birim: Alpha", "Risk: Yüksek"]
    }
    EQ_DB[c] = f"▸ Geçmiş: Mag {random.randint(6,8)}.{random.randint(0,9)}\n▸ Risk: %{random.randint(10,95)}\n▸ Tahmin: 2026-2030 arası kritik sismik aktivite bekleniyor."

# === UI TEMPLATE ===
UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>GGI_OS_v2.5</title>
    <style>
        :root{--b:#00f2ff;--g:#39ff14;--r:#f05;--bg:#010203;--p:rgba(10,25,45,0.95)}
        *{box-sizing:border-box;margin:0;padding:0;font-family:'Courier New',monospace}
        body{background:var(--bg);color:#fff;height:100vh;overflow:hidden;font-size:13px}
        
        header{height:50px;border-bottom:1px solid var(--b);display:flex;align-items:center;justify-content:space-between;padding:0 20px;background:#000;box-shadow:0 0 15px var(--b)}
        main{display:flex;height:calc(100vh - 50px);padding:10px;gap:10px}
        
        .panel{border:1px solid #224466;background:var(--p);display:flex;flex-direction:column;overflow:hidden}
        .panel-h{background:#0a111a;padding:10px;color:var(--b);font-size:12px;border-bottom:1px solid #224466;font-weight:bold}
        .scroll{flex:1;overflow-y:auto;padding:10px}
        
        .card{background:rgba(0,0,0,0.4);border:1px solid #112233;margin-bottom:8px;padding:12px;cursor:pointer;transition:0.2s}
        .card:hover{border-color:var(--b);background:rgba(0, 242, 255, 0.1)}
        .intel-box{color:var(--g);font-size:11px;white-space:pre-wrap;margin-top:8px;display:none;border-left:2px solid var(--g);padding-left:10px}

        #term-panel{flex:0 0 400px}
        #term-out{font-size:12px;color:var(--g);line-height:1.4}
        .cmd-line{display:flex;padding:10px;background:#050a10;border-top:1px solid #224466}
        input{background:transparent;border:none;color:var(--g);flex:1;outline:none;font-size:14px}

        /* Full Screen Overlays */
        .overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:#000;z-index:9999;display:none;flex-direction:column;padding:40px;overflow-y:auto}
        .nuke-icon{animation:blink 1s infinite; color:var(--r); font-size:30px}
        @keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
        .secret-item{margin-bottom:20px; border-left: 2px solid var(--r); padding-left:15px; cursor:pointer}
    </style>
</head>
<body>
    <audio id="snd-tick"><source src="https://www.soundjay.com/buttons/sounds/button-50.mp3" type="audio/mpeg"></audio>
    <audio id="snd-type"><source src="https://www.soundjay.com/communication/sounds/typewriter-key-1.mp3" type="audio/mpeg"></audio>
    <audio id="snd-alarm"><source src="https://www.soundjay.com/mechanical/sounds/alarm-clock-01.mp3" type="audio/mpeg"></audio>

    <header>
        <div style="color:var(--b)">GGI SUPREME OS [CORE_SYSTEM]</div>
        <div id="clock">00:00:00</div>
    </header>

    <main>
        <div class="panel" style="flex:1">
            <div class="panel-h">STRATEJİK ANALİZ (25 ÜLKE)</div>
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
            <div class="panel-h">COMMAND TERMINAL</div>
            <div class="scroll" id="term-out">Sistem hazır...<br>Komut girin (help)</div>
            <div class="cmd-line">
                <span style="color:var(--g)">root@ggi:~$ </span>
                <input type="text" id="term-cmd" autofocus autocomplete="off">
            </div>
        </div>
    </main>

    <div id="scr-secret" class="overlay">
        <h1 style="color:var(--r)">GGİ SECRET FİLEST <span class="nuke-icon">☢</span></h1>
        <div id="secret-list"></div>
        <button onclick="closeAll()" style="margin-top:20px; color:white; background:red; border:none; padding:10px; cursor:pointer">EXIT SYSTEM</button>
    </div>

    <div id="scr-eq" class="overlay" style="background:#001a00; border: 5px solid #00f2ff">
        <h1 style="color:var(--b)">SİSMİK RİSK ANALİZ PANELİ [EQ_FORECAST]</h1>
        <div id="eq-list" style="color:var(--g)"></div>
        <button onclick="closeAll()" style="margin-top:20px; color:white; background:blue; border:none; padding:10px; cursor:pointer">TERMINAL'E DÖN</button>
    </div>

    <script>
        const secretData = {{ secret_db|tojson }};
        const eqData = {{ eq_db|tojson }};
        const sndTick = document.getElementById('snd-tick');
        const sndType = document.getElementById('snd-type');
        const sndAlarm = document.getElementById('snd-alarm');

        function toggleIntel(el) {
            const box = el.querySelector('.intel-box');
            box.style.display = box.style.display === 'block' ? 'none' : 'block';
            sndTick.play();
        }

        function daktilo(text, element, speed=15) {
            let i = 0;
            element.innerHTML = "";
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    // Biribiribi sesi simülasyonu
                    if(text.charAt(i) !== " ") {
                        let s = sndType.cloneNode();
                        s.volume = 0.2;
                        s.play();
                    }
                    i++;
                    setTimeout(type, speed);
                }
            }
            type();
        }

        document.getElementById('term-cmd').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const cmd = this.value.toLowerCase().trim();
                const out = document.getElementById('term-out');
                out.innerHTML += `<div><span style="color:#fff">> ${cmd}</span></div>`;
                
                if (cmd === '78921secretfiles') {
                    showSecret();
                } else if (cmd === 'earthquake_forecast') {
                    showEQ();
                } else if (cmd === 'help') {
                    out.innerHTML += "<div>- help<br>- status<br>- clear<br>- earthquake_forecast<br>- 78921secretfiles</div>";
                } else if (cmd === 'status') {
                    out.innerHTML += "<div style='color:orange'>Sistem Kararlı. Siber kalkan aktif.</div>";
                } else if (cmd === 'clear') {
                    out.innerHTML = "";
                } else {
                    out.innerHTML += "<div style='color:red'>Hata: Erişim Engellendi.</div>";
                }
                
                this.value = '';
                out.scrollTop = out.scrollHeight;
            }
        });

        function showSecret() {
            sndAlarm.play();
            document.getElementById('scr-secret').style.display = 'flex';
            const list = document.getElementById('secret-list');
            list.innerHTML = "";
            Object.entries(secretData).forEach(([country, data]) => {
                const div = document.createElement('div');
                div.className = "secret-item";
                div.onclick = () => { sndTick.play(); alert('Nick!'); };
                list.appendChild(div);
                daktilo(`${data.flag} ${country} DOSYASI\\n` + data.intel.join('\\n'), div);
            });
        }

        function showEQ() {
            document.getElementById('scr-eq').style.display = 'flex';
            const list = document.getElementById('eq-list');
            list.innerHTML = "";
            Object.entries(eqData).forEach(([country, info]) => {
                const div = document.createElement('div');
                div.style.marginBottom = "15px";
                list.appendChild(div);
                daktilo(`[${country} SİSMİK RAPOR]\\n${info}`, div);
            });
        }

        function closeAll() {
            document.querySelectorAll('.overlay').forEach(e => e.style.display='none');
            sndAlarm.pause();
            sndAlarm.currentTime = 0;
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
    return render_template_string(UI_TEMPLATE, data=MAIN_COUNTRIES, secret_db=SECRET_DB, eq_db=EQ_DB)

if __name__ == '__main__':
    # Render için 10000 portu veya os.environ portu
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
