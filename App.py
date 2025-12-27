import os
import datetime
import random
import time
import math
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

STRATEGIC_INTEL = {
    "TÜRKİYE": "[KOZMİK SEVİYE]\\n- İHA/SİHA: Dünya lideri.\\n- HAVA: KAAN 5. nesil.\\n- DENİZ: TCG Anadolu operasyonel.\\n- SİBER: Kuantum şifreleme.\\n- UZAY: Ay görevi hazırlık.",
    "ABD": "[TOP SECRET]\\n- NÜKLEER: 11 Uçak gemisi.\\n- SİBER: NSA küresel dinleme.\\n- UZAY: Space Force aktif.\\n- EKONOMİ: Dolar hegemonyası.\\n- F-35: 450+ operasyonel.",
    "RUSYA": "[SIGMA-9]\\n- FÜZE: Zircon Mach 9.\\n- NÜKLEER: 5977 başlık.\\n- SİBER: GRU operasyonları.\\n- ARKTİK: Buzkıran filosu.\\n- Su-57: 5. nesil aktif.",
    "ÇİN": "[RED-DRAGON]\\n- EKONOMİ: 17.9 trilyon GSYİH.\\n- DONANMA: Tip 004 uçak gemisi.\\n- TEKNOLOJİ: 6G kuantum.\\n- UZAY: Tiangong istasyonu.\\n- J-20: 200+ adet.",
    "İNGİLTERE": "[MI6-ALPHA]\\n- SİBER: GCHQ merkezleri.\\n- DONANMA: Astute denizaltı.\\n- F-35B: Lightning II.\\n- İSTİHBARAT: Five Eyes.\\n- NÜKLEER: Vanguard SSBN.",
    "FRANSA": "[OMEGA-FR]\\n- NÜKLEER: 290 başlık bağımsız.\\n- HAVA: Rafale F4.\\n- DENİZ: Charles de Gaulle.\\n- UZAY: Ariane 6.\\n- LEJYON: Elit güç.",
    "ALMANYA": "[BUNDESWEHR]\\n- EKONOMİ: 4.3 trilyon GSYİH.\\n- TANK: Leopard 2A7+.\\n- HAVA: Eurofighter Typhoon.\\n- SİBER: BSI güvenlik.\\n- PUMA: Piyade aracı.",
    "İSRAİL": "[MOSSAD]\\n- SİBER: Unit 8200.\\n- HAVA: Iron Dome.\\n- NÜKLEER: 80-400 başlık.\\n- F-35I: Adir modifikasyon.\\n- MERKAVA: Mk.4 tank.",
    "JAPONYA": "[RISING-SUN]\\n- TEKNOLOJİ: Robotik lider.\\n- DONANMA: İzumo F-35B.\\n- EKONOMİ: 4.9 trilyon.\\n- UZAY: H3 roketi.\\n- AEGIS: 8 destroyer.",
    "HİNDİSTAN": "[BRAHMOS]\\n- NÜKLEER: Agni-V ICBM.\\n- UZAY: Chandrayaan-3.\\n- DONANMA: INS Vikrant.\\n- FÜZE: BrahMos 290+ adet.\\n- TEJAS: Yerli uçak.",
    "GÜNEY KORE": "[K-DEFENSE]\\n- TANK: K2 Black Panther.\\n- HAVA: KF-21 Boramae.\\n- K9: Thunder obüs.\\n- SİBER: KISA ajansı.\\n- Samsung: Tech dev.",
    "İTALYA": "[MARE-NOSTRUM]\\n- DONANMA: Trieste LHD.\\n- HAVA: F-35A/B.\\n- Leonardo: Savunma.\\n- FREMM: Fırkateyn.\\n- CAVOUR: Uçak gemisi.",
    "İSPANYA": "[IBERIA]\\n- DONANMA: S-80 Plus.\\n- HAVA: Eurofighter.\\n- TANK: Leopard 2E.\\n- NAVANTIA: Gemi inşa.\\n- F-110: Fırkateyn.",
    "POLONYA": "[EAGLE]\\n- TANK: K2 1000+ sipariş.\\n- HAVA: F-35A 32 adet.\\n- FÜZE: Patriot.\\n- ABRAMS: M1A2 250.\\n- FA-50: 48 adet.",
    "AVUSTRALYA": "[SOUTHERN-CROSS]\\n- DONANMA: AUKUS denizaltı.\\n- HAVA: F-35A 72.\\n- UZAY: Pine Gap.\\n- Five Eyes: İstihbarat.\\n- HUNTER: Fırkateyn.",
    "KANADA": "[MAPLE]\\n- HAVA: CF-18 Hornet.\\n- ARKTİK: Kuzey güvenlik.\\n- NORAD: Entegrasyon.\\n- F-35: 88 sipariş.\\n- LEOPARD: 2A4/2A6.",
    "BREZİLYA": "[AMAZON]\\n- HAVA: Gripen NG.\\n- DONANMA: Riachuelo.\\n- KC-390: Nakliye.\\n- ASTROS: Roketatar.\\n- Embraer: A-29.",
    "PAKİSTAN": "[ATOMIC]\\n- NÜKLEER: Shaheen-III.\\n- HAVA: JF-17 Thunder.\\n- TANK: Al-Khalid.\\n- FÜZE: Babur.\\n- ISI: İstihbarat.",
    "İRAN": "[PERSIAN]\\n- FÜZE: 2000+ balistik.\\n- DRONE: Shahed-136.\\n- DENİZ: Hürmüz kontrolü.\\n- FATEH: 110 füze.\\n- KHORDAD: Hava savunma.",
    "MISIR": "[PHARAOH]\\n- STRATEJİK: Suez Kanalı.\\n- HAVA: Rafale 30 adet.\\n- DONANMA: Mistral LHD.\\n- TANK: M1A1 1130.\\n- S-300VM: Savunma."
}

SECRET_INTEL_DB = {
    "☢ NAZI_REICH_ARCHIVE": "🔴 ULTRA SECRET DOSYA\\n━━━━━━━━━━━━━━━━━━━━━━\\n1. Nükleer Program: Vemork Ağır Su Reaktörü\\n2. Die Glocke Projesi: Anti-yerçekimi teknolojisi\\n3. V2 Füze Sistemi: Uzun menzilli balistik füze\\n4. Wolfsschanze Karargahı: Kozmik frekans iletimi\\n5. Antarktika Base 211: Gizli denizaltı üssü\\n6. Ahnenerbe Okült Araştırmaları: Paranormal silahlar\\n7. Wunderwaffe Programları: Mucize silah geliştirme\\n━━━━━━━━━━━━━━━━━━━━━━\\n⚠ SINIFLANDIRMA: OMEGA-9 KOZMIK\\n⚠ ERİŞİM: YALNIZCA FÜHRER ONAYIYLA"
}

COUNTRY_NAMES = ["ARNAVUTLUK", "CİBUTİ", "EKVADOR", "ETİYOPYA", "FAS", "FİJİ", "GANA", "GUATEMALA", "HAİTİ", "HIRVATİSTAN",
                 "IRAK", "İRLANDA", "İSKOÇYA", "İSVİÇRE", "İZLANDA", "KAMBOÇYA", "KATAR", "KENYA", "KIBRIS",
                 "KOLOMBİYA", "KONGO", "KOSTA RİKA", "KUVEYT", "LETONYA", "LİBYA", "LİTVANYA", "LÜKSEMBURG", "MACARİSTAN", "MAKEDONYA",
                 "MALEZYA", "MALİ", "MALTA", "MOĞOLİSTAN", "MOLDOVA", "MYANMAR", "NİJERYA", "NORVEÇ", "UMMAN",
                 "ÖZBEKİSTAN", "PANAMA", "PARAGUAY", "PERU", "PORTEKİZ", "ROMANYA", "RWANDA", "SENEGAL", "SIRBİSTAN", "SLOVAKYA",
                 "SLOVENYA", "SOMALİ", "SRİ LANKA", "SUDAN", "SURİYE", "SUUDİ ARABİSTAN", "ŞİLİ", "TAYLAND", "TANZANYA", "TAYVAN",
                 "TUNUS", "UGANDA", "UKRAYNA", "URUGUAY", "VENEZİLA", "VİETNAM", "YEMEN", "YENİ ZELANDA", "YUNANİSTAN", "ZİMBABVE",
                 "AZERBAYCAN", "BEYAZ RUSYA", "BULGARİSTAN", "ÇEK CUM.", "DANİMARKA", "ENDONEZYA", "ERİTRE", "ERMENİSTAN", "ESTONYA", "FİLİPİNLER",
                 "FİNLANDİYA", "GÜRCİSTAN", "HOLLANDA", "İSVEÇ", "KAZAKİSTAN", "KUZEY KORE", "LİBERYA", "LÜBNAN", "MEKSIKA", "NEPAL",
                 "NİKARAGUA", "AVUSTURYA", "BAE", "BAHREYN", "BELÇİKA", "BOLİVYA"]

for i, name in enumerate(COUNTRY_NAMES[:95], start=1):
    threat = random.randint(35, 98)
    SECRET_INTEL_DB[f"⚡ {name}"] = (
        f"📊 Tehdit Seviyesi: %{threat}\\n"
        f"🔬 Teknoloji: {random.choice(['Nükleer', 'Kuantum', 'Biyolojik', 'Siber', 'Plazma'])}\\n"
        f"⚔️ Doktrin: {random.choice(['Yıldırım Saldırı', 'Asimetrik Savaş', 'Hibrit Taktik', 'Siber Felç', 'Derin Darbe'])}\\n"
        f"📡 İstihbarat: {'🔴 KRİTİK' if threat > 70 else '🟡 ORTA' if threat > 50 else '🟢 DÜŞÜK'}\\n"
        f"🎯 Statü: {random.choice(['Aktif İzleme', 'Pasif Gözetim', 'Operasyonel Hazır', 'Devre Dışı'])}\\n"
        f"🛡️ Savunma: {random.choice(['Güçlü', 'Orta', 'Zayıf', 'Yoktur'])}"
    )

@app.route('/')
def index():
    return render_template_string(UI_TEMPLATE, data=STRATEGIC_INTEL, secret_db=SECRET_INTEL_DB)

@app.route('/health')
def health():
    return jsonify({"status":"OK","version":"2.1.6"})

UI_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>GGI_OS</title>
<style>
:root{--b:#00f2ff;--g:#39ff14;--r:#f05;--bg:#010203;--p:rgba(10,25,45,0.98)}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body,html{background:var(--bg);color:#fff;font-family:'Courier New',monospace;height:100vh;overflow:hidden;font-size:13px}
header{height:50px;border-bottom:1px solid var(--b);display:flex;align-items:center;padding:0 20px;background:#000;font-size:18px;box-shadow:0 0 20px var(--b)}
main{display:flex;height:calc(100vh - 50px);padding:10px;gap:10px}
@media(max-width:768px){main{flex-direction:column;overflow-y:auto}}
.panel-logs{flex:0 0 280px;border:1px solid #224466;background:var(--p);display:flex;flex-direction:column;overflow:hidden}
@media(max-width:768px){.panel-logs{flex:none;height:200px}}
.panel-main{flex:1;border:1px solid #224466;background:var(--p);display:flex;flex-direction:column;overflow:hidden}
@media(max-width:768px){.panel-main{flex:none;height:400px}}
.panel-term{flex:0 0 380px;border:1px solid #224466;background:var(--p);display:flex;flex-direction:column;overflow:hidden}
@media(max-width:768px){.panel-term{flex:none;height:250px}}
.panel-h{background:#0a111a;padding:10px;color:var(--b);font-size:12px;border-bottom:1px solid #224466;font-weight:bold;text-transform:uppercase}
.scroll-area{flex:1;overflow-y:auto;padding:10px}
.card{background:rgba(0,0,0,0.4);border:1px solid #112233;margin-bottom:8px;padding:15px;cursor:pointer;transition:0.3s;border-radius:4px}
.card:hover{border-color:var(--b);transform:translateX(5px)}
.intel-box{color:var(--g);font-size:11px;white-space:pre-wrap;margin-top:8px;display:none;border-left:2px solid var(--g);padding-left:10px;line-height:1.5}
.cmd-line{display:flex;padding:10px;background:#050a10;border-top:1px solid #224466}
.cmd-line span{color:var(--g);margin-right:8px}
#term-cmd{background:transparent;border:none;color:var(--g);flex:1;outline:none;font-family:inherit;font-size:13px}
#secret-screen{position:fixed;top:0;left:0;width:100%;height:100%;background:linear-gradient(135deg,#1a0000,#4a0000);z-index:9999;display:none;flex-direction:column;padding:20px;overflow-y:auto}
.secret-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:25px;flex-wrap:wrap}
.nuclear-icon{font-size:60px;animation:pulse 1.5s infinite,shake 0.5s infinite;text-shadow:0 0 30px #ff0,0 0 60px #f00}
@keyframes pulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.2);opacity:0.8}}
@keyframes shake{0%{transform:translate(0,0) rotate(0deg)}25%{transform:translate(-2px,2px) rotate(-1deg)}50%{transform:translate(2px,-2px) rotate(1deg)}75%{transform:translate(-2px,-2px) rotate(-1deg)}100%{transform:translate(0,0) rotate(0deg)}}
.secret-title{font-size:28px;color:#fff;text-shadow:0 0 20px var(--r),2px 2px 8px #000;font-weight:bold;letter-spacing:2px}
.btn-close{background:linear-gradient(135deg,#000,#500);color:#fff;border:3px solid #f00;padding:12px 30px;cursor:pointer;font-size:14px;font-weight:bold;font-family:inherit;border-radius:6px;box-shadow:0 0 30px rgba(255,0,0,0.5);transition:0.3s}
.btn-close:hover{background:linear-gradient(135deg,#500,#f00);transform:scale(1.05)}
.secret-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:15px;padding-bottom:50px}
@media(max-width:768px){.secret-grid{grid-template-columns:1fr}}
.secret-item{border:2px solid rgba(255,0,0,0.5);background:rgba(0,0,0,0.8);padding:15px;cursor:pointer;border-radius:6px;transition:0.3s;min-height:80px}
.secret-item:hover{border-color:var(--r);box-shadow:0 0 30px rgba(255,0,0,0.4);transform:translateY(-3px)}
.secret-intel-box{color:var(--g);font-size:11px;white-space:pre-wrap;margin-top:10px;display:none;border-top:1px dashed rgba(255,0,0,0.5);padding-top:10px;line-height:1.6}
</style>
</head>
<body>
<div id="secret-screen">
<div class="secret-header">
<div style="display:flex;align-items:center;gap:20px">
<div class="nuclear-icon">☢</div>
<div class="secret-title">GGİ KOZMİK ARŞİV</div>
</div>
<button class="btn-close" onclick="document.getElementById('secret-screen').style.display='none'">🔒 ÇIKIŞ 🔒</button>
</div>
<div class="secret-grid">
{% for c, d in secret_db.items() %}
<div class="secret-item" onclick="runSecretType(this)">
<strong style="font-size:13px;color:#ff0">{{ c }}</strong>
<div class="secret-intel-box" data-content="{{ d|replace('"', '&quot;')|replace("'", '&#39;') }}"></div>
</div>
{% endfor %}
</div>
</div>
<header>GGI_OS v2.1.6 | <span id="clock">00:00:00</span></header>
<main>
<div class="panel-logs"><div class="panel-h">LOGS</div><div class="scroll-area" id="logs"></div></div>
<div class="panel-main"><div class="panel-h">INTEL ANALİZ</div><div class="scroll-area">
{% for n, i in data.items() %}
<div class="card" onclick="runMainType(this)"><strong>{{ n }}</strong><div class="intel-box" data-content="{{ i|replace('"', '&quot;')|replace("'", '&#39;') }}"></div></div>
{% endfor %}
</div></div>
<div class="panel-term"><div class="panel-h">TERMİNAL</div><div id="history" style="flex:1;overflow-y:auto;padding:10px;background:#000;font-size:11px;color:#888"></div><div class="cmd-line"><span>root@ggi:~$</span><input type="text" id="term-cmd" autofocus></div></div>
</main>
<script>
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
function sfx(f,d){try{const o=audioCtx.createOscillator();const g=audioCtx.createGain();o.frequency.value=f;g.gain.value=0.02;o.connect(g);g.connect(audioCtx.destination);o.start();o.stop(audioCtx.currentTime+d)}catch(e){}}
async function daktilo(text,el){el.style.display="block";el.innerHTML="";const lines=text.split('\\n');for(let line of lines){let d=document.createElement('div');el.appendChild(d);for(let c of line){d.innerHTML+=c;sfx(1300,0.02);await new Promise(r=>setTimeout(r,15))}}}
function runMainType(card){const box=card.querySelector('.intel-box');if(box.style.display==="block"){box.style.display="none"}else{const text=box.getAttribute('data-content');daktilo(text,box)}}
function runSecretType(item){const box=item.querySelector('.secret-intel-box');if(box.style.display==="block"){box.style.display="none"}else{sfx(400,0.1);const text=box.getAttribute('data-content');daktilo(text,box)}}
document.getElementById('term-cmd').addEventListener('keypress',(e)=>{if(e.key==='Enter'){const v=e.target.value.trim();if(v==='78921secretfiles'){document.getElementById('secret-screen').style.display='flex';sfx(100,0.6)}e.target.value=""}});
setInterval(()=>{const l=document.createElement('div');l.style.fontSize='10px';l.style.color='var(--g)';l.innerText=`[${new Date().toLocaleTimeString()}] HEARTBEAT_${Math.random().toString(36).substr(2,5).toUpperCase()}`;const logs=document.getElementById('logs');logs.insertBefore(l,logs.firstChild);if(logs.children.length>50)logs.removeChild(logs.lastChild)},3000);
setInterval(()=>{document.getElementById('clock').innerText=new Date().toLocaleTimeString()},1000);
document.body.addEventListener('click',()=>{if(audioCtx.state==='suspended')audioCtx.resume()},{once:true});
</script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
