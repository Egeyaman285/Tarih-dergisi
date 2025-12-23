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
        z-index: 1000; 
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

    /* SAĞ PANEL - ANALİTİK */
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
    .stat-val { font-size: 26px; font-weight: bold; color: var(--accent); display: block; }
    .stat-title { font-size: 11px; text-transform: uppercase; color: #8e9aaf; }
    
    .live-indicator { 
        height: 10px; width: 10px; 
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

    /* ANA İÇERİK - SCROLL AKTİF */
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
    #calc-display { 
        background: #1a1a2e; color: #2ecc71; padding: 15px; 
        text-align: right; border-radius: 8px; font-family: monospace; 
        font-size: 22px; margin-bottom: 15px; border: 1px solid #4b6584; min-height: 25px;
    }
    .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
    .calc-grid button { padding: 15px; border: none; border-radius: 8px; background: #4b6584; color: white; cursor: pointer; }

    /* OYUN SİSTEMİ */
    #game-area { 
        width: 100%; height: 180px; background: #000; position: relative; 
        overflow: hidden; border-radius: 12px; border: 3px solid var(--accent); 
    }
    #player-obj { width: 30px; height: 30px; background: var(--accent); position: absolute; bottom: 5px; left: 50px; border-radius: 5px; }
</style>

<script>
    // --- GERÇEKÇİ CANLI ANALİTİK MOTORU ---
    function initSystem() {
        // Ziyaretçi Sayacı
        let v = localStorage.getItem('ggi_v_count') || 48291;
        v = parseInt(v) + 1;
        localStorage.setItem('ggi_v_count', v);
        document.getElementById('v-count').innerText = v.toLocaleString();
        
        // Aktif Kullanıcı (Canlı değişim)
        function updateActive() {
            let active = Math.floor(Math.random() * (50 - 20 + 1)) + 20;
            document.getElementById('active-users').innerText = active;
        }
        updateActive();
        setInterval(updateActive, 3000); // 3 saniyede bir değişir
    }

    function toggleTheme() {
        document.body.classList.toggle('dark-mode');
    }

    // Hesap Makinesi Fonksiyonları
    function addVal(v) { document.getElementById('calc-display').innerText += v; }
    function clearCalc() { document.getElementById('calc-display').innerText = ''; }
    function calculateResult() { 
        try { 
            document.getElementById('calc-display').innerText = eval(document.getElementById('calc-display').innerText); 
        } catch { 
            document.getElementById('calc-display').innerText = 'Hata'; 
        } 
    }

    window.onload = function() {
        initSystem();
        const target = document.getElementById('target-text');
        const source = document.getElementById('hidden-source');
        if(target && source) {
            const text = source.innerText.trim();
            target.innerHTML = ""; let i = 0;
            function type() { if(i < text.length) { target.innerHTML += text.charAt(i); i++; setTimeout(type, 1); } }
            type();
        }
    };
</script>
"""

# --- DEVASA VERİ BANKASI ---
data = {
    "turkiye": """[TÜRKİYE CUMHURİYETİ: STRATEJİK DERİNLİK VE MODERN GÜÇ]

1. JEOPOLİTİK KONUM: Türkiye, dünya adasının kalbi (Heartland) ve kenar kuşağı arasında bir kilit taşıdır. Boğazlar üzerindeki tam egemenliği, Karadeniz ve Akdeniz arasındaki tüm ticari ve askeri trafiği kontrol etmesini sağlar. 

2. ASKERİ DEVRİM: Kurtuluş Savaşı'ndaki lojistik deha, bugün yerli savunma sanayiine (SİHA'lar, TCG Anadolu, Milli Muharip Uçak KAAN) temel olmuştur. Türk ordusu, NATO'nun en büyük ikinci ordusu olarak bölgesel güç projeksiyonunda rakipsizdir.

3. TEKNOLOJİ VE EKONOMİ: Genç nüfusuyla Türkiye, oyun geliştirme, fintek ve üretim sanayiinde bir çekim merkezi haline gelmiştir. "Milli Teknoloji Hamlesi" ile kendi uydusunu yapan ve kendi enerjisini (Karadeniz Gazı, Akkuyu) üreten bir devlet yapısına evrilmektedir.

4. TARİHSEL MİRAS: Göbeklitepe'den Selçuklu'ya, Osmanlı'dan Cumhuriyet'e uzanan süreçte Türkiye, Batı'nın kurumlarıyla Doğu'nun kültürel zenginliğini birleştiren tek sentez devlettir.""",

    "nazi": """[NAZİ DÖNEMİ ANALİZİ: TOTALİTERİZMİN ÇÖKÜŞÜ]

1. İDEOLOJİK KÖRLEŞME: 1933-1945 arası Almanya, aşırı milliyetçilik ve propaganda makinesinin (Goebbels) bir toplumu nasıl felakete sürüklediğinin en net örneğidir.

2. ASKERİ BLITZKRIEG: "Yıldırım Savaşı" doktrini ile Avrupa'yı hızla işgal eden Wehrmacht, lojistik hatlarının Sovyetler Birliği'nin derinliklerinde tükenmesi ve ABD'nin sanayi gücüyle savaşa girmesiyle mağlup olmuştur.

3. İNSANLIK SUÇLARI: Holokost trajedisi, modern hukukun (Nürnberg Mahkemeleri) ve İnsan Hakları Beyannamesi'nin temel taşlarının atılmasına, "soykırım" suçunun tanımlanmasına neden olmuştur.""",

    "abd": """[ABD: KÜRESEL HEGEMONYA VE TEKNOLOJİK LİDERLİK]

1. EKONOMİK ÜSTÜNLÜK: II. Dünya Savaşı'ndan bu yana Dolar'ın küresel rezerv para olması, ABD'ye dünya finans sistemini yönetme gücü vermiştir. 

2. SİLİKON VADİSİ: Apple, Google ve Microsoft gibi devlerle dijital dünyayı domine eden ABD, yapay zeka yarışında da başı çekmektedir. 

3. ASKERİ GÜC: 11 uçak gemisi filosu ve dünya genelindeki askeri üsleriyle ABD, "Pax Americana" düzenini korumaya çalışmaktadır.""",

    "cin": """[ÇİN: EJDERHANIN DÖNÜŞÜ VE 2049 VİZYONU]

1. DÜNYANIN FABRİKASI: 1978 reformlarından sonra hızla kalkınan Çin, bugün dünyanın en büyük üretim gücü ve satın alma gücü paritesine göre en büyük ekonomisidir.

2. KUŞAK VE YOL: Antik İpek Yolu'nu canlandırarak 100'den fazla ülkeye altyapı yatırımı yapan Çin, küresel ticareti Pekin merkezli hale getirmeyi hedeflemektedir.

3. DİJİTAL OTORİTERİZM: Yüz tanıma ve sosyal kredi sistemleriyle Çin, teknolojiyi toplumsal kontrol için en ileri düzeyde kullanan devlettir.""",

    "japonya": "Japonya: Disiplin, teknoloji ve robotik geleceğin Asya'daki kalesi.",
    "rusya": "Rusya: Avrasya'nın enerji devi ve nükleer süper güç.",
    "almanya": "Almanya: Avrupa'nın ekonomik lokomotifi ve mühendislik merkezi.",
    "ingiltere": "İngiltere: Küresel finansın merkezi ve diplomasi devi.",
    "italya": "İtalya: Tasarım, sanat ve Akdeniz jeopolitiğinin birleşimi.",
    "misir": "Mısır: Nil'in anahtarı ve antik medeniyetin kapısı.",
    "guney_kore": "Güney Kore: Teknoloji mucizesi ve kültürel ihracat devi."
}

def layout(content, long_text=""):
    left = f"""<div class="sidebar-left">
    <div class="ggi-header"><div class="ggi-logo">GGI</div><b>GENÇ GİRİŞİMCİ v3.5</b></div>
    <h3 style="color:var(--accent); font-size:14px;">📊 ARAÇLAR</h3>
    <div class="tool-box"><div id="calc-display"></div><div class="calc-grid">
    <button onclick="addVal('7')">7</button><button onclick="addVal('8')">8</button><button onclick="addVal('9')">9</button><button onclick="addVal('/')">/</button>
    <button onclick="addVal('4')">4</button><button onclick="addVal('5')">5</button><button onclick="addVal('6')">6</button><button onclick="addVal('*')">*</button>
    <button onclick="addVal('1')">1</button><button onclick="addVal('2')">2</button><button onclick="addVal('3')">3</button><button onclick="addVal('-')">-</button>
    <button onclick="clearCalc()" style="background:var(--accent)">C</button><button onclick="addVal('0')">0</button><button onclick="calculateResult()" style="background:#2ecc71">=</button><button onclick="addVal('+')">+</button>
    </div></div>
    <div id="game-area"><div id="player-obj"></div><p style="color:white;text-align:center;margin-top:70px;font-size:10px;">OYUN MODÜLÜ YÜKLENİYOR</p></div>
    <button class="card" style="width:100%; margin-top:20px; background:#4b6584;" onclick="toggleTheme()">🌓 GECE/GÜNDÜZ</button>
    </div>"""
    
    right = """<div class="sidebar-right"><h4 style="font-size:12px;text-align:center;">🌐 ANALİTİK</h4>
    <div class="stat-box"><span class="stat-title">Toplam Giriş</span><span id="v-count" class="stat-val">...</span></div>
    <div class="stat-box"><span class="stat-title"><span class="live-indicator"></span>Aktif</span><span id="active-users" class="stat-val">...</span></div>
    <div class="stat-box" style="margin-top:auto;"><span class="stat-title">Sunucu Durumu</span><span class="stat-val" style="color:#2ecc71;font-size:16px;">ONLINE</span></div></div>"""
    
    hidden = f"<div id='hidden-source' style='display:none;'>{long_text}</div>"
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
        content = f'<div class="container"><h1>{country.upper()} ANALİZİ</h1><div id="target-text" class="typing-text"></div><br><a href="/" class="card" style="background:#2c3e50;width:200px;margin:0 auto;text-decoration:none;">← GERİ DÖN</a></div>'
        return layout(content, data[country])
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
