from flask import Flask
import os

app = Flask(__name__)

STYLE = """
<style>
    :root { --bg-color: #f0f2f5; --text-color: #333; --cont-bg: white; --accent: #e74c3c; }
    .dark-mode { --bg-color: #1a1a2e; --text-color: #ecf0f1; --cont-bg: #16213e; --accent: #f1c40f; }

    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg-color); margin: 0; display: flex; flex-direction: row; color: var(--text-color); min-height: 100vh; transition: 0.3s; }
    
    .ggi-logo { width: 60px; height: 60px; background: linear-gradient(45deg, #e74c3c, #c0392b); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 20px; color: white; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); border: 2px solid rgba(255,255,255,0.2); }

    .sidebar-left { width: 320px; background: #1a1a2e; color: white; height: 100vh; padding: 25px; position: fixed; left: 0; overflow-y: auto; z-index: 10; border-right: 3px solid var(--accent); }
    .main-content { margin-left: 340px; padding: 50px; flex-grow: 1; display: flex; justify-content: center; }
    .container { background: var(--cont-bg); padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 1100px; animation: fadeIn 0.8s ease; }
    
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    .settings-panel { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-top: 20px; border: 1px dashed #4b6584; }
    .admin-info { font-size: 13px; color: #bdc3c7; line-height: 1.6; margin-top: 10px; }
    .disclaimer { font-size: 11px; color: #95a5a6; margin-top: 20px; font-style: italic; border-top: 1px solid #34495e; padding-top: 10px; }

    .toggle-btn { cursor: pointer; padding: 8px 12px; border-radius: 5px; border: none; background: var(--accent); color: white; font-weight: bold; width: 100%; margin-top: 10px; transition: 0.2s; }
    .toggle-btn:hover { opacity: 0.8; transform: scale(1.02); }

    .tool-box { background: #16213e; padding: 15px; border-radius: 10px; margin-bottom: 25px; }
    #display { background: #0f3460; color: #2ecc71; padding: 15px; text-align: right; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 20px; margin-bottom: 10px; min-height: 25px; }
    .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
    .calc-grid button { padding: 12px; border: none; border-radius: 5px; background: #4b6584; color: white; font-weight: bold; cursor: pointer; }
    
    #game-container { width: 100%; height: 180px; background: #000; position: relative; overflow: hidden; border-radius: 10px; border: 2px solid var(--accent); cursor: pointer; }
    #player { width: 25px; height: 25px; background: #e74c3c; position: absolute; bottom: 5px; left: 40px; border-radius: 4px; }
    .obstacle { width: 20px; background: #f1c40f; position: absolute; bottom: 5px; border-radius: 3px; }
    
    .country-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 20px; }
    .card { padding: 18px; color: white; text-decoration: none; border-radius: 10px; text-align: center; font-size: 13px; font-weight: bold; transition: 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .card:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.3); filter: brightness(1.1); }
    
    .typing-text { line-height: 1.8; font-size: 16px; background: rgba(0,0,0,0.03); padding: 35px; border-left: 6px solid var(--accent); border-radius: 8px; white-space: pre-wrap; color: var(--text-color); text-align: justify; }
    .back-btn { display: inline-block; margin-top: 20px; padding: 12px 25px; background: #2c3e50; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; }

    @media (max-width: 1100px) {
        body { flex-direction: column; }
        .sidebar-left { position: relative; width: 100%; height: auto; border-right: none; }
        .main-content { margin-left: 0; padding: 20px; }
        .country-grid { grid-template-columns: repeat(2, 1fr); }
    }
</style>

<script>
    function toggleTheme() {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    }

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
            pos += 7; obs.style.right = pos + 'px';
            let p = document.getElementById('player').getBoundingClientRect();
            let o = obs.getBoundingClientRect();
            if (p.right > o.left && p.left < o.right && p.bottom > o.top && p.top < o.bottom) { 
                running = false; 
                location.reload(); 
            }
            if(pos > container.offsetWidth) { clearInterval(loop); obs.remove(); score++; document.getElementById('score-num').innerText = score; spawn(); }
        }, 20);
    }

    function startTyping() {
        const target = document.getElementById('target');
        const source = document.getElementById('hidden-text');
        if(!target || !source) return;
        const text = source.innerText.trim();
        target.innerHTML = ""; let i = 0;
        function run() { if (i < text.length) { target.innerHTML += text.charAt(i); i++; setTimeout(run, 1); } }
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
            <div id="msg-overlay" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); color:white;">TIKLA</div>
            <div id="player"></div>
        </div>
        <div class="settings-panel">
            <h4>⚙️ AYARLAR</h4>
            <button class="toggle-btn" onclick="toggleTheme()">Tema Değiştir</button>
            <div class="admin-info">
                <strong>👤 Admin:</strong> Ege | <strong>🎂 Yaş:</strong> 12<br>
                <strong>🚀 Altyapı:</strong> Render + Python
            </div>
            <div class="disclaimer">
                ⚠️ Bağımsız Tarih Arşivi v3.0
            </div>
        </div>
    </div>
    """
    hidden = f"<div id='hidden-data' style='display:none;'><div id='hidden-text'>{long_text}</div></div>"
    return f"{STYLE} {left} {hidden} <div class='main-content'>{content}</div>"

data = {
    "turkiye": """[TÜRKİYE: MEDENİYETLERİN DOĞUŞ VE YÜKSELİŞ MERKEZİ]

1. TARİH ÖNCESİ VE ANTROPOLOJİK MİRAS: Anadolu, insan türünün evrimsel yolculuğundaki en kritik duraktır. Karain Mağarası ve Yarımburgaz, 400.000 yıl öncesine dayanan insan izlerini barındırır. Göbeklitepe ise M.Ö. 10.000'de avcı-toplayıcı insanların yerleşik hayata geçmeden önce devasa tapınaklar inşa edebildiğini kanıtlayarak tüm dünya tarihini kökten değiştirmiştir.

2. CİHAN İMPARATORLUĞU VE STRATEJİ: Selçukluların Anadolu'yu yurt edinmesinden sonra filizlenen Osmanlı İmparatorluğu, 1453'te İstanbul'u fethederek Orta Çağ'ı kapatıp Yeni Çağ'ı açmıştır. Osmanlı; tebaasına din özgürlüğü tanıyan 'millet sistemi', devşirme usulüyle kurulan elit bürokrasi ve dünyanın en güçlü donanmalarından birini inşa ederek üç kıtada 600 yıl hüküm sürmüştür.

3. MODERN TÜRKİYE VE ATATÜRK DEVRİMLERİ: 1919'da başlayan Milli Mücadele, sömürgeciliğe karşı kazanılmış ilk büyük bağımsızlık savaşıdır. 1923'te Cumhuriyet'in ilanıyla birlikte:
- HARF DEVRİMİ: Bir gecede okuma yazma oranını artırmak için Latin alfabesine geçiş.
- KADIN HAKLARI: Fransa ve İtalya'dan bile önce kadınlara seçme ve seçilme hakkının verilmesi (1934).
- SANAYİLEŞME: Sümerbank ve Etibank gibi kurumlarla devlet eliyle sanayi hamlesinin başlatılması.
Anadolu bugün, hem antik tarih hem de laik-demokratik bir cumhuriyet olarak dünyanın en önemli jeopolitik noktasıdır.""",

    "nazi": """[NAZİ ALMANYASI: TOTALİTER REJİMİN ANATOMİSİ]

1. WEİMAR'IN ÇÖKÜŞÜ VE YÜKSELİŞ: I. Dünya Savaşı'ndan sonra Almanya, hiperenflasyon ve Versay Antlaşması'nın getirdiği utançla sarsıldı. 1933'te NSDAP'nin iktidara gelişiyle, propaganda bakanı Goebbels'in 'Büyük Yalan' tekniği kullanılarak kitleler hipnotize edildi.

2. İDEOLOJİK TERÖR: 'Lebensraum' (Yaşam Alanı) teorisiyle Doğu'ya yayılma planı yapıldı. Üretim tamamen savaş sanayisine kaydırıldı (Volkswagen - Halkın Arabası gibi projelerle maskelenerek). Toplumun her kesimi 'Gestapo' (Gizli Polis) tarafından izlenir hale geldi.

3. HOLOKOST VE SONUÇLAR: İkinci Dünya Savaşı sırasında 6 milyondan fazla Yahudi, Roman ve muhalif, endüstriyel bir yöntemle (gaz odaları) katledildi. Bu trajedi, bugün uluslararası hukukun ve insan hakları kavramının temel taşı olan 'Nürnberg Mahkemeleri'nin kurulmasına yol açmıştır.""",

    "abd": """[ABD: ÖZGÜRLÜK BİLDİRGESİNDEN KÜRESEL HEGEMONYAYA]

1. YENİ DÜNYA VE KURUCU BABALAR: 1776'da İngiliz sömürgeciliğine başkaldıran George Washington, Thomas Jefferson ve arkadaşları, Aydınlanma Çağı'nın ilkelerini (John Locke'un fikirleri gibi) bir devlet yapısına dönüştürdü. 'Her insan eşit doğar' ilkesi üzerine kurulan ilk modern cumhuriyettir.

2. İÇ SAVAŞ VE SANAYİ PATLAMASI: 1861-1865 yılları arasındaki İç Savaş, Kuzey'in (Sanayi) Güney'i (Köleci Tarım) yenmesiyle sonuçlandı ve kölelik yasaklandı. 1900'lerin başında Henry Ford'un 'T-Modeli' ile başlattığı seri üretim devrimi, tüketim toplumunun temellerini attı.

3. SAVAŞ SONRASI DÜZEN: II. Dünya Savaşı'ndan sonra 'Marshall Planı' ile Avrupa'yı yeniden inşa eden ABD, doların küresel rezerv para birimi olmasıyla ekonomik, Hollywood ve Silikon Vadisi ile de kültürel liderliğini pekiştirdi.""",

    "cin": """[ÇİN: MERKEZ İMPARATORLUKTAN TEKNOLOJİ DEVİNE]

1. KADİM BİLGELİK: M.Ö. 221'de Qin Shi Huang'ın Çin'i birleştirmesiyle başlayan imparatorluk süreci, kağıt, barut, matbaa ve pusula gibi medeniyet değiştirici icatlara ev sahipliği yaptı. Konfüçyüs öğretileri, Çin devlet disiplininin 2500 yıllık çekirdeğini oluşturur.

2. KOMÜNİST DEVRİM VE REFORM: 1949'da Mao Zedong ile başlayan süreç, 1978'de Deng Xiaoping'in 'Dışa Açılma' devrimiyle yön değiştirdi. 'Kedi ak ya da kara olsun, fare yakaladığı sürece iyidir' mantığıyla Çin, devlet kontrolünde bir kapitalizm uygulayarak yüz milyonlarca insanı fakirlikten çıkardı.

3. 21. YÜZYIL DOMİNASYONU: Bugün Çin, 'Kuşak ve Yol Girişimi' ile antik İpek Yolu'nu modern demiryolları ve limanlarla canlandırıyor. 5G teknolojisi, elektrikli araçlar (BYD) ve yapay zeka alanında ABD ile kıyasıya bir rekabet içinde.""",

    "japonya": """[JAPONYA: ONUR, DİSİPLİN VE TEKNOLOJİK RÖNESANS]

1. ŞOGUNLUK VE İZOLASYON: 1603-1868 arası 'Sakoku' politikasıyla Japonya dış dünyaya kapılarını kapattı. Bu dönemde Samuray sınıfı, Bushido (Savaşçının Yolu) etik kurallarını toplumsal DNA'ya kazıdı.

2. MEİJİ DEVRİMİ: 1868'de İmparator Meiji, Japonya'yı yok olmaktan kurtarmak için Batı'nın teknolojisini alıp Japon ruhunu koruyan radikal bir modernleşme başlattı. Sadece 30 yılda feodal bir toplumdan, Rusya'yı savaşta yenen (1905) bir endüstri gücüne dönüştüler.

3. YIKIMDAN MUCİZEYE: Hiroşima ve Nagazaki atom bombalarıyla tamamen yıkılan Japonya, II. Dünya Savaşı sonrası 'Sıfır Hata' (Kaizen) felsefesiyle otomotiv ve elektronikte (Sony, Toyota) dünya lideri oldu. Bugün dünyanın en yaşlı ama en disiplinli nüfusuna sahiptir.""",

    "rusya": """[RUSYA: AVRASYA'NIN ÇELİK İRADESİ]

1. ÇARLIK VE BÜYÜK PETRO: Bataklıklar üzerine St. Petersburg'u kuran Büyük Petro, Rusya'yı sakallarını kestirerek zorla Avrupalılaştırdı. Rusya, devasa toprakları sayesinde Napolyon ve Hitler'in ordularını 'General Kış' stratejisiyle yok etmiştir.

2. EKİM DEVRİMİ VE SOVYETLER: 1917'de Lenin önderliğinde gerçekleşen ihtilal, tarihteki en büyük ideolojik kırılmadır. Özel mülkiyet kaldırıldı ve merkezi planlı ekonomi denendi. SSCB, II. Dünya Savaşı'nda 27 milyon insanını kaybederek Nazileri durduran asıl güç oldu.

3. SOĞUK SAVAŞ VE SONRASI: Uzaya ilk insanı (Yuri Gagarin) gönderen Rusya, bugün nükleer gücü, doğal gaz kaynakları ve jeopolitik manevralarıyla dünyanın çok kutuplu yeni düzeninde kilit rol oynamaktadır.""",

    "fransa": """[FRANSA: AYDINLANMA VE SİYASİ ESTETİK]

1. MUTLAKİYET VE RÖNESANS: 14. Louis (Güneş Kral), 'Devlet benim' diyerek Versailles Sarayı'nı Avrupa siyasetinin ve modasının kalbi yaptı.

2. 1789 FRANSIZ İHTİLALİ: 'İnsan ve Yurttaş Hakları Bildirgesi' ile kralların tanrısal yetkisi yerle bir edildi. Bu devrim, feodalizmi bitirip yerine 'Vatandaşlık' kavramını getirdi. Fransız orduları, Napolyon yönetiminde bu fikirleri tüm Avrupa kıtasına ihraç etti.

3. KÜLTÜREL HEGEMONYA: Fransa bugün; Airbus ile havacılıkta, LVMH grubu ile lüks tüketimde ve Cannes/Louvre ile dünya sanatında belirleyici gücünü korumaktadır.""",

    "almanya": """[ALMANYA: SANAYİNİN VE FELSEFENİN KALBİ]

1. KUTSAL ROMA'DAN BİSMARCK'A: Yüzlerce küçük prenslikten oluşan Almanya, 1871'de Bismarck'ın 'Demir ve Kan' politikasıyla birleşti. Bu, modern Avrupa'nın en büyük sanayi gücünün doğuşuydu.

2. DÜŞÜNCE DEVRİMİ: Kant, Hegel, Nietzsche ve Marx gibi filozoflarla Almanya, modern düşüncenin laboratuvarı oldu. Klasik müzikte Beethoven ve Bach ile ruhun estetiğini zirveye taşıdı.

3. MÜHENDİSLİK ÜSTÜNLÜĞÜ: Savaş sonrası Berlin Duvarı'nın yıkılmasıyla (1990) yeniden birleşen Almanya, bugün 'Endüstri 4.0' devriminin öncüsüdür. Mercedes, Siemens ve SAP gibi devlerle dünya kalitesini belirler.""",

    "italya": """[İTALYA: ANTİK ROMA'DAN MODERTE TASARIMA]

1. ROMA İMPARATORLUĞU: M.Ö. 753'te kurulan Roma, hukuk (Roma Hukuku), mimari (Kemer ve Beton) ve askeri strateji ile bugünkü Batı medeniyetinin temel yazılımını oluşturdu.

2. RÖNESANS (YENİDEN DOĞUŞ): 14. yüzyılda İtalya'da başlayan bu hareket, insanı kainatın merkezine koydu. Da Vinci'nin anatomik çizimleri ve Galileo'nun gözlemleri bilimsel devrimin fitilini ateşledi.

3. TASARIM VE YAŞAM: Modern İtalya, 'Made in Italy' damgasıyla otomobil (Ferrari), moda (Gucci) ve mutfakta dünyanın en prestijli markasıdır.""",

    "misir": """[MISIR: EBEDİ PİRAMİTLER VE NİL STRATEJİSİ]

1. ANTİK MÜHENDİSLİK: Giza Piramitleri, M.Ö. 2500'de milimetrik hassasiyetle inşa edildi. Mısırlılar, tıpta, geometride ve hiyeroglif yazısıyla iletişimde döneminin binlerce yıl ilerisindeydi.

2. İSLAM VE OSMANLI DÖNEMİ: Kahire, El-Ezher Üniversitesi ile İslam dünyasının ilim merkezi oldu. Yavuz Sultan Selim'in fethiyle Osmanlı'nın en zengin eyaleti haline geldi.

3. MODERN DEVRİM: 1952'de Nasır'ın yaptığı devrim, Pan-Arabizm akımını doğurdu. Süveyş Kanalı, bugün dünya deniz ticaretinin %12'sinin geçtiği, Mısır'ın en büyük ekonomik ve siyasi kozudur.""",

    "ingiltere": """[İNGİLTERE: ADA DEVLETİNDEN DÜNYA DİLİNE]

1. MAGNA CARTA: 1215'te kralın yetkilerinin kısıtlanması, bugünkü parlamenter sistemlerin babasıdır.

2. SANAYİ DEVRİMİ: Buharlı makinenin icadı ve kömürün kullanımıyla İngiltere, insanlık tarihinin en büyük üretim sıçramasını başlattı. Bu güçle, dünya topraklarının %25'ine hükmeden bir imparatorluk kurdu.

3. TEKNOLOJİ VE FİNANS: Alan Turing ile modern bilgisayarın temellerini atan İngiltere, bugün Londra üzerinden dünya finans trafiğini yönetmektedir.""",

    "ispanya": """[İSPANYA: ALTIN ÇAĞ VE DEMOKRATİK GEÇİŞ]

1. KEŞİFLER VE KOLONİALİZM: 1492'de Granada'nın düşüşü ve Amerika'nın keşfiyle İspanya, dünyanın en zengin devleti oldu. İspanyolca bugün dünyada en çok konuşulan ikinci anadildir.

2. İÇ SAVAŞ VE FRANCO: 1930'lardaki iç savaş, faşizm ve demokrasi arasındaki küresel mücadelenin provasıydı.

3. MODERN RÖNESANS: 1975'te diktatörlükten krallık ve demokrasiye geçiş 'İspanyol Mucizesi' olarak bilinir. Turizm ve yenilenebilir enerjide öncüdür.""",

    "israıl": """[İSRAİL: TEKNOLOJİK GÜVENLİK VE START-UP EKOSİSTEMİ]

1. KURULUŞ VE SAVAŞLAR: 1948'de kurulan İsrail, kısıtlı kaynaklara ve sürekli çatışma ortamına rağmen hayatta kalma stratejisi geliştirdi.

2. SİBER VE SAVUNMA DEVRİMİ: Demir Kubbe (Iron Dome) ve siber güvenlik yazılımları (Check Point), ülkeyi dünyanın en gelişmiş askeri teknoloji ihracatçılarından biri yaptı.

3. TARIM MUCİZESİ: Çöl topraklarında topraksız tarım ve su arıtma teknolojileriyle dünyaya gıda teknolojisi ihraç etmektedir.""",

    "isvec": """[İSVEÇ: VİKİNG GENLERİNDEN SOSYAL REFAH DEVRİMİNE]

1. VİKİNG TİCARETİ: Vikingler sadece yağmacı değil, Bağdat'tan Kanada'ya kadar ticaret ağı kuran usta denizcilerdi.

2. İSKANDİNAV MODELİ: İsveç, yüksek vergiler ama karşılığında bedelsiz eğitim ve sağlık sunan 'Refah Devleti' modelinin dünyadaki en başarılı örneğidir.

3. DİJİTAL İHRACAT: Spotify, Minecraft ve Bluetooth gibi teknolojiler İsveç inovasyonunun meyveleridir.""",

    "guney_kore": """[GÜNEY KORE: KÜLTÜREL VE TEKNOLOJİK DOMİNASYON]

1. HAN NEHRİ MUCİZESİ: 1960'larda kişi başı geliri Afrika ülkelerinden düşük olan Güney Kore, ağır sanayi ve eğitime odaklanarak dünyanın en hızlı kalkınan ülkesi oldu.

2. ÇİP VE EKRAN DEVRİMİ: Dünyadaki yarı iletken (çip) ve OLED ekran pazarının yarısından fazlası Güney Koreli Samsung ve SK Hynix tarafından kontrol edilir.

3. YUMUŞAK GÜÇ (SOFT POWER): K-Pop (BTS) ve Oscar ödüllü sineması (Parasite) ile Güney Kore, bugün dünyadaki gençlik kültürünü belirleyen ana güçtür.""",

    "iran": """[İRAN: PERS MEDENİYETİ VE ENERJİ JEOPOLİTİĞİ]

1. ANTİK PERS: Ahameniş İmparatorluğu, dünyanın ilk büyük posta teşkilatını ve 'Krallar Yolu'nu kurdu. Pers kültürü; mimari, bahçe sanatı ve bürokrasiyle İslam medeniyetini derinden etkiledi.

2. PETROL VE DEVRİM: 1953'te Musaddık'ın petrolü millileştirme girişimi ve 1979 İslam Devrimi, Orta Doğu'daki dengeleri kalıcı olarak değiştirdi.

3. NÜKLEER VE STRATEJİK GÜÇ: İran bugün, Hürmüz Boğazı'ndaki kontrolü ve bölgedeki vekil güçleriyle küresel enerji güvenliğinde kritik bir aktördür.""",

    "hindistan": """[HİNDİSTAN: YAZILIM ORDUSU VE DEMOGRAFİK GÜÇ]

1. MATEMATİKSEL MİRAS: 'Sıfır' (0) sayısını ve bugünkü rakam sistemini dünyaya kazandıran Hindistan, kadim bir bilim merkezidir.

2. BİLGİ TEKNOLOJİLERİ DEVRİMİ: 1990'lardan sonra yazılım dış kaynak kullanımında (outsourcing) dünya merkezi oldu. Bugün Google ve Microsoft gibi devlerin CEO'ları Hindistan asıllıdır.

3. UZAY VE NÜKLEER: Hindistan, Ay'ın güney kutbuna inen ilk ülke (2023) olarak düşük maliyetli ama yüksek teknolojili uzay yarışında yeni bir devir başlattı.""",

    "brezilya": """[BREZİLYA: AMAZONLARIN JEOPOLİTİĞİ VE TARIM DEVRİMİ]

1. PORTEKİZ MİRASI: Portekiz kraliyet ailesinin Napolyon'dan kaçıp Brezilya'ya yerleşmesi, ülkeyi bir koloni olmaktan çıkarıp imparatorluk merkezine dönüştürdü.

2. TARIM VE ENERJİ: Dünyanın en büyük kahve, şeker ve soya üreticisidir. Ayrıca etanol yakıtı (şeker kamışından) üretiminde dünya lideridir.

3. HAVACILIK VE SAVUNMA: Embraer ile dünyanın en büyük üçüncü sivil uçak üreticisi konumundadır. Amazon ormanları, küresel iklim politikasının merkezindedir.""",

    "kanada": """[KANADA: KAYNAK ZENGİNLİĞİ VE DİPLOMASİ]

1. DOĞAL KAYNAKLAR: Dünyanın en büyük tatlı su rezervlerine ve petrol kumlarına sahiptir. Madencilik teknolojisinde dünya lideridir.

2. ÇOK KÜLTÜRLÜLÜK (MULTICULTURALISM): Dünyada resmi olarak çok kültürlülüğü devlet politikası yapan ilk ülkedir (1971).

3. ARKTİK STRATEJİSİ: İklim değişikliğiyle açılan Kuzey Kutbu ticaret yollarında Rusya ile birlikte en büyük hak sahibidir.""",

    "avustralya": """[AVUSTRALYA: KITA DEVLET VE MADEN DEVRİMİ]

1. JEOLOJİK ZENGİNLİK: Dünyanın en büyük demir cevheri ve lityum (batarya hammaddesi) ihracatçısıdır.

2. ANZAC VE KİMLİK: Çanakkale Savaşları, Avustralya'nın bir İngiliz kolonisinden bir millete dönüşme sürecindeki en önemli psikolojik dönüm noktasıdır.

3. AUKUS VE GÜVENLİK: ABD ve İngiltere ile yaptığı nükleer denizaltı anlaşmasıyla, Pasifik'te Çin'e karşı kurulan yeni savunma hattının merkezindedir.""",

    "yunanistan": """[YUNANİSTAN: DENİZCİLİK VE FELSEFİ TEMELLER]

1. ANTİK MİRAS: Demokrasi, tiyatro, olimpiyat oyunları ve Batı felsefesi burada doğdu. Arşimet ve Pisagor ile matematiksel dünya görüşü şekillendi.

2. KÜRESEL DENİZCİLİK: Yunanistan, dünyanın en büyük ticari gemi filosuna sahip ülkesidir. Dünya ticaretinin önemli bir kısmı Yunan armatörlerin gemilerinde taşınır.

3. TURİZM VE DİPLOMASİ: Akdeniz jeopolitiğinde AB'nin güneydoğu kalkanı görevini üstlenmektedir."""
}

@app.route("/")
def home():
    countries = [
        ("TÜRKİYE", "/turkiye", "#c0392b"), ("ABD", "/abd", "#2980b9"), ("İNGİLTERE", "/ingiltere", "#2c3e50"),
        ("ALMANYA", "/almanya", "#f39c12"), ("NAZİ DÖNEMİ", "/nazi", "#000000"), ("FRANSA", "/fransa", "#3498db"),
        ("RUSYA", "/rusya", "#16a085"), ("ÇİN", "/cin", "#d35400"), ("JAPONYA", "/japonya", "#7f8c8d"),
        ("İTALYA", "/italya", "#27ae60"), ("MISIR", "/misir", "#8e44ad"), ("İSPANYA", "/ispanya", "#e67e22"),
        ("BREZİLYA", "/brezilya", "#2ecc71"), ("HİNDİSTAN", "/hindistan", "#d35400"), ("KANADA", "/kanada", "#c0392b"),
        ("AVUSTRALYA", "/avustralya", "#2980b9"), ("İRAN", "/iran", "#27ae60"), ("G. KORE", "/guney_kore", "#3498db"),
        ("İSVEÇ", "/isvec", "#f1c40f"), ("YUNANİSTAN", "/yunanistan", "#2980b9"), ("İSRAİL", "/israıl", "#34495e")
    ]
    cards = "".join([f'<a href="{url}" class="card" style="background:{color}">{name}</a>' for name, url, color in countries])
    content = f"""<div class="container"><h1>🏛️ Genç Girişimci Tarih Ansiklopedisi</h1><p style="text-align:center; font-size:18px; color:#7f8c8d;">Sürüm 3.0 | 21 Ülke, 400.000 Yıllık Analiz</p><div class="country-grid">{cards}</div></div>"""
    return layout(content)

@app.route("/<country>")
def show_country(country):
    if country in data:
        name = country.replace("_", " ").upper()
        content = f'<div class="container"><h2>{name} ANALİZİ</h2><div id="target" class="typing-text"></div><br><a href="/" class="back-btn">← ANSİKLOPEDİYE DÖN</a></div>'
        return layout(content, data[country])
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
