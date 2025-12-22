from flask import Flask
import os

app = Flask(__name__)

STYLE = """
<style>
    body { font-family: 'Times New Roman', serif; background-color: #f0f2f5; margin: 0; display: flex; flex-direction: row; color: #333; min-height: 100vh; overflow-x: hidden; }
    
    @media (max-width: 1100px) {
        body { flex-direction: column; }
        .sidebar-left, .sidebar-right { position: relative !important; width: 100% !important; height: auto !important; margin: 0 !important; box-shadow: none !important; padding: 20px !important; box-sizing: border-box; }
        .main-content { margin: 0 !important; padding: 15px !important; width: 100% !important; }
        .container { padding: 25px !important; width: 95% !important; }
    }

    .sidebar-left { width: 320px; background: #1a1a2e; color: white; height: 100vh; padding: 25px; position: fixed; left: 0; overflow-y: auto; z-index: 10; border-right: 2px solid #e74c3c; }
    .sidebar-right { width: 320px; background: #ecf0f1; color: #2c3e50; height: 100vh; padding: 25px; position: fixed; right: 0; overflow-y: auto; border-left: 4px solid #bdc3c7; }
    .main-content { margin-left: 340px; margin-right: 340px; padding: 50px; flex-grow: 1; display: flex; justify-content: center; align-items: flex-start; }
    .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 850px; }
    
    h1 { color: #2c3e50; border-bottom: 3px solid #c0392b; padding-bottom: 10px; text-align: center; }
    
    /* HESAP MAKİNESİ */
    .tool-box { background: #16213e; padding: 15px; border-radius: 10px; margin-bottom: 25px; }
    #display { background: #0f3460; color: #2ecc71; padding: 15px; text-align: right; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 20px; margin-bottom: 10px; min-height: 25px; }
    .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .calc-grid button { padding: 12px; border: none; border-radius: 5px; background: #4b6584; color: white; font-weight: bold; cursor: pointer; }

    /* OYUN */
    #game-container { 
        width: 100%; height: 200px; background: #000; position: relative; 
        overflow: hidden; border-radius: 10px; border: 3px solid #e74c3c; cursor: pointer;
    }
    #player { width: 30px; height: 30px; background: #e74c3c; position: absolute; bottom: 5px; left: 40px; border-radius: 4px; z-index: 10; box-shadow: 0 0 10px #e74c3c; }
    .obstacle { width: 25px; background: #f1c40f; position: absolute; bottom: 5px; border-radius: 3px; }
    .bird { width: 35px; height: 15px; background: #3498db; position: absolute; border-radius: 10px; box-shadow: 0 0 8px #3498db; }
    #score-board { position: absolute; top: 10px; left: 10px; color: #2ecc71; font-family: monospace; font-size: 18px; z-index: 20; font-weight: bold; }
    #msg-overlay { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-weight: bold; pointer-events: none; }

    /* ANIMASYONLU METİN */
    .typing-text { line-height: 1.8; font-size: 18px; color: #444; background: #fffdf9; padding: 30px; border-left: 8px solid #c0392b; border-radius: 5px; min-height: 120px; white-space: pre-wrap; }
    .back-btn { display: inline-block; margin-top: 20px; padding: 12px 25px; background: #2c3e50; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }
    #hidden-data { display: none; }
</style>

<script>
    let running = false; let score = 0; let isJumping = false; let gameSpeed = 7;

    // HESAP MAKİNESİ
    function add(v) { document.getElementById('display').innerText += v; }
    function cls() { document.getElementById('display').innerText = ''; }
    function res() { try { document.getElementById('display').innerText = eval(document.getElementById('display').innerText); } catch { document.getElementById('display').innerText = 'Hata'; } }

    // OYUN FONKSİYONLARI
    function play() {
        if(running) { jump(); return; }
        running = true; score = 0; gameSpeed = 7;
        document.getElementById('score-num').innerText = '0';
        document.getElementById('msg-overlay').style.display = 'none';
        setTimeout(spawn, 1500); // 1.5 saniye sonra ilk engel
    }

    function jump() {
        if(isJumping) return;
        isJumping = true;
        let p = document.getElementById('player');
        let pos = 5;
        let up = setInterval(() => {
            if(pos >= 110) {
                clearInterval(up);
                let down = setInterval(() => {
                    if(pos <= 5) { clearInterval(down); isJumping = false; }
                    pos -= 5; p.style.bottom = pos + 'px';
                }, 15);
            }
            pos += 5; p.style.bottom = pos + 'px';
        }, 15);
    }

    function spawn() {
        if(!running) return;
        let container = document.getElementById('game-container');
        let obs = document.createElement('div');
        
        let isBird = score >= 10 && Math.random() > 0.5;
        if(isBird) {
            obs.className = 'bird';
            let isHigh = Math.random() > 0.5;
            obs.style.bottom = isHigh ? '95px' : '45px'; // Yüksek veya alçak kuş
        } else {
            obs.className = 'obstacle';
            obs.style.height = (Math.random() * 20 + 20) + 'px';
            obs.style.bottom = '5px';
        }

        obs.style.right = '-50px';
        container.appendChild(obs);

        let pos = -50;
        let loop = setInterval(() => {
            if(!running) { clearInterval(loop); obs.remove(); return; }
            pos += gameSpeed;
            obs.style.right = pos + 'px';

            // Çarpışma Algılama
            let p = document.getElementById('player').getBoundingClientRect();
            let o = obs.getBoundingClientRect();

            if (p.right > o.left && p.left < o.right && p.bottom > o.top && p.top < o.bottom) {
                running = false;
                location.reload(); // Yanınca anında baştan başla
            }

            if(pos > container.offsetWidth + 50) {
                clearInterval(loop);
                obs.remove();
                score++;
                document.getElementById('score-num').innerText = score;
                gameSpeed += 0.2;
                spawn(); // Tek engel mantığı: biri bitince diğeri başlar
            }
        }, 20);
    }

    // TYPING ANIMASYONU (KUSURSUZ)
    function startTyping() {
        const target = document.getElementById('target');
        const source = document.getElementById('hidden-text');
        if(!target || !source) return;
        
        const text = source.innerText.trim();
        target.innerHTML = "";
        let i = 0;
        
        function run() {
            if (i < text.length) {
                target.innerHTML += text.charAt(i);
                i++;
                setTimeout(run, 20);
            }
        }
        run();
    }

    window.onload = startTyping;
</script>
"""

def layout(content, long_text=""):
    left = f"""
    <div class="sidebar-left">
        <h2 style="color:#e74c3c; border-bottom:1px solid #333; padding-bottom:10px;">📊 PANEL</h2>
        <div class="tool-box">
            <div id="display"></div>
            <div class="calc-grid">
                <button onclick="add('7')">7</button><button onclick="add('8')">8</button><button onclick="add('9')">9</button><button onclick="add('/')">/</button>
                <button onclick="add('4')">4</button><button onclick="add('5')">5</button><button onclick="add('6')">6</button><button onclick="add('*')">*</button>
                <button onclick="add('1')">1</button><button onclick="add('2')">2</button><button onclick="add('3')">3</button><button onclick="add('-')">-</button>
                <button onclick="cls()" style="background:#e74c3c;">C</button><button onclick="add('0')">0</button><button onclick="res()" style="background:#2ecc71;">=</button><button onclick="add('+')">+</button>
            </div>
        </div>
        <div id="game-container" onclick="play()">
            <div id="score-board">SKOR: <span id="score-num">0</span></div>
            <div id="msg-overlay">BAŞLATMAK İÇİN TIKLA</div>
            <div id="player"></div>
        </div>
        <p style="font-size:12px; color:#888; margin-top:15px;">
            * 10 puandan sonra kuşlar gelir.<br>
            * Kuşlar yüksek veya alçak uçabilir.<br>
            * Yanarsan anında başa döner.
        </p>
    </div>
    """
    right = """
    <div class="sidebar-right">
        <h3 style="border-bottom:2px solid #2c3e50;">📜 ÖZETLER</h3>
        <p><b>🇹🇷 Türkiye:</b> 1923 İktisat Devrimi.</p>
        <p><b>🇩🇪 Almanya:</b> 1923 Hiperenflasyon.</p>
        <p><b>🏛️ Roma:</b> Paranın Çöküşü.</p>
    </div>
    """
    hidden = f"<div id='hidden-data'><div id='hidden-text'>{long_text}</div></div>"
    return f"{STYLE} {left} {right} {hidden} <div class='main-content'>{content}</div>"

@app.route("/")
def home():
    content = """
    <div class="container">
        <h1>🏛️ Dünya Tarih & Ekonomi Arşivi</h1>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin-top:30px;">
            <a href="/turkiye" style="padding:30px; background:#e74c3c; color:white; text-decoration:none; border-radius:10px; text-align:center; font-weight:bold;">🇹🇷 TÜRKİYE TARİHİ</a>
            <a href="/roma" style="padding:30px; background:#3498db; color:white; text-decoration:none; border-radius:10px; text-align:center; font-weight:bold;">🏛️ ROMA TARİHİ</a>
        </div>
    </div>
    """
    return layout(content)

@app.route("/turkiye")
def turkiye():
    text = "TÜRKİYE CUMHURİYETİ: 1923 yılında ilan edilen Cumhuriyet, sadece bir yönetim biçimi değil, büyük bir ekonomik bağımsızlık savaşıdır. Osmanlı'dan devralınan borçlar kuruşu kuruşuna ödenmiş, sanayi hamleleri başlatılmış ve Türk Lirası uzun yıllar değerini korumuştur. Bu dönem, yokluktan var edilen bir ulusun hikayesidir."
    content = '<h2>🇹🇷 Modern Türkiye</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
    return layout(content, text)

@app.route("/roma")
def roma():
    text = "ANTİK ROMA: Roma'nın çöküşündeki en büyük etkenlerden biri paradaki gümüş oranının düşürülmesidir. İmparatorlar daha fazla harcamak için parayı değersizleştirmiş, bu da tarihin gördüğü en büyük enflasyon krizlerinden birine yol açarak imparatorluğun ekonomik temelini yıkmıştır."
    content = '<h2>🏛️ Antik Roma</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
    return layout(content, text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
