from flask import Flask
import os

app = Flask(__name__)

STYLE = """
<style>
    body { font-family: 'Times New Roman', serif; background-color: #f0f2f5; margin: 0; display: flex; flex-direction: row; color: #333; min-height: 100vh; }
    
    @media (max-width: 1100px) {
        body { flex-direction: column; overflow-x: hidden; }
        .sidebar-left, .sidebar-right { position: relative !important; width: 100% !important; height: auto !important; margin: 0 !important; box-shadow: none !important; padding: 20px !important; box-sizing: border-box; }
        .main-content { margin: 0 !important; padding: 15px !important; width: 100% !important; box-sizing: border-box; }
        .container { padding: 25px !important; margin: 0 auto; width: 95% !important; box-shadow: none !important; }
        .grid { grid-template-columns: 1fr !important; gap: 12px !important; }
        .calc-grid button { padding: 18px !important; font-size: 1.2rem !important; }
        #game-container { height: 180px !important; }
        .typing-text { font-size: 16px !important; padding: 20px !important; min-height: 200px; }
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
    .calc-grid button { padding: 12px; border: none; border-radius: 5px; background: #4b6584; color: white; font-weight: bold; cursor: pointer; touch-action: manipulation; }

    #game-container { width: 100%; height: 160px; background: #000; position: relative; overflow: hidden; border-radius: 10px; border: 3px solid #555; cursor: pointer; touch-action: manipulation; }
    #player { width: 35px; height: 35px; background: #eb4d4b; position: absolute; bottom: 0; left: 30px; border-radius: 5px; transition: bottom 0.12s ease-out; }
    .obstacle { width: 25px; height: 25px; background: #f1c40f; position: absolute; bottom: 0; right: -30px; border-radius: 3px; }
    #score-board { position: absolute; top: 10px; left: 10px; color: white; font-weight: bold; z-index: 5; }

    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }
    .card { background: #ffffff; border: 1px solid #d1d8e0; padding: 25px; border-radius: 12px; text-decoration: none; text-align: center; color: #2d98da; font-weight: bold; transition: 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .card:hover { transform: translateY(-5px); border-color: #c0392b; }

    .typing-text { line-height: 1.8; font-size: 18px; color: #444; background: #fffdf9; padding: 30px; border-left: 8px solid #c0392b; border-radius: 5px; white-space: pre-wrap; margin-bottom: 20px; text-align: justify; }
    .back-btn { display: inline-block; margin-top: 20px; padding: 12px 25px; background: #2c3e50; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }
    
    #hidden-data { display: none; }
</style>

<script>
    function add(v) { document.getElementById('display').innerText += v; }
    function cls() { document.getElementById('display').innerText = ''; }
    function res() { try { document.getElementById('display').innerText = eval(document.getElementById('display').innerText); } catch { document.getElementById('display').innerText = 'Hata'; } }

    let running = false; let score = 0; let isJumping = false;
    function play() {
        if(!running) { running = true; score = 0; document.getElementById('score-num').innerText = '0'; document.getElementById('msg').style.display='none'; spawn(); }
        let p = document.getElementById('player');
        if(!isJumping) {
            isJumping = true;
            p.style.bottom = '90px';
            setTimeout(() => { p.style.bottom = '0px'; setTimeout(()=> { isJumping = false; }, 100); }, 400);
        }
    }
    function spawn() {
        if(!running) return;
        let container = document.getElementById('game-container');
        let obs = document.createElement('div');
        obs.className = 'obstacle';
        container.appendChild(obs);
        let pos = 0;
        let loop = setInterval(() => {
            if(!running) { clearInterval(loop); obs.remove(); return; }
            pos += 7; obs.style.right = pos + 'px';
            let pBottom = parseInt(window.getComputedStyle(document.getElementById('player')).getPropertyValue('bottom'));
            if(pos > (container.offsetWidth - 75) && pos < (container.offsetWidth - 30) && pBottom < 30) { 
                running = false;
                alert('Ekonomik Kriz! Skorun: ' + score); 
                location.reload(); 
            }
            if(pos > container.offsetWidth + 30) { clearInterval(loop); obs.remove(); score++; document.getElementById('score-num').innerText = score; }
        }, 20);
        setTimeout(spawn, Math.random() * 1200 + 600);
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
                setTimeout(run, 12);
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
        <div id="game-container" onclick="play()" ontouchstart="play()">
            <div id="score-board">SKOR: <span id="score-num">0</span></div>
            <div id="msg" style="color:white; text-align:center; margin-top:60px; font-weight:bold;">ENFLASYON CANAVARI: BAŞLA</div>
            <div id="player"></div>
        </div>
    </div>
    """
    right = """
    <div class="sidebar-right">
        <h3 style="border-bottom:2px solid #2c3e50;">📜 TARİHİ SÖZLÜK</h3>
        <p><b>Duyun-u Umumiye:</b> Osmanlı'nın iflasının ilanı.</p>
        <p><b>Hiperenflasyon:</b> Paranın kağıt parçasına dönüşü.</p>
        <p><b>Denarius:</b> Roma'nın değerini kaybeden gümüşü.</p>
        <p><b>Merkantilizm:</b> Fransa'nın altın biriktirme hırsı.</p>
        <p><b>Marshall Planı:</b> Avrupa'nın yeniden inşası.</p>
    </div>
    """
    hidden = f"<div id='hidden-data'><div id='hidden-text'>{long_text}</div></div>"
    return f"{STYLE} {left} {right} {hidden} <div class='main-content'>{content}</div>"

@app.route("/")
def home():
    content = """
    <div class="container">
        <h1>🏛️ Küresel Tarih & Ekonomi Arşivi</h1>
        <p style="text-align:center;">İmparatorlukların yükselişini ve çöküşünü tetikleyen ekonomik güçleri keşfedin.</p>
        <div class="grid">
            <a href="/turkiye" class="card">🇹🇷 MODERN TÜRKİYE</a>
            <a href="/osmanli" class="card">🕌 OSMANLI İMPARATORLUĞU</a>
            <a href="/weimar" class="card">🇩🇪 WEIMAR ALMANYASI</a>
            <a href="/nazi" class="card">🪖 NAZİ ALMANYASI</a>
            <a href="/fransa" class="card">🇫🇷 FRANSA EKONOMİSİ</a>
            <a href="/roma" class="card">🏛️ ANTİK ROMA</a>
        </div>
    </div>
    """
    return layout(content)

@app.route("/turkiye")
def turkiye():
    text = "TÜRKİYE CUMHURİYETİ (1923-Günümüz): Osmanlı'dan devralınan 161 milyon altın liralık devasa borç yüküne rağmen, Mustafa Kemal Atatürk önderliğinde 'Ekonomik Bağımsızlık' savaşı başlatıldı. 1923 İzmir İktisat Kongresi ile yerli üretim stratejisi belirlendi. Sümerbank, Etibank gibi kurumlarla sanayileşme hız kazandı. Cumhuriyet'in ilk 15 yılında dünya ortalamasının çok üzerinde bir büyüme hızı yakalandı. 1950 sonrası serbest piyasa geçişi, 1980'deki 24 Ocak kararları ve 2001 yapısal reformları Türkiye ekonomisinin modernleşme duraklarıdır."
    content = '<h2>🇹🇷 Modern Türkiye</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
    return layout(content, text)

@app.route("/osmanli")
def osmanli():
    text = "OSMANLI İMPARATORLUĞU: Kuruluş döneminde ticaret yollarını (İpek ve Baharat) ele geçirerek zenginleşen imparatorluk, 16. yüzyılda Amerika'dan Avrupa'ya akan gümüşün yarattığı enflasyonla (Fiyat Devrimi) sarsıldı. 1854 Kırım Savaşı ile başlayan dış borç sarmalı, 1875'te 'Ramazan Kararnamesi' ile devletin iflasını açıklamasına neden oldu. 1881'de kurulan Duyun-u Umumiye, devletin gelirlerine el koyan uluslararası bir idare olarak ekonomik bağımsızlığın sonunu temsil eder."
    content = '<h2>🕌 Osmanlı İmparatorluğu</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
    return layout(content, text)

@app.route("/weimar")
def weimar():
    text = "WEIMAR ALMANYASI (1919-1923): 1. Dünya Savaşı sonrası Versay Antlaşması'nın getirdiği 132 milyar altın marklık tazminat, Almanya'yı tarihin en meşhur hiperenflasyonuna sürükledi. 1923'te bir ABD doları 4.2 trilyon marka eşitlendi. İşçiler maaşlarını günde iki kez alıyor ve parayı hemen harcamak için dükkanlara koşuyordu. Bu ekonomik travma, orta sınıfın birikimlerini yok ederek siyasi istikrarsızlığa ve demokrasinin çöküşüne giden yolu açmıştır."
    content = '<h2>🇩🇪 Weimar Almanyası</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
    return layout(content, text)

@app.route("/nazi")
def nazi():
    text = "NAZİ ALMANYASI (1933-1945): Hitler iktidara geldiğinde ekonomiyi 'Autarky' (Kendi kendine yetme) ve savaş hazırlığı üzerine kurdu. Hjalmar Schacht tarafından geliştirilen 'MEFO Bonoları' ile gizlice silahlanma finanse edildi. İşsizlik, devasa kamu projeleri (Otobanlar gibi) ve zorunlu askerlik ile kağıt üzerinde sıfıra indirildi. Ancak bu büyüme, fethedilen topraklardaki kaynakların yağmalanmasına ve zorunlu çalışmaya dayanıyordu. Savaşın sonuna gelindiğinde Alman ekonomisi tamamen yerle bir olmuş ve para birimi yerini takas sistemine bırakmıştır."
    content = '<h2>🪖 Nazi Almanyası</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
    return layout(content, text)

@app.route("/fransa")
def fransa():
    text = "FRANSA EKONOMİSİ: 17. yüzyılda Jean-Baptiste Colbert liderliğinde geliştirilen 'Colbertizm' (Fransız Merkantilizmi), devletin ekonomiye sıkı müdahalesini ve ihracatın artırılmasını hedefledi. Ancak lüks harcamalar ve bitmek bilmeyen savaşlar, 1789 Fransız Devrimi'ni tetikleyen mali krize yol açtı. 2. Dünya Savaşı sonrası ise 'Dirigisme' modeliyle devlet planlaması öne çıktı. Bugün Fransa, yüksek tarımsal verimliliği, nükleer enerji yatırımları ve lüks tüketim ihracatıyla dünyanın en gelişmiş karma ekonomilerinden biri konumundadır."
    content = '<h2>🇫🇷 Fransa Ekonomisi</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
    return layout(content, text)

@app.route("/roma")
def roma():
    text = "ANTİK ROMA: Roma'nın çöküşü, 'para sahteciliği' yapan imparatorların hikayesidir. İlk dönemlerde gümüş oranı %98 olan Denarius parası, 3. yüzyılda %5'in altına düşürüldü. Paranın değer kaybı kontrol edilemez bir enflasyona yol açtı. İmparator Diocletianus fiyatları sabitlemeye çalışsa da (Tavan Fiyat Kararnamesi) karaborsayı engelleyemedi. Ekonomik çöküş, ordunun finanse edilememesine, şehirlerin boşalmasına ve Avrupa'nın karanlık bir feodalizm çağına girmesine neden olmuştur."
    content = '<h2>🏛️ Antik Roma</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
    return layout(content, text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
