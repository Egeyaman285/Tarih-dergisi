from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SHADOW RP | ULTIMATE TERMINAL V13</title>
    <style>
        :root { --red: #ff0000; --green: #00ff41; --bg: #050505; --blue: #00d4ff; --gold: #ffd700; --white: #ffffff; }
        * { box-sizing: border-box; cursor: crosshair; }
        body { background: var(--bg); color: #ccc; font-family: 'Courier New', monospace; margin: 0; overflow-x: hidden; }
        
        .bg-overlay { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 40%; opacity: 0.03; z-index: -1; pointer-events: none; }
        .shadow-tag { position: fixed; top: 20px; right: 30px; color: var(--red); font-weight: bold; font-size: 1.5rem; text-shadow: 0 0 10px var(--red); z-index: 2000; }

        .start-screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 5000; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .start-btn { padding: 20px 50px; background: none; border: 2px solid var(--red); color: var(--red); font-family: 'Courier New'; font-size: 1.5rem; cursor: pointer; transition: 0.3s; }
        .start-btn:hover { background: var(--red); color: white; box-shadow: 0 0 30px var(--red); }

        .terminal-header { background: rgba(0,0,0,0.95); border-bottom: 4px solid var(--red); padding: 30px; text-align: center; position: sticky; top: 0; z-index: 1500; }
        .auth-input { background: #000; border: 2px solid var(--red); color: var(--red); padding: 15px; width: 80%; max-width: 600px; margin: 15px auto; display: block; outline: none; text-align: center; font-size: 1.1rem; }

        .main-container { max-width: 900px; margin: 30px auto; padding: 20px; }

        .branch-box { background: rgba(10,10,10,0.98); border: 2px solid var(--blue); border-left: 10px solid var(--blue); padding: 25px; margin-bottom: 40px; display: none; }
        .o5-box { border-color: var(--gold); border-right: 10px solid var(--gold); }
        .title { font-size: 1.8rem; color: var(--white); border-bottom: 1px solid #333; margin-bottom: 20px; padding-bottom: 10px; font-weight: bold; }
        .desc { color: var(--green); font-size: 1rem; line-height: 1.6; white-space: pre-wrap; }

        .scp-folder { background: #0d0d0d; border: 1px solid #222; border-left: 5px solid var(--red); padding: 12px 20px; margin-bottom: 10px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; transition: 0.2s; }
        .scp-folder:hover { background: #151515; border-color: var(--red); transform: translateX(10px); }
        .scp-details { background: #000; border: 1px solid var(--red); border-top: none; border-left: 5px solid var(--red); padding: 20px; margin-bottom: 15px; display: none; color: var(--green); font-size: 0.9rem; animation: fadeIn 0.3s; }

        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .badge { padding: 2px 8px; font-size: 0.7rem; font-weight: bold; color: white; border-radius: 3px; }
        .badge-safe { background: #2ecc71; } .badge-euclid { background: #f1c40f; color: #000; } 
        .badge-keter { background: #e74c3c; } .badge-thaumiel { background: #9b59b6; }
        .badge-apollyon { background: #000; border: 1px solid var(--red); color: var(--red); animation: pulse 1s infinite; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <div id="startScreen" class="start-screen">
        <div style="color:var(--red); margin-bottom:20px; letter-spacing:5px;">SITE-SHADOW VERI TABANI</div>
        <button class="start-btn" onclick="initSystem()">SİSTEMİ BAŞLAT</button>
    </div>

    <div class="shadow-tag">SHADOW RP</div>
    <svg class="bg-overlay" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
        <path fill="red" d="M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256 256-114.6 256-256S397.4 0 256 0zm0 472c-119.3 0-216-96.7-216-216S136.7 40 256 40s216 96.7 216 216-96.7 216-216 216z"/><circle fill="red" cx="256" cy="256" r="40"/>
    </svg>

    <div class="terminal-header">
        <h1 style="color:var(--red); margin:0; letter-spacing: 5px;">SECURE TERMINAL V13</h1>
        <input type="password" id="passInput" class="auth-input" placeholder="YETKİ ANAHTARI GİRİNİZ...">
        <div id="status" style="color:var(--blue); font-size: 0.8rem; margin-top:10px;">STATUS: OFFLINE</div>
    </div>

    <div class="main-container">
        <div id="SEC-B" class="branch-box"><div class="title">GÜVENLİK DEPARTMANI</div><div id="sec-text" class="desc"></div></div>
        <div id="ENG-B" class="branch-box"><div class="title">MÜHENDİSLİK BİRİMİ</div><div id="eng-text" class="desc"></div></div>
        <div id="ETH-B" class="branch-box"><div class="title">ETİK KOMİTE</div><div id="eth-text" class="desc"></div></div>
        <div id="MED-B" class="branch-box"><div class="title">TIBBİ DEPARTMAN</div><div id="med-text" class="desc"></div></div>
        <div id="IGD-B" class="branch-box"><div class="title">İÇ GÜVENLİK (IGD)</div><div id="igd-text" class="desc"></div></div>
        <div id="TME-B" class="branch-box"><div class="title">TAKTIKSEL MÜDAHALE (TME)</div><div id="tme-text" class="desc"></div></div>
        <div id="O5-B" class="branch-box o5-box"><div class="title">O5 KONSEYİ</div><div id="o5-text" class="desc"></div></div>

        <div id="scp-list"></div>
    </div>

    <script>
        // Ses Sentezleyici Ayarı
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playTypeSound() {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'square'; osc.frequency.setValueAtTime(150, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.01, audioCtx.currentTime);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 0.02);
        }

        function initSystem() {
            document.getElementById('startScreen').style.display = 'none';
            audioCtx.resume();
        }

        const DATABASE = {
            "SEC-SHADOW-2026": { id: "SEC-B", txt: "sec-text", access: ["SAFE", "EUCLID"], data: "GÜVENLİK PROTOKOLÜ:\\n- Sadece Safe ve Euclid sınıflarına müdahale yetkisi.\\n- Keter ihlallerinde TME beklenmelidir.\\n- Tesis güvenliği 1. önceliktir." },
            "ENG-TECH-SYS": { id: "ENG-B", txt: "eng-text", access: ["SAFE", "EUCLID", "KETER", "THAUMIEL"], data: "TEKNİK REHBER:\\n- Thaumiel sınıfı muhafaza cihazları kontrol altındadır.\\n- Jeneratör bakımı her 24 saatte bir yapılır." },
            "ETHIC-BOARD-01": { id: "ETH-B", txt: "eth-text", access: ["SAFE", "EUCLID", "KETER", "THAUMIEL", "APOLLYON"], data: "ETİK BİLDİRGE:\\n- Tüm sınıflar üzerinde denetim yetkisi.\\n- Deneylerin insan onuruna uygunluğu izlenir." },
            "MED-DEPT-99": { id: "MED-B", txt: "med-text", access: ["SAFE", "EUCLID", "KETER"], data: "TIBBİ ANALİZ:\\n- Biyolojik sınıflar üzerinde tam yetki.\\n- Personel sağlığı ve amnezik kullanımı bizdedir." },
            "IGD-INTERNAL-00": { id: "IGD-B", txt: "igd-text", access: ["SAFE", "EUCLID", "KETER", "THAUMIEL", "APOLLYON"], data: "İÇ GÜVENLİK DİREKTİFİ:\\n- Vakıf içi hainlerin tespiti.\\n- Tüm departmanlar üzerinde gizli izleme yetkisi." },
            "TME-TACTICAL-X": { id: "TME-B", txt: "tme-text", access: ["SAFE", "EUCLID", "KETER", "THAUMIEL", "APOLLYON"], data: "MÜDAHALE PLANI:\\n- Ağır silahlı operasyon birimi.\\n- Keter ve Apollyon kaçışlarında ana güç." },
            "O5-secsysttem": { id: "O5-B", txt: "o5-text", access: ["SAFE", "EUCLID", "KETER", "THAUMIEL", "APOLLYON"], data: "KONSEY KARARI:\\n- Tam yetki onaylandı.\\n- Gerçeklik sizin ellerinizde." }
        };

        function daktilo(elId, text) {
            const el = document.getElementById(elId); el.innerHTML = ""; let i = 0;
            const timer = setInterval(() => {
                if(i < text.length) {
                    el.innerHTML += text.charAt(i) === "\\n" ? "<br>" : text.charAt(i);
                    playTypeSound(); i++;
                } else { clearInterval(timer); }
            }, 15);
        }

        document.getElementById('passInput').addEventListener('input', (e) => {
            const key = e.target.value;
            if(DATABASE[key]) {
                document.querySelectorAll('.branch-box').forEach(x => x.style.display = 'none');
                document.getElementById(DATABASE[key].id).style.display = 'block';
                daktilo(DATABASE[key].txt, DATABASE[key].data);
                buildList(DATABASE[key].access);
            }
        });

        function buildList(allowed) {
            const scpList = document.getElementById('scp-list');
            scpList.innerHTML = "";
            const classes = ["SAFE", "EUCLID", "KETER", "THAUMIEL", "APOLLYON"];
            
            for(let i=1; i<=50; i++) {
                const sClass = classes[i % 5];
                if(!allowed.includes(sClass)) continue;

                const id = "SCP-" + (i + 100).toString();
                const folder = document.createElement('div');
                folder.className = 'scp-folder';
                folder.innerHTML = `<span>${id}</span> <span class="badge badge-${sClass.toLowerCase()}">${sClass}</span>`;
                
                const det = document.createElement('div');
                det.className = 'scp-details'; det.id = "det-"+id;

                folder.onclick = () => {
                    const open = det.style.display === 'block';
                    document.querySelectorAll('.scp-details').forEach(d => d.style.display = 'none');
                    if(!open) {
                        det.style.display = 'block';
                        const info = `[ANALİZ BAŞLADI]\\n1. SIRA: Nesne muhafazası ${sClass} protokolündedir.\\n2. SIRA: Tesis ${i % 3 === 0 ? 'Site-19' : 'Site-Shadow'} içinde tutulmaktadır.\\n3. SIRA: Yetkisiz personel için amnezik tedavi uygulanır.`;
                        daktilo(det.id, info);
                    }
                };
                scpList.appendChild(folder); scpList.appendChild(det);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
