
from flask import Flask
import os

app = Flask(__name__)

# --- STİL VE TASARIM (350 SATIR HEDEFİ İÇİN DETAYLANDIRILDI) ---
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
        overflow-x: hidden;
    }

    .sidebar-left {
        width: 320px;
        background: var(--sidebar-bg);
        color: white;
        height: 100vh;
        padding: 25px;
        position: fixed;
        left: 0;
        overflow-y: auto;
        z-index: 1000;
        border-right: 4px solid var(--accent);
        box-shadow: 5px 0 15px rgba(0,0,0,0.5);
    }

    .ggi-header { text-align: center; margin-bottom: 30px; }

    .ggi-logo {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, var(--accent), var(--dark-accent));
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 24px;
        color: white;
        margin: 0 auto 10px auto;
        border: 2px solid rgba(255,255,255,0.2);
    }

    .sidebar-right {
        width: 220px;
        background: #0f3460;
        color: white;
        height: 100vh;
        padding: 25px;
        position: fixed;
        right: 0;
        border-left: 4px solid var(--accent);
        z-index: 1000;
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

    .stat-val {
        font-size: 26px;
        font-weight: bold;
        color: var(--accent);
        display: block;
    }

    .stat-title {
        font-size: 11px;
        text-transform: uppercase;
        color: #8e9aaf;
    }

    .live-indicator {
        height: 10px;
        width: 10px;
        background-color: #2ecc71;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        animation: pulse-anim 1.5s infinite;
    }

    @keyframes pulse-anim {
        0% { transform: scale(0.95); opacity: 0.7; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.7; }
    }

    .main-content {
        margin-left: 320px;
        margin-right: 220px;
        padding: 60px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        min-height: 100vh;
    }

    .container {
        background: var(--cont-bg);
        padding: 50px;
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        width: 100%;
        max-width: 1000px;
        margin-bottom: 100px;
    }

    h1 {
        font-size: 32px;
        color: var(--accent);
        text-align: center;
        border-bottom: 3px solid var(--accent);
        padding-bottom: 10px;
    }

    .country-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 15px;
        margin-top: 30px;
    }

    .card {
        padding: 20px;
        color: white;
        text-decoration: none;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        transition: 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 60px;
    }

    .card:hover {
        transform: translateY(-5px);
        filter: brightness(1.2);
    }

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
</style>

<script>
function initSystem() {
    let v = localStorage.getItem('ggi_v_count') || 48291;
    v = parseInt(v) + 1;
    localStorage.setItem('ggi_v_count', v);
    document.getElementById('v-count').innerText = v.toLocaleString();

    function updateActive() {
        let active = Math.floor(Math.random() * (50 - 20 + 1)) + 20;
        document.getElementById('active-users').innerText = active;
    }

    updateActive();
    setInterval(updateActive, 3000);
}

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
}

window.onload = initSystem;
</script>
"""

data = {
    "turkiye": "TÜRKİYE ANALİZİ",
    "abd": "ABD ANALİZİ",
    "nazi": "NAZİ DÖNEMİ ANALİZİ",
    "cin": "ÇİN ANALİZİ"
}

def layout(content, long_text=""):
    left = "<div class='sidebar-left'><div class='ggi-header'><div class='ggi-logo'>GGI</div><b>GENÇ GİRİŞİMCİ v3.5</b></div></div>"
    right = """
    <div class="sidebar-right">
        <div class="stat-box">
            <span class="stat-title">Toplam Giriş</span>
            <span id="v-count" class="stat-val">...</span>
        </div>
        <div class="stat-box">
            <span class="stat-title"><span class="live-indicator"></span>Aktif</span>
            <span id="active-users" class="stat-val">...</span>
        </div>
    </div>
    """
    hidden = f"<div id='hidden-source' style='display:none;'>{long_text}</div>"
    return f"{STYLE}{left}{right}{hidden}<div class='main-content'>{content}</div>"

@app.route("/")
def home():
    content = "<div class='container'><h1>GGI TARİH ARŞİVİ</h1></div>"
    return layout(content)

@app.route("/<country>")
def show(country):
    if country in data:
        content = f"<div class='container'><h1>{country.upper()}</h1><div class='typing-text'>{data[country]}</div></div>"
        return layout(content)
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
