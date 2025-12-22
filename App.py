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
    .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 900px; }
    
    h1 { color: #2c3e50; border-bottom: 3px solid #c0392b; padding-bottom: 10px; text-align: center; }
    
    .tool-box { background: #16213e; padding: 15px; border-radius: 10px; margin-bottom: 25px; }
    #display { background: #0f3460; color: #2ecc71; padding: 15px; text-align: right; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 20px; margin-bottom: 10px; min-height: 25px; }
    .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .calc-grid button { padding: 12px; border: none; border-radius: 5px; background: #4b6584; color: white; font-weight: bold; cursor: pointer; }

    #game-container { 
        width: 100%; height: 200px; background: #000; position: relative; 
        overflow: hidden; border-radius: 10px; border: 3px solid #e74c3c; cursor: pointer;
    }
    #player { width: 30px; height: 30px; background: #e74c3c; position: absolute; bottom: 5px; left: 40px; border-radius: 4px; z-index: 10; box-shadow: 0 0 10px #e74c3c; }
    .obstacle { width: 25px; background: #f1c40f; position: absolute; bottom: 5px; border-radius: 3px; }
    .bird { width: 35px; height: 15px; background: #3498db; position: absolute; border-radius: 10px; box-shadow: 0 0 8px #3498db; }
    #score-board { position: absolute; top: 10px; left: 10px; color: #2ecc71; font-family: monospace; font-size: 18px; z-index: 20; font-weight: bold; }
    #msg-overlay { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-weight: bold; pointer-events: none; }

    .typing-text { line-height: 1.8; font-size: 17px; color: #444; background: #fffdf9; padding: 30px; border-left: 8px solid #c0392b; border-radius: 5px; min-height: 150px; white-space: pre-wrap; }
    .back-btn { display: inline-block; margin-top: 20px; padding: 12px 25px; background: #2c3e50; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }
    
    .country-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 20px; }
    .card { padding: 20px; color: white; text-decoration: none; border-radius: 10px; text-align: center; font-weight: bold; transition: transform 0.2s; }
    .card:hover { transform: scale(1.02); }

    #hidden-data { display: none; }
</style>

<script>
    let running = false; let score = 0; let isJumping = false; let gameSpeed = 7;

    function add(v) { document.getElementById('display').innerText += v; }
    function cls() { document.getElementById('display').innerText = ''; }
    function res() { try { document.getElementById('display').innerText = eval(document.getElementById('display').innerText); } catch { document.getElementById('display').innerText = 'Hata'; } }

    function play() {
        if(running) { jump(); return; }
        running = true; score = 0; gameSpeed = 7;
        document.getElementById('score-num').innerText = '0';
        document.getElementById('msg-overlay').style.display = 'none';
        setTimeout(spawn, 1500);
    }

    function jump() {
        if(isJumping) return;
        isJumping = true;
        let p = document.getElementById('player');
        let pos = 5;
        let up = setInterval(() => {
            if(pos >= 115) {
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
        let isBird = score >= 10 && Math.random() > 0.4;
        
        if(isBird) {
            obs.className = 'bird';
            obs.style.bottom = (Math.random() > 0.5 ? '95px' : '45px');
        } else {
            obs.className = 'obstacle';
            obs.style.height = (Math.random() * 25 + 20) + 'px';
            obs.style.bottom = '5px';
        }
        obs.style.right = '-50px';
        container.appendChild(obs);

        let pos = -50;
        let loop = setInterval(() => {
            if(!running) { clearInterval(loop); obs.remove(); return; }
            pos += gameSpeed;
            obs.style.right = pos + 'px';
            let p = document.getElementById('player').getBoundingClientRect();
            let o = obs.getBoundingClientRect();
            if (p.right > o.left && p.left < o.right && p.bottom > o.top && p.top < o.bottom) {
                running = false; location.reload();
            }
            if(pos > container.offsetWidth + 50) {
                clearInterval(loop); obs.remove();
                score++; document.getElementById('score-num').innerText = score;
                gameSpeed += 0.2; spawn();
            }
        }, 20);
    }

    function startTyping() {
        const target = document.getElementById('target');
        const source = document.getElementById('hidden-text');
        if(!target || !source) return;
        const text = source.innerText.trim();
        target.innerHTML = ""; let i = 0;
        function run() {
            if (i < text.length) { target.innerHTML += text.charAt(i); i++; setTimeout(run, 15); }
        }
        run();
    }
    window.onload = startTyping;
</script>
"""

def layout(content, long_text=""):
    left = f"""
    <div class="sidebar-left">
        <h2 style="color:#e74c3c;">📊 PANEL</h2>
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
    </div>
    """
    hidden = f"<div id='hidden-data'><div id='hidden-text'>{long_text}</div></div>"
    return f"{STYLE} {left} {hidden} <div class='main-content'>{content}</div>"

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
    content = f"""<div class="container"><h1>🏛️ Dünya Tarih Arşivi (10 Ülke)</h1><div class="country-grid">{cards}</div></div>"""
    return layout(content)

# ÜLKE DATALARI
data = {
    "turkiye": "TÜRKİYE: 1923'te küllerinden doğan Cumhuriyet, Atatürk önderliğinde sanayi, eğitim ve hukuk devrimleriyle modernleşmiştir. 1923-1938 arası mucizevi büyüme yaşanmış, II. Dünya Savaşı'nda tarafsızlık korunmuş, 1950 sonrası çok partili döneme geçilmiştir. Günümüzde bölgesel bir güç olarak tarihine devam etmektedir.",
    "abd": "ABD: 1776'da İngiliz sömürgesinden bağımsızlığını ilan etti. 1860'lardaki İç Savaş sonrası sanayileşmede patlama yaşadı. İki dünya savaşından süper güç olarak çıktı. Soğuk Savaş döneminde teknoloji ve uzay yarışına yön verdi. Bugün dünyanın en büyük ekonomisi ve askeri gücü konumundadır.",
    "ingiltere": "İNGİLTERE: Magna Carta (1215) ile demokrasi temellerini attı. Sanayi Devrimi'nin beşiği oldu ve üzerinde güneş batmayan imparatorluğu kurdu. II. Dünya Savaşı'nda kilit rol oynadı. Günümüzde Avrupa'nın finans merkezi ve köklü monarşi geleneğini sürdüren modern bir demokrasidir.",
    "almanya": "ALMANYA: 1871'de Bismarck ile birleşti. I. Dünya Savaşı sonrası Weimar Cumhuriyeti ve hiperenflasyon dönemini yaşadı. II. Dünya Savaşı yıkımından 'Ekonomik Mucize' (Wirtschaftswunder) ile çıktı. 1990'da duvarın yıkılmasıyla birleşti ve bugün Avrupa Birliği'nin lokomotifidir.",
    "fransa": "FRANSA: 1789 Fransız İhtilali ile dünya siyasetini değiştirdi. Napolyon döneminde Avrupa'yı fethetti. İki dünya savaşında büyük bedeller ödedi. Beşinci Cumhuriyet ile De Gaulle önderliğinde istikrarı yakaladı. Kültür, sanat ve nükleer enerjide lider ülkelerden biridir.",
    "rusya": "RUSYA: Çarlık döneminden 1917 Bolşevik İhtilali ile SSCB'ye dönüştü. Sosyalist planlı ekonomi ile süper güç oldu. 1991'de SSCB'nin dağılmasıyla Rusya Federasyonu kuruldu. Devasa doğal kaynakları ve nükleer gücüyle dünya dengelerini belirleyen ana aktörlerden biridir.",
    "cin": "ÇİN: 5000 yıllık hanedanlık geçmişinden sonra 1949'da Mao ile Halk Cumhuriyeti kuruldu. 1978'de Deng Xiaoping'in reformlarıyla dünyaya açıldı. Son 40 yılda tarihin en hızlı ekonomik büyümesini gerçekleştirerek dünyanın üretim merkezi haline geldi.",
    "japonya": "JAPONYA: Meiji Restorasyonu ile feodalizmden moderniteye geçti. II. Dünya Savaşı'nda atom bombası yıkımını yaşadı. Ancak disiplin ve teknolojiyle küllerinden doğarak dünyanın en büyük üçüncü ekonomisi ve teknoloji devi oldu.",
    "italya": "İTALYA: Roma İmparatorluğu'nun varisidir. 1861'de birleşti (Risorgimento). Mussolini döneminde faşizmi yaşadı. Savaş sonrası moda, otomotiv ve turizmde dünya markası oldu. Akdeniz'in en önemli kültürel ve ekonomik merkezlerinden biridir.",
    "misir": "MISIR: Firavunlar döneminden İslam fethine, Osmanlı idaresinden İngiliz sömürgesine kadar devasa bir geçmişe sahiptir. 1952 devrimi ile cumhuriyet oldu. Süveyş Kanalı ile dünya ticaretinde stratejik öneme sahiptir ve Arap dünyasının kültürel kalbidir."
}

@app.route("/<country>")
def show_country(country):
    if country in data:
        name = country.upper()
        content = f'<h2>{name} TARİHİ</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
        return layout(content, data[country])
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
