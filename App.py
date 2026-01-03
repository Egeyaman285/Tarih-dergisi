import os
import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# === TÜM VERİ SETİ (Orijinal + 5 Satır Ek Bilgi) ===
MAIN_COUNTRIES = {
    "TÜRKİYE": "🇹🇷 KOZMİK SEVİYE\n▸ İHA/SİHA: Global liderlik.\n▸ HAVA: KAAN 5. Nesil entegrasyonu.\n▸ SİBER: AZRA kuantum işlemci.\n▸ DENİZ: Mavi Vatan doktrini.\n▸ UZAY: Yerli roket motoru testi.\n▸ FÜZE: Tayfun 1000km+ menzil.\n▸ RADAR: EİRS Erken ihbar sistemi.\n▸ TANK: Altay seri üretim fazı.\n▸ YAZILIM: Havelsan ADVENT ağ desteği.\n▸ OPERASYON: Sınır ötesi dijital kalkan.\n▸ LOJİSTİK: Akıllı mühimmat ağı.\n▸ ENERJİ: Akkuyu Nükleer tam kapasite.\n▸ İSTİHBARAT: MİT Sinyal istihbaratı.\n▸ SAVUNMA: Çelik Kubbe hava savunma.\n▸ EKONOMİ: Dijital Lira blokzincir.\n▸ DOCTRINE: Network-centric warfare.\n▸ QUANTUM: Yerli atomik saat projesi.\n▸ GLOBAL: TCG Anadolu Amfibi güç.\n▸ AI: Baykar otonom sürü zekası.\n▸ SPACE: Ay misyonu roket motoru.",
    "ABD": "🇺🇸 TOP SECRET\n▸ NÜKLEER: 11 Uçak gemisi grubu.\n▸ SİBER: NSA küresel veri madenciliği.\n▸ UZAY: Starshield askeri ağ.\n▸ EKONOMİ: Rezerv para kontrolü.\n▸ DOKTRİN: Full-spectrum dominance.\n▸ F-35: 500+ operasyonel uçak.\n▸ AI: Pentagon algoritmik savaş.\n▸ ÜSLER: 750+ denizaşırı nokta.\n▸ LAZER: HELIOS gemi savunma.\n▸ DENİZALTI: Columbia sınıfı gizlilik.\n▸ RADAR: B-21 Raider görünmezlik.\n▸ KOMUTA: NORAD derin sığınak.\n▸ SİLAH: Railgun gemi testleri.\n▸ ANALİZ: Palantir yapay zeka.\n▸ FON: Sınırsız savunma bütçesi.\n▸ GLOBAL: Prompt Global Strike.\n▸ TECH: Silicon Valley askeri Ar-Ge.\n▸ INTEL: CIA derin veri analitiği.\n▸ FINANCE: FED dolar hegemonyası.\n▸ SPACE: Space Force orbital savunma.",
    "RUSYA": "🇷🇺 SIGMA-9\n▸ FÜZE: Zircon hipersonik füze.\n▸ NÜKLEER: En büyük stratejik arsenal.\n▸ ARKTİK: Yeni nesil askeri üsler.\n▸ SİBER: Fancy Bear operasyonları.\n▸ TANK: T-14 Armata otonom mod.\n▸ HAVA: Su-57 Felon operasyonel.\n▸ ELEKTRONİK: Krasukha-4 bastırma.\n▸ DENİZ: Poseidon nükleer torpido.\n▸ İSTİHBARAT: SVR derin hücreler.\n▸ ENERJİ: Gaz sevkiyat silahlandırma.\n▸ SİSTEM: S-500 Prometheus aktif.\n▸ UZAY: GLONASS askeri hassasiyet.\n▸ DENİZALTI: Borei sınıfı nükleer.\n▸ RADYO: UVB-76 gizemli sinyal.\n▸ ÖZEL: Wagner hibrit savaş.\n▸ HYPERSONIC: Avangard süzülme aracı.\n▸ UNDERWATER: Yasen-M nükleer bot.\n▸ PROPAGANDA: Küresel dezenformasyon.\n▸ RESOURCES: Sibirya hammadde.\n▸ DEFENSE: A-135 füze kalkanı.",
    "ÇİN": "🇨🇳 RED-DRAGON\n▸ DONANMA: Tip 004 nükleer gemi.\n▸ TEKNOLOJİ: 6G ve kuantum uydu.\n▸ EKONOMİ: Kuşak Yol inisiyatifi.\n▸ J-20: 5. Nesil geniş filo.\n▸ UZAY: Tiangong istasyon genişlemesi.\n▸ AI: Yüz tanıma & sosyal kredi.\n▸ ÜRETİM: Nadir toprak element tekeli.\n▸ SİBER: Plazma kalkanı projesi.\n▸ FÜZE: DF-41 Kıtalararası menzil.\n▸ ASKERİ: 2 Milyon aktif personel.\n▸ ÇİP: Yerli 2nm üretim bandı.\n▸ ROBOTİK: Otonom köpek birlikleri.\n▸ SOSYAL: Dijital gözetim ağı.\n▸ MADEN: Ay üssü inşa planı.\n▸ DENİZ: Yapay ada tahkimatları.\n▸ NAVAL: Güney Çin Denizi kontrolü.\n▸ INFRA: Hızlı tren askeri lojistik.\n▸ CHIPS: SMIC yerli litografi.\n▸ DRONES: Wing Loong sürü saldırı.\n▸ QUANTUM: Jiuzhang hesaplama gücü."
}

others = ["ALMANYA", "İNGİLTERE", "FRANSA", "İSRAİL", "JAPONYA", "G.KORE", "POLONYA", "PAKİSTAN", "İRAN", "MISIR", "BREZİLYA", "İSPANYA", "İTALYA", "YUNANİSTAN", "UKRAYNA", "HİNDİSTAN", "İSVEÇ", "NORVEÇ", "KANADA", "AVUSTRALYA", "AZERBAYCAN"]
for c in others:
    if c not in MAIN_COUNTRIES:
        MAIN_COUNTRIES[c] = f"🌐 STRATEJİK VERİ\n▸ Statü: Aktif\n▸ Tehdit: %{random.randint(10,90)}\n▸ Teknoloji: Üst Düzey\n▸ Savunma: Modernize\n▸ İstihbarat: Tam\n▸ Ekonomi: Stabil\n▸ Siber: Korumalı\n▸ Doktrin: Savunma\n▸ Nükleer: {random.choice(['Var', 'Yok'])}\n▸ Operasyon: Bölgesel\n▸ Gözlem: 24/7\n▸ İletişim: Kriptolu\n▸ Lojistik: Tam Kapasite\n▸ Kaynak: Öz Yeterlilik\n▸ İkmal: Kesintisiz\n▸ Moral: Yüksek"

SECRET_DB = {k: [f"☢ PROTOKOL: {random.randint(1000,9999)}", f"☣ BİYOLOJİK: Seviye 4", f"🛰 UYDU: Takipte", f"💻 SİBER: Sızıldı", f"🗝 ANAHTAR: Kuantum", f"🛑 STATÜ: KRİTİK", f"🧬 PROJE: X-Alpha", f"🌑 ÜS: Bölge {random.randint(1,10)}", f"⚡ ENERJİ: Antimadde", f"💀 RİSK: OMEGA"] for k in list(MAIN_COUNTRIES.keys()) + ["KIBRIS", "İSVİÇRE", "KATAR"]}

def ip_to_alphabet(ip):
    parts = ip.split('.')
    result = []
    for part in parts:
        num = int(part) if part.isdigit() else 0
        if 1 <= num <= 26:
            result.append(chr(64 + num))
        else:
            result.append(chr(65 + (num % 26)))
    return '.'.join(result)

@app.route('/')
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if user_ip and ',' in user_ip:
        user_ip = user_ip.split(',')[0].strip()
    ip_coded = ip_to_alphabet(user_ip)
    return render_template_string(UI_TEMPLATE, data=MAIN_COUNTRIES, secret_db=SECRET_DB, user_ip=user_ip, ip_coded=ip_coded)

UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>GGI_OS_v5.0_ULTRA_EXTENDED</title>
    <style>
        :root{--b:#00f2ff;--g:#39ff14;--r:#f05;--bg:#010203;--p:rgba(10,25,45,0.98)}
        *{box-sizing:border-box;margin:0;padding:0;font-family:'Courier New',monospace}
        body{background:var(--bg);color:#fff;height:100vh;overflow:hidden;font-size:12px}
        
        #cookie-banner{position:fixed;bottom:0;left:0;right:0;background:#000;border-top:2px solid var(--b);padding:15px;z-index:10001;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}
        #cookie-banner button{background:var(--b);color:#000;border:none;padding:10px 20px;cursor:pointer;font-weight:bold;margin:5px}
        
        #ip-display{position:fixed;top:60px;left:10px;background:rgba(0,0,0,0.9);border:1px solid var(--b);padding:10px;font-size:11px;z-index:1000;color:var(--g)}
        
        #login-screen{position:fixed;inset:0;background:#000;z-index:10000;display:flex;flex-direction:column;align-items:center;justify-content:center}
        #pass-input{background:transparent;border:1px solid var(--b);color:var(--b);padding:10px;text-align:center;font-size:20px;outline:none;box-shadow:0 0 10px var(--b)}

        header{height:50px;border-bottom:1px solid var(--b);display:flex;align-items:center;justify-content:space-between;padding:0 20px;background:#000}
        main{display:grid;grid-template-columns:1fr 350px 300px;height:calc(100vh - 50px);padding:10px;gap:10px}
        
        .panel{border:1px solid #224466;background:var(--p);display:flex;flex-direction:column;overflow:hidden}
        .panel-h{background:#0a111a;padding:10px;color:var(--b);font-size:11px;border-bottom:1px solid #224466;font-weight:bold;text-transform:uppercase}
        .scroll{flex:1;overflow-y:auto;padding:10px;scrollbar-width:thin}
        
        .card{background:rgba(0,0,0,0.4);border:1px solid #112233;margin-bottom:8px;padding:12px;cursor:pointer;transition:0.3s}
        .card:hover{border-color:var(--b);background:rgba(0,242,255,0.05)}
        .intel-box{color:var(--g);font-size:11px;white-space:pre-wrap;margin-top:8px;display:none;border-left:2px solid var(--g);padding-left:10px}

        #term-out,#feed-out{font-size:11px;color:var(--g);line-height:1.4}
        .cmd-line{display:flex;padding:10px;background:#050a10;border-top:1px solid #224466}
        input{background:transparent;border:none;color:var(--g);flex:1;outline:none}

        .overlay{position:fixed;inset:0;background:#000;z-index:9999;display:none;flex-direction:column;padding:20px;overflow-y:auto}
        .secret-country-btn{border:1px solid var(--r);padding:10px;margin:3px;color:var(--r);cursor:pointer;display:inline-block;font-size:10px}

        /* NÜKLEER SİMÜLASYON VE HARİTA STİLİ */
        #map-container {
            width: 100%;
            height: 450px;
            background: #050a10;
            position: relative;
            border: 1px solid var(--b);
            overflow: hidden;
            cursor: crosshair;
        }
        #world-svg { width: 100%; height: 100%; fill: #1a2a3a; stroke: var(--b); stroke-width: 0.5; }
        .target-dot{position:absolute;width:12px;height:12px;background:var(--r);border-radius:50%;box-shadow:0 0 15px var(--r);transform:translate(-50%,-50%);animation:blink 0.5s infinite;z-index:10}
        .explosion{position:absolute;border-radius:50%;background:rgba(255,100,0,0.5);border:2px solid orange;transform:translate(-50%,-50%);animation:grow 2.5s forwards;z-index:5}
        @keyframes grow{from{width:0;height:0;opacity:1}to{width:400px;height:400px;opacity:0}}

        #matrix-screen{position:fixed;inset:0;background:#000;z-index:9998;display:none;overflow:hidden}
        .matrix-column{position:absolute;top:-100%;font-size:14px;color:var(--g);text-shadow:0 0 5px var(--g);white-space:pre;line-height:1.2}

        .weapon-btn { background: #112233; border: 1px solid var(--b); color: var(--b); padding: 8px; cursor: pointer; font-size: 11px; margin: 2px; }
        .weapon-btn.active { background: var(--r); color: white; }
        @keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
    </style>
</head>
<body>
    <audio id="snd-click" src="https://www.soundjay.com/buttons/sounds/button-16.mp3"></audio>
    <audio id="snd-nuke" src="https://www.soundjay.com/mechanical/sounds/explosion-01.mp3"></audio>
    <audio id="snd-alarm" src="https://www.soundjay.com/mechanical/sounds/alarm-clock-01.mp3" loop></audio>

    <div id="ip-display">
        <div>📡 IP: {{ user_ip }}</div>
        <div>🔤 KOD: {{ ip_coded }}</div>
    </div>

    <div id="login-screen">
        <h2 style="color:var(--r);margin-bottom:20px">GGI SUPREME SECURITY ACCESS</h2>
        <input type="password" id="pass-input" placeholder="78921" maxlength="5" autofocus>
    </div>

    <header>
        <div style="color:var(--b)">GGI_OS_v5.0 // ULTRA_SECURE</div>
        <div id="clock">00:00:00</div>
    </header>

    <main>
        <div class="panel">
            <div class="panel-h">STRATEJİK ANALİZ (KÜRESEL)</div>
            <div class="scroll">
                {% for country,info in data.items() %}
                <div class="card" onclick="playSound('snd-click');runMainDaktilo(this,`{{info}}`)">
                    <strong>{{country}}</strong>
                    <div class="intel-box"></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="panel" id="term-panel">
            <div class="panel-h">COMMAND TERMINAL</div>
            <div id="term-out" class="scroll">Sistem Aktif. 'help' yazın.</div>
            <div class="cmd-line">
                <span style="color:var(--g)">root@ggi:~$ </span>
                <input type="text" id="term-cmd" autocomplete="off" placeholder="...">
            </div>
        </div>

        <div class="panel" id="feed-panel">
            <div class="panel-h">LIVE INTELLIGENCE</div>
            <div id="feed-out" class="scroll"></div>
        </div>
    </main>

    <div id="scr-nuke" class="overlay">
        <h2 style="color:var(--r);text-align:center">NUCLEAR STRIKE COMMAND v2.0</h2>
        <div style="text-align:center; margin:10px;">
            <button class="weapon-btn active" onclick="setWeapon('Nuke', this)">☢ ATOM BOMBASI</button>
            <button class="weapon-btn" onclick="setWeapon('AirStrike', this)">✈ UÇAK FİLOSU</button>
            <button class="weapon-btn" onclick="setWeapon('Drone', this)">🛸 İHA SALDIRISI</button>
        </div>

        <div id="map-container" onclick="setTarget(event)">
            <svg id="world-svg" viewBox="0 0 1000 500">
                <path d="M150,150 L250,150 L300,100 L400,120 L500,100 L650,120 L800,150 L900,200 L850,350 L700,450 L500,400 L300,450 L100,350 Z" />
                <circle cx="530" cy="180" r="10" fill="red" /> <text x="510" y="165" fill="white" font-size="12">AVRASYA</text>
                <text x="200" y="250" fill="white" font-size="12">AMERİKA</text>
                <text x="800" y="250" fill="white" font-size="12">ASYA</text>
            </svg>
        </div>

        <div style="margin-top:15px;display:grid;grid-template-columns:1fr 1fr;gap:15px">
            <div class="panel" style="height:150px">
                <div class="panel-h">HEDEFLER</div>
                <div class="scroll" style="font-size:10px;color:orange">
                    * TÜRKİYE: Ankara HQ<br>
                    * ABD: NORAD<br>
                    * RUSYA: Yamantau<br>
                    * ÇİN: Hainan
                </div>
            </div>
            <div class="panel" style="height:150px">
                <div class="panel-h">DURUM</div>
                <div class="scroll" id="nuke-damage" style="color:var(--r)"></div>
            </div>
        </div>
        <button id="launch-btn" onclick="launchNuke()" style="background:var(--r);color:#fff;border:none;padding:15px;margin-top:10px;cursor:pointer;font-weight:bold">ATEŞLE</button>
        <button onclick="closeNuke()" style="background:#333;color:#fff;border:none;padding:10px;margin-top:10px;cursor:pointer">KAPAT</button>
    </div>

    <div id="scr-secret" class="overlay">
        <h2 style="color:var(--r);text-align:center">KOZMİK ARŞİV</h2>
        <div id="secret-btns" style="text-align:center">
            {% for country in secret_db.keys() %}
            <div class="secret-country-btn" onclick="runSecretDaktilo('{{country}}')">{{country}}</div>
            {% endfor %}
        </div>
        <div id="stream-output" style="color:var(--g);margin-top:20px;white-space:pre-wrap;padding:10px;border:1px dashed var(--r);min-height:200px"></div>
        <button onclick="closeSecret()" style="background:red;color:#fff;border:none;padding:15px;width:100%;cursor:pointer">ÇIKIŞ</button>
    </div>

    <div id="matrix-screen"></div>

    <script>
        const secretStore={{secret_db|tojson}};
        let currentTarget = null;
        let selectedWeapon = 'Nuke';

        function playSound(id){
            const s = document.getElementById(id);
            if(s) { s.currentTime = 0; s.play().catch(e=>{}); }
        }

        function setWeapon(type, btn) {
            selectedWeapon = type;
            document.querySelectorAll('.weapon-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            playSound('snd-click');
        }

        function setTarget(e){
            const map = document.getElementById('map-container');
            const rect = map.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            document.querySelectorAll('.target-dot').forEach(d=>d.remove());
            const dot = document.createElement('div');
            dot.className = 'target-dot';
            dot.style.left = x + 'px';
            dot.style.top = y + 'px';
            map.appendChild(dot);
            currentTarget = {x, y};
            playSound('snd-click');
        }

        function launchNuke(){
            if(!currentTarget) return alert("HEDEF SEÇİN!");
            playSound('snd-nuke');
            playSound('snd-alarm');
            
            const map = document.getElementById('map-container');
            const exp = document.createElement('div');
            exp.className = 'explosion';
            exp.style.left = currentTarget.x + 'px';
            exp.style.top = currentTarget.y + 'px';
            map.appendChild(exp);

            const dmg = document.getElementById('nuke-damage');
            dmg.innerHTML += `<div>[${selectedWeapon.toUpperCase()}] HEDEF VURULDU.</div>`;
            dmg.scrollTop = dmg.scrollHeight;
            setTimeout(()=> { document.getElementById('snd-alarm').pause(); }, 3000);
        }

        function closeNuke(){ document.getElementById('scr-nuke').style.display='none'; }

        document.getElementById('pass-input').addEventListener('input',function(e){
            if(this.value==='78921') document.getElementById('login-screen').style.display='none';
        });

        function daktiloExecution(text,element,speed=15){
            element.innerHTML=""; element.style.display="block";
            let i=0;
            function type(){
                if(i<text.length){ element.innerHTML+=text.charAt(i); i++; setTimeout(type,speed); }
            }
            type();
        }

        function runMainDaktilo(card,info){
            const box=card.querySelector('.intel-box');
            if(box.style.display==="block") box.style.display="none";
            else daktiloExecution(info,box,12);
        }

        function runSecretDaktilo(country){
            const output=document.getElementById('stream-output');
            daktiloExecution(`[ERİŞİM: ${country}]\\n━━━━━━━━━━━━━━━━\\n`+secretStore[country].join('\\n'),output,20);
        }

        function showMatrixScreen(data){
            const screen=document.getElementById('matrix-screen');
            screen.style.display='block'; screen.innerHTML='';
            for(let i=0;i<50;i++){
                const col=document.createElement('div');
                col.className='matrix-column';
                col.style.left=Math.random()*100+'%';
                col.style.animationDuration=(Math.random()*5+3)+'s';
                col.innerText=data[Math.floor(Math.random()*data.length)];
                screen.appendChild(col);
                setTimeout(()=>{ col.style.top='100%'; col.style.transition='top 8s linear'; },100);
            }
            setTimeout(()=>{screen.style.display='none';},8000);
        }

        const CMD_RESPONSES={
            'matrix_flow':()=>showMatrixScreen(['☢ FÜZE KODLARI','SİBER SALDIRI','ERİŞİM ONAYLANDI']),
            'bombsimulation':()=>{ document.getElementById('scr-nuke').style.display='flex'; }
        };

        document.getElementById('term-cmd').addEventListener('keypress',function(e){
            if(e.key==='Enter'){
                const cmd=this.value.toLowerCase().trim();
                const out=document.getElementById('term-out');
                out.innerHTML+=`<div><span style="color:#fff">> ${cmd}</span></div>`;
                if(cmd==='78921secretfiles') document.getElementById('scr-secret').style.display='flex';
                else if(cmd==='help') out.innerHTML+="<div>help, status, matrix_flow, bombsimulation, 78921secretfiles</div>";
                else if(CMD_RESPONSES[cmd]) CMD_RESPONSES[cmd]();
                this.value=""; out.scrollTop=out.scrollHeight;
            }
        });

        function closeSecret(){ document.getElementById('scr-secret').style.display='none'; }
        setInterval(()=>{document.getElementById('clock').innerText=new Date().toLocaleTimeString()},1000);
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
