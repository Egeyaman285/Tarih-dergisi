from flask import Flask
import os

app = Flask(__name__)

# --- STİL VE TASARIM (SCROLL VE ANALİTİK DÜZELTMELERİYLE) ---
STYLE = """
<style>
    :root { 
        --bg-color: #f0f2f5; 
        --text-color: #333; 
        --cont-bg: white; 
        --accent: #e74c3c; 
        --dark-accent: #c0392b; 
        --sidebar-bg: #1a1a2e;
    }
    .dark-mode { 
        --bg-color: #0f0f1b; 
        --text-color: #e0e0e0; 
        --cont-bg: #16213e; 
        --accent: #f1c40f; 
        --dark-accent: #d4ac0d; 
    }

    body { 
        font-family: 'Segoe UI', Arial, sans-serif; 
        background-color: var(--bg-color); 
        margin: 0; 
        display: flex; 
        flex-direction: row; 
        color: var(--text-color); 
        min-height: 100vh; 
        transition: 0.3s; 
        /* SCROLL HATASI ÇÖZÜMÜ: Overflow-x gizli ama y her zaman açık olmalı */
        overflow-x: hidden;
        overflow-y: auto; 
    }
    
    /* SOL PANEL - ARAÇLAR */
    .sidebar-left { 
        width: 320px; 
        background: var(--sidebar-bg); 
        color: white; 
        height: 100vh; 
        padding: 25px; 
        position: fixed; 
        left: 0; 
        overflow-y: auto; 
        z-index: 100; 
        border-right: 4px solid var(--accent); 
        box-shadow: 5px 0 15px rgba(0,0,0,0.5); 
    }
    
    .ggi-header { text-align: center; margin-bottom: 30px; }
    .ggi-logo { 
        width: 70px; height: 70px; 
        background: linear-gradient(135deg, var(--accent), var(--dark-accent)); 
        border-radius: 15px; display: flex; align-items: center; justify-content: center; 
        font-weight: 900; font-size: 24px; color: white; margin: 0 auto 10px auto; 
        border: 2px solid rgba(255,255,255,0.2); 
    }

    /* SAĞ PANEL - GERÇEKÇİ ANALİTİK */
    .sidebar-right { 
        width: 220px; 
        background: #0f3460; 
        color: white; 
        height: 100vh; 
        padding: 25px; 
        position: fixed; 
        right: 0; 
        border-left: 4px solid var(--accent); 
        z-index: 100; 
        display: flex; 
        flex-direction: column; 
    }
    
    .stat-box { 
        background: rgba(255,255,255,0.05); 
        padding: 15px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        border: 1px solid rgba(255,255,255,0.1); 
        text-align: center; 
        transition: 0.3s; 
    }
    .stat-box:hover { transform: scale(1.05); background: rgba(255,255,255,0.1); }
    .stat-val { font-size: 26px; font-weight: bold; color: var(--accent); display: block; }
    .stat-title { font-size: 11px; text-transform: uppercase; color: #8e9aaf; }
    
    .live-indicator { 
        height: 10px; width: 10px; 
        background-color: #2ecc71; 
        border-radius: 50%; 
        display: inline-block; 
        margin-right: 8px; 
        animation: pulse 1.5s infinite; 
    }
    @keyframes pulse { 
        0% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.7); } 
        70% { box-shadow: 0 0 0 10px rgba(46, 204, 113, 0); } 
        100% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); } 
    }

    /* ANA İÇERİK */
    .main-content { 
        margin-left: 320px; 
        margin-right: 220px; 
        padding: 60px; 
        flex-grow: 1; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        /* İÇERİK KAYDIRMA: Main content kendi scroll'una sahip olmalı */
        min-height: 100vh;
    }
    
    .container { 
        background: var(--cont-bg); 
        padding: 50px; 
        border-radius: 20px; 
        box-shadow: 0 15px 40px rgba(0,0,0,0.15); 
        width: 100%; 
        max-width: 1000px; 
        min-height: 120vh; /* İçeriğin kayması için yüksekliği artırdık */
        margin-bottom: 50px;
    }
    
    h1 { font-size: 32px; color: var(--accent); text-align: center; border-bottom: 3px solid var(--accent); padding-bottom: 10px; }

    /* ÜLKE TASARIMLARI */
    .country-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; margin-top: 30px; }
    .card { 
        padding: 20px; color: white; text-decoration: none; border-radius: 12px; 
        text-align: center; font-weight: bold; transition: 0.3s; 
        display: flex; align-items: center; justify-content: center; min-height: 60px; 
    }
    .card:hover { transform: translateY(-5px); filter: brightness(1.2); }

    .typing-text { 
        line-height: 2; 
        font-size: 17px; 
        background: rgba(0,0,0,0.02); 
        padding: 40px; 
        border-left: 8px solid var(--accent); 
        border-radius: 10px; 
        white-space: pre-wrap; 
        color: var(--text-color); 
        text-align: justify; 
    }

    /* ARAÇLAR: HESAP MAKİNESİ */
    .tool-box { background: #16213e; padding: 20px; border-radius: 15px; margin-bottom: 30px; }
    #display { 
        background: #1a1a2e; color: #2ecc71; padding: 15px; 
        text-align: right; border-radius: 8px; font-family: monospace; 
        font-size: 22px; margin-bottom: 15px; border: 1px solid #4b6584; 
    }
    .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
    .calc-grid button { padding: 15px; border: none; border-radius: 8px; background: #4b6584; color: white; cursor: pointer; }

    /* OYUN */
    #game-container { 
        width: 100%; height: 180px; background: #000; position: relative; 
        overflow: hidden; border-radius: 12px; border: 3px solid var(--accent); 
    }
    #player { width: 30px; height: 30px; background: var(--accent); position: absolute; bottom: 5px; left: 50px; border-radius: 5px; }
    .obstacle { width: 25px; background: #f1c40f; position: absolute; bottom: 5px; border-radius: 4px; }
</style>

<script>
    // --- ANALİTİK DÜZELTME: CANLI GÜNCELLEME ---
    function initStats() {
        let visitors = localStorage.getItem('ggi_total_v') || 48290;
        visitors = parseInt(visitors) + 1;
        localStorage.setItem('ggi_total_v', visitors);
        document.getElementById('v-count').innerText = visitors.toLocaleString();
        
        // Ziyaretçi sayısını her 10 saniyede bir sahte olarak artır
        setInterval(() => {
            let currentV = parseInt(localStorage.getItem('ggi_total_v'));
            let newV = currentV + Math.floor(Math.random() * 2);
            localStorage.setItem('ggi_total_v', newV);
            document.getElementById('v-count').innerText = newV.toLocaleString();
        }, 10000);

        function updateLive() {
            let active = Math.floor(Math.random() * (48 - 24 + 1)) + 24;
            document.getElementById('active-users').innerText = active;
        }
        updateLive();
        setInterval(updateLive, 3000); // Daha hızlı güncelleme
    }

    function toggleTheme() {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('ggi_theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
    }

    function add(v) { document.getElementById('display').innerText += v; }
    function cls() { document.getElementById('display').innerText = ''; }
    function res() { try { document.getElementById('display').innerText = eval(document.getElementById('display').innerText); } catch { document.getElementById('display').innerText = 'Hata'; } }

    // OYUN MOTORU (MEVCUT YAPI KORUNDU)
    let running = false; let score = 0; let isJumping = false;
    function play() {
        if(running) { jump(); return; }
        running = true; score = 0;
        document.getElementById('score-num').innerText = '0';
        document.getElementById('msg-overlay').style.display = 'none';
        spawn();
    }
    function jump() { 
        if(isJumping) return; isJumping = true; 
        let p = document.getElementById('player'); let pos = 5;
        let up = setInterval(() => { 
            if(pos >= 100) { clearInterval(up); let down = setInterval(() => { if(pos <= 5) { clearInterval(down); isJumping = false; } pos -= 5; p.style.bottom = pos + 'px'; }, 15); } 
            pos += 5; p.style.bottom = pos + 'px'; 
        }, 15);
    }
    function spawn() {
        if(!running) return;
        let container = document.getElementById('game-container');
        let obs = document.createElement('div');
        obs.className = 'obstacle';
        obs.style.height = (Math.random() * 30 + 20) + 'px';
        obs.style.right = '-30px';
        container.appendChild(obs);
        let pos = -30;
        let loop = setInterval(() => {
            if(!running) { clearInterval(loop); obs.remove(); return; }
            pos += 8; obs.style.right = pos + 'px';
            let p = document.getElementById('player').getBoundingClientRect();
            let o = obs.getBoundingClientRect();
            if (p.right > o.left && p.left < o.right && p.bottom > o.top && p.top < o.bottom) { running = false; location.reload(); }
            if(pos > container.offsetWidth) { clearInterval(loop); obs.remove(); score++; document.getElementById('score-num').innerText = score; spawn(); }
        }, 20);
    }

    window.onload = function() {
        initStats();
        if(localStorage.getItem('ggi_theme') === 'dark') document.body.classList.add('dark-mode');
        const target = document.getElementById('target');
        const source = document.getElementById('hidden-text');
        if(!target || !source) return;
        const text = source.innerText.trim();
        target.innerHTML = ""; let i = 0;
        function type() { if(i < text.length) { target.innerHTML += text.charAt(i); i++; setTimeout(type, 1); } }
        type();
    };
</script>
"""

# --- VERİ SETİ ---
data = {
    "turkiye": """[TÜRKİYE CUMHURİYETİ: STRATEJİK DERİNLİK]
1. JEOPOLİTİK KONUM: Boğazlar üzerindeki tam egemenlik (Montrö), Karadeniz güvenliğinin anahtarıdır.
2. ASKERİ DEVRİM: Kurtuluş Savaşı'ndaki lojistik deha, bugün yerli savunma sanayiine (SİHA'lar, TCG Anadolu) temel olmuştur.
3. TEKNOLOJİ: "Milli Teknoloji Hamlesi" ile kendi uydusunu yapan ve kendi enerjisini üreten bir devlettir.""",

    "nazi": """[NAZİ DÖNEMİ ANALİZİ]
1. İDEOLOJİK KÖRLEŞME: Propaganda makinesinin (Goebbels) bir toplumu nasıl felakete sürüklediğinin en net örneğidir.
2. ASKERİ BLITZKRIEG: "Yıldırım Savaşı" doktrini başta başarılı olsa da lojistik hatların tükenmesiyle mağlup olmuştur.
3. İNSANLIK SUÇLARI: Holokost trajedisi, modern insan hakları beyannamesinin temel taşlarının atılmasına neden olmuştur.""",

    "abd": """[ABD: KÜRESEL HEGEMONYA VE TEKNOLOJİK LİDERLİK]
1. EKONOMİK ÜSTÜNLÜK: Dolar'ın küresel rezerv para olması, ABD'ye dünya finans sistemini yönetme gücü vermiştir. 
2. SİLİKON VADİSİ: Apple, Google ve Microsoft gibi devlerle dijital dünyayı domine eden ABD, yapay zeka yarışında da başı çekmektedir. 
3. ASKERİ GÜC: 11 uçak gemisi filosu ve dünya genelindeki askeri üsleriyle küresel düzeni korumaya çalışmaktadır.""",

    "cin": """[ÇİN: EJDERHANIN DÖNÜŞÜ VE 2049 VİZYONU]
1. DÜNYANIN FABRİKASI: 1978 reformlarından sonra hızla kalkınan Çin, bugün dünyanın en büyük üretim gücüdür.
2. KUŞAK VE YOL: Antik İpek Yolu'nu canlandırarak küresel ticareti Pekin merkezli hale getirmeyi hedeflemektedir.
3. DİJİTAL OTORİTERİZM: Yüz tanıma ve sosyal kredi sistemleriyle teknolojiyi toplumsal kontrol için kullanmaktadır.""",

    "japonya": """[JAPONYA: DİSİPLİN VE ROBOTİK GELECEK]
1. MEIJI RESTORASYONU: Batı'ya hızla uyum sağlayan Japonya, yüksek teknoloji ve hassas mühendislikte dünya lideridir.
2. TEKNOLOJİ DEVLERİ: Sony, Toyota ve Panasonic gibi markalarla otomotiv ve elektronik pazarını domine etmiştir.""",

    "rusya": "Rusya: Avrasya'nın enerji devi ve nükleer süper güç analizi...",
    "almanya": "Almanya: Avrupa'nın ekonomik lokomotifi ve mühendislik merkezi...",
    "ingiltere": "İngiltere: Finans dünyasının kalbi ve diplomasi devi...",
    "italya": "İtalya: Tasarım, sanat ve Akdeniz jeopolitiği...",
    "misir": "Mısır: Nil'in anahtarı ve Orta Doğu'nun kapısı...",
    "guney_kore": "Güney Kore: Han Nehri Mucizesi ve teknoloji ihracatı..."
}

def layout(content, long_text=""):
    left = f"""<div class="sidebar-left"><div class="ggi-header"><div class="ggi-logo">GGI</div><span style="font-weight:bold;">GENÇ GİRİŞİMCİ v3.5</span></div>
    <h3 style="color:var(--accent); font-size:14px;">📊 ARAÇLAR</h3>
    <div class="tool-box"><div id="display"></div><div class="calc-grid">
    <button onclick="add('7')">7</button><button onclick="add('8')">8</button><button onclick="add('9')">9</button><button onclick="add('/')">/</button>
    <button onclick="add('4')">4</button><button onclick="add('5')">5</button><button onclick="add('6')">6</button><button onclick="add('*')">*</button>
    <button onclick="add('1')">1</button><button onclick="add('2')">2</button><button onclick="add('3')">3</button><button onclick="add('-')">-</button>
    <button onclick="cls()" style="background:var(--accent)">C</button><button onclick="add('0')">0</button><button onclick="res()" style="background:#2ecc71">=</button><button onclick="add('+')">+</button>
    </div></div>
    <div id="game-container" onclick="play()"><div id="score-board">SKOR: <span id="score-num">0</span></div><div id="msg-overlay" style="position:absolute;top:40%;left:35%;color:white;">OYNA</div><div id="player"></div></div>
    <button class="toggle-btn" onclick="toggleTheme()">🌓 GECE/GÜNDÜZ</button>
    <div style="margin-top:20px; font-size:12px; opacity:0.7;">👤 KURUCU: EGE (GGI)<br>💻 SİSTEM: PYTHON 3.10</div></div>"""
    
    right = """<div class="sidebar-right"><h4 style="font-size:12px;text-align:center;">🌐 ANALİTİK</h4>
    <div class="stat-box"><span class="stat-title">Ziyaretçi</span><span id="v-count" class="stat-val">...</span></div>
    <div class="stat-box"><span class="stat-title"><span class="live-indicator"></span>Aktif</span><span id="active-users" class="stat-val">...</span></div>
    <div class="stat-box" style="margin-top:auto;"><span class="stat-title">Sunucu</span><span class="stat-val" style="color:#2ecc71;font-size:16px;">ONLINE</span></div></div>"""
    
    hidden = f"<div id='hidden-text' style='display:none;'>{long_text}</div>"
    return f"{STYLE} {left} {right} {hidden} <div class='main-content'>{content}</div>"

@app.route("/")
def home():
    countries = [("TÜRKİYE", "/turkiye", "#c0392b"), ("ABD", "/abd", "#2980b9"), ("NAZİ", "/nazi", "#000"), ("ÇİN", "/cin", "#d35400"), ("JAPONYA", "/japonya", "#7f8c8d"), ("RUSYA", "/rusya", "#c0392b"), ("ALMANYA", "/almanya", "#f39c12"), ("İNGİLTERE", "/ingiltere", "#2c3e50"), ("İTALYA", "/italya", "#27ae60"), ("MISIR", "/misir", "#8e44ad"), ("G. KORE", "/guney_kore", "#3498db")]
    cards = "".join([f'<a href="{u}" class="card" style="background:{c}">{n}</a>' for n, u, c in countries])
    content = f'<div class="container"><h1>🏛️ GGI TARİH ARŞİVİ</h1><div class="country-grid">{cards}</div></div>'
    return layout(content)

@app.route("/<country>")
def show(country):
    if country in data:
        content = f'<div class="container"><h1>{country.upper()} ANALİZİ</h1><div id="target" class="typing-text"></div><br><a href="/" class="back-btn">← GERİ DÖN</a></div>'
        return layout(content, data[country])
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
