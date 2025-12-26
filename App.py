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
    "TÜRKİYE": "[KOZMİK SEVİYE]\nANALİZ: Bölgesel Güç Projeksiyonu.\n- İHA/SİHA: Dünya lideri otonom sistemler.\n- HAVA SAVUNMA: Çelik Kubbe (SİPER-2, HİSAR-U).\n- DENİZ: TCG Anadolu ve TF-2000 projesi.\n- SİBER: Milli Muharip İşlemci ve Kuantum Kripto.\n- UZAY: Yerli roket motoru ve ay görevi faz-1.\n- EKONOMİ: Savunma ihracatı 6 milyar dolar.\n- DİPLOMASİ: 5 kıtada aktif askeri varlık.",
    "ABD": "[TOP SECRET]\nANALİZ: Küresel Dominans.\n- NÜKLEER: 11 Uçak gemisi, Trident-II füzeleri.\n- SİBER: NSA küresel dinleme ve sıfır-gün açıkları.\n- EKONOMİ: Rezerv para birimi manipülasyonu.\n- TEKNOLOJİ: Starlink v3 ve Mars kolonizasyon hazırlığı.\n- UZAY: Space Force operasyonel üstünlük.\n- ASKERİ: 750+ denizaşırı askeri üs.\n- BÜTÇE: 877 milyar dolar savunma harcaması.",
    "RUSYA": "[SIGMA-9]\nANALİZ: Stratejik Caydırıcılık.\n- FÜZE: Zircon (Mach 9), Avangard.\n- ENERJİ: Gazprom üzerinden jeopolitik baskı.\n- SİBER: GRU siber harp ve dezenformasyon ağları.\n- ARKTİK: Buzkıran filosu ve Kuzey Deniz yolu kontrolü.\n- NÜKLEER: 5977 nükleer başlık envanteri.\n- HAVA: Su-57 Felon 5. nesil savaş uçağı.\n- DENİZ: Poseidon nükleer torpido sistemi.",
    "ÇİN": "[RED-DRAGON]\nANALİZ: Ekonomik Hegemonya.\n- ÜRETİM: Dünyanın sanayi motoru.\n- TEKNOLOJİ: 6G ve Kuantum haberleşme uyduları.\n- DONANMA: Tip 004 nükleer uçak gemisi projesi.\n- SOSYAL: Yapay zeka destekli gözetim toplumu.\n- EKONOMİ: 17.9 trilyon dolar GSYİH.\n- UZAY: Tiangong uzay istasyonu operasyonel.\n- ASKERİ: 2 milyon aktif personel.",
    "İNGİLTERE": "[MI6-ALPHA]\nANALİZ: Finansal İstihbarat.\n- SİBER: GCHQ veri toplama merkezleri.\n- DONANMA: Astute sınıfı nükleer denizaltılar.\n- DİPLOMASİ: Commonwealth üzerinden yumuşak güç.\n- HAVA: F-35B Lightning II filosu.\n- İSTİHBARAT: Five Eyes ağı kurucu üyesi.\n- NÜKLEER: Vanguard sınıfı SSBN platformu.",
}

DETAILED_META = {
    "JAPONYA": "Yüksek Teknoloji: Robotik ve yarı iletken hakimiyeti.",
    "HİNDİSTAN": "Nükleer Üçlü: Agni-V ICBM kapasitesi.",
    "GÜNEY KORE": "K2 Black Panther tank ihracatı.",
    "İRAN": "Asimetrik Güç: Balistik füze envanteri.",
    "PAKİSTAN": "Nükleer Caydırıcılık: Shaheen serisi füzeler.",
}

OTHER_COUNTRIES = list(DETAILED_META.keys())
for c in OTHER_COUNTRIES:
    if c not in STRATEGIC_INTEL:
        STRATEGIC_INTEL[c] = f"[DOSYA: {c[:3]}-2025]\nPuan: {random.randint(40,95)}\n{DETAILED_META[c]}"

ALL_DATA = [{"n": f"{k} ANALİZ", "i": v} for k, v in STRATEGIC_INTEL.items()]

UI_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>GGI_OS_v21</title>
<style>
:root{--b:#00f2ff;--g:#39ff14;--r:#f05;--bg:#010203;--p:rgba(10,25,45,0.9)}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body,html{margin:0;padding:0;background:var(--bg);color:#fff;font-family:'Courier New',monospace;height:100vh;overflow:hidden}
#matrix{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;opacity:0.15}
header{height:50px;border-bottom:2px solid var(--b);display:flex;align-items:center;justify-content:space-between;padding:0 15px;background:#000}
main{display:grid;grid-template-columns:1fr;gap:10px;padding:10px;height:calc(100vh - 50px);overflow-y:auto}
@media(min-width:768px){main{grid-template-columns:300px 1fr 350px;overflow-y:hidden}}
.panel{background:var(--p);border:1px solid #1a2a3a;display:flex;flex-direction:column;border-radius:6px;margin-bottom:10px}
.panel-h{background:linear-gradient(90deg,#0a111a,#1a2a3a);padding:12px;color:var(--b);font-size:13px;font-weight:bold;border-bottom:2px solid #1a2a3a;display:flex;justify-content:space-between}
.scroll-area{flex:1;overflow-y:auto;padding:12px}
.card{background:rgba(5,15,25,0.8);border:1px solid #112233;margin-bottom:10px;padding:12px;cursor:pointer;transition:0.3s}
.card:hover{border-color:var(--b);transform:translateX(5px)}
.intel-box{display:none;color:var(--g);font-size:12px;white-space:pre-wrap;margin-top:10px;border-top:1px dashed #224466;padding-top:8px}
.stat-row{margin-bottom:10px;font-size:11px}
.stat-bar{height:5px;background:#050505;border:1px solid #111;margin-top:4px}
.stat-fill{height:100%;width:0%;background:var(--b);transition:0.8s}
.term-input-box{background:#000;border-top:1px solid #1a2a3a;padding:10px;display:flex}
#term-cmd{background:transparent;border:none;color:var(--g);width:100%;outline:none;font-size:13px;font-family:inherit}
.log{font-size:11px;margin-bottom:5px;border-left:2px solid transparent;padding-left:6px}
.log.err{color:var(--r);border-left-color:var(--r)}
.log.valid{color:var(--g);border-left-color:var(--g)}
.log.sys-blue{color:var(--b);border-left-color:var(--b)}
#secret-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.95);z-index:9999;display:none;align-items:center;justify-content:center}
.secret-ui{width:90%;max-width:900px;height:85%;border:1px solid var(--r);background:#050000;padding:30px;overflow-y:auto}
.glitch-text{animation:glitch 0.2s infinite;color:var(--r);font-size:20px}
@keyframes glitch{0%{transform:translate(0)}20%{transform:translate(-2px,2px)}40%{transform:translate(-2px,-2px)}60%{transform:translate(2px,2px)}80%{transform:translate(2px,-2px)}100%{transform:translate(0)}}
.secret-grid{display:grid;grid-template-columns:1fr;gap:20px;margin-top:20px}
@media(min-width:768px){.secret-grid{grid-template-columns:1fr 1fr}}
.secret-box{border:1px solid var(--r);padding:20px;background:rgba(50,0,0,0.2);color:var(--r)}
.btn-close{margin-top:20px;background:var(--r);color:#fff;border:1px solid #fff;padding:10px 25px;font-family:monospace;cursor:pointer}
</style>
</head>
<body onclick="initAudio()">
<canvas id="matrix"></canvas>
<div id="secret-overlay">
<div class="secret-ui">
<h1 class="glitch-text">78921secret_PANDORA</h1>
<div class="secret-grid">
<div class="secret-box"><h3>SHADOW_PROJECTS</h3><p>PROJECT_OMEGA: Neural Overwrite v4.2</p><p>SKYFALL: Kinetic Orbital Strike</p><p>QUANTUM_VIRUS: SWIFT Backdoor</p></div>
<div class="secret-box"><h3>BIOMETRIC_TARGETS</h3><p>HASH: 0x9928AF11</p><p>STATUS: ACTIVE_SURVEILLANCE</p><p>LOCATION: [REDACTED]</p></div>
</div>
<button class="btn-close" onclick="closeSecret()">CLOSE</button>
</div>
</div>
<div>
<header>
<div style="font-size:18px;color:var(--b);font-weight:bold">GGI_OS_v21</div>
<div id="clock" style="color:var(--b);font-size:16px">00:00:00</div>
</header>
<main>
<div class="panel">
<div class="panel-h"><span>SYSTEM</span><span style="color:var(--g)">[OK]</span></div>
<div class="scroll-area">
<div class="stat-row"><div>CPU</div><div class="stat-bar"><div id="cpu-fill" class="stat-fill"></div></div></div>
<div class="stat-row"><div>RAM</div><div class="stat-bar"><div id="ram-fill" class="stat-fill"></div></div></div>
<div class="stat-row"><div>SYNC</div><div class="stat-bar"><div id="sync-fill" class="stat-fill"></div></div></div>
</div>
<div class="term-input-box">
<span style="color:var(--g);margin-right:8px">root@ggi:~#</span>
<input type="text" id="term-cmd" placeholder="Komut (help)" autocomplete="off">
</div>
</div>
<div class="panel">
<div class="panel-h"><span>INTELLIGENCE</span></div>
<div class="scroll-area">
{% for item in data %}
<div class="card" onclick="openD({{loop.index}})">
<div style="color:var(--b);font-weight:bold;font-size:13px">{{item.n}}</div>
<div class="intel-box" id="box-{{loop.index}}" data-raw="{{item.i}}"></div>
</div>
{% endfor %}
</div>
</div>
<div class="panel">
<div class="panel-h"><span>LOGS</span></div>
<div class="scroll-area" id="log-container"></div>
</div>
</main>
</div>
<script>
let audioCtx=null;
function initAudio(){if(!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)()}
function playTone(f,d){if(!audioCtx)return;const o=audioCtx.createOscillator();const g=audioCtx.createGain();o.frequency.value=f;g.gain.value=0.03;o.connect(g);g.connect(audioCtx.destination);o.start();o.stop(audioCtx.currentTime+d)}
function openD(id){const box=document.getElementById('box-'+id);if(box.style.display==='block'){box.style.display='none';return}box.style.display='block';playTone(880,0.05);if(box.innerHTML===""){const raw=box.getAttribute('data-raw');let i=0;function type(){if(i<raw.length){box.innerHTML+=raw.charAt(i);i++;setTimeout(type,3)}}type()}}
function closeSecret(){document.getElementById('secret-overlay').style.display='none'}
document.getElementById('term-cmd').addEventListener('keypress',function(e){if(e.key==='Enter'){const cmd=this.value.trim();addLog(cmd,"sys-blue");if(cmd.toLowerCase()==="78921secret"){document.getElementById('secret-overlay').style.display='flex';addLog("ACCESSING PANDORA","err");playTone(200,0.5)}else if(cmd.toLowerCase()==="help"){addLog("KOMUTLAR: help, clear, status, 78921secret","valid")}else if(cmd.toLowerCase()==="clear"){document.getElementById('log-container').innerHTML=''}else if(cmd.toLowerCase()==="status"){addLog("ALL SYSTEMS OK","valid")}else{addLog("ERROR: Unknown '"+cmd+"'","err")}this.value='';playTone(600,0.05)}});
function addLog(msg,type="valid"){const c=document.getElementById('log-container');const d=document.createElement('div');d.className='log '+type;d.innerText="["+new Date().toLocaleTimeString()+"] "+msg;c.appendChild(d);c.scrollTop=c.scrollHeight;if(c.childNodes.length>50)c.removeChild(c.firstChild)}
const canvas=document.getElementById('matrix');const ctx=canvas.getContext('2d');canvas.width=window.innerWidth;canvas.height=window.innerHeight;const drops=Array(Math.floor(canvas.width/18)).fill(1);
function drawMatrix(){ctx.fillStyle="rgba(0,0,0,0.08)";ctx.fillRect(0,0,canvas.width,canvas.height);ctx.fillStyle="#0F0";ctx.font="15px monospace";drops.forEach((y,i)=>{ctx.fillText(String.fromCharCode(0x30A0+Math.random()*96),i*18,y*18);if(y*18>canvas.height&&Math.random()>0.975)drops[i]=0;drops[i]++})}
setInterval(drawMatrix,50);
setInterval(()=>{document.getElementById('clock').innerText=new Date().toLocaleTimeString()},1000);
setInterval(()=>{['cpu-fill','ram-fill','sync-fill'].forEach(id=>{document.getElementById(id).style.width=(Math.random()*40+60)+"%"})},1500);
setInterval(()=>{const msgs=[{m:"VPN_ESTABLISHED",t:"sys-blue"},{m:"FIREWALL_BLOCKED",t:"err"},{m:"DB_SYNCED",t:"valid"}];const item=msgs[Math.floor(Math.random()*msgs.length)];addLog(item.m,item.t)},5000);
</script>
</body>
</html>"""

def process_system_heartbeat(): return math.sin(time.time())*100
def calculate_encryption_entropy(d): return len(set(d))/len(d) if d else 0.99
def validate_root_access(t): return t==base64.b64encode("ADMİN_EGE".encode('utf-8'))
def rotate_security_keys(): return "".join([random.choice("ABCDEF0123456789") for _ in range(32)])
def monitor_thermal_levels(): return random.uniform(35.5,72.4)
def optimize_neural_network(): return "OPTIMIZED"
def log_kernel_event(e,d): return f"[{datetime.datetime.now()}] KERNEL_{e}: {d}"
def check_database_integrity(): 
    try: return SystemUser.query.count()>=0
    except: return False
def generate_noise_buffer(): return [random.random() for _ in range(100)]
def execute_cyber_defense_v21(): return f"DEFENSE_ACTIVE_{calculate_encryption_entropy('GGI')}"
def sys_init_core_01(): return "CORE_ACTIVE"
def sys_init_core_02(): return "MEMORY_READY"
def sys_init_core_03(): return "IO_BUFFERED"
def sys_init_core_04(): return "THREAD_SYNC"
def sys_init_core_05(): return "SOCKET_OPEN"
def layer_check_06(): return "L06_OK"
def layer_check_07(): return "L07_OK"
def layer_check_08(): return "L08_OK"
def layer_check_09(): return "L09_OK"
def layer_check_10(): return "L10_OK"

@app.route('/health')
def health():
    return jsonify({"status":"OK","id":"GGI-v21"})

@app.route('/')
def index():
    with app.app_context():
        db.create_all()
        if not SystemUser.query.filter_by(username="ADMİN_EGE").first():
            db.session.add(SystemUser(username="ADMİN_EGE",password=generate_password_hash("supreme2025"),access_level="ROOT"))
            db.session.commit()
    return render_template_string(UI_TEMPLATE, data=ALL_DATA)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
