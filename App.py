from flask import Flask
import os

app = Flask(__name__)

# --- STİL VE TASARIM ---
STYLE = """
<style>
    :root { --bg-color: #f0f2f5; --text-color: #333; --cont-bg: white; --accent: #e74c3c; --dark-accent: #c0392b; }
    .dark-mode { --bg-color: #0f0f1b; --text-color: #e0e0e0; --cont-bg: #1a1a2e; --accent: #f1c40f; --dark-accent: #d4ac0d; }

    body { font-family: 'Segoe UI', Arial, sans-serif; background-color: var(--bg-color); margin: 0; display: flex; flex-direction: row; color: var(--text-color); min-height: 100vh; transition: 0.3s; overflow-x: hidden; }
    
    /* SOL PANEL - ARAÇLAR VE YÖNETİM */
    .sidebar-left { width: 320px; background: #1a1a2e; color: white; height: 100vh; padding: 25px; position: fixed; left: 0; overflow-y: auto; z-index: 100; border-right: 4px solid var(--accent); box-shadow: 5px 0 15px rgba(0,0,0,0.5); }
    .ggi-header { text-align: center; margin-bottom: 30px; }
    .ggi-logo { width: 70px; height: 70px; background: linear-gradient(135deg, var(--accent), var(--dark-accent)); border-radius: 15px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 24px; color: white; margin: 0 auto 10px auto; border: 2px solid rgba(255,255,255,0.2); }

    /* SAĞ PANEL - GELİŞMİŞ ANALİTİK */
    .sidebar-right { width: 220px; background: #16213e; color: white; height: 100vh; padding: 25px; position: fixed; right: 0; border-left: 4px solid var(--accent); z-index: 100; display: flex; flex-direction: column; }
    .stat-box { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1); text-align: center; transition: 0.3s; }
    .stat-box:hover { transform: scale(1.05); background: rgba(255,255,255,0.1); }
    .stat-val { font-size: 26px; font-weight: bold; color: var(--accent); display: block; text-shadow: 0 0 10px rgba(231, 76, 60, 0.3); }
    .stat-title { font-size: 11px; text-transform: uppercase; color: #8e9aaf; letter-spacing: 1px; }
    .live-indicator { height: 10px; width: 10px; background-color: #2ecc71; border-radius: 50%; display: inline-block; margin-right: 8px; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(46, 204, 113, 0); } 100% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); } }

    /* ANA İÇERİK ALANI */
    .main-content { margin-left: 320px; margin-right: 220px; padding: 60px; flex-grow: 1; display: flex; flex-direction: column; align-items: center; }
    .container { background: var(--cont-bg); padding: 50px; border-radius: 20px; box-shadow: 0 15px 40px rgba(0,0,0,0.15); width: 100%; max-width: 1000px; min-height: 80vh; position: relative; }
    
    h1 { font-size: 32px; color: var(--accent); border-bottom: 3px solid var(--accent); padding-bottom: 10px; margin-bottom: 30px; text-align: center; }
    
    /* ÜLKE KARTLARI */
    .country-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; margin-top: 30px; }
    .card { padding: 20px; color: white; text-decoration: none; border-radius: 12px; text-align: center; font-weight: bold; font-size: 14px; transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); display: flex; align-items: center; justify-content: center; min-height: 60px; }
    .card:hover { transform: translateY(-8px) rotate(2deg); box-shadow: 0 10px 20px rgba(0,0,0,0.2); filter: brightness(1.2); }

    /* BİLGİ METNİ ALANI */
    .typing-text { line-height: 2; font-size: 17px; background: rgba(0,0,0,0.02); padding: 40px; border-left: 8px solid var(--accent); border-radius: 10px; white-space: pre-wrap; color: var(--text-color); text-align: justify; box-shadow: inset 5px 5px 15px rgba(0,0,0,0.05); }

    /* HESAP MAKİNESİ */
    .tool-box { background: #0f3460; padding: 20px; border-radius: 15px; margin-bottom: 30px; box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }
    #display { background: #16213e; color: #2ecc71; padding: 15px; text-align: right; border-radius: 8px; font-family: 'Consolas', monospace; font-size: 22px; margin-bottom: 15px; border: 1px solid #4b6584; min-height: 30px; }
    .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
    .calc-grid button { padding: 15px; border: none; border-radius: 8px; background: #4b6584; color: white; font-weight: bold; cursor: pointer; transition: 0.2s; }
    .calc-grid button:hover { background: var(--accent); }

    /* DİNOZOR OYUNU */
    #game-container { width: 100%; height: 200px; background: #000; position: relative; overflow: hidden; border-radius: 12px; border: 3px solid var(--accent); cursor: pointer; }
    #player { width: 30px; height: 30px; background: #e74c3c; position: absolute; bottom: 5px; left: 50px; border-radius: 5px; transition: 0.1s; box-shadow: 0 0 10px #e74c3c; }
    .obstacle { width: 25px; background: #f1c40f; position: absolute; bottom: 5px; border-radius: 4px; box-shadow: 0 0 10px #f1c40f; }
    #score-board { position: absolute; top: 10px; right: 10px; color: #2ecc71; font-family: monospace; font-size: 18px; font-weight: bold; }

    /* BUTONLAR */
    .toggle-btn { cursor: pointer; padding: 12px; border-radius: 8px; border: none; background: var(--accent); color: white; font-weight: bold; width: 100%; margin-top: 15px; transition: 0.3s; }
    .back-btn { display: inline-block; margin-top: 30px; padding: 15px 30px; background: #2c3e50; color: white; text-decoration: none; border-radius: 10px; font-weight: bold; transition: 0.3s; }
    .back-btn:hover { background: var(--accent); transform: translateX(-5px); }

    /* RESPONSIVE */
    @media (max-width: 1300px) { .sidebar-right { display: none; } .main-content { margin-right: 0; } }
    @media (max-width: 900px) { 
        body { flex-direction: column; } 
        .sidebar-left { position: relative; width: 100%; height: auto; border-right: none; } 
        .main-content { margin-left: 0; padding: 20px; } 
        .country-grid { grid-template-columns: repeat(2, 1fr); }
    }
</style>

<script>
    // --- ANALİTİK MOTORU ---
    function initStats() {
        let visitors = localStorage.getItem('ggi_v_count') || 15420;
        visitors = parseInt(visitors) + Math.floor(Math.random() * 3) + 1;
        localStorage.setItem('ggi_v_count', visitors);
        document.getElementById('v-count').innerText = visitors.toLocaleString();
        
        setInterval(() => {
            let active = Math.floor(Math.random() * 15) + 5;
            document.getElementById('active-users').innerText = active;
        }, 3000);
    }

    // --- TEMA MOTORU ---
    function toggleTheme() {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('ggi_pref_theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
    }

    // --- HESAP MAKİNESİ FONKSİYONLARI ---
    function add(v) { document.getElementById('display').innerText += v; }
    function cls() { document.getElementById('display').innerText = ''; }
    function res() { 
        try { 
            let exp = document.getElementById('display').innerText;
            document.getElementById('display').innerText = eval(exp); 
        } catch { 
            document.getElementById('display').innerText = 'HATA'; 
        } 
    }

    // --- OYUN MOTORU (HİÇ BOZULMADI) ---
    let running = false; let score = 0; let isJumping = false;
    function play() {
        if(running) { jump(); return; }
        running = true; score = 0;
        document.getElementById('score-num').innerText = '0';
        document.getElementById('msg-overlay').style.display = 'none';
        spawn();
    }
    function jump() { 
        if(isJumping) return; 
        isJumping = true; 
        let p = document.getElementById('player'); 
        let pos = 5;
        let up = setInterval(() => { 
            if(pos >= 120) { 
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
            if (p.right > o.left && p.left < o.right && p.bottom > o.top && p.top < o.bottom) { 
                running = false; 
                location.reload(); 
            }
            if(pos > container.offsetWidth) { 
                clearInterval(loop); obs.remove(); 
                score++; 
                document.getElementById('score-num').innerText = score; 
                spawn(); 
            }
        }, 20);
    }

    // --- YAZI EFEKTİ VE AÇILIŞ ---
    function start() {
        initStats();
        if(localStorage.getItem('ggi_pref_theme') === 'dark') document.body.classList.add('dark-mode');
        
        const target = document.getElementById('target');
        const source = document.getElementById('hidden-text');
        if(!target || !source) return;
        
        const text = source.innerText.trim();
        target.innerHTML = ""; 
        let i = 0;
        function typing() { 
            if (i < text.length) { 
                target.innerHTML += text.charAt(i); 
                i++; 
                setTimeout(typing, 1); 
            } 
        }
        typing();
    }
    window.onload = start;
</script>
"""

# --- DEVASA VERİ SETİ ---
data = {
    "turkiye": """[TÜRKİYE CUMHURİYETİ: STRATEJİK, TARİHSEL VE TEKNOLOJİK ANALİZ]

1. JEOPOLİTİK KONUM: Türkiye, dünya adasının kalbi (Heartland) ve kenar kuşağı (Rimland) arasında bir kilit taşıdır. İstanbul ve Çanakkale Boğazları, Karadeniz'in dünyaya açılan tek kapısıdır. Bu konum, Türkiye'yi hem NATO'nun en güçlü kanadı hem de Orta Doğu ve Kafkaslar'ın istikrar merkezi yapar.

2. KURTULUŞ SAVAŞI VE ASKERİ DEHA: 1919-1922 yılları arasında Mustafa Kemal Atatürk önderliğinde verilen mücadele, lojistik imkansızlıklara rağmen kazanılmış bir strateji harikasıdır. Sakarya Meydan Muharebesi, dünya harp tarihine "Topyekün Savaş" kavramını sokmuştur. 1923'te Lozan ile tescillenen bağımsızlık, sömürge altındaki tüm uluslara ilham vermiştir.

3. MODERN TEKNOLOJİ VE SAVUNMA: 21. yüzyılda Türkiye, savunma sanayiinde bir devrim yapmıştır. Bayraktar TB2 ve AKINCI gibi İHA/SİHA sistemleri, modern savaş doktrinini değiştirmiş ve Karabağ'dan Ukrayna'ya kadar pek çok sahada dengeleri belirlemiştir. TCG Anadolu gemisi ve yerli otomobil TOGG, ülkenin ağır sanayi ve dijital dönüşümündeki kararlılığını gösterir.

4. KÜLTÜREL VE GENETİK MİRAS: Anadolu, Hititlerden Osmanlı'ya kadar 20'den fazla büyük medeniyete ev sahipliği yapmıştır. Göbeklitepe (M.Ö. 10.000), tarımın ve yerleşik hayatın sıfır noktası olarak kabul edilir. Bugün Türkiye, laik-demokratik yapısıyla İslam dünyasında eşi benzeri olmayan bir modeldir.""",

    "nazi": """[NAZİ ALMANYASI: TOTALİTER REJİMİN ANATOMİSİ VE ÇÖKÜŞÜ]

1. PROPAGANDA VE KİTLE KONTROLÜ: 1933 yılında NSDAP'nin iktidara gelişiyle, Joseph Goebbels tarafından yönetilen "Halkı Aydınlatma ve Propaganda Bakanlığı", radyoyu ve sinemayı bir silah olarak kullanmıştır. "Büyük Yalan" tekniği ile Alman toplumu tek bir ideoloji etrafında militarize edilmiştir.

2. ASKERİ STRATEJİ VE BLITZKRIEG: Nazi ordusu (Wehrmacht), II. Dünya Savaşı'nın başında "Blitzkrieg" (Yıldırım Savaşı) taktiğini geliştirmiştir. Tank birlikleri (Panzer), hava desteği (Luftwaffe) ve hızlı piyade hareketleriyle Polonya ve Fransa'yı haftalar içinde düşürmüştür. Ancak bu lojistik hızı, Sovyetler Birliği'nin devasa coğrafyasında (Barbarossa Harekatı) tükenmiştir.

3. İNSANLIK SUÇLARI VE HOLOKOST: Rejim, "Ari Irk" yaratma saplantısıyla 6 milyon Yahudi, Roman ve muhalifi toplama kamplarında (Auschwitz gibi) endüstriyel yöntemlerle katletmiştir. Bu trajedi, 1945'teki Nürnberg Mahkemeleri ile modern uluslararası ceza hukukunun doğmasına neden olmuştur.""",

    "abd": """[ABD: KÜRESEL HEGEMONYA VE TEKNOLOJİK ÜSTÜNLÜK]

1. KURULUŞ VE ANAYASAL DÜZEN: 1776'da ilan edilen Bağımsızlık Bildirgesi, Aydınlanma Çağı'nın "Kuvvetler Ayrılığı" ve "Bireysel Özgürlük" fikirlerini ilk kez bir devlet yapısına dönüştürmüştür. 1787 Anayasası, dünyadaki en eski ve hala yürürlükte olan yazılı anayasadır.

2. EKONOMİK DOMİNASYON: II. Dünya Savaşı'ndan sonra Bretton Woods Sistemi ile ABD Doları küresel rezerv para birimi olmuştur. Marshall Planı ile Avrupa'yı finanse ederek Batı dünyasının liderliğini ele almıştır. Bugün Silikon Vadisi üzerinden Apple, Google ve Microsoft gibi devlerle dijital dünyayı kontrol etmektedir.

3. ASKERİ GÜÇ VE NASA: ABD, dünyanın en büyük askeri bütçesine sahip ülkesidir. 11 uçak gemisi filosuyla okyanuslarda hakimiyet kurar. 1969'da Apollo 11 ile Ay'a iniş yapması, Soğuk Savaş'taki teknolojik üstünlüğünü kanıtlamıştır.""",

    "cin": """[ÇİN: MERKEZ İMPARATORLUK VE 2049 VİZYONU]

1. TARİHSEL DERİNLİK: Çin, kesintisiz 4000 yıllık bir bürokrasi geleneğine sahiptir. "Mandate of Heaven" (Göklerin Yetkisi) inancı, hanedanların meşruiyetini sağlamıştır. Çin Seddi, tarihteki en büyük savunma projesi olarak kuzeydeki göçebe akınlarını (Türk ve Moğol) durdurmak için inşa edilmiştir.

2. EKONOMİK MUCİZE: 1978'de Deng Xiaoping'in başlattığı "Dört Modernizasyon", komünist bir yapıyı kapitalist piyasa ekonomisiyle birleştirmiştir. Bugün Çin, satın alma gücü paritesine göre dünyanın en büyük ekonomisidir. "Kuşak ve Yol Girişimi" ile Asya, Avrupa ve Afrika'yı ticaret yollarıyla kendine bağlamaktadır.

3. TEKNOLOJİK YARIŞ: Çin, 5G, kuantum bilgisayarlar ve yapay zeka alanında ABD ile kafa kafaya yarışmaktadır. Sosyal Kredi Sistemi ile vatandaşlarını dijital olarak izleyen ilk büyük devlettir.""",

    "japonya": """[JAPONYA: SAMURAY RUHU VE ROBOTİK GELECEK]

1. MEİJİ RESTORASYONU: 1868'de Japonya, sömürge olmaktan kurtulmak için "Batı'nın ilmini al, Japonya'nın ruhunu koru" prensibiyle devasa bir modernleşme başlattı. Sadece 30 yılda feodal bir toplumdan, Rusya'yı yenen bir endüstri gücüne dönüştü.

2. II. DÜNYA SAVAŞI VE ATOM BOMBASI: Hiroşima ve Nagazaki'ye atılan atom bombaları Japonya'yı teslim olmaya zorladı. Ancak bu yıkım, Japonların "Kaizen" (Sürekli İyileştirme) felsefesini doğurdu.

3. TEKNOLOJİ VE OTOMOTİV: Bugün Japonya, hassas mühendislik ve robotikte dünya lideridir. Toyota, Honda ve Panasonic gibi markalar kalite standartlarını belirler. Dünyanın en yaşlı nüfusuna sahip olmasına rağmen otomasyon sayesinde gücünü korumaktadır.""",

    "rusya": """[RUSYA: AVRASYA'NIN ÇELİK DUVARI VE ENERJİ SİLAHI]

1. ÇARLIKTAN SOVYETLERE: 1917 Bolşevik İhtilali, dünyada ilk kez sosyalist bir devletin kurulmasını sağladı. Stalin döneminde Rusya, ağır sanayileşme hamlesiyle bir süper güce dönüştü.

2. SOĞUK SAVAŞ VE UZAY: 1957'de Sputnik'in fırlatılması ve 1961'de Yuri Gagarin'in uzaya çıkması, Rusya'nın bilimsel zirvesiydi. Bugün Rusya, dünyanın en büyük nükleer cephaneliğine sahiptir.

3. ENERJİ JEOPOLİTİĞİ: Dünyanın en büyük doğal gaz rezervlerine sahip olan Rusya, enerjiyi Avrupa ve Asya üzerinde bir dış politika aracı olarak kullanmaktadır.""",

    "ingiltere": """[İNGİLTE: ÜZERİNDE GÜNEŞ BATMAYAN İMPARATORLUKTAN FİNANS MERKEZİNE]

1. SANAYİ DEVRİMİ: Buharlı makinenin icadı (James Watt) ile insanlık tarihinde kas gücünden makine gücüne geçiş burada başladı. Bu devrim, İngiltere'yi 19. yüzyılın küresel atölyesi yaptı.

2. DONANMA VE KOLONİALİZM: İngiliz Kraliyet Donanması, 200 yıl boyunca okyanusların tek hakimiydi. Hindistan'dan Avustralya'ya kadar uzanan koloniler, bugünkü İngilizce dominasyonunun sebebidir.

3. LONDRA VE FİNANS: Bugün Londra (The City), New York ile birlikte dünya para piyasalarının iki kalbinden biridir.""",

    "italya": """[İTALYA: RÖNESANS'IN BEŞİĞİ VE TASARIMIN KALBİ]

1. ROMA MİRASI: Modern Batı medeniyetinin hukuk, mimari ve yönetim sistemleri Roma'da kuruldu. Vatikan ise Katolik dünyasının ruhani merkezi olarak İtalya'nın ortasındadır.

2. RÖNESANS: Da Vinci, Michelangelo ve Galilei gibi dehalar; sanatı ve bilimi Orta Çağ dogmalarından kurtarmıştır.

3. TASARIM VE MODA: Ferrari, Lamborghini, Armani... İtalya bugün "Lüks ve Estetik" dendiğinde dünyada ilk akla gelen ülkedir.""",

    "misir": """[MISIR: NİL'İN ARMAĞANI VE PİRAMİTLERİN SIRRI]

1. ANTİK MÜHENDİSLİK: Giza Piramitleri, 4500 yıl önce inşa edilmesine rağmen hala gizemini korumaktadır. Nil Nehri'nin taşma zamanlarını hesaplayan Mısırlılar, gelişmiş bir astronomi ve matematik kültürü kurmuştur.

2. SÜVEYŞ KANALI: 1869'da açılan kanal, Avrupa ile Asya arasındaki deniz yolunu binlerce kilometre kısalttı. Mısır bugün bu kanal sayesinde küresel ticaretin boğazını tutmaktadır.""",

    "guney_kore": """[GÜNEY KORE: HAN NEHRİ MUCİZESİ VE K-KÜLTÜR]

1. SAVAŞTAN ZİRVEYE: 1953'te sona eren Kore Savaşı'ndan sonra dünyanın en fakir ülkelerinden biri olan G. Kore, eğitime yaptığı yatırımla 30 yılda devleşti.

2. TEKNOLOJİ DEVLERİ: Samsung ve LG, bugün dünya panel ve yarı iletken pazarının liderleridir.

3. KÜLTÜREL İHRACAT: BTS, Squid Game ve Oscar ödüllü Parasite... Güney Kore, "Yumuşak Güç" (Soft Power) ile dünyadaki gençlik trendlerini belirlemektedir."""
}

# --- YAPI OLUŞTURUCU ---
def layout(content, long_text=""):
    left = f"""
    <div class="sidebar-left">
        <div class="ggi-header">
            <div class="ggi-logo">GGI</div>
            <span style="font-weight:bold; font-size:14px; color:#8e9aaf;">GENÇ GİRİŞİMİ TARİH v3.5</span>
        </div>
        
        <h3 style="color:var(--accent); font-size:14px; margin-bottom:10px;">📊 ARAÇLAR</h3>
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
            <div id="msg-overlay" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); color:white;">OYNA</div>
            <div id="player"></div>
        </div>

        <div class="settings-panel">
            <button class="toggle-btn" onclick="toggleTheme()">🌓 GECE/GÜNDÜZ</button>
            <div class="admin-info">
                <p><strong>👤 KURUCU:</strong> Ege (GGI)</p>
                <p><strong>💻 SİSTEM:</strong> Python / Render</p>
                <p><strong>📅 GÜNCELLEME:</strong> 2025 v3.5</p>
            </div>
        </div>
    </div>
    """
    
    right = """
    <div class="sidebar-right">
        <h4 style="font-size:12px; margin-bottom:20px; text-align:center;">🌐 CANLI ANALİTİK</h4>
        <div class="stat-box">
            <span class="stat-title">Toplam Ziyaretçi</span>
            <span id="v-count" class="stat-val">...</span>
        </div>
        <div class="stat-box">
            <span class="stat-title"><span class="live-indicator"></span>Aktif Kullanıcı</span>
            <span id="active-users" class="stat-val">...</span>
        </div>
        <div class="stat-box" style="margin-top:auto;">
            <span class="stat-title">Sunucu Durumu</span>
            <span class="stat-val" style="color:#2ecc71; font-size:18px;">AKTİF</span>
        </div>
    </div>
    """
    
    hidden_div = f"<div id='hidden-data' style='display:none;'><div id='hidden-text'>{long_text}</div></div>"
    return f"{STYLE} {left} {right} {hidden_div} <div class='main-content'>{content}</div>"

@app.route("/")
def home():
    countries = [
        ("TÜRKİYE", "/turkiye", "#c0392b"), ("ABD", "/abd", "#2980b9"), ("İNGİLTERE", "/ingiltere", "#2c3e50"),
        ("ALMANYA", "/almanya", "#f39c12"), ("NAZİ DÖNEMİ", "/nazi", "#000000"), ("ÇİN", "/cin", "#d35400"),
        ("JAPONYA", "/japonya", "#7f8c8d"), ("RUSYA", "/rusya", "#c0392b"), ("İTALYA", "/italya", "#27ae60"),
        ("MISIR", "/misir", "#8e44ad"), ("G. KORE", "/guney_kore", "#3498db")
    ]
    cards = "".join([f'<a href="{url}" class="card" style="background:{color}">{name}</a>' for name, url, color in countries])
    content = f"""
    <div class="container">
        <h1>🏛️ GENÇ GİRİŞİMCİ TARİH ARŞİVİ</h1>
        <p style="text-align:center; font-size:18px; color:#7f8c8d;">Dünya Tarihini Değiştiren Medeniyetler ve Jeopolitik Analizler</p>
        <div class="country-grid">{cards}</div>
        <hr style="margin-top:40px; border:0; border-top:1px solid #ddd;">
        <p style="font-size:13px; color:#95a5a6; text-align:center;">Bu platform Ege tarafından genç girişimciler için tasarlanmış bağımsız bir bilgi bankasıdır.</p>
    </div>
    """
    return layout(content)

@app.route("/<country>")
def show_country(country):
    if country in data:
        name = country.replace("_", " ").upper()
        content = f"""
        <div class="container">
            <h1>{name} ANALİZ RAPORU</h1>
            <div id="target" class="typing-text"></div>
            <br>
            <a href="/" class="back-btn">← ANSİKLOPEDİYE GERİ DÖN</a>
        </div>
        """
        return layout(content, data[country])
    return home()

if __name__ == "__main__":
    # Render port desteği
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
