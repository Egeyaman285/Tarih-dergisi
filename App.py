import os
import datetime
import random
import time
import base64
import json
import math
from flask import Flask, render_template_string, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ggi-ultra-v21-genesis-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ggi_v21_final.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

class SecretFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    content_hash = db.Column(db.String(500))
    clearance = db.Column(db.String(20))

STRATEGIC_INTEL = {
    "TÜRKİYE": "[KOZMİK SEVİYE]\nANALİZ: Bölgesel Güç Projeksiyonu.\n- İHA/SİHA: Dünya lideri otonom sistemler.\n- HAVA SAVUNMA: Çelik Kubbe (SİPER-2, HİSAR-U).\n- DENİZ: TCG Anadolu ve TF-2000 projesi.\n- SİBER: Milli Muharip İşlemci ve Kuantum Kripto.\n- UZAY: Yerli roket motoru ve ay görevi faz-1.\n- EKONOMİ: Savunma ihracatı 6 milyar dolar.\n- DİPLOMASİ: 5 kıtada aktif askeri varlık.\n- YERLİ: KAAN 5. nesil savaş uçağı.",
    "ABD": "[TOP SECRET]\nANALİZ: Küresel Dominans.\n- NÜKLEER: 11 Uçak gemisi, Trident-II füzeleri.\n- SİBER: NSA küresel dinleme ve sıfır-gün açıkları.\n- EKONOMİ: Rezerv para birimi manipülasyonu.\n- TEKNOLOJİ: Starlink v3 ve Mars kolonizasyon hazırlığı.\n- UZAY: Space Force operasyonel üstünlük.\n- ASKERİ: 750+ denizaşırı askeri üs.\n- BÜTÇE: 877 milyar dolar savunma harcaması.",
    "RUSYA": "[SIGMA-9]\nANALİZ: Stratejik Caydırıcılık.\n- FÜZE: Zircon (Mach 9), Avangard.\n- ENERJİ: Gazprom üzerinden jeopolitik baskı.\n- SİBER: GRU siber harp ve dezenformasyon ağları.\n- ARKTİK: Buzkıran filosu ve Kuzey Deniz yolu kontrolü.",
    "ÇİN": "[RED-DRAGON]\nANALİZ: Ekonomik Hegemonya.\n- ÜRETİM: Dünyanın sanayi motoru.\n- TEKNOLOJİ: 6G ve Kuantum haberleşme uyduları.\n- DONANMA: Tip 004 nükleer uçak gemisi projesi.",
    "İNGİLTERE": "[MI6-ALPHA]\nANALİZ: Finansal İstihbarat.\n- SİBER: GCHQ veri toplama merkezleri.\n- DONANMA: Astute sınıfı nükleer denizaltılar.",
    "FRANSA": "[OMEGA-FR]\nANALİZ: Avrupa Askeri Gücü.\n- NÜKLEER: Bağımsız caydırıcı güç.\n- HAVA: Rafale F4 çok rollü üstünlük.",
    "ALMANYA": "[BUNDESWEHR-X]\nANALİZ: Avrupa Sanayi Devi.\n- EKONOMİ: 4.3 trilyon dolar GSYİH.\n- TANK: Leopard 2A7+ dünya standardı.",
    "İSRAİL": "[MOSSAD-ULTRA]\nANALİZ: İstihbarat Üstünlüğü.\n- SİBER: Unit 8200 küresel siber elit.\n- HAVA: Iron Dome savunma.",
    "JAPONYA": "[RISING-SUN]\nANALİZ: Teknoloji Gücü.\n- TEKNOLOJİ: Robotik liderliği.\n- DONANMA: İzumo sınıfı F-35B platformu.",
    "HİNDİSTAN": "[BRAHMOS-NET]\nANALİZ: Yükselen Güç.\n- NÜKLEER: Agni-V ICBM.\n- FÜZE: BrahMos süpersonik.",
    "GÜNEY KORE": "[K-DEFENSE]\nANALİZ: Teknoloji İhracatçısı.\n- TANK: K2 Black Panther.\n- HAVA: KF-21 Boramae yerli savaş uçağı.",
    "İTALYA": "[MARE-NOSTRUM]\nANALİZ: Akdeniz Gücü.\n- DONANMA: Trieste LHD.\n- HAVA: F-35A/B programı.",
    "İSPANYA": "[IBERIA-GUARD]\nANALİZ: Akdeniz Köprüsü.\n- DONANMA: S-80 Plus denizaltı.\n- HAVA: Eurofighter Typhoon.",
    "POLONYA": "[EAGLE-FORTRESS]\nANALİZ: Doğu Kalkanı.\n- TANK: K2 Black Panther 1000+ sipariş.\n- HAVA: F-35A Lightning II.",
    "AVUSTRALYA": "[SOUTHERN-CROSS]\nANALİZ: Indo-Pasifik Gücü.\n- DONANMA: AUKUS nükleer denizaltı.\n- HAVA: F-35A Lightning II.",
    "KANADA": "[MAPLE-SHIELD]\nANALİZ: Kuzey Amerika Savunması.\n- HAVA: CF-18 Hornet.\n- ARKTİK: Kuzey geçidi güvenliği.",
    "BREZİLYA": "[AMAZON-FORCE]\nANALİZ: Güney Amerika Lideri.\n- HAVA: Gripen NG üretimi.\n- EKONOMİ: Bölgesel güç.",
    "PAKİSTAN": "[ATOMIC-SHIELD]\nANALİZ: Nükleer Denge.\n- NÜKLEER: Shaheen füze serisi.\n- HAVA: JF-17 Thunder.",
    "İRAN": "[PERSIAN-SHADOW]\nANALİZ: Asimetrik Strateji.\n- FÜZE: Balistik füze envanteri.\n- DRONE: Shahed İHA serisi.",
    "MISIR": "[PHARAOH-NET]\nANALİZ: Bölgesel Otorite.\n- STRATEJİK: Suez Kanalı kontrolü.\n- HAVA: Rafale savaş uçakları."
}

ALL_DATA = [{"n": f"{k} ANALİZ", "i": v} for k, v in STRATEGIC_INTEL.items()]

def get_html():
    return '''<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><title>GGI_OS_v21</title><style>:root{--b:#00f2ff;--g:#39ff14;--r:#f05;--bg:#010203;--p:rgba(10,25,45,0.9)}*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}body,html{margin:0;padding:0;background:var(--bg);color:#fff;font-family:'Courier New',monospace;height:100vh;overflow:hidden;font-size:13px}@media(max-width:768px){body{font-size:12px}}#matrix{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;opacity:0.15}header{height:50px;border-bottom:2px solid var(--b);display:flex;align-items:center;justify-content:space-between;padding:0 15px;background:#000;box-shadow:0 0 20px var(--b)}@media(max-width:768px){header{height:45px;padding:0 10px}}main{display:grid;grid-template-columns:1fr;gap:8px;padding:8px;height:calc(100vh - 50px);overflow-y:auto}@media(min-width:769px){main{grid-template-columns:280px 1fr 320px;overflow:hidden}}.panel{background:var(--p);border:1px solid #1a2a3a;display:flex;flex-direction:column;border-radius:6px;margin-bottom:8px;min-height:200px}@media(min-width:769px){.panel{margin-bottom:0;height:100%}}.panel-h{background:linear-gradient(90deg,#0a111a,#1a2a3a);padding:10px;color:var(--b);font-size:12px;font-weight:bold;border-bottom:2px solid #1a2a3a;display:flex;justify-content:space-between}.scroll-area{flex:1;overflow-y:auto;padding:10px}.card{background:rgba(5,15,25,0.8);border:1px solid #112233;margin-bottom:8px;padding:10px;cursor:pointer;transition:0.3s;border-radius:4px}.card:active{transform:scale(0.98)}.card:hover{border-color:var(--b);transform:translateX(3px)}.intel-box{display:none;color:var(--g);font-size:11px;white-space:pre-wrap;margin-top:8px;border-top:1px dashed #224466;padding-top:6px}.stat-row{margin-bottom:8px;font-size:10px}.stat-bar{height:4px;background:#050505;border:1px solid #111;margin-top:3px;border-radius:2px;overflow:hidden}.stat-fill{height:100%;width:0%;background:var(--b);transition:0.8s}.term-input-box{background:#000;border-top:1px solid #1a2a3a;padding:8px;display:flex}#term-cmd{background:transparent;border:none;color:var(--g);width:100%;outline:none;font-size:12px;font-family:inherit}@media(max-width:768px){#term-cmd{font-size:14px}}.log{font-size:10px;margin-bottom:4px;border-left:2px solid transparent;padding-left:5px;word-break:break-word}.log.err{color:var(--r);border-left-color:var(--r)}.log.valid{color:var(--g);border-left-color:var(--g)}.log.sys-blue{color:var(--b);border-left-color:var(--b)}#secret-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.98);z-index:9999;display:none;align-items:center;justify-content:center}.secret-ui{width:95%;max-width:1000px;height:90%;border:2px solid var(--r);background:#050000;padding:20px;overflow-y:auto;box-shadow:0 0 80px var(--r);border-radius:8px}@media(min-width:769px){.secret-ui{padding:40px}}.glitch-text{animation:glitch 0.3s infinite;color:var(--r);font-size:18px;text-align:center;margin-bottom:10px}@media(min-width:769px){.glitch-text{font-size:28px}}@keyframes glitch{0%{transform:translate(0)}20%{transform:translate(-3px,3px)}40%{transform:translate(-3px,-3px)}60%{transform:translate(3px,3px)}80%{transform:translate(3px,-3px)}100%{transform:translate(0)}}.secret-grid{display:grid;grid-template-columns:1fr;gap:15px;margin-top:15px}@media(min-width:769px){.secret-grid{grid-template-columns:1fr 1fr;gap:25px}}.secret-box{border:1px solid var(--r);padding:15px;background:rgba(50,0,0,0.3);color:var(--r);border-radius:6px}@media(min-width:769px){.secret-box{padding:20px}}.secret-box h3{margin:0 0 10px 0;font-size:13px}@media(min-width:769px){.secret-box h3{font-size:16px}}.secret-box p{margin:6px 0;font-size:10px}@media(min-width:769px){.secret-box p{font-size:12px}}.btn-close{margin-top:20px;background:var(--r);color:#fff;border:2px solid #fff;padding:10px 25px;font-family:monospace;cursor:pointer;font-size:13px;border-radius:4px;display:block;margin-left:auto;margin-right:auto}@media(min-width:769px){.btn-close{font-size:16px;padding:12px 35px}}.btn-close:hover{background:#fff;color:#000}</style></head><body ontouchstart=""><canvas id="matrix"></canvas><div id="secret-overlay"><div class="secret-ui"><h1 class="glitch-text">⚠ 78921secret_PANDORA ⚠</h1><div class="secret-grid"><div class="secret-box"><h3>🔴 SHADOW PROJECTS</h3><p>▸ PROJECT_OMEGA: Neural Overwrite v4.2</p><p>▸ SKYFALL: Kinetic Orbital Strike</p><p>▸ QUANTUM_VIRUS: SWIFT Backdoor</p><p>▸ DARK_EYE: Global Face Tracking</p><p>▸ GHOST_NET: Underground Internet</p><p>▸ MINDFORGE: Brain-Computer Weapon</p></div><div class="secret-box"><h3>🎯 BIOMETRIC TARGETS</h3><p>▸ HASH: 0x9928AF11BC7 (VERIFIED)</p><p>▸ STATUS: ACTIVE_SURVEILLANCE_24/7</p><p>▸ BRAIN_WAVE: DELTA_STASIS</p><p>▸ LOCATION: [REDACTED]</p><p>▸ THREAT: CRITICAL_ALPHA</p><p>▸ EXTRACTION: GREEN_LIGHT</p></div><div class="secret-box"><h3>☢ CLASSIFIED OPS</h3><p>▸ BLACK_SUN: Solar Weapon System</p><p>▸ DEEP_ABYSS: Ocean Floor Bases</p><p>▸ SILENT_THUNDER: EMP Strike</p><p>▸ CRIMSON_TIDE: Bio Warfare</p><p>▸ IRON_PHOENIX: DNA Cloning</p><p>▸ VOID_WALKER: Dimensional Gateway</p></div><div class="secret-box"><h3>🌐 CONTROL NODES</h3><p>▸ NODE_ALPHA: Brussels Shadow Command</p><p>▸ NODE_BETA: Beijing Quantum Net</p><p>▸ NODE_GAMMA: Moscow Dark Web</p><p>▸ NODE_DELTA: Washington Deep State</p><p>▸ NODE_EPSILON: Tel Aviv Unit 8200</p><p>▸ NODE_ZETA: London City Finance</p></div><div class="secret-box"><h3>⚡ WEAPONS SYSTEMS</h3><p>▸ HAARP_OMEGA: Weather manipulation</p><p>▸ BLUE_BEAM: Holographic projection</p><p>▸ STUXNET_V9: Industrial sabotage</p><p>▸ NEURAL_DUST: Nano-surveillance</p></div><div class="secret-box"><h3>📡 INTELLIGENCE NETS</h3><p>▸ ECHELON_PLUS: Total global intercept</p><p>▸ PRISM_INFINITY: Silicon Valley backdoors</p><p>▸ CARNIVORE_X: Deep packet inspection</p><p>▸ TEMPEST_SHADOW: EM eavesdropping</p></div></div><button class="btn-close" onclick="closeSecret()">🔒 PURGE & EXIT 🔒</button></div></div><div><header><div style="font-size:16px;color:var(--b);font-weight:bold">GGI_OS_v21</div><div id="clock" style="color:var(--b);font-size:14px">00:00:00</div></header><main><div class="panel"><div class="panel-h"><span>SYSTEM</span><span style="color:var(--g)">[OK]</span></div><div class="scroll-area"><div class="stat-row"><div>CPU</div><div class="stat-bar"><div id="cpu-fill" class="stat-fill"></div></div></div><div class="stat-row"><div>RAM</div><div class="stat-bar"><div id="ram-fill" class="stat-fill"></div></div></div><div class="stat-row"><div>SYNC</div><div class="stat-bar"><div id="sync-fill" class="stat-fill"></div></div></div></div><div class="term-input-box"><span style="color:var(--g);margin-right:8px">root@ggi:~#</span><input type="text" id="term-cmd" placeholder="Komut (help)" autocomplete="off"></div></div><div class="panel"><div class="panel-h"><span>INTELLIGENCE</span></div><div class="scroll-area">{% for item in data %}<div class="card" onclick="openD({{loop.index}})"><div style="color:var(--b);font-weight:bold;font-size:12px">{{item.n}}</div><div class="intel-box" id="box-{{loop.index}}" data-raw="{{item.i}}"></div></div>{% endfor %}</div></div><div class="panel"><div class="panel-h"><span>LOGS</span></div><div class="scroll-area" id="log-container"></div></div></main></div><script>function openD(id){const b=document.getElementById('box-'+id);if(b.style.display==='block'){b.style.display='none';return}b.style.display='block';if(b.innerHTML===""){const r=b.getAttribute('data-raw');let i=0;function t(){if(i<r.length){b.innerHTML+=r.charAt(i);i++;setTimeout(t,3)}}t()}}function closeSecret(){document.getElementById('secret-overlay').style.display='none'}document.getElementById('term-cmd').addEventListener('keypress',function(e){if(e.key==='Enter'){const c=this.value.trim();addLog(c,"sys-blue");if(c.toLowerCase()==="78921secret"){document.getElementById('secret-overlay').style.display='flex';addLog("ACCESSING PANDORA","err")}else if(c.toLowerCase()==="help"){addLog("KOMUTLAR: help, clear, status, 78921secret","valid")}else if(c.toLowerCase()==="clear"){document.getElementById('log-container').innerHTML=''}else if(c.toLowerCase()==="status"){addLog("ALL SYSTEMS OK","valid")}else{addLog("ERROR: Unknown '"+c+"'","err")}this.value=''}});function addLog(m,t="valid"){const c=document.getElementById('log-container');const d=document.createElement('div');d.className='log '+t;d.innerText="["+new Date().toLocaleTimeString()+"] "+m;c.appendChild(d);c.scrollTop=c.scrollHeight;if(c.childNodes.length>50)c.removeChild(c.firstChild)}const cv=document.getElementById('matrix');const ctx=cv.getContext('2d');cv.width=window.innerWidth;cv.height=window.innerHeight;const drops=Array(Math.floor(cv.width/18)).fill(1);function drawMatrix(){ctx.fillStyle="rgba(0,0,0,0.08)";ctx.fillRect(0,0,cv.width,cv.height);ctx.fillStyle="#0F0";ctx.font="15px monospace";drops.forEach((y,i)=>{ctx.fillText(String.fromCharCode(0x30A0+Math.random()*96),i*18,y*18);if(y*18>cv.height&&Math.random()>0.975)drops[i]=0;drops[i]++})}setInterval(drawMatrix,50);setInterval(()=>{document.getElementById('clock').innerText=new Date().toLocaleTimeString()},1000);setInterval(()=>{['cpu-fill','ram-fill','sync-fill'].forEach(id=>{document.getElementById(id).style.width=(Math.random()*40+60)+"%"})},1500);setInterval(()=>{const msgs=[{m:"VPN_ESTABLISHED",t:"sys-blue"},{m:"FIREWALL_BLOCKED",t:"err"},{m:"DB_SYNCED",t:"valid"}];const item=msgs[Math.floor(Math.random()*msgs.length)];addLog(item.m,item.t)},5000)</script></body></html>'''

@app.route('/health')
def health():
    return jsonify({"status":"OK"})

@app.route('/')
def index():
    with app.app_context():
        db.create_all()
        if not SystemUser.query.filter_by(username="ADMİN_EGE").first():
            db.session.add(SystemUser(username="ADMİN_EGE",password=generate_password_hash("supreme2025")))
            db.session.commit()
    return render_template_string(get_html(), data=ALL_DATA)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
