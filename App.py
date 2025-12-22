from flask import Flask
import os

app = Flask(__name__)

STYLE = """
<style>
    body { font-family: 'Times New Roman', serif; background-color: #f0f2f5; margin: 0; display: flex; color: #333; overflow-x: hidden; }
    
    /* Yan Menü (Sidebar) */
    .sidebar { width: 340px; background: #2c3e50; color: white; height: 100vh; padding: 20px; position: fixed; overflow-y: auto; box-shadow: 2px 0 10px rgba(0,0,0,0.3); }
    .sidebar h2 { border-bottom: 2px solid #34495e; padding-bottom: 10px; font-size: 20px; color: #ecf0f1; text-align: center; }
    
    /* Ana İçerik */
    .main-content { margin-left: 380px; padding: 40px; flex-grow: 1; display: flex; justify-content: center; }
    .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); width: 100%; max-width: 900px; }
    
    /* Araç Kutuları */
    .tool-box { background: #34495e; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-top: 3px solid #3498db; }
    .tool-box h4 { margin: 0 0 10px 0; color: #3498db; font-size: 16px; text-align: center; }
    
    /* Standart Hesap Makinesi */
    .calc-display { width: 100%; height: 40px; background: #222; color: #0f0; text-align: right; padding: 5px; margin-bottom: 10px; font-family: monospace; font-size: 20px; border-radius: 4px; }
    .calc-buttons { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; }
    .calc-buttons button { padding: 10px; background: #444; border: none; color: white; border-radius: 4px; cursor: pointer; font-weight: bold; }
    .calc-buttons button:hover { background: #555; }
    .calc-buttons .op { background: #e67e22; }
    
    /* Oyun Alanı */
    #game-container { width: 100%; height: 150px; background: #111; position: relative; overflow: hidden; border-radius: 8px; border: 2px solid #555; cursor: pointer; }
    #player { width: 30px; height: 30px; background: #e74c3c; position: absolute; bottom: 0; left: 20px; border-radius: 4px; }
    .obstacle { width: 20px; height: 20px; background: #f1c40f; position: absolute; bottom: 0; right: -20px; border-radius: 2px; }
    #score { position: absolute; top: 5px; right: 10px; color: white; font-family: monospace; font-size: 14px; }
    
    /* Kartlar */
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }
    .card { background: #fff; border: 1px solid #ddd; padding: 20px; border-radius: 10px; text-decoration: none; text-align: center; transition: 0.3s; color: #2c3e50; }
    .card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); border-color: #3498db; }
    .card img { width: 60px; margin-bottom: 10px; border-radius: 4px; }
    
    .typing-text { line-height: 1.8; font-size: 18px; background: #fffdf9; padding: 25px; border-left: 6px solid #c0392b; border-radius: 4px; white-space: pre-wrap; }
</style>

<script>
    // --- HESAP MAKİNESİ MANTIĞI ---
    function addToCalc(val) { document.getElementById('display').innerText += val; }
    function clearCalc() { document.getElementById('display').innerText = ''; }
    function solveCalc() {
        try { document.getElementById('display').innerText = eval(document.getElementById('display').innerText); }
        catch { document.getElementById('display').innerText = 'Hata'; }
    }

    // --- OYUN MANTIĞI (Enflasyon Canavarı) ---
    let isJumping = false;
    let score = 0;
    function jump() {
        if (isJumping) return;
        let player = document.getElementById("player");
        isJumping = true;
        let pos = 0;
        let timer = setInterval(function() {
            if (pos >= 80) {
                clearInterval(timer);
                let downTimer = setInterval(function() {
                    if (pos <= 0) { clearInterval(downTimer); isJumping = false; }
                    pos -= 5;
                    player.style.bottom = pos + "px";
                }, 20);
            }
            pos += 5;
            player.style.bottom = pos + "px";
        }, 20);
    }

    function createObstacle() {
        let container = document.getElementById("game-container");
        let obs = document.createElement("div");
        obs.classList.add("obstacle");
        container.appendChild(obs);
        let obsPos = 300;
        let timer = setInterval(function() {
            if (obsPos < -20) {
                clearInterval(timer);
                container.removeChild(obs);
                score++;
                document.getElementById("score").innerText = "Skor: " + score;
            }
            // Çarpışma Kontrolü
            let playerBottom = parseInt(window.getComputedStyle(document.getElementById("player")).getPropertyValue("bottom"));
            if (obsPos > 20 && obsPos < 50 && playerBottom < 20) {
                alert("Canavar seni yakaladı! Skor: " + score);
                score = 0;
                document.getElementById("score").innerText = "Skor: 0";
                obsPos = -50;
            }
            obsPos -= 5;
            obs.style.right = (300 - obsPos) + "px";
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
    sidebar = f"""
    <div class="sidebar">
        <h2>🛠️ ARAÇLAR & OYUN</h2>
        
        <div class="tool-box">
            <h4>🧮 Hesap Makinesi</h4>
            <div id="display" class="calc-display"></div>
            <div class="calc-buttons">
                <button onclick="addToCalc('7')">7</button><button onclick="addToCalc('8')">8</button><button onclick="addToCalc('9')">9</button><button class="op" onclick="addToCalc('/')">/</button>
                <button onclick="addToCalc('4')">4</button><button onclick="addToCalc('5')">5</button><button onclick="addToCalc('6')">6</button><button class="op" onclick="addToCalc('*')">*</button>
                <button onclick="addToCalc('1')">1</button><button onclick="addToCalc('2')">2</button><button onclick="addToCalc('3')">3</button><button class="op" onclick="addToCalc('-')">-</button>
                <button onclick="clearCalc()">C</button><button onclick="addToCalc('0')">0</button><button onclick="solveCalc()">=</button><button class="op" onclick="addToCalc('+')">+</button>
            </div>
        </div>

        <div class="tool-box" style="border-top-color: #e74c3c;">
            <h4>🏃 Canavardan Kaç (Zıpla: Tıkla)</h4>
            <div id="game-container" onclick="jump()">
                <div id="score">Skor: 0</div>
                <div id="player"></div>
            </div>
            <p style="font-size: 11px; text-align:center; color:#bdc3c7; margin-top:5px;">Enflasyon canavarına (sarı kutu) çarpmadan zıpla!</p>
        </div>
        
        <script>setTimeout(createObstacle, 2000);</script>
    </div>
    """
    return f"{STYLE} {sidebar} <div class='main-content'>{content}</div>"

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
        <h1 style="font-size: 36px; text-align:center;">📜 Dünya Tarih & Ekonomi Portalı</h1>
        <div class="grid">
            <a href="/osmanli" class="card"><img src="{FLAGS['OSMANLI']}"><b>Osmanlı İmparatorluğu</b><br><small>Kuruluş: 1299</small></a>
            <a href="/almanya" class="card"><img src="{FLAGS['ALMANYA']}"><b>Almanya (Weimar)</b><br><small>Kuruluş: 1919</small></a>
            <a href="/turkiye" class="card"><img src="{FLAGS['TURKIYE']}"><b>Türkiye Cumhuriyeti</b><br><small>Kuruluş: 1923</small></a>
            <a href="/roma" class="card"><img src="{FLAGS['ROMA']}"><b>Antik Roma</b><br><small>Kuruluş: M.Ö. 753</small></a>
            <a href="/macaristan" class="card"><img src="{FLAGS['MACARISTAN']}"><b>Macaristan</b><br><small>Kuruluş: 895</small></a>
            <a href="/usa" class="card"><img src="{FLAGS['USA']}"><b>ABD</b><br><small>Kuruluş: 1776</small></a>
        </div>
    </div>
    """
    return layout(content)

@app.route("/osmanli")
def osmanli():
    text = """KURULUŞ: 1299. Osmanlı, Söğüt'te küçük bir beylikten cihan şümul bir devlete dönüştü. Ekonomisi uzun süre 'Akçe' üzerine kuruluydu. Ancak 16. yy'da Amerika'dan gelen gümüş akımı ve savaş masrafları nedeniyle 'Tağşiş' (paranın değerini düşürme) başladı... (Buraya istediğin kadar uzun bilgi ekleyebilirsin)"""
    content = f"""<div class="container"><h2>📜 Osmanlı Tarihi</h2><div id="target" class="typing-text"></div><a href="/" class="back-link">← Geri Dön</a></div><script>typeWriter("target", `{text}`, 20);</script>"""
    return layout(content)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
