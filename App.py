from flask import Flask, render_template_string, request
import random
import time

app = Flask(__name__)

# ======================
# SADECE KURGUSAL VERİ
# ======================
SIM_LOGS = []  # basit in-memory kayıt

HTML = """
<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>SIM_CORE</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--g:#39ff14;--b:#00e5ff;--r:#ff355e;--bg:#05080c}
*{box-sizing:border-box;font-family:Courier New,monospace}
body{margin:0;background:var(--bg);color:#e6f7ff}
header{height:48px;border-bottom:1px solid #123;display:flex;align-items:center;justify-content:space-between;padding:0 12px}
main{display:grid;grid-template-columns:1fr 420px;height:calc(100vh - 48px)}
.panel{border-left:1px solid #123;display:flex;flex-direction:column}
.scroll{flex:1;overflow:auto;padding:10px}
#term{background:#02050a}
#out{font-size:12px;color:var(--g)}
.cmd{display:flex;border-top:1px solid #123}
.cmd span{padding:10px;color:var(--g)}
.cmd input{flex:1;background:transparent;border:0;color:var(--g);padding:10px;outline:none}

.overlay{position:fixed;inset:0;background:#000d;display:none;flex-direction:column;padding:16px}
canvas{border:1px solid #234;background:#02050a}
.btn{margin-top:10px;padding:10px;border:1px solid var(--b);background:transparent;color:var(--b);cursor:pointer}
.btn:hover{background:var(--b);color:#000}

.badge{color:var(--r)}
.small{font-size:11px;color:#9bb}
</style>
</head>
<body>
<header>
  <div>SIM_CORE // EDUCATIONAL MODE</div>
  <div id="clock"></div>
</header>

<main>
  <div class="scroll">
    <h3>Bilgi</h3>
    <p class="small">
      Bu uygulama tamamen <b>kurgusaldır</b>. Gerçek yer, hedef, nüfus veya
      “en mantıklı vurulacak yer” analizi içermez.
    </p>
    <ul class="small">
      <li>Komut: <b>bombsimulation</b></li>
      <li>Komut: <b>clear</b></li>
      <li>Komut: <b>logs</b></li>
    </ul>
  </div>

  <div class="panel" id="term">
    <div class="scroll" id="out">Sistem hazır.</div>
    <div class="cmd">
      <span>root@sim:~$</span>
      <input id="cmd" autocomplete="off" placeholder="komut yaz">
    </div>
  </div>
</main>

<div class="overlay" id="sim">
  <h3>☢ Etki Simülasyonu <span class="badge">(KURGUSAL)</span></h3>
  <canvas id="map" width="900" height="420"></canvas>
  <div class="small" id="simlog"></div>
  <button class="btn" onclick="closeSim()">Kapat</button>
</div>

<script>
const out = document.getElementById('out');
const cmd = document.getElementById('cmd');

function log(t,c){
  const d=document.createElement('div');
  if(c) d.style.color=c;
  d.textContent=t;
  out.appendChild(d);
  out.scrollTop=out.scrollHeight;
}

cmd.addEventListener('keypress',e=>{
  if(e.key!=='Enter') return;
  const v=cmd.value.trim().toLowerCase();
  log('> '+v,'#fff');
  cmd.value='';
  if(v==='clear'){ out.innerHTML=''; return; }
  if(v==='bombsimulation'){ openSim(); log('[SIM] Açıldı', 'var(--g)'); return; }
  if(v==='logs'){ fetch('/logs').then(r=>r.json()).then(j=>{
    log('Kayıtlar:','var(--b)');
    j.forEach(x=>log(x,'var(--g)'));
  }); return; }
  log('Geçersiz komut','var(--r)');
});

function openSim(){
  document.getElementById('sim').style.display='flex';
  drawSim();
  beep();
}
function closeSim(){
  document.getElementById('sim').style.display='none';
}

function drawGrid(ctx,w,h){
  ctx.strokeStyle='#0a2';
  for(let x=0;x<w;x+=45){ for(let y=0;y<h;y+=45){ ctx.strokeRect(x,y,45,45); } }
}

function ring(ctx,x,y,r,color){
  ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fillStyle=color; ctx.fill();
}

function drawSim(){
  const c=document.getElementById('map');
  const ctx=c.getContext('2d');
  ctx.clearRect(0,0,c.width,c.height);
  drawGrid(ctx,c.width,c.height);

  const cx=Math.random()*c.width;
  const cy=Math.random()*c.height;

  let step=0;
  const anim=setInterval(()=>{
    step++;
    ctx.clearRect(0,0,c.width,c.height);
    drawGrid(ctx,c.width,c.height);
    if(step>=1) ring(ctx,cx,cy,40,'rgba(255,255,0,.25)');
    if(step>=2) ring(ctx,cx,cy,85,'rgba(255,140,0,.25)');
    if(step>=3) ring(ctx,cx,cy,130,'rgba(255,0,0,.25)');
    if(step>=3) clearInterval(anim);
  },250);

  const txt = "Merkez: YÜKSEK | İkincil: ORTA | Çevre: DÜŞÜK";
  document.getElementById('simlog').textContent = txt;

  fetch('/log', {method:'POST', headers:{'Content-Type':'application/json'},
    body:JSON.stringify({t:txt, ts:Date.now()})});
}

function beep(){
  const ac=new (window.AudioContext||window.webkitAudioContext)();
  const o=ac.createOscillator(); const g=ac.createGain();
  o.type='sine'; o.frequency.value=880;
  g.gain.value=.05; o.connect(g); g.connect(ac.destination);
  o.start(); setTimeout(()=>o.stop(),150);
}

setInterval(()=>document.getElementById('clock').textContent=
  new Date().toLocaleTimeString(),1000);
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/log', methods=['POST'])
def add_log():
    data = request.get_json(force=True)
    SIM_LOGS.append(f"{time.strftime('%H:%M:%S')} | {data.get('t','')}")
    if len(SIM_LOGS) > 50:
        SIM_LOGS.pop(0)
    return {"ok": True}

@app.route('/logs')
def get_logs():
    return SIM_LOGS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
