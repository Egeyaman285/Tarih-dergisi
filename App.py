from flask import Flask
import os

app = Flask(__name__)

STYLE = """
<style>
    body { font-family: 'Times New Roman', serif; background-color: #f0f2f5; margin: 0; display: flex; flex-direction: row; color: #333; }
    
    /* Mobil ve Tablet Uyumluluğu (Responsive) */
    @media (max-width: 1100px) {
        body { flex-direction: column; }
        .sidebar-left, .sidebar-right { position: relative !important; width: 100% !important; height: auto !important; margin: 0 !important; box-shadow: none !important; }
        .main-content { margin: 0 !important; padding: 20px !important; }
        .grid { grid-template-columns: 1fr !important; }
    }

    /* Sol Panel: Araçlar ve Oyun */
    .sidebar-left { width: 320px; background: #2c3e50; color: white; height: 100vh; padding: 25px; position: fixed; left: 0; overflow-y: auto; z-index: 10; box-shadow: 2px 0 10px rgba(0,0,0,0.3); }
    
    /* Sağ Panel: Ansiklopedik Özetler */
    .sidebar-right { width: 320px; background: #ecf0f1; color: #2c3e50; height: 100vh; padding: 25px; position: fixed; right: 0; overflow-y: auto; border-left: 4px solid #bdc3c7; }
    
    /* Ana İçerik Alanı */
    .main-content { margin-left: 340px; margin-right: 340px; padding: 50px; flex-grow: 1; display: flex; justify-content: center; }
    .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 850px; }
    
    h1 { color: #2c3e50; border-bottom: 3px solid #c0392b; padding-bottom: 10px; text-align: center; }
    h2 { color: #c0392b; margin-top: 0; }

    /* Hesap Makinesi Tasarımı */
    .tool-box { background: #34495e; padding: 15px; border-radius: 10px; margin-bottom: 25px; }
    #display { background: #1a1a1a; color: #2ecc71; padding: 15px; text-align: right; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 20px; margin-bottom: 10px; min-height: 25px; }
    .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .calc-grid button { padding: 12px; border: none; border-radius: 5px; background: #4b6584; color: white; font-weight: bold; cursor: pointer; transition: 0.2s; }
    .calc-grid button:hover { background: #778ca3; }

    /* Oyun Alanı Tasarımı */
    #game-container { width: 100%; height: 160px; background: #000; position: relative; overflow: hidden; border-radius: 10px; border: 3px solid #555; cursor: pointer; }
    #player { width: 35px; height: 35px; background: #eb4d4b; position: absolute; bottom: 0; left: 30px; border-radius: 5px; transition: bottom 0.1s; }
    .obstacle { width: 25px; height: 25px; background: #f1c40f; position: absolute; bottom: 0; right: -30px; border-radius: 3px; }
    #score-board { position: absolute; top: 10px; left: 10px; color: white; font-weight: bold; font-family: sans-serif; }

    /* Bilgi Kartları */
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }
    .card { background: #ffffff; border: 1px solid #d1d8e0; padding: 25px; border-radius: 12px; text-decoration: none; text-align: center; color: #2d98da; font-weight: bold; transition: 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); border-color: #2d98da; }

    /* Yazı Efekti Paneli */
    .typing-text { line-height: 1.9; font-size: 18px; color: #444; background: #fffdf9; padding: 30px; border-left: 8px solid #c0392b; border-radius: 5px; white-space: pre-wrap; margin-bottom: 20px; }
    .back-btn { display: inline-block; margin-top: 20px; padding: 10px 20px; background: #2c3e50; color: white; text-decoration: none; border-radius: 5px; }
</style>

<script>
    // --- Matematiksel İşlemler ---
    function add(v) { document.getElementById('display').innerText += v; }
    function cls() { document.getElementById('display').innerText = ''; }
    function res() { try { document.getElementById('display').innerText = eval(document.getElementById('display').innerText); } catch { document.getElementById('display').innerText = 'Hata'; } }

    // --- Enflasyon Canavarı Oyunu ---
    let running = false; let score = 0;
    function play() {
        if(!running) { running = true; document.getElementById('msg').style.display='none'; spawn(); }
        let p = document.getElementById('player');
        if(p.style.bottom == '0px' || p.style.bottom == '') {
            p.style.bottom = '90px';
            setTimeout(() => { p.style.bottom = '0px'; }, 400);
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
            pos += 6; obs.style.right = pos + 'px';
            let pTop = parseInt(document.getElementById('player').style.bottom);
            if(pos > 230 && pos < 270 && pTop < 25) { 
                alert('Enflasyona yenildin! Skor: ' + score); location.reload(); 
            }
            if(pos > 400) { clearInterval(loop); obs.remove(); score++; document.getElementById('score-num').innerText = score; }
        }, 20);
        setTimeout(spawn, Math.random() * 1500 + 800);
    }

    // --- Yazı Yazma Fonksiyonu (Hatasız) ---
    function type(txt) {
        let i = 0; let target = document.getElementById('target');
        if(!target) return;
        target.innerHTML = "";
        function run() { if(i < txt.length) { target.innerHTML += txt.charAt(i); i++; setTimeout(run, 15); } }
        run();
    }
</script>
"""

def layout(content):
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
            <div id="msg" style="color:white; text-align:center; margin-top:60px; font-weight:bold;">BAŞLATMAK İÇİN TIKLA!</div>
            <div id="player"></div>
        </div>
        <p style="font-size:12px; color:#bdc3c7; text-align:center; margin-top:10px;">Enflasyon canavarından (sarı kutu) zıplayarak kaç!</p>
    </div>
    """
    right = """
    <div class="sidebar-right">
        <h3 style="border-bottom:2px solid #2c3e50;">📜 KISA ÖZETLER</h3>
        <p><b>🇹🇷 Türkiye:</b> 1923'te küllerinden doğan bir ekonomi.</p>
        <p><b>🕌 Osmanlı:</b> 600 yıllık bir devin mali evrimi.</p>
        <p><b>🇩🇪 Almanya:</b> Hiperenflasyonun ders niteliğindeki örneği.</p>
        <p><b>🏛️ Roma:</b> Paranın değerini düşürerek çöken ilk imparatorluk.</p>
        <p><b>🇺🇸 ABD:</b> 1929 Büyük Buhranı ve dünya krizi.</p>
        <p><b>🇭🇺 Macaristan:</b> Tarihin en büyük enflasyon rekoru (1946).</p>
    </div>
    """
    return f"{STYLE} {left} {right} <div class='main-content'>{content}</div>"

@app.route("/")
def home():
    content = """
    <div class="container">
        <h1>🏛️ Dünya Tarih & Ekonomi Arşivi</h1>
        <p style="text-align:center; font-style:italic;">Büyük medeniyetlerin yükselişini, ekonomik krizlerini ve devrimlerini keşfedin.</p>
        <div class="grid">
            <a href="/turkiye" class="card">🇹🇷 MODERN TÜRKİYE</a>
            <a href="/osmanli" class="card">🕌 OSMANLI İMPARATORLUĞU</a>
            <a href="/almanya" class="card">🇩🇪 WEIMAR ALMANYASI</a>
            <a href="/roma" class="card">🏛️ ANTİK ROMA</a>
            <a href="/macaristan" class="card">🇭🇺 MACARİSTAN REKORU</a>
            <a href="/usa" class="card">🇺🇸 ABD BÜYÜK BUHRANI</a>
        </div>
    </div>
    """
    return layout(content)

@app.route("/turkiye")
def turkiye():
    t = """KURULUŞ: 29 Ekim 1923
Tarihsel Süreç: Birinci Dünya Savaşı'ndan yorgun çıkan bir milletin, Mustafa Kemal Atatürk liderliğinde gerçekleştirdiği ekonomik mucizedir. 1923 İzmir İktisat Kongresi, 'siyasi bağımsızlığın ancak ekonomik bağımsızlıkla taçlanacağını' ilan etmiştir.

Büyük Devrimler: 
1. Saltanatın Kaldırılması (1922) ve Cumhuriyet'in İlanı (1923).
2. Şapka ve Kıyafet Devrimi (1925), Medeni Kanun (1926).
3. Harf Devrimi (1928): Okuryazarlık oranını bir gecede değiştiren en büyük kültürel devrimdir.

Ekonomik Krizler: 1958 borç krizi, 1970'lerin döviz darlığı, 1994 krizi ve 2001 büyük bankacılık krizi. Türkiye, her krizden yapısal reformlar ve güçlü bir üretim iradesiyle çıkmayı başarmıştır."""
    return layout(f'<div class="container"><h2>🇹🇷 Türkiye Cumhuriyeti</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a></div><script>setTimeout(() => {{ type("{t}"); }}, 300);</script>')

@app.route("/osmanli")
def osmanli():
    t = """KURULUŞ: 1299 (Söğüt)
Tarihsel Süreç: Küçük bir uç beyliğinden, üç kıtaya hükmeden bir cihan devletine uzanan yolculuk. Fatih Sultan Mehmet'in İstanbul'u fethi (1453), Orta Çağ'ı kapatıp Yeni Çağ'ı açan en büyük askeri ve siyasi devrimdir.

Ekonomik Sistem: Osmanlı ekonomisi 'Narh' sistemi ve 'Lonca' teşkilatı üzerine kuruluydu. Ancak 16. yüzyılda Amerika'dan gelen gümüşün Avrupa'yı istila etmesi, Osmanlı akçesinin değerini ilk kez sarsmıştır.

Çöküşün Mali Sebepleri: 1854 Kırım Savaşı sırasında alınan ilk dış borç, imparatorluğun mali sonunun başlangıcı olmuştur. Ödenemeyen borçlar sonrası 1881'de Duyun-u Umumiye'nin kurulması, ekonomik bağımsızlığın fiilen yitirilmesine yol açmıştır."""
    return layout(f'<div class="container"><h2>🕌 Osmanlı İmparatorluğu</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a></div><script>setTimeout(() => {{ type("{t}"); }}, 300);</script>')

@app.route("/almanya")
def almanya():
    t = """DÖNEM: Weimar Cumhuriyeti (1919-1933)
Ekonomik Facia: 1923 yılı, dünya tarihindeki en meşhur hiperenflasyon dönemidir. Birinci Dünya Savaşı sonrası ağır tazminatlar altında ezilen Almanya, karşılıksız para basarak borçlarını ödemeye çalıştı.

Sonuç: Para o kadar değersizleşti ki, insanlar bir somun ekmek almak için el arabasıyla banknot taşıyordu. Çocuklar paralarla kule yaparak oyun oynuyor, ev hanımları odun almaktan daha ucuz olduğu için banknotları şöminede yakıyordu. Bu ekonomik yıkım, aşırı uç siyasi hareketlerin (Nazizm) yükselmesine zemin hazırlamıştır."""
    return layout(f'<div class="container"><h2>🇩🇪 Almanya Hiperenflasyonu</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a></div><script>setTimeout(() => {{ type("{t}"); }}, 300);</script>')

@app.route("/roma")
def roma():
    t = """KURULUŞ: M.Ö. 753
Düşüşün Sebebi: Roma İmparatorluğu'nun çöküşü sadece savaşlar değil, 'paranın hileyle bitirilmesi'dir. İmparatorlar, ordu maaşlarını ödemek için gümüş paranın (Denarius) içindeki gümüş miktarını sürekli azaltıp bakır oranını artırdılar.

Ekonomik Devrim: Roma, tarihteki ilk enflasyon kontrol yasası olan 'Diocletianus Fiyat Fermanı'nı çıkarmıştır ancak bu emir fiyat artışlarını durduramamıştır. Ticaret çökmüş, insanlar şehri terk ederek kendi yemeklerini yetiştirmek üzere köylere kaçmıştır. Bu durum feodalizmin temellerini atmıştır."""
    return layout(f'<div class="container"><h2>🏛️ Antik Roma</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a></div><script>setTimeout(() => {{ type("{t}"); }}, 300);</script>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
