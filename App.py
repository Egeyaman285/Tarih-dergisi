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

    .sidebar-left { width: 320px; background: #2c3e50; color: white; height: 100vh; padding: 25px; position: fixed; left: 0; overflow-y: auto; z-index: 10; box-shadow: 2px 0 10px rgba(0,0,0,0.3); }
    .sidebar-right { width: 320px; background: #ecf0f1; color: #2c3e50; height: 100vh; padding: 25px; position: fixed; right: 0; overflow-y: auto; border-left: 4px solid #bdc3c7; }
    .main-content { margin-left: 340px; margin-right: 340px; padding: 50px; flex-grow: 1; display: flex; justify-content: center; align-items: flex-start; }
    .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 850px; }
    
    h1 { color: #2c3e50; border-bottom: 3px solid #c0392b; padding-bottom: 10px; text-align: center; }
    h2 { color: #c0392b; margin-top: 0; }

    .tool-box { background: #34495e; padding: 15px; border-radius: 10px; margin-bottom: 25px; }
    #display { background: #1a1a1a; color: #2ecc71; padding: 15px; text-align: right; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 20px; margin-bottom: 10px; min-height: 25px; }
    .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .calc-grid button { padding: 12px; border: none; border-radius: 5px; background: #4b6584; color: white; font-weight: bold; cursor: pointer; }

    /* OYUN ALANI */
    #game-container { 
        width: 100%; height: 180px; background: #1a1a2e; 
        position: relative; overflow: hidden; border-radius: 10px; border: 3px solid #444; cursor: pointer;
    }
    #player { 
        width: 30px; height: 30px; background: #ff4757; position: absolute; 
        bottom: 10px; left: 50px; border-radius: 5px; z-index: 100;
        box-shadow: 0 0 10px #ff4757;
    }
    .obstacle { 
        position: absolute; bottom: 10px; border-radius: 4px; z-index: 90;
    }
    #score-board { position: absolute; top: 10px; left: 10px; color: #2ecc71; font-weight: bold; z-index: 110; }
    #ground { position: absolute; bottom: 0; width: 100%; height: 10px; background: #2ed573; }
</style>

<script>
    function add(v) { document.getElementById('display').innerText += v; }
    function cls() { document.getElementById('display').innerText = ''; }
    function res() { try { document.getElementById('display').innerText = eval(document.getElementById('display').innerText); } catch { document.getElementById('display').innerText = 'Hata'; } }

    let running = false; 
    let score = 0; 
    let isJumping = false;
    let speed = 7;

    function play() {
        if(!running) {
            running = true;
            score = 0;
            speed = 7;
            document.getElementById('score-num').innerText = '0';
            document.getElementById('msg').style.display = 'none';
            spawn();
        }
        
        if(!isJumping) {
            isJumping = true;
            let p = document.getElementById('player');
            let startPos = 10;
            let jumpHeight = 100;
            
            let up = setInterval(() => {
                startPos += 6;
                p.style.bottom = startPos + 'px';
                if(startPos >= jumpHeight) {
                    clearInterval(up);
                    let down = setInterval(() => {
                        startPos -= 6;
                        p.style.bottom = startPos + 'px';
                        if(startPos <= 10) {
                            clearInterval(down);
                            isJumping = false;
                        }
                    }, 15);
                }
            }, 15);
        }
    }

    function spawn() {
        if(!running) return;
        
        const container = document.getElementById('game-container');
        const obs = document.createElement('div');
        obs.className = 'obstacle';
        
        // Rastgele engel tipleri
        const heights = [25, 45, 60];
        const colors = ['#ffa502', '#ff6348', '#ced6e0'];
        const h = heights[Math.floor(Math.random() * heights.length)];
        
        obs.style.height = h + 'px';
        obs.style.width = '25px';
        obs.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        obs.style.right = '-30px';
        container.appendChild(obs);

        let pos = -30;
        let moveObs = setInterval(() => {
            if(!running) { clearInterval(moveObs); obs.remove(); return; }
            
            pos += speed;
            obs.style.right = pos + 'px';

            // Çarpışma Kontrolü
            let p = document.getElementById('player');
            let pRect = p.getBoundingClientRect();
            let oRect = obs.getBoundingClientRect();

            if (pRect.right > oRect.left && pRect.left < oRect.right && pRect.bottom > oRect.top) {
                running = false;
                location.reload(); // Yanınca anında baştan başla
            }

            if(pos > container.offsetWidth + 30) {
                clearInterval(moveObs);
                obs.remove();
                score++;
                document.getElementById('score-num').innerText = score;
                if(score % 5 == 0) speed += 0.8; // Her 5 engelde hızlan
            }
        }, 20);

        // Bir sonraki engeli oluştur
        setTimeout(spawn, Math.random() * 1000 + 800);
    }

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
                setTimeout(run, 15);
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
        <h2>📊 EKONOMİ PANELİ</h2>
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
            <div id="msg" style="color:white; text-align:center; margin-top:70px; font-weight:bold; font-family:sans-serif;">BAŞLAMAK İÇİN TIKLA</div>
            <div id="player"></div>
            <div id="ground"></div>
        </div>
    </div>
    """
    right = """
    <div class="sidebar-right">
        <h3 style="border-bottom:2px solid #2c3e50;">📜 KISA ÖZETLER</h3>
        <p><b>🇹🇷 Türkiye:</b> 1923'te küllerinden doğan ekonomi.</p>
        <p><b>🕌 Osmanlı:</b> Cihan devletinin mali yükselişi.</p>
        <p><b>🇩🇪 Almanya:</b> Hiperenflasyonun acı dersi.</p>
        <p><b>🏛️ Roma:</b> Parası bozulan imparatorluğun sonu.</p>
    </div>
    """
    hidden = f"<div id='hidden-data'><div id='hidden-text'>{long_text}</div></div>"
    return f"{STYLE} {left} {right} {hidden} <div class='main-content'>{content}</div>"

@app.route("/")
def home():
    content = """
    <div class="container">
        <h1>🏛️ Dünya Tarih & Ekonomi Arşivi</h1>
        <div class="grid">
            <a href="/turkiye" class="card">🇹🇷 MODERN TÜRKİYE</a>
            <a href="/osmanli" class="card">🕌 OSMANLI İMPARATORLUĞU</a>
            <a href="/almanya" class="card">🇩🇪 WEIMAR ALMANYASI</a>
            <a href="/roma" class="card">🏛️ ANTİK ROMA</a>
        </div>
    </div>
    """
    return layout(content)

@app.route("/turkiye")
def turkiye():
    text = "TÜRKİYE CUMHURİYETİ: 1923 yılında ilan edilen Cumhuriyet, sadece siyasi değil aynı zamanda dev bir ekonomik devrimdir. İzmir İktisat Kongresi ile yerli üretim hedeflenmiş, Osmanlı'dan kalan borçlar onurlu bir şekilde ödenmiş ve devlet destekli sanayileşme ile Türkiye modern dünyanın bir parçası haline gelmiştir."
    content = '<h2>🇹🇷 Modern Türkiye</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
    return layout(content, text)

@app.route("/osmanli")
def osmanli():
    text = "OSMANLI İMPARATORLUĞU: 600 yılı aşkın süren bu devasa devlet, ekonomisini 'İaşe' ve 'Gelenekçilik' prensipleri üzerine kurmuştur. İstanbul'un fethiyle ticaret yollarını kontrol altına almış, ancak Coğrafi Keşifler ve sanayi devrimini yakalayamaması mali yapısını sarsmıştır."
    content = '<h2>🕌 Osmanlı İmparatorluğu</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
    return layout(content, text)

@app.route("/almanya")
def almanya():
    text = "WEIMAR ALMANYASI: 1. Dünya Savaşı sonrası Versay Antlaşması'nın getirdiği ağır tazminat yükü altında ezilen Almanya, tarihin en dramatik hiperenflasyon dönemini yaşamıştır. 1923 yılında kağıt para o kadar değersizleşmiştir ki, bir somun ekmek almak için el arabasıyla para taşınması gerekmiştir."
    content = '<h2>🇩🇪 Weimar Almanyası</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
    return layout(content, text)

@app.route("/roma")
def roma():
    text = "ANTİK ROMA: Roma'nın çöküşü sadece askeri değil, aynı zamanda paranın saflığının bozulmasıyla gelen bir ekonomik faciadır. İmparatorlar masrafları karşılamak için gümüş Denarius'un içindeki gümüşü azaltıp yerine bakır koymuşlardır. Bu durum kontrol edilemez enflasyona yol açmıştır."
    content = '<h2>🏛️ Antik Roma</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
    return layout(content, text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
