from flask import Flask
import os

app = Flask(__name__)

STYLE = """
<style>
    :root { --bg-color: #f0f2f5; --text-color: #333; --cont-bg: white; --accent: #e74c3c; }
    .dark-mode { --bg-color: #1a1a2e; --text-color: #ecf0f1; --cont-bg: #16213e; --accent: #f1c40f; }

    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg-color); margin: 0; display: flex; flex-direction: row; color: var(--text-color); min-height: 100vh; transition: 0.3s; }
    
    .ggi-logo { width: 60px; height: 60px; background: linear-gradient(45deg, #e74c3c, #c0392b); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 20px; color: white; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); border: 2px solid rgba(255,255,255,0.2); }

    .sidebar-left { width: 300px; background: #1a1a2e; color: white; height: 100vh; padding: 25px; position: fixed; left: 0; overflow-y: auto; z-index: 10; border-right: 3px solid var(--accent); }
    
    /* SAĞ PANEL - ZİYARETÇİ SAYACI */
    .sidebar-right { width: 180px; background: #1a1a2e; color: white; height: 100vh; padding: 20px; position: fixed; right: 0; border-left: 3px solid var(--accent); display: flex; flex-direction: column; align-items: center; z-index: 10; }
    .stat-card { background: rgba(255,255,255,0.05); width: 100%; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.1); }
    .stat-number { font-size: 22px; font-weight: bold; color: var(--accent); display: block; margin-top: 5px; }
    .stat-label { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; color: #bdc3c7; }
    .live-dot { height: 8px; width: 8px; background-color: #2ecc71; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink 1s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }

    .main-content { margin-left: 320px; margin-right: 200px; padding: 40px; flex-grow: 1; display: flex; justify-content: center; }
    .container { background: var(--cont-bg); padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 1000px; animation: fadeIn 0.8s ease; }
    
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    .settings-panel { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-top: 10px; border: 1px dashed #4b6584; }
    .admin-info { font-size: 12px; color: #bdc3c7; line-height: 1.5; margin-top: 8px; }

    .toggle-btn { cursor: pointer; padding: 8px; border-radius: 5px; border: none; background: var(--accent); color: white; font-weight: bold; width: 100%; margin-top: 10px; transition: 0.2s; }
    
    .tool-box { background: #16213e; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    #display { background: #0f3460; color: #2ecc71; padding: 10px; text-align: right; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 18px; margin-bottom: 8px; min-height: 20px; }
    .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; }
    .calc-grid button { padding: 10px; border: none; border-radius: 4px; background: #4b6584; color: white; cursor: pointer; font-size: 12px; }
    
    #game-container { width: 100%; height: 150px; background: #000; position: relative; overflow: hidden; border-radius: 8px; border: 2px solid var(--accent); cursor: pointer; }
    #player { width: 20px; height: 20px; background: #e74c3c; position: absolute; bottom: 5px; left: 30px; border-radius: 3px; }
    .obstacle { width: 15px; background: #f1c40f; position: absolute; bottom: 5px; border-radius: 2px; }
    
    .country-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 20px; }
    .card { padding: 15px; color: white; text-decoration: none; border-radius: 8px; text-align: center; font-size: 12px; font-weight: bold; transition: 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .card:hover { transform: translateY(-3px); filter: brightness(1.1); }
    
    .typing-text { line-height: 1.8; font-size: 16px; background: rgba(0,0,0,0.03); padding: 30px; border-left: 6px solid var(--accent); border-radius: 8px; white-space: pre-wrap; color: var(--text-color); text-align: justify; }
    .back-btn { display: inline-block; margin-top: 20px; padding: 12px 25px; background: #2c3e50; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }

    @media (max-width: 1200px) { .sidebar-right { display: none; } .main-content { margin-right: 0; } }
    @media (max-width: 900px) { body { flex-direction: column; } .sidebar-left { position: relative; width: 100%; height: auto; border-right: none; } .main-content { margin-left: 0; padding: 20px; } .country-grid { grid-template-columns: repeat(2, 1fr); } }
</style>

<script>
    function updateStats() {
        let count = localStorage.getItem('ggi_visitors') || 2540;
        count = parseInt(count) + 1;
        localStorage.setItem('ggi_visitors', count);
        document.getElementById('v-count').innerText = count.toLocaleString();
        document.getElementById('active-count').innerText = Math.floor(Math.random() * 8) + 3;
    }

    function toggleTheme() {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('ggi_theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
    }

    function add(v) { document.getElementById('display').innerText += v; }
    function cls() { document.getElementById('display').innerText = ''; }
    function res() { try { document.getElementById('display').innerText = eval(document.getElementById('display').innerText); } catch { document.getElementById('display').innerText = 'Hata'; } }

    let running = false; let score = 0; let isJumping = false;
    function play() {
        if(running) { jump(); return; }
        running = true; score = 0;
        document.getElementById('score-num').innerText = '0';
        document.getElementById('msg-overlay').style.display = 'none';
        spawn();
    }
    function jump() { if(isJumping) return; isJumping = true; let p = document.getElementById('player'); let pos = 5;
        let up = setInterval(() => { if(pos >= 80) { clearInterval(up); let down = setInterval(() => { if(pos <= 5) { clearInterval(down); isJumping = false; } pos -= 5; p.style.bottom = pos + 'px'; }, 15); } pos += 5; p.style.bottom = pos + 'px'; }, 15);
    }
    function spawn() {
        if(!running) return;
        let container = document.getElementById('game-container');
        let obs = document.createElement('div');
        obs.className = 'obstacle';
        obs.style.height = (Math.random() * 20 + 15) + 'px';
        obs.style.right = '-20px';
        container.appendChild(obs);
        let pos = -20;
        let loop = setInterval(() => {
            if(!running) { clearInterval(loop); obs.remove(); return; }
            pos += 6; obs.style.right = pos + 'px';
            let p = document.getElementById('player').getBoundingClientRect();
            let o = obs.getBoundingClientRect();
            if (p.right > o.left && p.left < o.right && p.bottom > o.top && p.top < o.bottom) { 
                running = false; 
                location.reload(); 
            }
            if(pos > container.offsetWidth) { clearInterval(loop); obs.remove(); score++; document.getElementById('score-num').innerText = score; spawn(); }
        }, 20);
    }

    function startTyping() {
        updateStats();
        const target = document.getElementById('target');
        const source = document.getElementById('hidden-text');
        if(!target || !source) return;
        const text = source.innerText.trim();
        target.innerHTML = ""; let i = 0;
        function run() { if (i < text.length) { target.innerHTML += text.charAt(i); i++; setTimeout(run, 1); } }
        run();
        if(localStorage.getItem('ggi_theme') === 'dark') document.body.classList.add('dark-mode');
    }
    window.onload = startTyping;
</script>
"""

def layout(content, long_text=""):
    left = f"""
    <div class="sidebar-left">
        <div class="ggi-logo">GGI</div>
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
            <div style="position:absolute; padding:5px; color:#2ecc71; font-size:10px; font-weight:bold;">SKOR: <span id="score-num">0</span></div>
            <div id="msg-overlay" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); color:white; font-size:12px;">OYNA</div>
            <div id="player"></div>
        </div>
        <div class="settings-panel">
            <button class="toggle-btn" onclick="toggleTheme()">Görünüm Değiştir</button>
            <div class="admin-info">
                <strong>👤 Admin:</strong> Ege (12)<br>
                <strong>⚡ Sistem:</strong> Python 3.10
            </div>
        </div>
    </div>
    """
    
    right = """
    <div class="sidebar-right">
        <h4 style="font-size:12px; margin-bottom:15px; color:var(--accent);">📈 CANLI VERİ</h4>
        <div class="stat-card">
            <span class="stat-label">Toplam Giriş</span>
            <span id="v-count" class="stat-number">...</span>
        </div>
        <div class="stat-card">
            <span class="stat-label"><span class="live-dot"></span>Aktif Kişi</span>
            <span id="active-count" class="stat-number">...</span>
        </div>
        <div style="margin-top:auto; font-size:9px; color:#576574; text-align:center;">GGI ANALYTICS v3.0</div>
    </div>
    """
    
    hidden = f"<div id='hidden-data' style='display:none;'><div id='hidden-text'>{long_text}</div></div>"
    return f"{STYLE} {left} {right} {hidden} <div class='main-content'>{content}</div>"

data = {
    "turkiye": """[TÜRKİYE: ANADOLU'NUN EBEDİ ŞAHLANIŞI]
Anadolu, insanlık tarihinin başladığı yerdir. M.Ö. 10.000'de Göbeklitepe ile inancın merkezine dönüşmüş, Selçuklu ve Osmanlı ile cihan hakimiyeti kurmuştur. 1923'te Atatürk önderliğinde kurulan Cumhuriyet; Harf Devrimi, Kadın Hakları ve sanayi hamleleriyle modern bir ulus inşa etmiştir. Anadolu bugün, antik tarihle modern teknolojinin birleştiği stratejik bir köprüdür.""",

    "nazi": """[NAZİ DÖNEMİ ANALİZİ]
1933-1945 arası Almanya'yı kapsayan bu dönem, totaliter bir diktatörlük ve propaganda makinesinin (Goebbels) sonucudur. Holokost trajedisi ve II. Dünya Savaşı ile milyonlarca insanın hayatına mal olan bu karanlık süreç, günümüzde insan hakları hukukunun temel dersi haline gelmiştir.""",

    "abd": """[ABD: SÜPER GÜCÜN DOĞUŞU]
1776'da bağımsızlığını kazanan ABD, 19. yüzyılda Sanayi Devrimi ve İç Savaş sonrası köleliği kaldırarak yükselişe geçti. Bugün Silikon Vadisi ile teknolojiye, Hollywood ile kültüre ve Dolar ile dünya ekonomisine yön veren küresel bir aktördür.""",

    "cin": """[ÇİN: EJDERHANIN DÖNÜŞÜ]
5000 yıllık bir medeniyet olan Çin; kağıt, barut ve pusulanın mucididir. 1978'deki ekonomik reformlarla "Dünyanın Fabrikası" haline gelmiş, bugün yapay zeka ve elektrikli araç teknolojilerinde liderliğe oynamaktadır.""",

    "japonya": """[JAPONYA: DİSİPLİN VE TEKNOLOJİ]
Samuray geleneğinden gelen Japonya, 1868 Meiji Restorasyonu ile dünyadaki en hızlı modernleşmeyi başarmıştır. II. Dünya Savaşı sonrası ağır yıkımdan robotik ve otomotiv devine (Sony, Toyota) dönüşmesi bir kalkınma mucizesidir.""",
    
    "rusya": "1917 Bolşevik İhtilali ile kurulan SSCB'den modern Rusya'ya uzanan, uzay yarışının öncüsü bir güç analizi...",
    "almanya": "Bismarck'ın birliğinden bugünkü AB'nin sanayi lokomotifi olan modern Almanya'ya geçiş süreci...",
    "misir": "Nil kıyısındaki piramitlerin mühendislik sırlarından modern Orta Doğu diplomasisindeki kilit rolüne...",
    "guney_kore": "1950 savaşından sonra yıkılan bir ülkenin, Samsung ve K-Pop ile dünyayı domine eden bir deve dönüşümü...",
    "israıl": "Çöl tarımından siber güvenlik ve Start-Up dünyasının zirvesine ulaşan yüksek teknoloji analizi..."
}

@app.route("/")
def home():
    countries = [
        ("TÜRKİYE", "/turkiye", "#c0392b"), ("ABD", "/abd", "#2980b9"), ("İNGİLTERE", "/ingiltere", "#2c3e50"),
        ("ALMANYA", "/almanya", "#f39c12"), ("NAZİ DÖNEMİ", "/nazi", "#000000"), ("ÇİN", "/cin", "#d35400"),
        ("JAPONYA", "/japonya", "#7f8c8d"), ("MISIR", "/misir", "#8e44ad"), ("G. KORE", "/guney_kore", "#3498db"),
        ("İSRAİL", "/israıl", "#34495e")
    ]
    cards = "".join([f'<a href="{url}" class="card" style="background:{color}">{name}</a>' for name, url, color in countries])
    content = f"""<div class="container"><h1>🏛️ GGI Tarih Ansiklopedisi</h1><p style="text-align:center;">Antik Çağlardan Modern Devrimlere</p><div class="country-grid">{cards}</div></div>"""
    return layout(content)

@app.route("/<country>")
def show_country(country):
    if country in data:
        name = country.replace("_", " ").upper()
        content = f'<div class="container"><h2>{name} ANALİZİ</h2><div id="target" class="typing-text"></div><br><a href="/" class="back-btn">← ANA SAYFA</a></div>'
        return layout(content, data[country])
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
