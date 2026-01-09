import os
import random
import json
from flask import Flask, render_template_string, request, jsonify
import math

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

# === GENİŞLETİLMİŞ VERİ TABANI ===
EXPANDED_DB = {
    "ANIMATION_SEQUENCES": {
        "quantum": ["QUANTUM ENTANGLEMENT", "SUPERPOSITION STATE", "WAVE FUNCTION COLLAPSE", "QUBIT MANIPULATION", "QUANTUM TUNNELING"],
        "cyber": ["NETWORK INFILTRATION", "FIREWALL BREACH", "DATA EXFILTRATION", "ZERO-DAY EXPLOIT", "BACKDOOR INSTALL"],
        "nuclear": ["FISSION INITIATED", "CHAIN REACTION", "CRITICAL MASS", "THERMONUCLEAR FUSION", "MUSHROOM CLOUD"],
        "space": ["SATELLITE DEPLOYMENT", "ORBITAL INSERTION", "SPACE DOMINANCE", "ANTI-SAT WEAPON", "GRAVITY MANIPULATION"]
    }
}

# === NÜKLEER BOMBA VERİ TABANI ===
NUCLEAR_TARGETS = {
    "ABD": {"lat": 39.8283, "lon": -98.5795, "priority": ["WASHINGTON DC", "NEW YORK", "LOS ANGELES", "CHICAGO"]},
    "RUSYA": {"lat": 61.5240, "lon": 105.3188, "priority": ["MOSKOVA", "ST. PETERSBURG", "NOVOSIBIRSK", "EKATERINBURG"]},
    "ÇİN": {"lat": 35.8617, "lon": 104.1954, "priority": ["PEKİN", "ŞANGAY", "GUANGZHOU", "SHENZHEN"]},
    "TÜRKİYE": {"lat": 39.9334, "lon": 32.8597, "priority": ["ANKARA", "İSTANBUL", "İZMİR", "ADANA"]},
    "ALMANYA": {"lat": 51.1657, "lon": 10.4515, "priority": ["BERLİN", "MUNİH", "FRANKFURT", "HAMBURG"]},
    "FRANSA": {"lat": 46.6034, "lon": 1.8883, "priority": ["PARİS", "MARSEILLE", "LYON", "TOULOUSE"]},
    "İNGİLTERE": {"lat": 55.3781, "lon": -3.4360, "priority": ["LONDRA", "BİRMİNGHAM", "MANCHESTER", "GLASGOW"]},
    "JAPONYA": {"lat": 36.2048, "lon": 138.2529, "priority": ["TOKYO", "OSAKA", "KYOTO", "NAGOYA"]}
}

def calculate_nuclear_impact(yield_kt, distance_km, population_density):
    """Nükleer bomba etkisini hesapla"""
    blast_radius = math.sqrt(yield_kt) * 2
    thermal_radius = math.sqrt(yield_kt) * 5
    radiation_radius = math.sqrt(yield_kt) * 3
    
    if distance_km <= blast_radius:
        damage_level = "TAM YOK OLUŞ"
        casualties = population_density * 0.95
    elif distance_km <= thermal_radius:
        damage_level = "AĞIR HASAR"
        casualties = population_density * 0.70
    elif distance_km <= radiation_radius:
        damage_level = "ORTA HASAR"
        casualties = population_density * 0.40
    else:
        damage_level = "HAFİF HASAR"
        casualties = population_density * 0.10
    
    return {
        "blast_radius": round(blast_radius, 2),
        "thermal_radius": round(thermal_radius, 2),
        "radiation_radius": round(radiation_radius, 2),
        "damage_level": damage_level,
        "estimated_casualties": int(casualties),
        "fallout_zone": round(radiation_radius * 1.5, 2)
    }

@app.route('/')
def index():
    return render_template_string(UI_TEMPLATE, data=MAIN_COUNTRIES, secret_db=SECRET_DB, 
                                 expanded_db=EXPANDED_DB, nuclear_targets=NUCLEAR_TARGETS)

@app.route('/nuclear_simulate', methods=['POST'])
def nuclear_simulate():
    data = request.json
    country = data.get('country', 'ABD')
    city = data.get('city', 'WASHINGTON DC')
    yield_kt = data.get('yield', 1000)
    latitude = data.get('lat', 39.8283)
    longitude = data.get('lon', -98.5795)
    
    population_density = random.randint(5, 50)
    impact = calculate_nuclear_impact(yield_kt, random.uniform(0, 20), population_density)
    
    return jsonify({
        "status": "SIMULATION_COMPLETE",
        "parameters": {
            "target_country": country,
            "target_city": city,
            "yield_kt": yield_kt,
            "coordinates": f"{latitude}, {longitude}"
        },
        "impact_analysis": impact,
        "additional_effects": [
            f"ELEKTROMANYETİK PULS: {random.randint(50, 200)} km etki",
            f"NÜKLEER KIŞ ETKİSİ: Global sıcaklıkta {random.randint(1, 10)}°C düşüş",
            f"RADYASYON YAYILIMI: {random.randint(100, 500)} km²",
            f"ALTYAPI ÇÖKÜŞÜ: %{random.randint(70, 100)}",
            f"EKONOMİK KAYIP: ${random.randint(100, 1000)} milyar"
        ],
        "recommended_targets": NUCLEAR_TARGETS.get(country, {}).get('priority', []),
        "timestamp": "2024-ULTRA-SIM"
    })

# ===== TAM UI_TEMPLATE =====
UI_TEMPLATE = '''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>GGI_OS_v5.0_ULTRA</title>
    <style>
        :root{--b:#00f2ff;--g:#39ff14;--r:#f05;--bg:#010203;--p:rgba(10,25,45,0.98)}
        *{box-sizing:border-box;margin:0;padding:0;font-family:'Courier New',monospace}
        body{background:var(--bg);color:#fff;font-size:12px;overflow-x:hidden}
        
        /* Mobil Optimizasyon */
        @media (max-width: 768px) {
            body{font-size:14px}
            header{height:60px;padding:0 10px}
            main{grid-template-columns:1fr;gap:5px;padding:5px}
            .panel{height:auto;min-height:300px}
            .card{padding:10px;margin-bottom:5px}
            .sim-controls{grid-template-columns:1fr;gap:5px}
            .sim-controls button{grid-column:1/-1}
        }
        
        @media (max-width: 480px) {
            body{font-size:12px}
            .card{padding:8px}
            .panel-h{padding:8px;font-size:10px}
            .audio-btn{bottom:10px;font-size:10px}
            .audio-btn{right:10px;width:40px;height:40px}
        }

        #login-screen{position:fixed;inset:0;background:#000;z-index:10000;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px}
        #pass-input{background:transparent;border:1px solid var(--b);color:var(--b);padding:15px;text-align:center;font-size:24px;outline:none;box-shadow:0 0 10px var(--b);width:200px;border-radius:5px}
        @media (max-width: 480px){#pass-input{width:150px;font-size:20px;padding:12px}}

        header{height:50px;border-bottom:1px solid var(--b);display:flex;align-items:center;justify-content:space-between;padding:0 20px;background:#000;position:sticky;top:0;z-index:100}
        main{display:grid;grid-template-columns:1fr 350px 300px;height:calc(100vh - 50px);padding:10px;gap:10px}
        
        @media (max-width:1024px){
            main{grid-template-columns:1fr;height:auto;min-height:calc(100vh - 50px)}
            #term-panel,#feed-panel{height:300px}
        }

        .panel{border:1px solid #224466;background:var(--p);display:flex;flex-direction:column;overflow:hidden;border-radius:5px}
        .panel-h{background:#0a111a;padding:10px;color:var(--b);font-size:11px;border-bottom:1px solid #224466;font-weight:bold;text-transform:uppercase}
        .scroll{flex:1;overflow-y:auto;padding:10px;scrollbar-width:thin}
        
        .card{background:rgba(0,0,0,0.4);border:1px solid #112233;margin-bottom:8px;padding:12px;cursor:pointer;transition:0.3s;border-radius:3px}
        .card:hover{border-color:var(--b);background:rgba(0,242,255,0.05)}
        .intel-box{color:var(--g);font-size:11px;white-space:pre-wrap;margin-top:8px;display:none;border-left:2px solid var(--g);padding-left:10px}
        
        #term-out,#feed-out{font-size:11px;color:var(--g);line-height:1.4}
        .cmd-line{display:flex;padding:10px;background:#050a10;border-top:1px solid #224466}
        input{background:transparent;border:none;color:var(--g);flex:1;outline:none;padding:5px}

        .overlay{position:fixed;inset:0;background:#000;z-index:9999;display:none;flex-direction:column;padding:20px;overflow-y:auto}
        .secret-country-btn{border:1px solid var(--r);padding:10px;margin:3px;color:var(--r);cursor:pointer;display:inline-block;font-size:10px;transition:0.3s;border-radius:3px}
        .secret-country-btn:hover{background:var(--r);color:#fff}
        .nuke-icon{animation:blink 1s infinite;color:var(--r)}
        @keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
        
        @keyframes pulse {0%,100%{opacity:1}50%{opacity:0.5}}
        @keyframes expand{from{width:0;height:0}to{width:300px;height:300px;opacity:0}}
        
        .pulse{animation:pulse 2s infinite}
        
        /* Nükleer Simülasyon */
        #nuke-sim{position:fixed;inset:0;background:#000;z-index:9999;display:none;flex-direction:column;color:#fff;overflow:hidden}
        #world-map{width:100%;height:60%;background:#112233;position:relative;border:2px solid var(--r)}
        .map-target{position:absolute;width:15px;height:15px;background:var(--r);border-radius:50%;cursor:pointer;transform:translate(-50%,-50%)}
        .map-target:hover{width:20px;height:20px;box-shadow:0 0 20px var(--r)}
        .blast-wave{position:absolute;border:2px solid orange;border-radius:50%;opacity:0.7;transform:translate(-50%,-50%);animation:expand 3s ease-out}
        
        .sim-controls{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:15px;background:rgba(0,0,0,0.7)}
        .sim-result{flex:1;padding:15px;overflow-y:auto;border-top:2px solid var(--r)}
        
        .audio-btn{position:fixed;bottom:20px;right:20px;width:50px;height:50px;border-radius:50%;background:var(--b);color:#000;border:none;cursor:pointer;z-index:999;font-size:20px}
        .audio-btn:hover{background:var(--g);transform:scale(1.1)}
        
        #matrix-screen{position:fixed;inset:0;background:#000;z-index:9998;display:none;overflow:hidden}
        .matrix-column{position:absolute;top:-100%;font-size:14px;color:var(--g);text-shadow:0 0 5px var(--g);white-space:pre;line-height:1.2}
        
        /* Scrollbar */
        .scroll::-webkit-scrollbar{width:6px}
        .scroll::-webkit-scrollbar-track{background:#0a111a}
        .scroll::-webkit-scrollbar-thumb{background:var(--b);border-radius:3px}
        .scroll::-webkit-scrollbar-thumb:hover{background:var(--g)}
    </style>
</head>
<body>
    <button class="audio-btn" onclick="toggleAudio()" title="Sesleri Aç/Kapat">🔊</button>
    
    <div id="login-screen">
        <h2 style="color:var(--r);margin-bottom:20px;text-align:center">GGI SECURITY ACCESS</h2>
        <input type="password" id="pass-input" placeholder="78921" maxlength="5" autofocus>
        <p id="login-msg" style="margin-top:15px;color:gray;text-align:center">Şifre: 78921</p>
    </div>

    <header>
        <div style="color:var(--b)">GGI_OS_v5.0 // ULTRA_SECURE</div>
        <div id="clock">00:00:00</div>
    </header>

    <main>
        <div class="panel">
            <div class="panel-h">STRATEJİK ANALİZ (25 ÜLKE)</div>
            <div class="scroll" id="countries-list">
                {% for country,info in data.items() %}
                <div class="card" onclick="toggleCountryInfo(this, `{{info.replace("'", "\\'").replace('"', '\\"')}}`)">
                    <strong>{{country}}</strong>
                    <div class="intel-box"></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="panel" id="term-panel">
            <div class="panel-h">COMMAND TERMINAL</div>
            <div id="term-out" class="scroll">Sistem Aktif. Komut Bekleniyor...\\n> help yazın</div>
            <div class="cmd-line">
                <span style="color:var(--g)">root@ggi:~$ </span>
                <input type="text" id="term-cmd" autocomplete="off" placeholder="help...">
            </div>
        </div>

        <div class="panel" id="feed-panel">
            <div class="panel-h">LIVE INTELLIGENCE</div>
            <div id="feed-out" class="scroll"></div>
        </div>
    </main>

    <div id="scr-secret" class="overlay">
        <h2 style="color:var(--r);text-align:center">KOZMİK GİZLİ ARŞİV <span class="nuke-icon">☢</span></h2>
        <div id="secret-btns" style="margin-top:20px;text-align:center">
            {% for country in secret_db.keys() %}
            <div class="secret-country-btn" onclick="runSecretDaktilo('{{country}}')">{{country}}</div>
            {% endfor %}
        </div>
        <div id="stream-output" style="color:var(--g);margin-top:30px;white-space:pre-wrap;padding:20px;border:1px dashed var(--r);min-height:200px"></div>
        <button onclick="closeSecret()" style="margin-top:20px;background:red;color:#fff;border:none;padding:15px;width:100%;cursor:pointer;border-radius:5px">KAPAT</button>
    </div>

    <div id="nuke-sim">
        <div style="background:rgba(255,0,0,0.2);padding:15px;text-align:center;font-size:18px;border-bottom:2px solid var(--r)">
            ⚠️ NÜKLEER SİMÜLASYON ⚠️
            <button onclick="closeNukeSim()" style="position:absolute;right:20px;top:10px;background:var(--r);color:#fff;border:none;padding:5px 10px;cursor:pointer;border-radius:3px">X</button>
        </div>
        
        <div id="world-map"></div>
        
        <div class="sim-controls">
            <div>
                <label style="color:var(--g)">Hedef Ülke:</label>
                <select id="target-country" style="width:100%;background:#000;color:var(--g);border:1px solid var(--b);padding:5px;border-radius:3px">
                    {% for country in nuclear_targets.keys() %}
                    <option value="{{country}}">{{country}}</option>
                    {% endfor %}
                </select>
            </div>
            <div>
                <label style="color:var(--g)">Şehir:</label>
                <select id="target-city" style="width:100%;background:#000;color:var(--g);border:1px solid var(--b);padding:5px;border-radius:3px">
                    <option value="BAŞKENT">BAŞKENT</option>
                </select>
            </div>
            <div>
                <label style="color:var(--g)">Bomba Gücü (kT):</label>
                <input type="range" id="yield-slider" min="10" max="50000" value="1000" style="width:100%">
                <div id="yield-display" style="color:orange">1000 kT</div>
            </div>
            <div>
                <label style="color:var(--g)">Koordinatlar:</label>
                <input type="text" id="coords-input" value="39.8283, -98.5795" style="width:100%;background:#000;color:var(--g);border:1px solid var(--b);padding:5px;border-radius:3px">
            </div>
        </div>
        
        <div class="sim-controls">
            <button onclick="launchSimulation()" style="grid-column:1/3;background:var(--r);color:#fff;border:none;padding:15px;cursor:pointer;font-size:16px;border-radius:5px">
                🚀 SİMÜLASYONU BAŞLAT
            </button>
            <button onclick="generateRandomTarget()" style="grid-column:3/5;background:var(--b);color:#000;border:none;padding:15px;cursor:pointer;border-radius:5px">
                🎯 RASTGELE HEDEF
            </button>
        </div>
        
        <div class="sim-result" id="sim-result">
            <h3 style="color:var(--r)">Simülasyon Sonuçları:</h3>
            <div id="simulation-output"></div>
        </div>
    </div>

    <div id="matrix-screen"></div>

    <audio id="click-sound" preload="auto"></audio>
    <audio id="typing-sound" preload="auto"></audio>
    <audio id="alert-sound" preload="auto"></audio>
    <audio id="nuke-sound" preload="auto"></audio>
    <audio id="matrix-sound" preload="auto"></audio>
    <audio id="bg-music" loop preload="auto"></audio>

    <script>
        const secretStore = {{secret_db|tojson}};
        const expandedStore = {{expanded_db|tojson}};
        const nuclearTargets = {{nuclear_targets|tojson}};
        
        let audioEnabled = false;
        let currentCountry = '';
        
        function toggleAudio() {
            audioEnabled = !audioEnabled;
            const btn = document.querySelector('.audio-btn');
            if (audioEnabled) {
                btn.style.background = 'var(--g)';
                btn.textContent = '🔊';
                playSound('bg-music');
            } else {
                btn.style.background = 'var(--r)';
                btn.textContent = '🔇';
                document.getElementById('bg-music').pause();
            }
        }
        
        function playSound(soundId) {
            if (!audioEnabled) return;
            const sound = document.getElementById(soundId);
            if (sound) {
                sound.currentTime = 0;
                sound.play().catch(e => console.log("Ses çalınamadı"));
            }
        }
        
        function daktiloExecution(text, element, speed = 30) {
            element.innerHTML = "";
            element.style.display = "block";
            let i = 0;
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                    playSound('typing-sound');
                    setTimeout(type, speed);
                }
            }
            type();
        }
        
        function toggleCountryInfo(card, info) {
            const box = card.querySelector('.intel-box');
            playSound('click-sound');
            
            if (box.style.display === "block") {
                box.style.display = "none";
                box.innerHTML = "";
            } else {
                daktiloExecution(info, box, 25);
            }
        }
        
        function runSecretDaktilo(country) {
            const output = document.getElementById('stream-output');
            const data = secretStore[country] ? secretStore[country].join('\\n') : "Veri bulunamadı";
            daktiloExecution('[ERİŞİM: ' + country + ']\\n━━━━━━━━━━━━━━━━\\n' + data, output, 20);
        }
        
        function closeSecret() {
            document.getElementById('scr-secret').style.display = 'none';
        }
        
        function closeNukeSim() {
            document.getElementById('nuke-sim').style.display = 'none';
        }
        
        function showMatrixScreen(data) {
            const screen = document.getElementById('matrix-screen');
            screen.style.display = 'block';
            screen.innerHTML = '';
            
            playSound('matrix-sound');
            
            for (let i = 0; i < 50; i++) {
                const col = document.createElement('div');
                col.className = 'matrix-column';
                col.style.left = Math.random() * 100 + '%';
                col.style.animationDuration = (Math.random() * 5 + 3) + 's';
                col.innerText = data[Math.floor(Math.random() * data.length)];
                screen.appendChild(col);
                
                setTimeout(() => {
                    col.style.top = '100%';
                    col.style.transition = 'top ' + (Math.random() * 5 + 5) + 's linear';
                }, 100);
            }
            
            setTimeout(() => {
                screen.style.display = 'none';
                screen.innerHTML = '';
            }, 8000);
        }
        
        const CMD_RESPONSES = {
            'bombsimulation': () => {
                document.getElementById('nuke-sim').style.display = 'flex';
                playSound('alert-sound');
                return "Nükleer simülasyon açıldı";
            },
            'help': () => {
                return "KOMUTLAR:\\n• help - Bu mesaj\\n• clear - Terminali temizle\\n• status - Sistem durumu\\n• bombsimulation - Nükleer simülasyon\\n• 78921secretfiles - Gizli arşiv\\n• matrix - Matrix efekti";
            },
            'clear': () => {
                document.getElementById('term-out').innerHTML = '';
                return "Terminal temizlendi";
            },
            'status': () => {
                return "SİSTEM DURUMU:\\n✓ CPU: %87\\n✓ RAM: %92\\n✓ AĞ: Aktif\\n✓ GÜVENLİK: Seviye 5";
            },
            '78921secretfiles': () => {
                document.getElementById('scr-secret').style.display = 'flex';
                return "Gizli arşiv açıldı";
            },
            'matrix': () => {
                showMatrixScreen(['SİSTEM AKTİF','VERİ AKIŞI','ANALİZ TAMAM','GÜVENLİK: %100','SİBER KALKAN AKTİF']);
                return "Matrix efekti başlatıldı";
            }
        };
        
        document.getElementById('term-cmd').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const cmd = this.value.toLowerCase().trim();
                const out = document.getElementById('term-out');
                out.innerHTML += '<div><span style="color:#fff">> ' + cmd + '</span></div>';
                
                if (cmd && CMD_RESPONSES[cmd]) {
                    const response = CMD_RESPONSES[cmd]();
                    if (response) {
                        out.innerHTML += '<div style="color:var(--g)">' + response + '</div>';
                    }
                } else if (cmd) {
                    out.innerHTML += '<div style="color:var(--r)">Geçersiz komut: ' + cmd + '</div>';
                }
                
                this.value = "";
                out.scrollTop = out.scrollHeight;
            }
        });
        
        document.getElementById('pass-input').addEventListener('input', function(e) {
            if (this.value === '78921') {
                document.getElementById('login-screen').style.display = 'none';
                startLiveFeed();
                playSound('click-sound');
            } else if (this.value.length === 5) {
                this.value = "";
                document.getElementById('login-msg').innerText = "HATALI ŞİFRE! Doğrusu: 78921";
                document.getElementById('login-msg').style.color = "red";
                playSound('alert-sound');
            }
        });
        
        function startLiveFeed() {
            const feed = document.getElementById('feed-out');
            const logs = ["[SİBER] Kalkan Aktif","[UYDU] Takip Devam","[LOG] Anahtar Döndür","[NÜKLEER] Hazır","[FÜZE] Operasyonel","[RADAR] Tarama","[AI] Öğrenme Modu","[DRONE] Swarm Aktif"];
            setInterval(() => {
                const log = logs[Math.floor(Math.random() * logs.length)];
                feed.innerHTML += '<div style="color:var(--g)">> ' + log + '</div>';
                if (feed.children.length > 50) feed.removeChild(feed.firstChild);
                feed.scrollTop = feed.scrollHeight;
            }, 3000);
        }
        
        document.getElementById('yield-slider').addEventListener('input', function() {
            document.getElementById('yield-display').textContent = this.value + ' kT';
        });
        
        document.getElementById('target-country').addEventListener('change', function() {
            const data = nuclearTargets[this.value];
            if (data) {
                document.getElementById('coords-input').value = data.lat + ', ' + data.lon;
            }
        });
        
        function generateRandomTarget() {
            const countries = Object.keys(nuclearTargets);
            const randomCountry = countries[Math.floor(Math.random() * countries.length)];
            const data = nuclearTargets[randomCountry];
            const randomYield = Math.floor(Math.random() * 50000) + 10;
            
            document.getElementById('target-country').value = randomCountry;
            document.getElementById('yield-slider').value = randomYield;
            document.getElementById('yield-display').textContent = randomYield + ' kT';
            document.getElementById('coords-input').value = data.lat + ', ' + data.lon;
        }
        
        function launchSimulation() {
            const country = document.getElementById('target-country').value;
            const city = document.getElementById('target-city').value;
            const yieldValue = document.getElementById('yield-slider').value;
            const coords = document.getElementById('coords-input').value;
            
            playSound('nuke-sound');
            
            const map = document.getElementById('world-map');
            const blast = document.createElement('div');
            blast.className = 'blast-wave';
            blast.style.left = '50%';
            blast.style.top = '50%';
            map.appendChild(blast);
            
            setTimeout(() => blast.remove(), 3000);
            
            fetch('/nuclear_simulate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    country: country,
                    city: city,
                    yield: parseInt(yieldValue),
                    lat: parseFloat(coords.split(',')[0]),
                    lon: parseFloat(coords.split(',')[1])
                })
            })
            .then(response => response.json())
            .then(data => {
                const output = document.getElementById('simulation-output');
                let html = '<div style="color:orange;margin-bottom:10px">🚀 FÜZE FIRLATILDI → ' + city + ', ' + country + '</div>';
                html += '<div style="color:var(--g);margin:10px 0">📊 SİMÜLASYON SONUÇLARI:</div>';
                html += '<div>💥 Patlama Yarıçapı: ' + data.impact_analysis.blast_radius + ' km</div>';
                html += '<div>🔥 Termal Yarıçap: ' + data.impact_analysis.thermal_radius + ' km</div>';
                html += '<div>☢️ Radyasyon Yarıçapı: ' + data.impact_analysis.radiation_radius + ' km</div>';
                html += '<div>💀 Hasar Seviyesi: <span style="color:red">' + data.impact_analysis.damage_level + '</span></div>';
                html += '<div>👥 Tahmini Kayıp: ' + data.impact_analysis.estimated_casualties.toLocaleString() + ' bin kişi</div>';
                html += '<div style="margin-top:15px;color:var(--b)">📈 DİĞER ETKİLER:</div>';
                data.additional_effects.forEach(effect => {
                    html += '<div>• ' + effect + '</div>';
                });
                
                output.innerHTML = html;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('simulation-output').innerHTML = 
                    '<div style="color:red">Simülasyon tamamlandı (Demo Modu)</div>';
            });
        }
        
        setInterval(() => {
            document.getElementById('clock').innerText = new Date().toLocaleTimeString();
        }, 1000);
    </script>
</body>
</html>'''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)""
