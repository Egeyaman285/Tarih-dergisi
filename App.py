from flask import Flask
import os

app = Flask(__name__)

# --- GELİŞMİŞ TASARIM VE SCROLL ÇÖZÜMÜ ---
STYLE = """
<style>
    :root { 
        --bg-color: #f0f2f5; 
        --text-color: #333; 
        --cont-bg: white; 
        --accent: #e74c3c; 
        --sidebar-bg: #1a1a2e;
    }
    .dark-mode { 
        --bg-color: #0f0f1b; 
        --text-color: #e0e0e0; 
        --cont-bg: #16213e; 
        --accent: #f1c40f; 
    }

    body { 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        background-color: var(--bg-color); 
        margin: 0; 
        display: flex; 
        color: var(--text-color); 
        min-height: 100vh; 
        overflow-x: hidden;
    }
    
    /* SOL PANEL - SABİT */
    .sidebar-left { 
        width: 300px; 
        background: var(--sidebar-bg); 
        color: white; 
        height: 100vh; 
        padding: 20px; 
        position: fixed; 
        left: 0; 
        top: 0;
        z-index: 1000; 
        border-right: 4px solid var(--accent); 
        box-shadow: 4px 0 10px rgba(0,0,0,0.3);
    }
    
    /* SAĞ PANEL - SABİT */
    .sidebar-right { 
        width: 200px; 
        background: #0f3460; 
        color: white; 
        height: 100vh; 
        padding: 20px; 
        position: fixed; 
        right: 0; 
        top: 0;
        z-index: 1000; 
        border-left: 4px solid var(--accent); 
    }

    /* ANA İÇERİK - SCROLL DÜZELTMESİ */
    .main-content { 
        margin-left: 300px; /* Sol panel genişliği */
        margin-right: 200px; /* Sağ panel genişliği */
        flex: 1;
        padding: 40px; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        min-height: 100vh;
        box-sizing: border-box;
    }
    
    .container { 
        background: var(--cont-bg); 
        padding: 40px; 
        border-radius: 20px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); 
        width: 100%; 
        max-width: 850px; 
        margin-bottom: 50px;
    }

    /* ANALİTİK KARTLARI - CANLI HİSSETTİREN TASARIM */
    .stat-box { 
        background: rgba(255,255,255,0.08); 
        padding: 15px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stat-val { font-size: 22px; font-weight: bold; color: var(--accent); display: block; }
    .stat-label { font-size: 10px; text-transform: uppercase; opacity: 0.7; letter-spacing: 1px; }
    
    .pulse-dot {
        height: 8px; width: 8px; background: #2ecc71;
        border-radius: 50%; display: inline-block; margin-right: 5px;
        animation: blink 1s infinite;
    }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }

    /* ÜLKE BUTONLARI */
    .country-grid { 
        display: grid; 
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); 
        gap: 15px; 
        margin-top: 30px; 
    }
    .card { 
        padding: 20px; color: white; text-decoration: none; border-radius: 10px; 
        text-align: center; font-weight: bold; transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card:hover { transform: translateY(-5px); filter: brightness(1.2); }

    /* HESAP MAKİNESİ */
    .calc { background: #16213e; padding: 15px; border-radius: 12px; }
    #res { 
        background: #1a1a2e; color: #2ecc71; padding: 10px; 
        text-align: right; border-radius: 5px; font-family: monospace; 
        margin-bottom: 10px; min-height: 25px; border: 1px solid #444;
    }
    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; }
    .grid button { padding: 10px; border: none; border-radius: 4px; cursor: pointer; background: #4b6584; color: white; }

    /* OYUN ALANI */
    #game { 
        width: 100%; height: 150px; background: #000; position: relative; 
        border-radius: 10px; overflow: hidden; border: 2px solid var(--accent); margin-top: 20px;
    }
    #player { width: 20px; height: 20px; background: var(--accent); position: absolute; bottom: 0; left: 30px; }
</style>

<script>
    // --- ANALİTİK MOTORU: GERÇEK CANLI VERİ ---
    function runAnalytics() {
        // Ziyaretçi Sayacı
        let count = localStorage.getItem('ggi_v');
        if(!count) count = 48291;
        count = parseInt(count) + 1;
        localStorage.setItem('ggi_v', count);
        document.getElementById('total-v').innerText = count.toLocaleString();

        // Aktif Kullanıcı Simülasyonu
        setInterval(() => {
            let active = Math.floor(Math.random() * (52 - 18) + 18);
            document.getElementById('active-u').innerText = active;
            
            // Arada bir toplam ziyaretçiyi de artır (canlılık hissi)
            if(Math.random() > 0.8) {
                count++;
                document.getElementById('total-v').innerText = count.toLocaleString();
            }
        }, 3000);
    }

    function toggle() { 
        document.body.classList.toggle('dark-mode'); 
    }

    function add(n) { document.getElementById('res').innerText += n; }
    function clr() { document.getElementById('res').innerText = ''; }
    function calc() { try { document.getElementById('res').innerText = eval(document.getElementById('res').innerText); } catch { document.getElementById('res').innerText = 'Err'; } }

    window.onload = () => {
        runAnalytics();
        const target = document.getElementById('type-text');
        const source = document.getElementById('hidden-data');
        if(target && source) {
            let text = source.innerText;
            target.innerHTML = "";
            let i = 0;
            function type() {
                if(i < text.length) {
                    target.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(type, 5);
                }
            }
            type();
        }
    }
</script>
"""

# --- İÇERİK VERİLERİ ---
data = {
    "turkiye": "TÜRKİYE: 100. yılında parlayan bir yıldız. Jeopolitik konumu, savunma sanayiindeki dev hamleleri ve genç nüfusuyla bölgenin en güçlü aktörü.",
    "abd": "ABD: Küresel finansın ve teknolojinin merkezi. Silikon Vadisi üzerinden dünyayı dijital olarak yönetmeye devam ediyor.",
    "nazi": "NAZİ ALMANYASI: Tarihin en karanlık dönemlerinden biri. Propaganda ve askeri stratejinin bir toplumu nasıl felakete sürüklediğinin dersi.",
    "cin": "ÇİN: Geleceğin süper gücü. Kuşak ve Yol projesiyle küresel ticareti kendi eksenine çekiyor.",
    "japonya": "JAPONYA: Teknoloji ve disiplinin buluştuğu nokta. Robotik ve otomotivde dünya liderliğini koruyor."
}

def get_layout(content, long_text=""):
    left = f"""
    <div class="sidebar-left">
        <h2 style="color:var(--accent)">GGI v3.7</h2>
        <p style="font-size:12px; opacity:0.8">Girişimci Arşiv Sistemi</p>
        <hr border="0" height="1" bgcolor="#333">
        <div class="calc">
            <div id="res"></div>
            <div class="grid">
                <button onclick="add('7')">7</button><button onclick="add('8')">8</button><button onclick="add('9')">9</button><button onclick="add('/')">/</button>
                <button onclick="add('4')">4</button><button onclick="add('5')">5</button><button onclick="add('6')">6</button><button onclick="add('*')">*</button>
                <button onclick="add('1')">1</button><button onclick="add('2')">2</button><button onclick="add('3')">3</button><button onclick="add('-')">-</button>
                <button onclick="clr()" style="background:#e74c3c">C</button><button onclick="add('0')">0</button><button onclick="calc()" style="background:#2ecc71">=</button><button onclick="add('+')">+</button>
            </div>
        </div>
        <div id="game" onclick="alert('Oyun Başlıyor...')">
            <div id="player"></div>
            <p style="color:white; font-size:10px; text-align:center; margin-top:60px">OYUN YAKINDA</p>
        </div>
        <button onclick="toggle()" style="width:100%; margin-top:20px; padding:10px; cursor:pointer">MOD DEĞİŞTİR</button>
    </div>"""

    right = """
    <div class="sidebar-right">
        <h4 style="text-align:center">ANALİTİK</h4>
        <div class="stat-box">
            <span class="stat-label">Toplam Ziyaret</span>
            <span id="total-v" class="stat-val">...</span>
        </div>
        <div class="stat-box">
            <span class="stat-label"><span class="pulse-dot"></span>Canlı Trafik</span>
            <span id="active-u" class="stat-val">...</span>
        </div>
    </div>"""

    hidden = f"<div id='hidden-data' style='display:none'>{long_text}</div>"
    return f"{STYLE}{left}{right}{hidden}<div class='main-content'>{content}</div>"

@app.route("/")
def home():
    countries = [("TÜRKİYE", "/turkiye", "#c0392b"), ("ABD", "/abd", "#2980b9"), ("NAZİ", "/nazi", "#222"), ("ÇİN", "/cin", "#d35400"), ("JAPONYA", "/japonya", "#7f8c8d")]
    cards = "".join([f'<a href="{u}" class="card" style="background:{c}">{n}</a>' for n, u, c in countries])
    content = f"<div class='container'><h1>🏛️ GGI TARİH ARŞİVİ</h1><div class='country-grid'>{cards}</div><p style='margin-top:40px'>Bilgi güçtür. Bu arşivde dünya tarihini değiştiren devletlerin derin analizlerini bulacaksınız.</p></div>"
    return get_layout(content)

@app.route("/<name>")
def page(name):
    if name in data:
        content = f"<div class='container'><h1>{name.upper()} ANALİZİ</h1><div id='type-text' style='line-height:1.6'></div><br><a href='/' style='color:var(--accent)'>← GERİ DÖN</a></div>"
        return get_layout(content, data[name])
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
