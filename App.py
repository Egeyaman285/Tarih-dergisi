from flask import Flask
import os

app = Flask(__name__)

STYLE = """
<style>
    :root { --bg-color: #f0f2f5; --text-color: #333; --cont-bg: white; --accent: #e74c3c; }
    .dark-mode { --bg-color: #1a1a2e; --text-color: #ecf0f1; --cont-bg: #16213e; --accent: #f1c40f; }

    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg-color); margin: 0; display: flex; flex-direction: row; color: var(--text-color); min-height: 100vh; transition: 0.3s; }
    
    /* GGI LOGO STİLİ */
    .ggi-logo { width: 60px; height: 60px; background: linear-gradient(45deg, #e74c3c, #c0392b); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 20px; color: white; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); border: 2px solid rgba(255,255,255,0.2); }

    .sidebar-left { width: 320px; background: #1a1a2e; color: white; height: 100vh; padding: 25px; position: fixed; left: 0; overflow-y: auto; z-index: 10; border-right: 3px solid var(--accent); }
    .main-content { margin-left: 340px; padding: 50px; flex-grow: 1; display: flex; justify-content: center; }
    .container { background: var(--cont-bg); padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 900px; animation: fadeIn 0.8s ease; }
    
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    /* AYARLAR VE ADMİN BÖLÜMÜ */
    .settings-panel { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-top: 20px; border: 1px dashed #4b6584; }
    .admin-info { font-size: 13px; color: #bdc3c7; line-height: 1.6; margin-top: 10px; }
    .disclaimer { font-size: 11px; color: #95a5a6; margin-top: 20px; font-style: italic; border-top: 1px solid #34495e; padding-top: 10px; }

    .toggle-btn { cursor: pointer; padding: 8px 12px; border-radius: 5px; border: none; background: var(--accent); color: white; font-weight: bold; width: 100%; margin-top: 10px; transition: 0.2s; }
    .toggle-btn:hover { opacity: 0.8; transform: scale(1.02); }

    /* HESAP MAKİNESİ VE OYUN AYNI KALDI */
    .tool-box { background: #16213e; padding: 15px; border-radius: 10px; margin-bottom: 25px; }
    #display { background: #0f3460; color: #2ecc71; padding: 15px; text-align: right; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 20px; margin-bottom: 10px; min-height: 25px; }
    .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .calc-grid button { padding: 12px; border: none; border-radius: 5px; background: #4b6584; color: white; font-weight: bold; cursor: pointer; }
    #game-container { width: 100%; height: 180px; background: #000; position: relative; overflow: hidden; border-radius: 10px; border: 2px solid var(--accent); cursor: pointer; }
    #player { width: 25px; height: 25px; background: #e74c3c; position: absolute; bottom: 5px; left: 40px; border-radius: 4px; }
    .obstacle { width: 20px; background: #f1c40f; position: absolute; bottom: 5px; border-radius: 3px; }
    
    .country-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 20px; }
    .card { padding: 20px; color: white; text-decoration: none; border-radius: 10px; text-align: center; font-weight: bold; transition: 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.2); }
    
    .typing-text { line-height: 1.8; font-size: 17px; background: rgba(0,0,0,0.02); padding: 30px; border-left: 8px solid var(--accent); border-radius: 5px; white-space: pre-wrap; color: var(--text-color); }
    .back-btn { display: inline-block; margin-top: 20px; padding: 12px 25px; background: #2c3e50; color: white; text-decoration: none; border-radius: 5px; }

    @media (max-width: 1100px) {
        body { flex-direction: column; }
        .sidebar-left { position: relative; width: 100%; height: auto; border-right: none; border-bottom: 3px solid var(--accent); }
        .main-content { margin-left: 0; padding: 20px; }
    }
</style>

<script>
    function toggleTheme() {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }

    // Mevcut Fonksiyonlar (Hesap Makinesi & Oyun)
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
        let up = setInterval(() => { if(pos >= 100) { clearInterval(up); let down = setInterval(() => { if(pos <= 5) { clearInterval(down); isJumping = false; } pos -= 5; p.style.bottom = pos + 'px'; }, 15); } pos += 5; p.style.bottom = pos + 'px'; }, 15);
    }
    function spawn() {
        if(!running) return;
        let container = document.getElementById('game-container');
        let obs = document.createElement('div');
        obs.className = 'obstacle';
        obs.style.height = (Math.random() * 20 + 20) + 'px';
        obs.style.right = '-30px';
        container.appendChild(obs);
        let pos = -30;
        let loop = setInterval(() => {
            if(!running) { clearInterval(loop); obs.remove(); return; }
            pos += 6; obs.style.right = pos + 'px';
            let p = document.getElementById('player').getBoundingClientRect();
            let o = obs.getBoundingClientRect();
            if (p.right > o.left && p.left < o.right && p.bottom > o.top && p.top < o.bottom) { running = false; alert('Oyun Bitti! Skor: ' + score); location.reload(); }
            if(pos > container.offsetWidth) { clearInterval(loop); obs.remove(); score++; document.getElementById('score-num').innerText = score; spawn(); }
        }, 20);
    }

    function startTyping() {
        const target = document.getElementById('target');
        const source = document.getElementById('hidden-text');
        if(!target || !source) return;
        const text = source.innerText.trim();
        target.innerHTML = ""; let i = 0;
        function run() { if (i < text.length) { target.innerHTML += text.charAt(i); i++; setTimeout(run, 15); } }
        run();
        if(localStorage.getItem('theme') === 'dark') document.body.classList.add('dark-mode');
    }
    window.onload = startTyping;
</script>
"""

def layout(content, long_text=""):
    left = f"""
    <div class="sidebar-left">
        <div class="ggi-logo">GGI</div>
        <h3 style="color:var(--accent); margin-bottom:10px;">🛠️ ARAÇLAR</h3>
        
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
            <div id="score-board" style="position:absolute; padding:10px; color:#2ecc71; font-weight:bold;">SKOR: <span id="score-num">0</span></div>
            <div id="msg-overlay" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); color:white;">TIKLA VE BAŞLAT</div>
            <div id="player"></div>
        </div>

        <div class="settings-panel">
            <h4 style="margin:0;">⚙️ AYARLAR</h4>
            <button class="toggle-btn" onclick="toggleTheme()">Koyu/Açık Tema Değiştir</button>
            
            <div class="admin-info">
                <strong>👤 Admin:</strong> Ege<br>
                <strong>🎂 Yaş:</strong> 12<br>
                <strong>🚀 Altyapı:</strong> Render + GitHub + Python
            </div>
            
            <div class="disclaimer">
                ⚠️ <strong>UYARI:</strong> Bu site tamamen bağımsız bir projedir. Hiçbir siyasi veya ticari oluşumun yancısı değildir. Veriler eğitim amaçlıdır.
            </div>
        </div>
    </div>
    """
    hidden = f"<div id='hidden-data' style='display:none;'><div id='hidden-text'>{long_text}</div></div>"
    return f"{STYLE} {left} {hidden} <div class='main-content'>{content}</div>"

# Veriler (Aynı kaldı)
data = {
    "turkiye": "TÜRKİYE: 1923'te kurulan Cumhuriyet, modernleşme ve ulusal egemenlik temelinde yükselmiştir...",
    "abd": "AMERİKA BİRLEŞİK DEVLETLERİ: 1776 Bağımsızlık Bildirgesi ile kurulan federal bir cumhuriyettir...",
    "ingiltere": "İNGİLTERE: Magna Carta'dan Sanayi Devrimi'ne uzanan derin bir demokrasi ve endüstri tarihine sahiptir...",
    "almanya": "ALMANYA: 1871'de birliğini sağlayan, bugün Avrupa'nın ekonomik lokomotifi olan mühendislik devidir...",
    "fransa": "FRANSA: 1789 Devrimi ile hürriyet ve eşitlik fikirlerini dünyaya yayan kültürel bir merkezdir...",
    "rusya": "RUSYA: Çarlık döneminden Sovyetlere, oradan günümüz Rusya Federasyonu'na uzanan devasa bir güçtür...",
    "cin": "ÇİN: 5000 yıllık medeniyetini modern ekonomiyle birleştiren, dünyanın yeni üretim merkezidir...",
    "japonya": "JAPONYA: Geleneksel samuray ruhunu yüksek teknoloji ve disiplinle harmanlayan ada ülkesidir...",
    "italya": "İTALYA: Rönesans'ın beşiği, sanat, moda ve tasarımın dünyadaki en ikonik temsilcisidir...",
    "misir": "MISIR: Nil'in hediyesi, antik medeniyetlerin merkezi ve Arap dünyasının en kalabalık ülkesidir."
}

@app.route("/")
def home():
    countries = [
        ("TÜRKİYE", "/turkiye", "#c0392b"), ("ABD", "/abd", "#2980b9"),
        ("İNGİLTERE", "/ingiltere", "#2c3e50"), ("ALMANYA", "/almanya", "#f39c12"),
        ("FRANSA", "/fransa", "#3498db"), ("RUSYA", "/rusya", "#16a085"),
        ("ÇİN", "/cin", "#d35400"), ("JAPONYA", "/japonya", "#7f8c8d"),
        ("İTALYA", "/italya", "#27ae60"), ("MISIR", "/misir", "#8e44ad")
    ]
    cards = "".join([f'<a href="{url}" class="card" style="background:{color}">{name}</a>' for name, url, color in countries])
    content = f"""<div class="container"><h1>🏛️ Genç Girişimci Tarih Arşivi</h1><p style="text-align:center; color:#7f8c8d;">Dünya tarihini keşfetmek için bir ülke seçin.</p><div class="country-grid">{cards}</div></div>"""
    return layout(content)

@app.route("/<country>")
def show_country(country):
    if country in data:
        name = country.upper()
        content = f'<div class="container"><h2>{name} ANALİZİ</h2><div id="target" class="typing-text"></div><br><a href="/" class="back-btn">← ANA SAYFA</a></div>'
        return layout(content, data[country])
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
