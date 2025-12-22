from flask import Flask
import os

app = Flask(__name__)

STYLE = """
<style>
    body { font-family: 'Times New Roman', serif; background-color: #f0f2f5; margin: 0; display: flex; color: #333; overflow-x: hidden; }
    
    /* Yan Menü (Sol Sidebar) */
    .sidebar-left { width: 300px; background: #2c3e50; color: white; height: 100vh; padding: 20px; position: fixed; left: 0; overflow-y: auto; box-shadow: 2px 0 10px rgba(0,0,0,0.3); z-index: 10; }
    
    /* Sağ Panel (Tarih Paneli) */
    .sidebar-right { width: 300px; background: #ecf0f1; color: #2c3e50; height: 100vh; padding: 20px; position: fixed; right: 0; overflow-y: auto; box-shadow: -2px 0 10px rgba(0,0,0,0.1); border-left: 4px solid #bdc3c7; }
    
    /* Ana İçerik */
    .main-content { margin-left: 320px; margin-right: 320px; padding: 40px; flex-grow: 1; display: flex; justify-content: center; }
    .container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); width: 100%; max-width: 800px; }
    
    /* Oyun Alanı Geliştirmesi */
    #game-container { width: 100%; height: 150px; background: #111; position: relative; overflow: hidden; border-radius: 8px; border: 2px solid #555; cursor: pointer; }
    #game-start-msg { position: absolute; width: 100%; text-align: center; top: 40%; color: #2ecc71; font-weight: bold; font-family: sans-serif; }
    #player { width: 30px; height: 30px; background: #e74c3c; position: absolute; bottom: 0; left: 20px; border-radius: 4px; }
    .obstacle { width: 20px; height: 20px; background: #f1c40f; position: absolute; bottom: 0; right: -20px; border-radius: 2px; }
    #score { position: absolute; top: 5px; right: 10px; color: white; font-family: monospace; }
    
    /* Araç ve Tarih Kutuları */
    .tool-box { background: #34495e; padding: 12px; border-radius: 8px; margin-bottom: 15px; }
    .history-item { margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid #bdc3c7; font-size: 14px; }
    .history-item b { color: #c0392b; display: block; margin-bottom: 5px; }
    
    /* Kartlar */
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px; }
    .card { background: #fff; border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-decoration: none; text-align: center; color: #2c3e50; font-size: 14px; }
    .card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .card img { width: 40px; margin-bottom: 5px; }

    .typing-text { line-height: 1.6; font-size: 16px; background: #fffdf9; padding: 20px; border-left: 5px solid #c0392b; white-space: pre-wrap; }
</style>

<script>
    // --- HESAP MAKİNESİ ---
    function addToCalc(val) { document.getElementById('display').innerText += val; }
    function clearCalc() { document.getElementById('display').innerText = ''; }
    function solveCalc() { try { document.getElementById('display').innerText = eval(document.getElementById('display').innerText); } catch { document.getElementById('display').innerText = 'Hata'; } }

    // --- GELİŞMİŞ OYUN MANTIĞI ---
    let isJumping = false;
    let score = 0;
    let gameStarted = false;

    function startGame() {
        if (gameStarted) { jump(); return; }
        gameStarted = true;
        document.getElementById("game-start-msg").style.display = "none";
        createObstacle();
    }

    function jump() {
        if (isJumping || !gameStarted) return;
        let player = document.getElementById("player");
        isJumping = true;
        let pos = 0;
        let upTimer = setInterval(() => {
            if (pos >= 80) {
                clearInterval(upTimer);
                let downTimer = setInterval(() => {
                    if (pos <= 0) { clearInterval(downTimer); isJumping = false; }
                    pos -= 5; player.style.bottom = pos + "px";
                }, 20);
            }
            pos += 5; player.style.bottom = pos + "px";
        }, 20);
    }

    function createObstacle() {
        if (!gameStarted) return;
        let container = document.getElementById("game-container");
        let obs = document.createElement("div");
        obs.classList.add("obstacle");
        container.appendChild(obs);
        let obsPos = 0;
        let timer = setInterval(() => {
            obsPos += 5;
            obs.style.right = obsPos + "px";
            
            let playerBottom = parseInt(window.getComputedStyle(document.getElementById("player")).getPropertyValue("bottom"));
            let obsRight = parseInt(obs.style.right);

            if (obsRight > 240 && obsRight < 270 && playerBottom < 20) {
                alert("Enflasyona yenildin! Skor: " + score);
                location.reload(); 
            }

            if (obsPos > 320) {
                clearInterval(timer);
                container.removeChild(obs);
                score++;
                document.getElementById("score").innerText = "Skor: " + score;
            }
        }, 20);
        setTimeout(createObstacle, Math.random() * 2000 + 1000);
    }

    function typeWriter(elementId, text, speed) {
        let i = 0; let el = document.getElementById(elementId);
        function type() { if (i < text.length) { el.innerHTML += text.charAt(i); i++; setTimeout(type, speed); } }
        type();
    }
</script>
"""

def layout(content):
    # Sol Sidebar: Araçlar ve Oyun
    sidebar_left = f"""
    <div class="sidebar-left">
        <h2>🛠️ ARAÇLAR</h2>
        <div class="tool-box">
            <div id="display" style="background:#222; color:#0f0; padding:10px; text-align:right; margin-bottom:5px; border-radius:4px; font-family:monospace; height:20px;"></div>
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:5px;">
                <button onclick="addToCalc('7')">7</button><button onclick="addToCalc('8')">8</button><button onclick="addToCalc('9')">9</button><button onclick="addToCalc('/')">/</button>
                <button onclick="addToCalc('4')">4</button><button onclick="addToCalc('5')">5</button><button onclick="addToCalc('6')">6</button><button onclick="addToCalc('*')">*</button>
                <button onclick="clearCalc()">C</button><button onclick="addToCalc('0')">0</button><button onclick="solveCalc()">=</button><button onclick="addToCalc('+')">+</button>
            </div>
        </div>
        <div class="tool-box">
            <h4>🏃 ENFLASYON KOŞUSU</h4>
            <div id="game-container" onclick="startGame()">
                <div id="game-start-msg">BAŞLATMAK İÇİN TIKLA</div>
                <div id="score">Skor: 0</div>
                <div id="player"></div>
            </div>
        </div>
    </div>
    """
    
    # Sağ Sidebar: Kuruluş ve Devrimler
    sidebar_right = f"""
    <div class="sidebar-right">
        <h2 style="font-size:18px; border-bottom:2px solid #333;">🏛️ TARİH ÇİZELGESİ</h2>
        <div class="history-item"><b>🇹🇷 Türkiye (1923)</b>Cumhuriyet'in ilanı ile büyük bir ekonomik ve sosyal devrim başladı. 1928 Harf Devrimi okuryazarlığı sıçrattı.</div>
        <div class="history-item"><b>🏛️ Antik Roma (M.Ö. 753)</b>Sezar'ın geçişi (M.Ö. 44) Roma'yı cumhuriyetten imparatorluğa taşıyan en büyük devrimdir.</div>
        <div class="history-item"><b>🇩🇪 Almanya (1919)</b>Weimar Devrimi ile monarşi yıkıldı. Ancak 1923 hiperenflasyonu halkı sefalete sürükledi.</div>
        <div class="history-item"><b>🇺🇸 ABD (1776)</b>1776 Bağımsızlık Bildirgesi modern demokrasinin en büyük devrimidir. 1929 Buhranı ise ekonomiyi yıktı.</div>
        <div class="history-item"><b>🇭🇺 Macaristan (895)</b>1848 Macar Devrimi, Avrupa'daki özgürlük ateşinin en büyük parçalarından biriydi.</div>
        <div class="history-item"><b>🕌 Osmanlı (1299)</b>1453 İstanbul'un Fethi, devleti bir imparatorluğa dönüştüren en büyük askeri ve kültürel devrimdir.</div>
    </div>
    """
    
    return f"{STYLE} {sidebar_left} {sidebar_right} <div class='main-content'>{content}</div>"

FLAGS = {
    "OSMANLI": "https://flagcdn.com/w160/tr.png",
    "ALMANYA": "https://flagcdn.com/w160/de.png",
    "TURKIYE": "https://flagcdn.com/w160/tr.png",
    "ROMA": "https://flagcdn.com/w160/it.png",
    "MACARISTAN": "https://flagcdn.com/w160/hu.png",
    "USA": "https://flagcdn.com/w160/us.png"
}

@app.route("/")
def home():
    content = f"""
    <div class="container">
        <h1 style="text-align:center;">📜 Dünya Tarih & Ekonomi Portalı</h1>
        <div class="grid">
            <a href="/osmanli" class="card"><img src="{FLAGS['OSMANLI']}"><br>Osmanlı</a>
            <a href="/almanya" class="card"><img src="{FLAGS['ALMANYA']}"><br>Almanya</a>
            <a href="/turkiye" class="card"><img src="{FLAGS['TURKIYE']}"><br>Türkiye</a>
            <a href="/roma" class="card"><img src="{FLAGS['ROMA']}"><br>Roma</a>
            <a href="/macaristan" class="card"><img src="{FLAGS['MACARISTAN']}"><br>Macaristan</a>
            <a href="/usa" class="card"><img src="{FLAGS['USA']}"><br>ABD</a>
        </div>
    </div>
    """
    return layout(content)

@app.route("/osmanli")
def osmanli():
    text = "Osmanlı İmparatorluğu'nda ekonomik devrimler genellikle savaş finansmanı üzerine kuruluydu. 1854'te alınan ilk dış borç, mali yapıda dönüm noktası oldu..."
    content = f"""<div class="container"><h2>🕌 Osmanlı Devrimleri</h2><div id="target" class="typing-text"></div><a href="/" style="display:block; text-align:center; margin-top:20px; color:#2980b9;">← Geri Dön</a></div><script>typeWriter("target", `{text}`, 20);</script>"""
    return layout(content)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
