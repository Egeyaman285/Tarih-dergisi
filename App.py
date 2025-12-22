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
    content = f"""<div class="container"><h1>🏛️ Dünya Tarih Arşivi (Derinlemesine Analiz)</h1><div class="country-grid">{cards}</div></div>"""
    return layout(content)

# GENİŞLETİLMİŞ ÜLKE DATALARI (2 KAT BİLGİ)
data = {
    "turkiye": "TÜRKİYE: 1923'te küllerinden doğan Cumhuriyet, sadece askeri değil, topyekün bir toplumsal dönüşümdür. Mustafa Kemal Atatürk'ün liderliğinde İzmir İktisat Kongresi ile temelleri atılan milli ekonomi, 'devletçilik' ilkesiyle sanayi tesislerini kurmuştur. Eğitim birliği (Tevhid-i Tedrisat), medeni kanun ve kadın hakları gibi devrimlerle Batı medeniyeti seviyesi hedeflenmiştir. II. Dünya Savaşı'nın yıkıcı etkilerinden 'aktif tarafsızlık' ile korunan Türkiye, 1946 sonrası çok partili hayata geçmiş ve 1952'de NATO'ya girerek jeopolitik önemini tescillemiştir. Bugün 100. yılını geride bırakan ülke, savunma sanayiinden enerji koridorlarına kadar geniş bir yelpazede küresel bir aktör olma yolunda tarihsel mirasını taşımaktadır.",
    "abd": "AMERİKA BİRLEŞİK DEVLETLERİ: 1776'da 'Bağımsızlık Bildirgesi' ile İngiliz monarşisine başkaldıran 13 koloni, tarihin ilk modern anayasal demokrasisini kurmuştur. 19. yüzyılda 'Kader Birliği' (Manifest Destiny) anlayışıyla batıya genişleyen ülke, 1861-1865 yılları arasındaki kanlı İç Savaş ile köleliği kaldırmış ve endüstriyel birliğini sağlamıştır. I. Dünya Savaşı'na sonradan girerek dengeleri değiştiren ABD, 1929 Büyük Buhranı'nı Roosevelt'in 'New Deal' politikalarıyla aşmıştır. II. Dünya Savaşı sonrası 'Truman Doktrini' ve 'Marshall Planı' ile Batı dünyasının lideri (Süper Güç) olmuş, Soğuk Savaş'ta Sovyetler Birliği'ni teknolojik ve ekonomik olarak mağlup etmiştir. Günümüzde dijital devrimin merkezi olan Silikon Vadisi ve küresel finansın kalbi Wall Street ile dünya ekonomisini yönlendirmeyi sürdürmektedir.",
    "ingiltere": "İNGİLTERE: Adanın tarihsel yolculuğu 1215'te kralın yetkilerini kısıtlayan 'Magna Carta' ile başlamış, bu adım modern parlamenter demokrasinin tohumlarını atmıştır. 18. yüzyılda buharlı makinenin icadıyla başlayan Sanayi Devrimi, İngiltere'yi 'dünyanın atölyesi' haline getirmiş ve Britanya İmparatorluğu'nun denizlerdeki mutlak hakimiyetini başlatmıştır. Viktorya döneminde sömürgeciliğin zirvesine ulaşan krallık, 'üzerinde güneş batmayan imparatorluk' unvanını almıştır. I. ve II. Dünya Savaşları'nda Almanya'ya karşı direncin kalesi olan ülke, savaş sonrası sömürgelerinden çekilerek İngiliz Milletler Topluluğu'nu (Commonwealth) kurmuştur. 1970'lerdeki ekonomik durgunluğu Thatcher döneminin serbest piyasa hamleleriyle aşan Birleşik Krallık, Brexit ile Avrupa Birliği'nden ayrılarak kendine yeni bir küresel rota çizmiştir.",
    "almanya": "ALMANYA: 1871'de Otto von Bismarck'ın 'Kan ve Çelik' politikasıyla Prusya liderliğinde birleşen Alman İmparatorluğu, kısa sürede Avrupa'nın endüstriyel devi olmuştur. I. Dünya Savaşı'nın yenilgisi ve Versay Antlaşması'nın ağır tazminatları, Weimar Cumhuriyeti'nde hiperenflasyona ve siyasi istikrarsızlığa yol açmıştır. Bu ortamdan doğan Nazi rejimi, II. Dünya Savaşı ve Holokost trajedisiyle dünyayı yıkıma sürüklemiştir. 1945'te harabeye dönen ülke Doğu ve Batı olarak ikiye bölünmüş, Batı Almanya 'Sosyal Piyasa Ekonomisi' modeliyle mucizevi bir kalkınma (Wirtschaftswunder) gerçekleştirmiştir. 1989'da Berlin Duvarı'nın yıkılması ve 1990'daki resmi birleşme ile Almanya, bugün Avrupa Birliği'nin en büyük ekonomisi, teknoloji ve mühendislik merkezi konumuna yükselmiştir.",
    "fransa": "FRANSA: 1789 Fransız İhtilali'nin 'Hürriyet, Müsavat, Uhuvvet' sloganı, sadece Fransa'yı değil tüm dünyayı ulus devlet fikriyle tanıştırmıştır. Napolyon Bonapart döneminde Avrupa'nın büyük kısmına hükmeden Fransız orduları, aynı zamanda modern hukuk normlarını da yaymıştır. 19. ve 20. yüzyıllarda geniş bir sömürge imparatorluğu kuran ülke, her iki dünya savaşında da topraklarında ağır çarpışmalar yaşamıştır. 1958'de Charles de Gaulle'ün kurduğu Beşinci Cumhuriyet ile siyasi istikrarı sağlayan Fransa, nükleer güç sahibi olması ve BM Güvenlik Konseyi'ndeki veto hakkıyla küresel siyasette söz sahibidir. Havacılıktan (Airbus) lüks tüketime, felsefeden gastronomiye kadar geniş bir kültürel etki alanına sahip olan ülke, AB'nin siyasi vizyonunun mimarlarındandır.",
    "rusya": "RUSYA: Çarlık Rusyası'nın 19. yüzyıldaki genişlemesi, 1917'de patlak veren Bolşevik İhtilali ile tarihin en büyük toplumsal deneylerinden biri olan SSCB'nin kurulmasıyla sonuçlanmıştır. Stalin döneminde ağır sanayileşme ve kolektifleştirme ile bir köylü toplumundan nükleer süper güce dönüşen Sovyetler, II. Dünya Savaşı'nda Nazileri yenen ana güçlerden biri olmuştur. Soğuk Savaş'ta ABD ile uzay yarışı ve ideolojik rekabete giren SSCB, 1991'de ekonomik tıkanıklık sonucu dağılmıştır. Yeltsin dönemindeki kaotik geçişten sonra Putin ile birlikte devlet otoritesini yeniden sağlayan Rusya Federasyonu, devasa enerji kaynaklarını (Doğalgaz ve Petrol) stratejik bir koz olarak kullanmaktadır. Bugün, Ukrayna savaşı ve Batı ile olan gerilimler ışığında Avrasya'nın belirleyici askeri gücü olma özelliğini korumaktadır.",
    "cin": "ÇİN: 5000 yıllık kadim bir uygarlıktan, 19. yüzyılda 'Afyon Savaşları' ile sömürgeleşme aşamasına gelen Çin, 1949'da Mao Zedong önderliğindeki komünist devrimle yeni bir kimlik kazanmıştır. 'Büyük İleri Atılım' ve 'Kültür Devrimi' gibi sancılı süreçlerden sonra 1978'de Deng Xiaoping'in başlattığı 'Açılım ve Reform' politikası, Çin'in devlet kontrolündeki kapitalizm modeline geçişini sağlamıştır. Son 40 yılda 800 milyon insanı yoksulluktan çıkaran ülke, dünyanın üretim merkezi haline gelmiştir. 'Kuşak ve Yol İnisiyatifi' ile küresel altyapıya yatırım yapan Çin, bugün yapay zekadan yeşil enerjiye kadar birçok teknolojide ABD'nin en büyük rakibidir. 21. yüzyılın 'Asya Yüzyılı' olması yönündeki vizyonuyla, askeri ve ekonomik gücünü Pasifik ötesine taşımaktadır.",
    "japonya": "JAPONYA: 1868 Meiji Restorasyonu ile samuray döneminden modern sanayi toplumuna jet hızıyla geçen Japonya, Doğu Asya'nın ilk emperyal gücü olmuştur. II. Dünya Savaşı'nda Hiroşima ve Nagazaki'ye atılan atom bombalarıyla teslim olan ülke, Amerikan işgali altında pasifist bir anayasa kabul etmiştir. Savaş sonrası askeri harcamaları kısıp eğitime ve yüksek teknolojiye odaklanan Japonya, 1960-1980 yılları arasında otomotiv ve tüketici elektroniğinde dünya liderliğine oturmuştur. Sony, Toyota ve Honda gibi markalarla küresel pazarın hakimi olmuştur. 1990'lardaki ekonomik balonun sönmesiyle başlayan 'Kayıp On Yıllar'a rağmen, bugün robotik teknolojiler, temiz enerji ve kültürel ihracat (Anime ve Gastronomi) alanında dünyanın en gelişmiş ve disiplinli toplumlarından biridir.",
    "italya": "İTALYA: Orta Çağ boyunca şehir devletlerine bölünmüş olan İtalya, Rönesans ile sanat, bilim ve ticaretin beşiği olmuş, ancak siyasi birliğini 1861'deki 'Risorgimento' (Yeniden Diriliş) hareketine kadar tamamlayamamıştır. Benito Mussolini liderliğindeki faşizm döneminde II. Dünya Savaşı'na giren ülke, yenilgi sonrası monarşiyi terk ederek cumhuriyet olmuştur. 1950'lerden itibaren yaşanan ekonomik büyüme ile 'İtalyan Mucizesi'ne imza atan ülke, tasarımın ve lüksün (Ferrari, Gucci, Prada) dünyadaki bir numaralı adresi olmuştur. Kuzeydeki sanayi bölgeleri ile güneydeki tarım alanları arasındaki ekonomik farklara ve siyasi koalisyon istikrarsızlıklarına rağmen İtalya, G7 üyesi olarak Akdeniz havzasının kültürel miras ve turizm başkentidir.",
    "misir": "MISIR: Nil Nehri kıyısında 3000 yıl süren Firavunlar döneminden sonra sırasıyla Pers, Yunan, Roma ve İslam hakimiyetine giren Mısır, 1517'de Yavuz Sultan Selim ile Osmanlı toprağı olmuştur. 19. yüzyılda Kavalalı Mehmet Ali Paşa'nın modernleşme hamleleri ve Süveyş Kanalı'nın açılmasıyla jeopolitik önemi zirve yapmıştır. 1952'de Cemal Abdül Nasır'ın askeri darbesiyle krallık yıkılmış, Arap milliyetçiliğinin merkezi haline gelinmiştir. İsrail ile yaşanan savaşlar sonrası Enver Sedat döneminde barış masasına oturulmuş, bu durum Mısır'ın bölgesel dengeleyici rolünü pekiştirmiştir. Günümüzde 100 milyonu aşan nüfusuyla Arap dünyasının en kalabalık ülkesi olan Mısır, turizm potansiyeli ve Süveyş Kanalı'ndan gelen geliriyle ekonomik krizleri aşmaya ve tarihsel liderlik iddiasını sürdürmeye çalışmaktadır."
}

@app.route("/<country>")
def show_country(country):
    if country in data:
        name = country.upper()
        content = f'<h2>{name} TARİHİ VE ANALİZİ</h2><div id="target" class="typing-text"></div><a href="/" class="back-btn">← ANA SAYFA</a>'
        return layout(content, data[country])
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
