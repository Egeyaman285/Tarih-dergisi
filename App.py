import os
import random
import time
from flask import Flask, render_template_string

app = Flask(__name__)

# === ANA MENÜ: 25 ÜLKE (10 SATIR BİLGİ) ===
# Bilgiler tıklanınca açılacak şekilde optimize edildi
MAIN_COUNTRIES = {
    "TÜRKİYE": "🇹🇷 KOZMİK SEVİYE\n▸ İHA/SİHA: Global liderlik.\n▸ HAVA: KAAN 5. Nesil entegrasyonu.\n▸ SİBER: AZRA kuantum işlemci.\n▸ DENİZ: Mavi Vatan doktrini.\n▸ UZAY: Yerli roket motoru testi.\n▸ FÜZE: Tayfun 1000km+ menzil.\n▸ RADAR: EİRS Erken ihbar sistemi.\n▸ TANK: Altay seri üretim fazı.\n▸ YAZILIM: Havelsan ADVENT ağ desteği.\n▸ OPERASYON: Sınır ötesi dijital kalkan.",
    "ABD": "🇺🇸 TOP SECRET\n▸ NÜKLEER: 11 Uçak gemisi grubu.\n▸ SİBER: NSA küresel veri madenciliği.\n▸ UZAY: Starshield askeri ağ.\n▸ EKONOMİ: Rezerv para kontrolü.\n▸ DOKTRİN: Full-spectrum dominance.\n▸ F-35: 500+ operasyonel uçak.\n▸ AI: Pentagon algoritmik savaş.\n▸ ÜSLER: 750+ denizaşırı nokta.\n▸ LAZER: HELIOS gemi savunma.\n▸ DENİZALTI: Columbia sınıfı gizlilik.",
    "RUSYA": "🇷🇺 SIGMA-9\n▸ FÜZE: Zircon hipersonik füze.\n▸ NÜKLEER: En büyük stratejik arsenal.\n▸ ARKTİK: Yeni nesil askeri üsler.\n▸ SİBER: Fancy Bear operasyonları.\n▸ TANK: T-14 Armata otonom mod.\n▸ HAVA: Su-57 Felon operasyonel.\n▸ ELEKTRONİK: Krasukha-4 bastırma.\n▸ DENİZ: Poseidon nükleer torpido.\n▸ İSTİHBARAT: SVR derin hücreler.\n▸ ENERJİ: Gaz sevkiyat silahlandırma.",
    "ÇİN": "🇨🇳 RED-DRAGON\n▸ DONANMA: Tip 004 nükleer gemi.\n▸ TEKNOLOJİ: 6G ve kuantum uydu.\n▸ EKONOMİ: Kuşak Yol inisiyatifi.\n▸ J-20: 5. Nesil geniş filo.\n▸ UZAY: Tiangong istasyon genişlemesi.\n▸ AI: Yüz tanıma & sosyal kredi.\n▸ ÜRETİM: Nadir toprak element tekeli.\n▸ SİBER: Plazma kalkanı projesi.\n▸ FÜZE: DF-41 Kıtalararası menzil.\n▸ ASKERİ: 2 Milyon aktif personel.",
    "AZERBAYCAN": "🇦🇿 KASPIAN-ALPHA\n▸ SAVUNMA: Modern SİHA doktrini.\n▸ ENERJİ: TANAP stratejik hat.\n▸ ASKERİ: Türk ordusu modeli.\n▸ SİBER: Kritik altyapı koruma.\n▸ DOKTRİN: Tek millet, iki devlet.\n▸ FÜZE: LORA ve Polonez sistemleri.\n▸ ÖZEL KUVVET: Yaşma operasyonel gücü.\n▸ İSTİHBARAT: Bölgesel derin gözlem.\n▸ MODERNİZASYON: Su-25ML moderniz.\n▸ DENİZ: Hazar güvenliği kalkanı."
}

# Diğer ülkeleri 25'e tamamlamak için otomatik üretici
others = ["ALMANYA", "İNGİLTERE", "FRANSA", "İSRAİL", "JAPONYA", "G.KORE", "POLONYA", "PAKİSTAN", "İRAN", "MISIR", "BREZİLYA", "İSPANYA", "İTALYA", "YUNANİSTAN", "UKRAYNA", "HİNDİSTAN", "İSVEÇ", "NORVEÇ", "KANADA", "AVUSTRALYA"]
for c in others:
    MAIN_COUNTRIES[c] = f"🌐 STRATEJİK VERİ\n▸ Statü: Aktif\n▸ Tehdit: %{random.randint(10,90)}\n▸ Teknoloji: Üst Düzey\n▸ Savunma: Modernize\n▸ İstihbarat: Tam\n▸ Ekonomi: Stabil\n▸ Siber: Korumalı\n▸ Doktrin: Savunma\n▸ Nükleer: {random.choice(['Var', 'Yok'])}\n▸ Operasyon: Bölgesel"

# === GİZLİ VERİTABANI (78921secretfiles için) ===
SECRET_DB = {}
for name in list(MAIN_COUNTRIES.keys()) + ["KIBRIS", "KATAR", "İSVİÇRE", "BELÇİKA"]: # 100+ ülke için genişletilebilir
    SECRET_DB[name] = [
        f"☢ PROTOKOL: {random.randint(1000,9999)}",
        f"☣ BİYOLOJİK: Seviye 4 Laboratuvar",
        f"🛰 UYDU: Gerçek zamanlı takipte",
        f"💻 SİBER: Arka kapı erişimi açık",
        f"🗝 ANAHTAR: Kuantum şifreli",
        f"🛑 STATÜ: {random.choice(['İMHA EDİLECEK', 'GÖZLEMDE', 'KORUMADA'])}",
        f"🧬 PROJE: Genetik Asker Programı",
        f"🌑 ÜS: Yeraltı Tesisi - Bölge {random.randint(1,50)}",
        f"⚡ ENERJİ: Antimadde Deneyi",
        f"💀 SONUÇ: OMEGA SEVİYE TEHDİT"
    ]

UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>GGI_SUPREME_OS_v3</title>
    <style>
        :root{--b:#00f2ff;--g:#39ff14;--r:#f05;--bg:#010203;--p:rgba(10,25,45,0.98)}
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
        .overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:#000;z-index:9999;display:none;flex-direction:column;padding:40px;overflow-y:auto}
        .nuke-icon{animation:blink 1s infinite; color:var(--r); font-size:30px; display:inline-block}
        @keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
        .secret-country-btn{background:rgba(255,0,85,0.1); border:1px solid var(--r); padding:15px; margin:5px; color:var(--r); cursor:pointer; display:inline-block; transition:0.3s}
        .secret-country-btn:hover{background:var(--r); color:#fff; box-shadow:0 0 20px var(--r)}
        .data-stream{color:var(--g); margin-top:20px; font-size:14px; white-space:pre-wrap; min-height:200px; border-top:1px dashed var(--r); padding-top:20px}
    </style>
</head>
<body>
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
                <div class="card" onclick="toggleMainIntel(this)">
                    <strong>{{ country }}</strong>
                    <div class="intel-box">{{ info }}</div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="panel" id="term-panel">
            <div class="panel-h">COMMAND TERMINAL</div>
            <div class="scroll" id="term-out">Sistem hazır...<br>Komut bekleniyor...</div>
            <div class="cmd-line">
                <span style="color:var(--g)">root@ggi:~$ </span>
                <input type="text" id="term-cmd" autofocus autocomplete="off">
            </div>
        </div>
    </main>

    <div id="scr-secret" class="overlay">
        <h1 style="color:var(--r); text-align:center">GGİ SECRET FİLEST <span class="nuke-icon">☢</span></h1>
        <div style="text-align:center; margin-bottom:20px;">[ ERİŞİM ONAYLANDI - ÜLKE SEÇİN ]</div>
        <div id="secret-btns" style="display:flex; flex-wrap:wrap; justify-content:center">
            {% for country in secret_db.keys() %}
            <div class="secret-country-btn" onclick="loadSecretData('{{ country }}')">{{ country }}</div>
            {% endfor %}
        </div>
        <div id="stream-output" class="data-stream"></div>
        <button onclick="closeSecret()" style="position:fixed; bottom:20px; right:20px; background:red; color:#fff; border:none; padding:15px; cursor:pointer">OTURUMU KAPAT</button>
    </div>

    <script>
        const secretStore = {{ secret_db|tojson }};
        const sndType = document.getElementById('snd-type');
        const sndAlarm = document.getElementById('snd-alarm');

        function toggleMainIntel(el) {
            const box = el.querySelector('.intel-box');
            box.style.display = box.style.display === 'block' ? 'none' : 'block';
            playSound();
        }

        function playSound() {
            let s = sndType.cloneNode();
            s.volume = 0.2;
            s.play();
        }

        function daktilo(text, element) {
            element.innerHTML = "";
            let i = 0;
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    if(text.charAt(i) !== " ") playSound();
                    i++;
                    setTimeout(type, 15);
                }
            }
            type();
        }

        function loadSecretData(country) {
            const output = document.getElementById('stream-output');
            const data = secretStore[country].join('\\n');
            daktilo(`[${country} - KOZMİK ARŞİV VERİSİ]\\n------------------------------\\n` + data, output);
        }

        document.getElementById('term-cmd').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const cmd = this.value.toLowerCase().trim();
                const out = document.getElementById('term-out');
                out.innerHTML += `<div><span style="color:#fff">> ${cmd}</span></div>`;
                
                if (cmd === '78921secretfiles') {
                    sndAlarm.play();
                    document.getElementById('scr-secret').style.display = 'block';
                } else if (cmd === 'clear') {
                    out.innerHTML = "";
                } else if (cmd === 'help') {
                    out.innerHTML += "<div>Komutlar: help, clear, 78921secretfiles, status</div>";
                } else if (cmd === 'status') {
                    out.innerHTML += "<div>SİSTEM DURUMU: NOMİNAL. SİBER KALKAN %100.</div>";
                } else {
                    out.innerHTML += "<div style='color:red'>HATA: Geçersiz yetkilendirme.</div>";
                }
                this.value = '';
                out.scrollTop = out.scrollHeight;
            }
        });

        function closeSecret() {
            document.getElementById('scr-secret').style.display = 'none';
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
    return render_template_string(UI_TEMPLATE, data=MAIN_COUNTRIES, secret_db=SECRET_DB)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
