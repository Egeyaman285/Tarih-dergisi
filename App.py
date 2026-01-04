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

# Ülke güvenlik kodları (her ülke için benzersiz kod)
COUNTRY_CODES = {
    "TÜRKİYE": "78921",  # Ana şifre olarak da kullanılıyor
    "ABD": "911US2024",
    "RUSYA": "007RU007",
    "ÇİN": "886CNXI",
    "ALMANYA": "491DE55",
    "İNGİLTERE": "44UK007",
    "FRANSA": "33FRANCE",
    "İSRAİL": "972ILMOSSAD",
    "JAPONYA": "81JPNINJA",
    "G.KORE": "82KOREA1",
    "POLONYA": "48PLNATO",
    "PAKİSTAN": "92PKISI",
    "İRAN": "98IRIRGC",
    "MISIR": "20EGYPT1",
    "BREZİLYA": "55BRAMZN",
    "İSPANYA": "34ES007",
    "İTALYA": "39ITMAFIA",
    "YUNANİSTAN": "30GRS300",
    "UKRAYNA": "380UAF",
    "HİNDİSTAN": "91INMODI",
    "İSVEÇ": "46SENATO",
    "NORVEÇ": "47NONATO",
    "KANADA": "1CANADA",
    "AVUSTRALYA": "61AUSKGB",
    "AZERBAYCAN": "994AZERI"
}

SECRET_DB = {k: [f"☢ PROTOKOL: {random.randint(1000,9999)}", f"☣ BİYOLOJİK: Seviye 4", f"🛰 UYDU: Takipte", f"💻 SİBER: Sızıldı", f"🗝 ANAHTAR: Kuantum", f"🛑 STATÜ: KRİTİK", f"🧬 PROJE: X-Alpha", f"🌑 ÜS: Bölge {random.randint(1,10)}", f"⚡ ENERJİ: Antimadde", f"💀 RİSK: OMEGA"] for k in list(MAIN_COUNTRIES.keys()) + ["KIBRIS", "İSVİÇRE", "KATAR"]}

# === GENİŞLETİLMİŞ VERİ TABANI ===
EXPANDED_DB = {
    "ULTRA_PROJECTS": [
        "PROJE: HAVVA - AI ÜSTÜN İSTİHBARAT",
        "PROJE: ZAMAN KATMANI - KRONOLOJİK SAVAŞ",
        "PROJE: QUANTUM SHIELD - ENERJİ KALKANI",
        "PROJE: NEURAL DOMINANCE - BEYİN KONTROL",
        "PROJE: TERRAFORM - İKLİM SİLAHI",
        "PROJE: DARK MATTER - GÖRÜNMEZLİK",
        "PROJE: PSI-WAVE - PSİKİK SAVAŞ",
        "PROJE: BIO-TITAN - SÜPER ASKER",
        "PROJE: COSMIC EYE - UZAY GÖZETİM",
        "PROJE: DIGITAL GOD - SİBER TANRI"
    ],
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

def ip_to_alphabet(ip):
    """IP adresini Latin alfabesine çevirir (1=A, 2=B, vb.)"""
    parts = ip.split('.')
    result = []
    for part in parts:
        num = int(part) if part.isdigit() else 0
        if 1 <= num <= 26:
            result.append(chr(64 + num))
        else:
            result.append(chr(65 + (num % 26)))
    return '.'.join(result)

def calculate_nuclear_impact(yield_kt, distance_km, population_density):
    """Nükleer bomba etkisini hesapla"""
    # Basit etki hesaplama
    blast_radius = math.sqrt(yield_kt) * 2  # km
    thermal_radius = math.sqrt(yield_kt) * 5  # km
    radiation_radius = math.sqrt(yield_kt) * 3  # km
    
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
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if user_ip and ',' in user_ip:
        user_ip = user_ip.split(',')[0].strip()
    ip_coded = ip_to_alphabet(user_ip)
    return render_template_string(UI_TEMPLATE, data=MAIN_COUNTRIES, secret_db=SECRET_DB, 
                                 expanded_db=EXPANDED_DB, nuclear_targets=NUCLEAR_TARGETS,
                                 country_codes=COUNTRY_CODES,
                                 user_ip=user_ip, ip_coded=ip_coded)

@app.route('/nuclear_simulate', methods=['POST'])
def nuclear_simulate():
    data = request.json
    country = data.get('country', 'ABD')
    city = data.get('city', 'WASHINGTON DC')
    yield_kt = data.get('yield', 1000)  # kiloton
    latitude = data.get('lat', 39.8283)
    longitude = data.get('lon', -98.5795)
    
    # Rastgele nüfus yoğunluğu (bin kişi/km²)
    population_density = random.randint(5, 50)
    
    # Hasar hesapla
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

@app.route('/check_country_code', methods=['POST'])
def check_country_code():
    data = request.json
    country = data.get('country')
    code = data.get('code')
    
    correct_code = COUNTRY_CODES.get(country, "")
    
    if code == correct_code:
        return jsonify({
            "success": True,
            "message": "KOD DOĞRU! ERİŞİM VERİLDİ.",
            "country_info": MAIN_COUNTRIES.get(country, "Bilgi bulunamadı.")
        })
    else:
        return jsonify({
            "success": False,
            "message": "HATALI KOD! ERİŞİM REDDEDİLDİ.",
            "hint": f"Kod {len(correct_code)} haneli" if correct_code else "Kod bulunamadı"
        })

# Ana HTML şablonu
UI_TEMPLATE = '''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>GGI_OS_v5.0_ULTRA</title>
    <style>
        :root{--b:#00f2ff;--g:#39ff14;--r:#f05;--bg:#010203;--p:rgba(10,25,45,0.98)}
        *{box-sizing:border-box;margin:0;padding:0;font-family:'Courier New',monospace}
        body{background:var(--bg);color:#fff;height:100vh;overflow:hidden;font-size:12px}
        
        @media screen and (orientation: portrait) and (max-width: 768px) {
            body::before {
                content: "⚠ YATAY MODA GEÇİN ⚠";
                position: fixed;
                inset: 0;
                background: #000;
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 99999;
                font-size: 20px;
                color: var(--r);
                animation: blink 1s infinite;
            }
        }

        #cookie-banner{position:fixed;bottom:0;left:0;right:0;background:#000;border-top:2px solid var(--b);padding:15px;z-index:10001;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}
        #cookie-banner button{background:var(--b);color:#000;border:none;padding:10px 20px;cursor:pointer;font-weight:bold;margin:5px}
        #cookie-banner button:hover{background:var(--g)}
        
        #ip-display{position:fixed;top:60px;left:10px;background:rgba(0,0,0,0.9);border:1px solid var(--b);padding:10px;font-size:11px;z-index:1000;color:var(--g)}
        
        #login-screen{position:fixed;inset:0;background:#000;z-index:10000;display:flex;flex-direction:column;align-items:center;justify-content:center}
        #pass-input{background:transparent;border:1px solid var(--b);color:var(--b);padding:10px;text-align:center;font-size:20px;outline:none;box-shadow:0 0 10px var(--b)}

        header{height:50px;border-bottom:1px solid var(--b);display:flex;align-items:center;justify-content:space-between;padding:0 20px;background:#000}
        main{display:grid;grid-template-columns:1fr 350px 300px;height:calc(100vh - 50px);padding:10px;gap:10px}
        
        @media (max-width:1024px){
            main{grid-template-columns:1fr;overflow-y:auto;height:auto}
            body{overflow-y:auto}
            #term-panel,#feed-panel{height:400px;margin-top:10px}
        }

        .panel{border:1px solid #224466;background:var(--p);display:flex;flex-direction:column;overflow:hidden}
        .panel-h{background:#0a111a;padding:10px;color:var(--b);font-size:11px;border-bottom:1px solid #224466;font-weight:bold;text-transform:uppercase}
        .scroll{flex:1;overflow-y:auto;padding:10px;scrollbar-width:thin}
        
        .card{background:rgba(0,0,0,0.4);border:1px solid #112233;margin-bottom:8px;padding:12px;cursor:pointer;transition:0.3s}
        .card:hover{border-color:var(--b);background:rgba(0,242,255,0.05)}
        .intel-box{color:var(--g);font-size:11px;white-space:pre-wrap;margin-top:8px;display:none;border-left:2px solid var(--g);padding-left:10px}
        
        /* Yapay Zeka Asistanı */
        #ai-assistant{position:fixed;bottom:80px;right:20px;width:60px;height:60px;border-radius:50%;background:var(--r);color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:900;font-size:24px;box-shadow:0 0 20px var(--r);animation:pulse 2s infinite}
        #ai-panel{position:fixed;bottom:150px;right:20px;width:300px;background:rgba(0,0,0,0.95);border:1px solid var(--b);padding:15px;display:none;z-index:901;border-radius:10px}
        #ai-panel input{width:100%;background:#111;color:#fff;border:1px solid var(--g);padding:8px;margin-top:10px}
        #ai-response{color:var(--g);font-size:11px;margin-top:10px;max-height:200px;overflow-y:auto}

        #term-out,#feed-out{font-size:11px;color:var(--g);line-height:1.4}
        .cmd-line{display:flex;padding:10px;background:#050a10;border-top:1px solid #224466}
        input{background:transparent;border:none;color:var(--g);flex:1;outline:none}

        .overlay{position:fixed;inset:0;background:#000;z-index:9999;display:none;flex-direction:column;padding:20px;overflow-y:auto}
        .secret-country-btn{border:1px solid var(--r);padding:10px;margin:3px;color:var(--r);cursor:pointer;display:inline-block;font-size:10px;transition:0.3s}
        .secret-country-btn:hover{background:var(--r);color:#fff}
        .nuke-icon{animation:blink 1s infinite;color:var(--r)}
        @keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
        
        /* Yeni Animasyonlar */
        @keyframes pulse {0%,100%{opacity:1}50%{opacity:0.5}}
        @keyframes shake {0%,100%{transform:translateX(0)}25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
        @keyframes float {0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
        @keyframes scan {0%{background-position:0 0}100%{background-position:100% 100%}}
        @keyframes glitch {0%{transform:translate(0)}20%{transform:translate(-2px,2px)}40%{transform:translate(-2px,-2px)}60%{transform:translate(2px,2px)}80%{transform:translate(2px,-2px)}100%{transform:translate(0)}}
        @keyframes fall {0%{transform:translateY(-100px) rotate(0deg);opacity:1}100%{transform:translateY(100vh) rotate(360deg);opacity:0}}
        
        .pulse{animation:pulse 2s infinite}
        .shake{animation:shake 0.5s}
        .float{animation:float 3s ease-in-out infinite}
        .scan-line{background:linear-gradient(to bottom, transparent 50%, rgba(0,242,255,0.1) 50%);background-size:100% 4px;animation:scan 2s linear infinite}
        .glitch{animation:glitch 0.5s}
        .falling-text{position:fixed;top:-50px;color:var(--g);font-size:14px;z-index:9997;animation:fall linear forwards;pointer-events:none}
        
        /* Nükleer Simülasyon Stilleri */
        #nuke-sim{position:fixed;inset:0;background:#000;z-index:9999;display:none;flex-direction:column;color:#fff;overflow:hidden}
        #world-map{width:100%;height:60%;background:#112233;position:relative;border:2px solid var(--r)}
        .map-target{position:absolute;width:15px;height:15px;background:var(--r);border-radius:50%;cursor:pointer;transform:translate(-50%,-50%)}
        .map-target:hover{width:20px;height:20px;box-shadow:0 0 20px var(--r)}
        .blast-wave{position:absolute;border:2px solid orange;border-radius:50%;opacity:0.7;transform:translate(-50%,-50%);animation:expand 3s ease-out}
        @keyframes expand{from{width:0;height:0}to{width:300px;height:300px;opacity:0}}
        
        .sim-controls{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:15px;background:rgba(0,0,0,0.7)}
        .sim-result{flex:1;padding:15px;overflow-y:auto;border-top:2px solid var(--r)}
        .damage-meter{height:20px;background:#333;margin:10px 0;position:relative;border:1px solid #666}
        .damage-fill{height:100%;background:linear-gradient(to right, green, yellow, orange, red);width:0%;transition:width 1s}
        
        .audio-btn{position:fixed;bottom:20px;right:90px;width:50px;height:50px;border-radius:50%;background:var(--b);color:#000;border:none;cursor:pointer;z-index:999}
        .audio-btn:hover{background:var(--g);transform:scale(1.1)}
        
        /* Ülke Kodu Girişi */
        .code-input-container{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.95);padding:30px;border:2px solid var(--r);z-index:10002;display:none;min-width:400px}
        .code-input-container input{width:100%;padding:15px;background:#111;color:#fff;border:1px solid var(--b);text-align:center;font-size:16px;letter-spacing:2px}

        #matrix-screen{position:fixed;inset:0;background:#000;z-index:9998;display:none;overflow:hidden}
        .matrix-column{position:absolute;top:-100%;font-size:14px;color:var(--g);text-shadow:0 0 5px var(--g);white-space:pre;line-height:1.2}
        
        /* Gravity Effect Toggle */
        #gravity-toggle{position:fixed;bottom:20px;left:20px;background:var(--b);color:#000;border:none;padding:10px 15px;cursor:pointer;z-index:999;border-radius:5px;font-size:11px}
        #gravity-toggle:hover{background:var(--g)}
    </style>
</head>
<body>
    <!-- Ses Kontrolü -->
    <button class="audio-btn" onclick="toggleAudio()" title="Sesleri Aç/Kapat">🔊</button>
    
    <!-- Gravity Effect Toggle -->
    <button id="gravity-toggle" onclick="toggleGravity()">GRAVITY: ON</button>
    
    <!-- Yapay Zeka Asistanı -->
    <div id="ai-assistant" onclick="toggleAIPanel()">🤖</div>
    <div id="ai-panel">
        <div style="color:var(--b);font-weight:bold">YAPAY ZEKA ASİSTANI</div>
        <div style="color:#aaa;font-size:10px;margin-bottom:10px">Ülke kodlarını sorabilirsiniz</div>
        <input type="text" id="ai-question" placeholder="Fransa'nın güvenlik kodu nedir?" onkeypress="handleAIQuestion(event)">
        <div id="ai-response"></div>
    </div>
    
    <div id="cookie-banner" style="display:none">
        <div style="color:#fff;font-size:12px">
            🔒 Bu site IP erişimi ve çerezler kullanır. Devam etmek için izin verin.
        </div>
        <div>
            <button onclick="acceptCookies()">KABUL ET</button>
            <button onclick="rejectCookies()" style="background:var(--r);color:#fff">REDDET</button>
        </div>
    </div>

    <div id="ip-display">
        <div>📡 IP: {{ user_ip }}</div>
        <div>🔤 KOD: {{ ip_coded }}</div>
        <div style="margin-top:5px;font-size:9px;color:#666">Latin: 1=A, 2=B...</div>
    </div>

    <!-- Ülke Kodu Giriş Ekranı -->
    <div id="country-code-modal" class="code-input-container">
        <div style="color:var(--r);font-size:18px;text-align:center;margin-bottom:20px" id="code-country-name">ÜLKE KODU GİRİN</div>
        <div style="color:var(--g);font-size:12px;text-align:center;margin-bottom:10px" id="code-hint"></div>
        <input type="text" id="country-code-input" placeholder="Güvenlik kodunu girin..." maxlength="20">
        <div style="margin-top:15px;display:flex;gap:10px">
            <button onclick="submitCountryCode()" style="flex:1;background:var(--b);color:#000;border:none;padding:10px;cursor:pointer">DOĞRULA</button>
            <button onclick="closeCodeModal()" style="flex:1;background:var(--r);color:#fff;border:none;padding:10px;cursor:pointer">İPTAL</button>
        </div>
        <div id="code-result" style="margin-top:15px;text-align:center"></div>
    </div>

    <div id="login-screen">
        <h2 style="color:var(--r);margin-bottom:20px">GGI SUPREME SECURITY ACCESS</h2>
        <input type="password" id="pass-input" placeholder="78921" maxlength="5" autofocus>
        <p id="login-msg" style="margin-top:15px;color:gray">YETKİLENDİRME BEKLENİYOR...</p>
    </div>

    <header>
        <div style="color:var(--b)">GGI_OS_v5.0 // ULTRA_SECURE</div>
        <div id="clock">00:00:00</div>
    </header>

    <main>
        <div class="panel">
            <div class="panel-h">STRATEJİK ANALİZ (25 ÜLKE) <span style="color:var(--r);font-size:9px">*Kod gereklidir</span></div>
            <div class="scroll">
                {% for country,info in data.items() %}
                <div class="card" onclick="requestCountryAccess('{{country}}')">
                    <strong>{{country}}</strong>
                    <div style="font-size:9px;color:#666;margin-top:3px">🔒 Kilitli - Kodu girin</div>
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
            <div class="panel-h">LIVE INTELLIGENCE</div>
            <div id="feed-out" class="scroll"></div>
        </div>
    </main>

    <!-- Gizli Arşiv -->
    <div id="scr-secret" class="overlay">
        <h2 style="color:var(--r);text-align:center">KOZMİK GİZLİ ARŞİV <span class="nuke-icon">☢</span></h2>
        <div id="secret-btns" style="margin-top:20px;text-align:center">
            {% for country in secret_db.keys() %}
            <div class="secret-country-btn" onclick="runSecretDaktilo('{{country}}')">{{country}}</div>
            {% endfor %}
        </div>
        <div id="stream-output" style="color:var(--g);margin-top:30px;white-space:pre-wrap;padding:20px;border:1px dashed var(--r);min-height:200px"></div>
        <button onclick="closeSecret()" style="margin-top:20px;background:red;color:#fff;border:none;padding:15px;width:100%;cursor:pointer">SİSTEMDEN ÇIK</button>
    </div>

    <!-- Nükleer Simülasyon -->
    <div id="nuke-sim">
        <div style="background:rgba(255,0,0,0.2);padding:15px;text-align:center;font-size:18px;border-bottom:2px solid var(--r)">
            ⚠️ NÜKLEER SAVAŞ SIMÜLASYONU v3.0 ⚠️
            <button onclick="closeNukeSim()" style="position:absolute;right:20px;top:10px;background:var(--r);color:#fff;border:none;padding:5px 10px;cursor:pointer">X</button>
        </div>
        
        <div id="world-map">
            <!-- Dünya haritası ve hedefler buraya eklenecek -->
        </div>
        
        <div class="sim-controls">
            <div>
                <label style="color:var(--g)">Hedef Ülke:</label>
                <select id="target-country" style="width:100%;background:#000;color:var(--g);border:1px solid var(--b);padding:5px">
                    {% for country in nuclear_targets.keys() %}
                    <option value="{{country}}">{{country}}</option>
                    {% endfor %}
                </select>
            </div>
            <div>
                <label style="color:var(--g)">Şehir:</label>
                <select id="target-city" style="width:100%;background:#000;color:var(--g);border:1px solid var(--b);padding:5px">
                    <option value="WASHINGTON DC">WASHINGTON DC</option>
                </select>
