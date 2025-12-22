from flask import Flask
import os

app = Flask(__name__)

STYLE = """
<style>
    body { font-family: 'Times New Roman', serif; background-color: #f0f2f5; margin: 0; display: flex; flex-direction: row; color: #333; }
    
    /* Mobil Uyumluluk Ayarı */
    @media (max-width: 1024px) {
        body { flex-direction: column; }
        .sidebar-left, .sidebar-right { position: relative !important; width: 100% !important; height: auto !important; margin: 0 !important; }
        .main-content { margin: 0 !important; padding: 15px !important; }
        .grid { grid-template-columns: 1fr 1fr !important; }
    }

    .sidebar-left { width: 300px; background: #2c3e50; color: white; height: 100vh; padding: 20px; position: fixed; left: 0; overflow-y: auto; z-index: 10; box-sizing: border-box; }
    .sidebar-right { width: 300px; background: #ecf0f1; color: #2c3e50; height: 100vh; padding: 20px; position: fixed; right: 0; overflow-y: auto; border-left: 4px solid #bdc3c7; box-sizing: border-box; }
    .main-content { margin-left: 320px; margin-right: 320px; padding: 40px; flex-grow: 1; display: flex; justify-content: center; }
    
    .container { background: white; padding: 25px; border-radius: 12px; shadow: 0 4px 20px rgba(0,0,0,0.1); width: 100%; max-width: 800px; }
    
    /* Hesap Makinesi & Oyun */
    .tool-box { background: #34495e; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
    #display { background:#222; color:#0f0; padding:10px; text-align:right; margin-bottom:5px; border-radius:4px; font-family:monospace; height:20px; }
    .calc-btn { width:100%; padding:10px; background:#444; border:none; color:white; border-radius:4px; cursor:pointer; }
    
    #game-container { width: 100%; height: 120px; background: #111; position: relative; overflow: hidden; border-radius: 8px; cursor: pointer; }
    #player { width: 20px; height: 20px; background: #e74c3c; position: absolute; bottom: 0; left: 20px; border-radius: 4px; }
    .obstacle { width: 15px; height: 15px; background: #f1c40f; position: absolute; bottom: 0; right: -20px; }

    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px; }
    .card { background: #fff; border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-decoration: none; text-align: center; color: #2c3e50; display: block; }
    .typing-text { line-height: 1.7; font-size: 16px; background: #fffdf9; padding: 20px; border-left: 5px solid #c0392b; white-space: pre-wrap; min-height: 100px; }
</style>

<script>
    // Oyun ve Hesap Makinesi Fonksiyonları
    function addToCalc(v) { document.getElementById('display').innerText += v; }
    function clearCalc() { document.getElementById('display').innerText = ''; }
    function solveCalc() { try { document.getElementById('display').innerText = eval(document.getElementById('display').innerText); } catch { document.getElementById('display').innerText = 'Hata'; } }

    let gameStarted = false; let score = 0;
    function startGame() { 
        if(gameStarted) { jump(); return; }
        gameStarted = true;
        document.getElementById('start-msg').style.display = 'none';
        setInterval(createObs, 2000);
    }
    function jump() {
        let p = document.getElementById('player');
        p.style.bottom = '60px';
        setTimeout(() => { p.style.bottom = '0px'; }, 300);
    }
    function createObs() {
        let container = document.getElementById('game-container');
        let obs = document.createElement('div');
        obs.className = 'obstacle';
        container.appendChild(obs);
        let pos = 0;
        let t = setInterval(() => {
            pos += 4; obs.style.right = pos + 'px';
            if(pos > 240 && pos < 270 && parseInt(document.getElementById('player').style.bottom) < 15) {
                alert('Oyun Bitti! Skor: ' + score); location.reload();
            }
            if(pos > 300) { clearInterval(t); obs.remove(); score++; document.getElementById('score').innerText = score; }
        }, 20);
    }

    // YAZI YÜKLENME SORUNUNU ÇÖZEN FONKSİYON
    function typeWriter(text) {
        let i = 0;
        let target = document.getElementById("target");
        if(!target) return; // Eğer alan yoksa hata verme, dur.
        target.innerHTML = "";
        function type() {
            if (i < text.length) {
                target.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, 20);
            }
        }
        type();
    }
</script>
"""

def layout(content):
    sidebar_left = f"""
    <div class="sidebar-left">
        <h3>🛠️ ARAÇLAR</h3>
        <div class="tool-box">
            <div id="display"></div>
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:5px;">
                <button class="calc-btn" onclick="addToCalc('7')">7</button><button class="calc-btn" onclick="addToCalc('8')">8</button><button class="calc-btn" onclick="addToCalc('9')">9</button><button class="calc-btn" onclick="addToCalc('/')">/</button>
                <button class="calc-btn" onclick="clearCalc()">C</button><button class="calc-btn" onclick="addToCalc('0')">0</button><button class="calc-btn" onclick="solveCalc()">=</button><button class="calc-btn" onclick="addToCalc('+')">+</button>
            </div>
        </div>
        <div id="game-container" onclick="startGame()">
            <div id="start-msg" style="color:white; text-align:center; padding-top:40px;">BAŞLAT (TIKLA)</div>
            <div id="score" style="color:white; position:absolute; top:5px; right:5px;">0</div>
            <div id="player" style="bottom:0px;"></div>
        </div>
    </div>
    """
    sidebar_right = """
    <div class="sidebar-right">
        <h3>🏛️ TARİHÇE</h3>
        <p><b>🇹🇷 Türkiye:</b> 1923 - Cumhuriyet Devrimi</p>
        <p><b>🕌 Osmanlı:</b> 1453 - İstanbul'un Fethi</p>
        <p><b>🏛️ Roma:</b> MÖ 44 - İmparatorluk Geçişi</p>
    </div>
    """
    return f"{STYLE} {sidebar_left} {sidebar_right} <div class='main-content'>{content}</div>"

@app.route("/")
def home():
    content = """
    <div class="container">
        <h1>📜 Dünya Tarih Arşivi</h1>
        <div class="grid">
            <a href="/turkiye" class="card">🇹🇷 Türkiye</a>
            <a href="/osmanli" class="card">🕌 Osmanlı</a>
            <a href="/roma" class="card">🏛️ Roma</a>
            <a href="/almanya" class="card">🇩🇪 Almanya</a>
        </div>
    </div>
    """
    return layout(content)

@app.route("/turkiye")
def turkiye():
    t = "Türkiye Cumhuriyeti, 1923 yılında Mustafa Kemal Atatürk önderliğinde kurulmuştur. Cumhuriyetin ilanı, Türk milletinin tarihindeki en büyük modernleşme devrimidir."
    return layout(f'<div class="container"><h2>🇹🇷 Türkiye Cumhuriyeti</h2><div id="target" class="typing-text"></div><a href="/">← Geri Dön</a></div><script>setTimeout(() => {{ typeWriter("{t}"); }}, 500);</script>')

@app.route("/osmanli")
def osmanli():
    t = "Osmanlı İmparatorluğu 1299 yılında Söğüt'te kurulmuştur. 1453 yılında İstanbul'un fethi ile bir dünya imparatorluğu haline gelmiştir."
    return layout(f'<div class="container"><h2>🕌 Osmanlı İmparatorluğu</h2><div id="target" class="typing-text"></div><a href="/">← Geri Dön</a></div><script>setTimeout(() => {{ typeWriter("{t}"); }}, 500);</script>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
