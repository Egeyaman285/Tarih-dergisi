import os
import random
from flask import Flask, render_template_string

app = Flask(__name__)

# === VERİ SETİ ===
MAIN_COUNTRIES = {
    "TÜRKİYE": "🇹🇷 KOZMİK SEVİYE\n▸ İHA/SİHA: Global liderlik.\n▸ HAVA: KAAN 5. Nesil entegrasyonu.\n▸ SİBER: AZRA kuantum işlemci.\n▸ DENİZ: Mavi Vatan doktrini.\n▸ UZAY: Yerli roket motoru testi.\n▸ FÜZE: Tayfun 1000km+ menzil.\n▸ RADAR: EİRS Erken ihbar sistemi.\n▸ TANK: Altay seri üretim fazı.\n▸ YAZILIM: Havelsan ADVENT ağ desteği.\n▸ OPERASYON: Sınır ötesi dijital kalkan.",
    "ABD": "🇺🇸 TOP SECRET\n▸ NÜKLEER: 11 Uçak gemisi grubu.\n▸ SİBER: NSA küresel veri madenciliği.\n▸ UZAY: Starshield askeri ağ.\n▸ EKONOMİ: Rezerv para kontrolü.\n▸ DOKTRİN: Full-spectrum dominance.\n▸ F-35: 500+ operasyonel uçak.\n▸ AI: Pentagon algoritmik savaş.\n▸ ÜSLER: 750+ denizaşırı nokta.\n▸ LAZER: HELIOS gemi savunma.\n▸ DENİZALTI: Columbia sınıfı gizlilik.",
    "RUSYA": "🇷🇺 SIGMA-9\n▸ FÜZE: Zircon hipersonik füze.\n▸ NÜKLEER: En büyük stratejik arsenal.\n▸ ARKTİK: Yeni nesil askeri üsler.\n▸ SİBER: Fancy Bear operasyonları.\n▸ TANK: T-14 Armata otonom mod.\n▸ HAVA: Su-57 Felon operasyonel.\n▸ ELEKTRONİK: Krasukha-4 bastırma.\n▸ DENİZ: Poseidon nükleer torpido.\n▸ İSTİHBARAT: SVR derin hücreler.\n▸ ENERJİ: Gaz sevkiyat silahlandırma.",
    "ÇİN": "🇨🇳 RED-DRAGON\n▸ DONANMA: Tip 004 nükleer gemi.\n▸ TEKNOLOJİ: 6G ve kuantum uydu.\n▸ EKONOMİ: Kuşak Yol inisiyatifi.\n▸ J-20: 5. Nesil geniş filo.\n▸ UZAY: Tiangong istasyon genişlemesi.\n▸ AI: Yüz tanıma & sosyal kredi.\n▸ ÜRETİM: Nadir toprak element tekeli.\n▸ SİBER: Plazma kalkanı projesi.\n▸ FÜZE: DF-41 Kıtalararası menzil.\n▸ ASKERİ: 2 Milyon aktif personel."
}

others = ["ALMANYA", "İNGİLTERE", "FRANSA", "İSRAİL", "JAPONYA", "G.KORE", "POLONYA", "PAKİSTAN", "İRAN", "MISIR", "BREZİLYA", "İSPANYA", "İTALYA", "YUNANİSTAN", "UKRAYNA", "HİNDİSTAN", "İSVEÇ", "NORVEÇ", "KANADA", "AVUSTRALYA", "AZERBAYCAN"]
for c in others:
    if c not in MAIN_COUNTRIES:
        MAIN_COUNTRIES[c] = f"🌐 STRATEJİK VERİ\n▸ Statü: Aktif\n▸ Tehdit: %{random.randint(10,90)}\n▸ Teknoloji: Üst Düzey\n▸ Savunma: Modernize\n▸ İstihbarat: Tam\n▸ Ekonomi: Stabil\n▸ Siber: Korumalı\n▸ Doktrin: Savunma\n▸ Nükleer: {random.choice(['Var', 'Yok'])}\n▸ Operasyon: Bölgesel\n▸ Gözlem: 24/7"

SECRET_DB = {k: [f"☢ PROTOKOL: {random.randint(1000,9999)}", f"☣ BİYOLOJİK: Seviye 4", f"🛰 UYDU: Takipte", f"💻 SİBER: Sızıldı", f"🗝 ANAHTAR: Kuantum", f"🛑 STATÜ: KRİTİK", f"🧬 PROJE: X-Alpha", f"🌑 ÜS: Bölge {random.randint(1,10)}", f"⚡ ENERJİ: Antimadde", f"💀 RİSK: OMEGA"] for k in list(MAIN_COUNTRIES.keys()) + ["KIBRIS", "İSVİÇRE", "KATAR"]}

UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>GGI_OS_v4.5_FINAL</title>
    <style>
        :root{--b:#00f2ff;--g:#39ff14;--r:#f05;--bg:#010203;--p:rgba(10,25,45,0.98)}
        *{box-sizing:border-box;margin:0;padding:0;font-family:'Courier New',monospace}
        body{background:var(--bg);color:#fff;height:100vh;overflow:hidden;font-size:12px}
        
        #login-screen{position:fixed;inset:0;background:#000;z-index:10000;display:flex;flex-direction:column;align-items:center;justify-content:center}
        #pass-input{background:transparent;border:1px solid var(--b);color:var(--b);padding:10px;text-align:center;font-size:20px;outline:none;box-shadow:0 0 10px var(--b)}

        header{height:50px;border-bottom:1px solid var(--b);display:flex;align-items:center;justify-content:space-between;padding:0 20px;background:#000}
        main{display:grid;grid-template-columns: 1fr 350px 300px;height:calc(100vh - 50px);padding:10px;gap:10px}
        
        @media (max-width: 1024px) {
            main { grid-template-columns: 1fr; overflow-y: auto; height: auto; }
            body { overflow-y: auto; }
            #term-panel, #feed-panel { height: 400px; margin-top:10px}
        }

        .panel{border:1px solid #224466;background:var(--p);display:flex;flex-direction:column;overflow:hidden}
        .panel-h{background:#0a111a;padding:10px;color:var(--b);font-size:11px;border-bottom:1px solid #224466;font-weight:bold;text-transform:uppercase}
        .scroll{flex:1;overflow-y:auto;padding:10px;scrollbar-width:thin}
        
        .card{background:rgba(0,0,0,0.4);border:1px solid #112233;margin-bottom:8px;padding:12px;cursor:pointer}
        .card:hover{border-color:var(--b);background:rgba(0,242,255,0.05)}
        .intel-box{color:var(--g);font-size:11px;white-space:pre-wrap;margin-top:8px;display:none;border-left:2px solid var(--g);padding-left:10px}

        #term-out, #feed-out{font-size:11px;color:var(--g);line-height:1.4}
        .cmd-line{display:flex;padding:10px;background:#050a10;border-top:1px solid #224466}
        input{background:transparent;border:none;color:var(--g);flex:1;outline:none}

        .overlay{position:fixed;inset:0;background:#000;z-index:9999;display:none;flex-direction:column;padding:20px;overflow-y:auto}
        .secret-country-btn{border:1px solid var(--r);padding:10px;margin:3px;color:var(--r);cursor:pointer;display:inline-block;font-size:10px;transition:0.3s}
        .secret-country-btn:hover{background:var(--r);color:#fff}
        .nuke-icon{animation:blink 1s infinite; color:var(--r)}
        @keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
    </style>
</head>
<body>
    <audio id="snd-type"><source src="https://www.soundjay.com/communication/sounds/typewriter-key-1.mp3" type="audio/mpeg"></audio>
    <audio id="snd-alarm"><source src="https://www.soundjay.com/mechanical/sounds/alarm-clock-01.mp3" type="audio/mpeg"></audio>
    <audio id="snd-click"><source src="https://www.soundjay.com/buttons/sounds/button-50.mp3" type="audio/mpeg"></audio>

    <div id="login-screen">
        <h2 style="color:var(--r);margin-bottom:20px">GGI SUPREME SECURITY ACCESS</h2>
        <input type="password" id="pass-input" placeholder="78921" maxlength="5" autofocus>
        <p id="login-msg" style="margin-top:15px;color:gray">YETKİLENDİRME BEKLENİYOR...</p>
    </div>

    <header>
        <div style="color:var(--b)">GGI_OS_v4.5 // SECURE_LINE</div>
        <div id="clock">00:00:00</div>
    </header>

    <main>
        <div class="panel">
            <div class="panel-h">STRATEJİK ANALİZ (25 ÜLKE)</div>
            <div class="scroll">
                {% for country, info in data.items() %}
                <div class="card" onclick="runMainDaktilo(this, `{{ info }}`)">
                    <strong>{{ country }}</strong>
                    <div class="intel-box"></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="panel" id="term-panel">
            <div class="panel-h">COMMAND TERMINAL</div>
            <div id="term-out" class="scroll">Sistem Aktif. Komut Bekleniyor...</div>
            <div class="cmd-line">
                <span style="color:var(--g)">root@ggi:~$ </span>
                <input type="text" id="term-cmd" autocomplete="off" placeholder="help...">
            </div>
        </div>

        <div class="panel" id="feed-panel">
            <div class="panel-h">LIVE INTELLIGENCE LOGS</div>
            <div id="feed-out" class="scroll"></div>
        </div>
    </main>

    <div id="scr-secret" class="overlay">
        <h2 style="color:var(--r);text-align:center">KOZMİK GİZLİ ARŞİV <span class="nuke-icon">☢</span></h2>
        <div id="secret-btns" style="margin-top:20px;text-align:center">
            {% for country in secret_db.keys() %}
            <div class="secret-country-btn" onclick="runSecretDaktilo('{{ country }}')">{{ country }}</div>
            {% endfor %}
        </div>
        <div id="stream-output" style="color:var(--g);margin-top:30px;white-space:pre-wrap;padding:20px;border:1px dashed var(--r);min-height:200px"></div>
        <button onclick="closeSecret()" style="margin-top:20px;background:red;color:#fff;border:none;padding:15px;width:100%;cursor:pointer">SİSTEMDEN ÇIK</button>
    </div>

    <script>
        const secretStore = {{ secret_db|tojson }};
        const sndType = document.getElementById('snd-type');
        const sndAlarm = document.getElementById('snd-alarm');
        const sndClick = document.getElementById('snd-click');

        document.getElementById('pass-input').addEventListener('input', function(e) {
            if(this.value === '78921') {
                document.getElementById('login-screen').style.display = 'none';
                startLiveFeed();
            } else if(this.value.length === 5) {
                this.value = "";
                document.getElementById('login-msg').innerText = "HATALI ŞİFRE!";
                document.getElementById('login-msg').style.color = "red";
            }
        });

        function playHarfSesi() {
            let s = sndType.cloneNode();
            s.volume = 0.15;
            s.play();
        }

        function daktiloExecution(text, element, speed = 15) {
            element.innerHTML = "";
            element.style.display = "block";
            let i = 0;
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    if(text.charAt(i) !== " " && text.charAt(i) !== "\\n") {
                        playHarfSesi();
                    }
                    i++;
                    setTimeout(type, speed);
                }
            }
            type();
        }

        function runMainDaktilo(card, info) {
            sndClick.play();
            const box = card.querySelector('.intel-box');
            if(box.style.display === "block") {
                box.style.display = "none";
            } else {
                daktiloExecution(info, box, 12);
            }
        }

        function runSecretDaktilo(country) {
            sndClick.play();
            const output = document.getElementById('stream-output');
            const data = secretStore[country].join('\\n');
            daktiloExecution(`[ERİŞİM ONAYLANDI: ${country}]\\n------------------------------\\n` + data, output, 20);
        }

        document.getElementById('term-cmd').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const cmd = this.value.toLowerCase().trim();
                const out = document.getElementById('term-out');
                out.innerHTML += `<div><span style="color:#fff">> ${cmd}</span></div>`;
                
                if (cmd === '78921secretfiles') {
                    sndAlarm.play();
                    document.getElementById('scr-secret').style.display = 'flex';
                } else if (cmd === 'help') {
                    out.innerHTML += "<div>- help, status, clear, 78921secretfiles, threat_matrix, system_override</div>";
                } else if (cmd === 'clear') { out.innerHTML = ""; }
                else { out.innerHTML += "<div style='color:var(--r)'>GEÇERSİZ YETKİ KODU.</div>"; }
                this.value = "";
                out.scrollTop = out.scrollHeight;
            }
        });

        function closeSecret() {
            document.getElementById('scr-secret').style.display = 'none';
            sndAlarm.pause();
        }

        function startLiveFeed() {
            const feed = document.getElementById('feed-out');
            const logs = ["[SİBER] Kalkan Aktif.", "[UYDU] Takip Başladı.", "[LOG] Şifreler Güncellendi."];
            setInterval(() => {
                const log = logs[Math.floor(Math.random()*logs.length)];
                feed.innerHTML += `<div>> ${log}</div>`;
                feed.scrollTop = feed.scrollHeight;
            }, 5000);
        }

        setInterval(() => { document.getElementById('clock').innerText = new Date().toLocaleTimeString(); }, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(UI_TEMPLATE, data=MAIN_COUNTRIES, secret_db=SECRET_DB)

if __name__ == '__main__':
    # Render ve diğer platformlar için en sağlıklı port ayarı
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
