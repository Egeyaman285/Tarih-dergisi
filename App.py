<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FIRST OF THE FOREST | PUFFTON CORP. ARCHIVE</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;400;600;700&family=Oswald:wght@200;400;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #050507;
    --panel: #0a0a0f;
    --border: #1a1a2e;
    --red: #c0151a;
    --red-dim: #6b0b0e;
    --green: #0f8c4a;
    --green-bright: #1aff7a;
    --amber: #c87f00;
    --amber-bright: #ffb800;
    --text: #c8c4b8;
    --text-dim: #5a5850;
    --text-bright: #e8e4d8;
    --mono: 'Share Tech Mono', monospace;
    --head: 'Oswald', sans-serif;
    --body: 'Rajdhani', sans-serif;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--body);
    line-height: 1.7;
    cursor: crosshair;
  }

  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.3) 2px, rgba(0,0,0,0.3) 3px);
    pointer-events: none;
    z-index: 999;
  }

  .hero {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 4rem 2rem;
    background: radial-gradient(ellipse 80% 60% at 50% 40%, #0d1a0d 0%, #050507 70%);
  }

  .corp-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    border: 1px solid var(--red-dim);
    padding: 6px 18px;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--red);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
    animation: flicker 4s infinite;
  }

  .corp-badge::before {
    content: '';
    width: 6px;
    height: 6px;
    background: var(--red);
    border-radius: 50%;
    animation: blink 1.2s infinite;
  }

  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.1} }
  @keyframes flicker { 0%,100%{opacity:1} 92%{opacity:1} 93%{opacity:0.7} 94%{opacity:1} 97%{opacity:0.8} 98%{opacity:1} }

  .hero-title {
    font-family: var(--head);
    font-weight: 700;
    font-size: clamp(3rem, 10vw, 7rem);
    letter-spacing: 0.08em;
    line-height: 0.9;
    text-align: center;
    color: var(--text-bright);
    text-shadow: 0 0 80px rgba(192,21,26,0.3);
  }

  .hero-title span {
    color: var(--red);
    display: block;
    font-size: 0.45em;
    letter-spacing: 0.35em;
    margin-bottom: 0.5rem;
  }

  .hero-sub {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--text-dim);
    letter-spacing: 4px;
    margin-top: 2rem;
  }

  .slogan {
    font-family: var(--head);
    font-weight: 200;
    font-size: 1rem;
    color: var(--red);
    letter-spacing: 0.2em;
    margin-top: 0.8rem;
    font-style: italic;
  }

  .scroll-hint {
    position: absolute;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-dim);
    letter-spacing: 3px;
    animation: scrollpulse 2s infinite;
  }

  @keyframes scrollpulse { 0%,100%{opacity:0.3;transform:translateX(-50%) translateY(0)} 50%{opacity:0.8;transform:translateX(-50%) translateY(6px)} }

  .section {
    max-width: 1200px;
    margin: 0 auto;
    padding: 5rem 2rem;
  }

  .section-label {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--red);
    letter-spacing: 5px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--red-dim), transparent);
  }

  .section-title {
    font-family: var(--head);
    font-weight: 700;
    font-size: clamp(2rem, 5vw, 3.2rem);
    color: var(--text-bright);
    margin-bottom: 2.5rem;
    letter-spacing: 0.03em;
  }

  .timeline {
    position: relative;
    padding-left: 2.5rem;
  }

  .timeline::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 1px;
    background: linear-gradient(180deg, transparent, var(--red-dim) 10%, var(--red-dim) 90%, transparent);
  }

  .timeline-item {
    position: relative;
    margin-bottom: 2.5rem;
    padding: 1.2rem 1.8rem;
    background: var(--panel);
    border: 1px solid var(--border);
    border-left: 2px solid var(--red-dim);
  }

  .timeline-item::before {
    content: '';
    position: absolute;
    left: -3rem;
    top: 1.5rem;
    width: 8px;
    height: 8px;
    background: var(--red);
    border-radius: 50%;
    box-shadow: 0 0 12px var(--red);
  }

  .timeline-num {
    font-family: var(--mono);
    font-size: 9px;
    color: var(--red);
    letter-spacing: 3px;
    margin-bottom: 0.3rem;
  }

  .timeline-item h3 {
    font-family: var(--head);
    font-weight: 600;
    font-size: 1.2rem;
    color: var(--text-bright);
    margin-bottom: 0.5rem;
    letter-spacing: 0.05em;
  }

  .cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
  }

  .card {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 1.5rem;
    transition: border-color 0.3s, transform 0.3s;
  }

  .card:hover {
    border-color: var(--red-dim);
    transform: translateY(-3px);
  }

  .card h4 {
    font-family: var(--head);
    font-size: 1.1rem;
    color: var(--green-bright);
    margin-bottom: 0.5rem;
    letter-spacing: 2px;
  }

  .cave-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.8rem;
    margin-top: 2rem;
  }

  .cave-card {
    background: var(--panel);
    border: 1px solid var(--border);
    overflow: hidden;
    transition: border-color 0.3s;
  }

  .cave-card:hover { border-color: var(--amber); }
  .cave-card.important { border-left: 3px solid var(--red); }
  .cave-card.omega { border-left: 3px solid #8a4aff; }

  .cave-header {
    padding: 1rem 1.2rem 0.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .cave-name {
    font-family: var(--head);
    font-weight: 700;
    font-size: 1rem;
    color: var(--text-bright);
  }

  .cave-tag {
    font-family: var(--mono);
    font-size: 8px;
    padding: 2px 8px;
    border: 1px solid;
  }

  .cave-tag.danger { color: var(--red); border-color: var(--red-dim); }
  .cave-tag.caution { color: var(--amber); border-color: var(--amber); }
  .cave-tag.omega { color: #8a4aff; border-color: #8a4aff; }

  .cave-body {
    padding: 1rem 1.2rem;
  }

  .cave-body p {
    font-size: 13px;
    color: var(--text);
    line-height: 1.7;
    margin-bottom: 0.8rem;
  }

  .cave-stats {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: 0.8rem;
    padding-top: 0.5rem;
    border-top: 1px solid var(--border);
  }

  .cave-stat {
    font-family: var(--mono);
    font-size: 10px;
  }

  .cave-stat span:first-child { color: var(--text-dim); margin-right: 6px; }
  .cave-stat span:last-child { color: var(--amber-bright); }

  .inv-list {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
  }

  .inv-item {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    padding: 1rem 1.5rem;
    background: var(--panel);
    border: 1px solid var(--border);
    border-left: 3px solid var(--green);
  }

  .inv-name {
    font-family: var(--mono);
    font-size: 13px;
    color: var(--green-bright);
    letter-spacing: 2px;
  }

  .inv-desc {
    font-size: 11px;
    color: var(--text-dim);
  }

  .creature-block {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    align-items: center;
  }

  .creature-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1rem;
  }

  .stat-box {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 0.8rem;
    text-align: center;
  }

  .stat-box-label {
    font-family: var(--mono);
    font-size: 8px;
    color: var(--text-dim);
    letter-spacing: 2px;
    display: block;
  }

  .stat-box-val {
    font-family: var(--head);
    font-weight: 700;
    font-size: 1.5rem;
    color: var(--red);
  }

  footer {
    border-top: 1px solid var(--border);
    padding: 2rem;
    text-align: center;
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-dim);
    letter-spacing: 3px;
  }

  .divider {
    border: none;
    border-top: 1px solid var(--border);
  }

  @media (max-width: 768px) {
    .creature-block { grid-template-columns: 1fr; }
    .section { padding: 3rem 1.2rem; }
  }
</style>
</head>
<body>

<section class="hero">
  <div class="corp-badge">PUFFTON CORPORATION — CLASSIFIED ARCHIVE</div>
  <h1 class="hero-title">
    <span>FIRST OF THE</span>
    FOREST
  </h1>
  <p class="hero-sub">SUBJECT FILE — MILON — PROTOTYPE SERIES</p>
  <p class="slogan">"Live a Beautiful Life."</p>
  <div class="scroll-hint">▼ SCROLL TO ACCESS ▼</div>
</section>

<hr class="divider">

<!-- HIKAYE -->
<div class="section">
  <p class="section-label">01 — HIKAYE / STORY</p>
  <h2 class="section-title">BASLANGIC KAYDI</h2>
  <div class="timeline">
    <div class="timeline-item">
      <p class="timeline-num">// OLAY — 001</p>
      <h3>UYANIS — TESIS IC KORIDOR</h3>
      <p>Milon gözlerini açar. Uzun, loş bir koridorun ortasında yatmaktadır. Her iki yönde de uzanan koridor boyunca diğer deneklerin hücreleri boştur — bir kısmı ölmüş, bir kısmı gizemli bir şekilde götürülmüştür. Yerde parlayan küçük bir nesne dikkatini çeker: <strong style="color:var(--green-bright)">ERISIM SEVIYESI 2 kimlik karti.</strong> Üzerinde kırmızı harflerle PUFFTON CORPORATION etiketi ve slogan: <em>"Live a Beautiful Life."</em></p>
    </div>
    <div class="timeline-item">
      <p class="timeline-num">// OLAY — 002</p>
      <h3>CUTSCENE — JIRKOLIFST KARSILASMASI</h3>
      <p>Milon koridorun sonundaki kapiyi kartiyla açar. Içeride bir kaos sahnesi onu karsilar: <strong style="color:var(--red)">JIRKOLIFST</strong> — 16 kollu, 3 bacakli insansi bir yaratik — güvenlik personeli ile amansiz bir dövüsün içindedir. Yaratik, güvenlik görevlisinin kafasini kopararak öldürür. Ardindan kanli gözleriyle Milon'u fark eder ve üzerine kosmaya baslar. Tam o anda tiz, cizirtili bir frekans dalgasi tüm alani kaplar. <strong style="color:var(--amber-bright)">ARIA SISTEMI</strong> devreye girmistir. Jirkolifst aninda ölür. Milon, biyolojik modifikasyonu tamamlanmadigi için sag kalir — ama geçici olarak sagir olur.</p>
    </div>
    <div class="timeline-item">
      <p class="timeline-num">// OLAY — 003</p>
      <h3>ESYA TOPLANMASI — ÖLÜ GÜVENLIK GÖREVLISI</h3>
      <p>Milon kendine geldiginde artik gece olmustur. Ölen güvenlik görevlisinin yanina gider, üstünü arar. Üç kritik esya bulur:</p>
    </div>
    <div class="timeline-item">
      <p class="timeline-num">// OLAY — 004</p>
      <h3>KAPIDAN ÇIKIS — ORMAN BASLIYOR</h3>
      <p>Karsi duvarda bir kapi fark eder. Arastirmaci karti (LVL 2) bu kapiyi açamaz. Güvenlik görevlisinin <strong style="color:var(--green-bright)">LVL 4 karti</strong>yla kapi açilir. Disarida; ucu bucagi görünmeyen bir deniz ve günesi bile geçirmeyen yogun agaç ve çalilik... Ada. Milon ilk adimini atar. <strong style="color:var(--amber-bright)">Oyun baslar.</strong></p>
    </div>
  </div>
</div>

<hr class="divider">

<!-- ENVANTER -->
<div class="section">
  <p class="section-label">02 — ENVANTER</p>
  <h2 class="section-title">BULUNAN ESYALAR</h2>
  <div class="inv-list">
    <div class="inv-item">
      <div class="inv-name">🔫 SILAH — LVL 4</div>
      <div class="inv-desc">Puffton Corp. güvenlik sinifi — ölü güvenlik görevlisinden alindi</div>
    </div>
    <div class="inv-item" style="border-left-color: var(--amber)">
      <div class="inv-name" style="color:var(--amber-bright)">🪪 ERISIM KARTI — LVL 4</div>
      <div class="inv-desc">Güvenlik personeli sinifi — tüm tesis kapilarini açar</div>
    </div>
    <div class="inv-item" style="border-left-color: var(--red)">
      <div class="inv-name" style="color:var(--red)">⚡ 3 × SARJÖR — 12/3</div>
      <div class="inv-desc">Her sarjörde 12 mermi — 3 sarjör, toplam 36 atis kapasitesi</div>
    </div>
  </div>
</div>

<hr class="divider">

<!-- MAĞARALAR -->
<div class="section">
  <p class="section-label">03 — MAGARALAR / CAVES</p>
  <h2 class="section-title">ADA YERALTI HARITASI</h2>
  <div class="cave-grid">
    <div class="cave-card important">
      <div class="cave-header"><span class="cave-name">RITOL IN THE CAVE</span><span class="cave-tag danger">KRITIK</span></div>
      <div class="cave-body">
        <p>Adanin en uzun magrasidir. Içeride aktif <strong>12 Jirkolifst</strong> barinmaktadir. Derinlerde eski bir güvenlik odasinda çalisan bir televizyon bulunur — ekranda sürekli Puffton Corporation reklami döner.</p>
        <p>Magaranin sonundaki kasada <strong style="color:#8a4aff">ADA IMHA BOMBA ERISIM KARTI</strong> saklidir. Kart alindiginda haritaya otomatik olarak <em>Imha Magarasi'nin</em> konumu yüklenir.</p>
        <div class="cave-stats"><span><span>JIRKOLIFST:</span><span>12</span></span><span><span>UZUNLUK:</span><span>UZUN</span></span><span><span>ÖDÜL:</span><span>BOMBA KARTI</span></span></div>
      </div>
    </div>
    <div class="cave-card important">
      <div class="cave-header"><span class="cave-name">ENERGY EXPLOSION CAVE</span><span class="cave-tag danger">NÜKLEER</span></div>
      <div class="cave-body">
        <p>Tüm ada tesislerinin enerjisini karsilamak amaciyla insa edilmistir. Bir kaza sonucu <strong>nükleer reaktörün çekirdegi, sogutma tankerleri ve türbinleri</strong> es zamanli patlama yasadi.</p>
        <p>Patlama adada <strong>6.7 büyüklügünde deprem</strong>e yol açti. Bu depremde <strong>4 prototip denek</strong> tesislerden kaçti. 8 tesisin 3'ü terk edildi — tesis sayisi 5'e düstü.</p>
        <p style="color:var(--amber);font-size:12px;margin-top:6px;">// 3. TESIS (bizim tesisimiz) bu kaçista 2 prototip kaybetti. Milon bunlardan biridir.</p>
        <div class="cave-stats"><span><span>DEPREM:</span><span>M 6.7</span></span><span><span>KAÇAN DENEK:</span><span>4</span></span><span><span>TERK TESIS:</span><span>3</span></span></div>
      </div>
    </div>
    <div class="cave-card">
      <div class="cave-header"><span class="cave-name">SHADOW PASSAGE</span><span class="cave-tag caution">DIKKAT</span></div>
      <div class="cave-body">
        <p>Ada'nin en karmasik tünel sistemine sahip magrasidir. Çok sayida dallanma ve kör nokta içerir. Içeride kaybolmak kolaydir.</p>
        <div class="cave-stats"><span><span>DALLANMA:</span><span>ÇOK</span></span><span><span>JIRKOLIFST:</span><span>4</span></span></div>
      </div>
    </div>
    <div class="cave-card">
      <div class="cave-header"><span class="cave-name">THE FLOODED CHAMBER</span><span class="cave-tag caution">DIKKAT</span></div>
      <div class="cave-body">
        <p>Depremden sonra yer alti sulari bu magraya dolmustur. Kismen geçilebilir ama alt katlar tamamen su altindadir.</p>
        <div class="cave-stats"><span><span>SU DURUMU:</span><span>KISMI</span></span><span><span>JIRKOLIFST:</span><span>2</span></span></div>
      </div>
    </div>
    <div class="cave-card">
      <div class="cave-header"><span class="cave-name">ARCHIVE CAVE</span><span class="cave-tag" style="color:var(--green-bright);border-color:var(--green)">GÜVENLI</span></div>
      <div class="cave-body">
        <p>Puffton Corporation'in eski deney kayitlarinin bir kismi bu magarada korunmaktadir. Jirkolifst yoktur — Milon burada sirketin geçmisini ögrenebilir.</p>
        <div class="cave-stats"><span><span>JIRKOLIFST:</span><span style="color:var(--green-bright)">0</span></span><span><span>LOR KARTI:</span><span>8</span></span></div>
      </div>
    </div>
    <div class="cave-card">
      <div class="cave-header"><span class="cave-name">COLD STORAGE CAVE</span><span class="cave-tag caution">DIKKAT</span></div>
      <div class="cave-body">
        <p>Puffton'in basarisiz denek serilerini dondurarak sakladigi tesis. Içeride kriyojenik kapsüller bulunur. Bazi kapsüller patlamistir.</p>
        <div class="cave-stats"><span><span>JIRKOLIFST:</span><span>6</span></span><span><span>KAPSÜL:</span><span>KIRIK</span></span></div>
      </div>
    </div>
    <div class="cave-card">
      <div class="cave-header"><span class="cave-name">ARIA CONTROL NODE</span><span class="cave-tag danger">TEHLIKELI</span></div>
      <div class="cave-body">
        <p>ARIA sisteminin ada genelindeki kontrol dügümü burada bulunmaktadir. Bu magara ele geçirilirse Jirkolifst'ler üzerindeki frekans imha sistemi devre disi birakilabilir.</p>
        <div class="cave-stats"><span><span>JIRKOLIFST:</span><span>8</span></span><span><span>ARIA NODE:</span><span>AKTIF</span></span></div>
      </div>
    </div>
    <div class="cave-card omega">
      <div class="cave-header"><span class="cave-name">DESTRUCTION CAVE — OMEGA</span><span class="cave-tag omega">OMEGA</span></div>
      <div class="cave-body">
        <p>Konumu yalnizca Ritol Magarasi'ndaki bomba erisim karti alindiktan sonra haritaya yüklenir. Ada'nin imha mekanizmasi bu magrada bulunur. Aktive edilirse <strong style="color:var(--red)">geri dönüs yoktur.</strong></p>
        <p style="color:var(--text-dim);font-size:11px;">// Konum: KART ALINMADAN ÖNCE GIZLI</p>
        <div class="cave-stats"><span><span>ERISIM:</span><span>OMEGA KARTI</span></span><span><span>GERI DÖNÜS:</span><span style="color:var(--red)">YOK</span></span></div>
      </div>
    </div>
  </div>
</div>

<hr class="divider">

<!-- YARATIK -->
<div class="section">
  <p class="section-label">04 — YARATIKLAR</p>
  <h2 class="section-title">JIRKOLIFST</h2>
  <div class="creature-block">
    <div style="background:var(--panel);border:1px solid var(--border);padding:1.5rem;text-align:center">
      <div style="font-family:var(--mono);font-size:80px;color:var(--red);line-height:1;">🕷️</div>
      <div style="font-family:var(--mono);font-size:11px;color:var(--text-dim);margin-top:0.5rem;">JIRKOLIFST — SPECIES UNKNOWN</div>
    </div>
    <div>
      <p>Puffton Corporation'in tesislerinde gözlemlenen birincil tehdit türüdür. Insana benzer iskelet yapisi tasir ancak vücudunun her yanindan uzanan <strong style="color:var(--red)">16 kolu</strong> ve dengesini saglayan <strong style="color:var(--red)">3 bacagi</strong> ile tamamen bilinmeyene ait bir türdür. Köken belgelerinde "basarisiz biyolojik denek" olarak geçmektedir.</p>
      <p style="margin-top:1rem;">ARIA frekans sistemine karsi son derece hassastir. Puffton bu zayifligi deneylerin kontrolü için aktif olarak kullanmaktaydi.</p>
      <div class="creature-stats">
        <div class="stat-box"><span class="stat-box-label">KOLLAR</span><div class="stat-box-val">16</div></div>
        <div class="stat-box"><span class="stat-box-label">BACAKLAR</span><div class="stat-box-val">3</div></div>
        <div class="stat-box"><span class="stat-box-label">ARIA ZAFIYETI</span><div class="stat-box-val" style="color:var(--green-bright)">+</div></div>
        <div class="stat-box"><span class="stat-box-label">TEHLIKE SEVIYESI</span><div class="stat-box-val">KRITIK</div></div>
      </div>
    </div>
  </div>
</div>

<hr class="divider">

<!-- TESISLER -->
<div class="section">
  <p class="section-label">05 — TESISLER</p>
  <h2 class="section-title">ADA TESIS DURUMU</h2>
  <div class="cards-grid">
    <div class="card"><h4>TOPLAM TESIS</h4><p style="font-size:2.5rem;font-weight:700;color:var(--text-bright)">8</p><p style="font-size:12px;color:var(--text-dim)">Ada'daki baslangiç tesis sayisi</p></div>
    <div class="card"><h4 style="color:var(--amber-bright)">TERK EDILEN</h4><p style="font-size:2.5rem;font-weight:700;color:var(--amber-bright)">3</p><p style="font-size:12px;color:var(--text-dim)">Nükleer patlama sonrasi terk edildi</p></div>
    <div class="card"><h4 style="color:var(--green-bright)">AKTIF TESIS</h4><p style="font-size:2.5rem;font-weight:700;color:var(--green-bright)">5</p><p style="font-size:12px;color:var(--text-dim)">Hâlâ aktif Puffton operasyonlari</p></div>
    <div class="card"><h4 style="color:var(--red)">KAÇAN DENEK</h4><p style="font-size:2.5rem;font-weight:700;color:var(--red)">4</p><p style="font-size:12px;color:var(--text-dim)">Depremde 4 prototip denek kaçti</p></div>
  </div>
</div>

<hr class="divider">

<!-- LORE -->
<div class="section">
  <p class="section-label">06 — GECMIS / LORE</p>
  <h2 class="section-title">KURUCU LION & D-01</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;">
    <div>
      <div class="timeline">
        <div class="timeline-item">
          <p class="timeline-num">// KAYIT — ALPHA</p>
          <h3>PUFFTON'IN KURULUSU</h3>
          <p>Kurucu Lion, "mükemmel insan" projesiyle Puffton Corporation'i kurdu. Ada, dis dünyadan izole bir deney alani olarak seçildi. Slogan: <em>"Live a Beautiful Life"</em> — ironik bir perde.</p>
        </div>
        <div class="timeline-item">
          <p class="timeline-num">// KAYIT — BETA</p>
          <h3>D-01 — ILK DENEK</h3>
          <p>Lion'in yarattigi ilk denek D-01, gelisimi tamamlandiginda beklenmedik bir bilinç kazandi. Puffton'in yaptiklarini anladi. Kamera kayitlarina göre tüm arastirmacilarla birlikte Lion'i öldürdü.</p>
        </div>
        <div class="timeline-item">
          <p class="timeline-num">// KAYIT — GAMMA</p>
          <h3>NÜKLEER KAZA & KAÇIS</h3>
          <p>Enerji Patlama Magarasi'ndaki reaktör kazasi 6.7'lik depreme yol açti. Bu kaosta 4 prototip denek (Milon dahil) tesislerden kaçti. Ada artik kontrolden çikmisti.</p>
        </div>
      </div>
    </div>
    <div style="background:var(--panel);border:1px solid var(--border);padding:1.5rem;text-align:center">
      <div style="font-family:var(--mono);font-size:11px;color:var(--red);margin-bottom:1rem;">● REC CAM-07</div>
      <div style="font-family:var(--head);font-size:3rem;color:var(--red);">D-01</div>
      <div style="font-family:var(--mono);font-size:10px;color:var(--text-dim);margin:0.5rem 0;">↓</div>
      <div style="font-family:var(--head);font-size:2rem;color:var(--text-bright);">KURUCU LION</div>
      <div style="font-family:var(--mono);font-size:9px;color:var(--red);margin-top:1rem;">[TERMINATED — ALL RESEARCHERS]</div>
      <div style="border-top:1px solid var(--border);margin-top:1rem;padding-top:1rem;font-family:var(--mono);font-size:10px;color:var(--text-dim);">"Yarattigin sey seni yok eder."</div>
    </div>
  </div>
</div>

<hr class="divider">

<footer>
  <p>PUFFTON CORPORATION — CLASSIFIED ARCHIVE SYSTEM v2.4.1</p>
  <p>"Live a Beautiful Life."</p>
  <p style="margin-top:0.8rem;color:var(--border)">FIRST OF THE FOREST — PRE-FOREST CHRONICLE</p>
</footer>

</body>
</html>
