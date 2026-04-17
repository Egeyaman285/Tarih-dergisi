<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FIRST OF THE FOREST — PUFFTON CORP.</title>
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

  html { scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--body);
    font-size: 16px;
    line-height: 1.7;
    cursor: crosshair;
    overflow-x: hidden;
  }

  /* Grain overlay */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 999;
    opacity: 0.4;
  }

  /* Scanlines */
  body::after {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.08) 3px, rgba(0,0,0,0.08) 4px);
    pointer-events: none;
    z-index: 998;
  }

  /* ── HERO ── */
  .hero {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    padding: 4rem 2rem;
  }

  .hero-bg {
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% 40%, #0d1a0d 0%, #050507 70%);
  }

  .hero-trees {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 45%;
    opacity: 0.35;
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
    position: relative;
    z-index: 2;
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
    font-size: clamp(3.5rem, 10vw, 8rem);
    letter-spacing: 0.08em;
    line-height: 0.9;
    text-align: center;
    color: var(--text-bright);
    position: relative;
    z-index: 2;
    text-shadow: 0 0 80px rgba(192,21,26,0.3);
  }

  .hero-title span {
    color: var(--red);
    display: block;
    font-weight: 200;
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
    position: relative;
    z-index: 2;
  }

  .slogan {
    font-family: var(--head);
    font-weight: 200;
    font-size: 1.1rem;
    color: var(--red);
    letter-spacing: 0.2em;
    margin-top: 0.8rem;
    position: relative;
    z-index: 2;
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
    z-index: 2;
  }
  @keyframes scrollpulse { 0%,100%{opacity:0.3;transform:translateX(-50%) translateY(0)} 50%{opacity:0.8;transform:translateX(-50%) translateY(6px)} }

  /* ── LAYOUT ── */
  .section {
    max-width: 1200px;
    margin: 0 auto;
    padding: 6rem 2rem;
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
    font-size: clamp(2rem, 5vw, 3.5rem);
    color: var(--text-bright);
    line-height: 1;
    margin-bottom: 3rem;
    letter-spacing: 0.03em;
  }

  /* ── STORY TIMELINE ── */
  .timeline {
    position: relative;
    padding-left: 3rem;
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
    margin-bottom: 3rem;
    padding: 1.5rem 2rem;
    background: var(--panel);
    border: 1px solid var(--border);
    border-left: 2px solid var(--red-dim);
  }

  .timeline-item::before {
    content: '';
    position: absolute;
    left: -3.55rem;
    top: 1.8rem;
    width: 10px;
    height: 10px;
    background: var(--red);
    border-radius: 50%;
    box-shadow: 0 0 12px var(--red);
  }

  .timeline-num {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--red);
    letter-spacing: 3px;
    margin-bottom: 0.5rem;
  }

  .timeline-item h3 {
    font-family: var(--head);
    font-weight: 600;
    font-size: 1.3rem;
    color: var(--text-bright);
    margin-bottom: 0.7rem;
    letter-spacing: 0.05em;
  }

  .timeline-item p {
    font-size: 15px;
    color: var(--text);
    line-height: 1.8;
  }

  /* ── CARDS GRID ── */
  .cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
  }

  .card {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.3s;
  }

  .card:hover {
    border-color: var(--red-dim);
    transform: translateY(-3px);
  }

  .card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--red), transparent);
    opacity: 0;
    transition: opacity 0.3s;
  }

  .card:hover::after { opacity: 1; }

  /* ── ACCESS CARDS ── */
  .access-card {
    width: 320px;
    height: 200px;
    border-radius: 12px;
    position: relative;
    overflow: hidden;
    display: inline-block;
    box-shadow: 0 8px 40px rgba(0,0,0,0.8);
  }

  .access-cards-row {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    align-items: flex-start;
    margin-top: 2rem;
  }

  /* ── CAVE GRID ── */
  .cave-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
  }

  .cave-card {
    background: var(--panel);
    border: 1px solid var(--border);
    overflow: hidden;
    position: relative;
    transition: border-color 0.3s;
  }

  .cave-card:hover { border-color: var(--amber); }

  .cave-card.important { border-color: var(--red-dim); }
  .cave-card.important:hover { border-color: var(--red); }

  .cave-header {
    padding: 1.2rem 1.5rem 0.8rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .cave-num {
    font-family: var(--mono);
    font-size: 9px;
    color: var(--text-dim);
    letter-spacing: 3px;
    display: block;
    margin-bottom: 4px;
  }

  .cave-name {
    font-family: var(--head);
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text-bright);
    letter-spacing: 0.05em;
  }

  .cave-tag {
    font-family: var(--mono);
    font-size: 9px;
    padding: 3px 8px;
    border: 1px solid;
    letter-spacing: 2px;
    white-space: nowrap;
  }

  .cave-tag.danger { color: var(--red); border-color: var(--red-dim); }
  .cave-tag.caution { color: var(--amber); border-color: var(--amber); }
  .cave-tag.clear { color: var(--green-bright); border-color: var(--green); }

  .cave-body {
    padding: 1.2rem 1.5rem;
  }

  .cave-body p {
    font-size: 14px;
    color: var(--text);
    line-height: 1.8;
    margin-bottom: 1rem;
  }

  .cave-stats {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-top: 0.5rem;
  }

  .cave-stat {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .cave-stat-label {
    font-family: var(--mono);
    font-size: 9px;
    color: var(--text-dim);
    letter-spacing: 2px;
  }

  .cave-stat-val {
    font-family: var(--mono);
    font-size: 14px;
    color: var(--amber-bright);
  }

  /* ── FACILITY MAP ── */
  .facility-map-wrap {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 2rem;
    margin-top: 2rem;
  }

  /* ── INVENTORY LIST ── */
  .inv-list {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
    margin-top: 1.5rem;
  }

  .inv-item {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 1rem 1.5rem;
    background: var(--panel);
    border: 1px solid var(--border);
    border-left: 3px solid var(--green);
    font-family: var(--mono);
  }

  .inv-icon { width: 40px; height: 40px; flex-shrink: 0; }

  .inv-name {
    font-size: 13px;
    color: var(--green-bright);
    letter-spacing: 3px;
    text-transform: uppercase;
  }

  .inv-desc {
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 1px;
    margin-top: 2px;
  }

  /* ── CREATURE ── */
  .creature-block {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    align-items: center;
    margin-top: 2rem;
  }

  .creature-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .stat-box {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 1rem;
    text-align: center;
  }

  .stat-box-label {
    font-family: var(--mono);
    font-size: 9px;
    color: var(--text-dim);
    letter-spacing: 2px;
    margin-bottom: 6px;
    display: block;
  }

  .stat-box-val {
    font-family: var(--head);
    font-weight: 700;
    font-size: 1.6rem;
    color: var(--red);
  }

  /* ── FOOTER ── */
  footer {
    border-top: 1px solid var(--border);
    padding: 3rem 2rem;
    text-align: center;
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-dim);
    letter-spacing: 3px;
  }

  /* ── DIVIDER ── */
  .divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 0;
  }

  /* ── GLITCH ── */
  .glitch {
    position: relative;
  }
  .glitch::before, .glitch::after {
    content: attr(data-text);
    position: absolute;
    top: 0; left: 0;
    width: 100%;
  }
  .glitch::before {
    color: var(--red);
    clip-path: polygon(0 30%, 100% 30%, 100% 50%, 0 50%);
    transform: translateX(-3px);
    animation: glitch1 5s infinite;
    opacity: 0.7;
  }
  .glitch::after {
    color: #0ff;
    clip-path: polygon(0 60%, 100% 60%, 100% 80%, 0 80%);
    transform: translateX(3px);
    animation: glitch2 5s infinite;
    opacity: 0.3;
  }
  @keyframes glitch1 {
    0%,90%,100%{transform:translateX(0);opacity:0}
    91%{transform:translateX(-4px);opacity:0.7}
    93%{transform:translateX(4px);opacity:0.7}
    95%{transform:translateX(0);opacity:0}
  }
  @keyframes glitch2 {
    0%,90%,100%{transform:translateX(0);opacity:0}
    92%{transform:translateX(4px);opacity:0.3}
    94%{transform:translateX(-4px);opacity:0.3}
    96%{transform:translateX(0);opacity:0}
  }

  @media (max-width: 768px) {
    .creature-block { grid-template-columns: 1fr; }
    .access-cards-row { flex-direction: column; align-items: center; }
  }
</style>
</head>
<body>

<!-- ═══════════════════════════════════════════════════════════════ HERO -->
<section class="hero">
  <div class="hero-bg"></div>

  <!-- Background forest silhouette -->
  <svg class="hero-trees" viewBox="0 0 1440 400" preserveAspectRatio="xMidYMax meet" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="treeGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#0a1a0a"/>
        <stop offset="100%" stop-color="#050507"/>
      </linearGradient>
    </defs>
    <!-- Dense tree silhouettes -->
    <g fill="url(#treeGrad)">
      <!-- Far trees -->
      <ellipse cx="80" cy="280" rx="35" ry="110"/>
      <ellipse cx="160" cy="260" rx="28" ry="130"/>
      <ellipse cx="240" cy="270" rx="40" ry="120"/>
      <ellipse cx="340" cy="250" rx="30" ry="140"/>
      <ellipse cx="420" cy="265" rx="45" ry="125"/>
      <ellipse cx="510" cy="255" rx="35" ry="135"/>
      <ellipse cx="600" cy="245" rx="38" ry="145"/>
      <ellipse cx="690" cy="260" rx="32" ry="130"/>
      <ellipse cx="780" cy="250" rx="42" ry="140"/>
      <ellipse cx="870" cy="240" rx="35" ry="150"/>
      <ellipse cx="960" cy="255" rx="40" ry="135"/>
      <ellipse cx="1060" cy="245" rx="36" ry="145"/>
      <ellipse cx="1150" cy="258" rx="38" ry="132"/>
      <ellipse cx="1240" cy="248" rx="33" ry="142"/>
      <ellipse cx="1340" cy="262" rx="44" ry="128"/>
      <ellipse cx="1420" cy="270" rx="36" ry="120"/>
      <!-- Foreground trunks -->
      <rect x="70" y="320" width="20" height="80"/>
      <rect x="150" y="310" width="16" height="90"/>
      <rect x="228" y="315" width="22" height="85"/>
      <rect x="325" y="300" width="18" height="100"/>
      <rect x="405" y="308" width="24" height="92"/>
      <rect x="492" y="298" width="20" height="102"/>
      <rect x="580" y="290" width="22" height="110"/>
      <rect x="674" y="305" width="18" height="95"/>
      <rect x="762" y="295" width="24" height="105"/>
      <rect x="854" y="285" width="20" height="115"/>
      <rect x="944" y="300" width="22" height="100"/>
      <rect x="1044" y="292" width="20" height="108"/>
      <rect x="1136" y="303" width="22" height="97"/>
      <rect x="1226" y="293" width="18" height="107"/>
      <rect x="1322" y="307" width="24" height="93"/>
      <!-- Ground fill -->
      <rect x="0" y="370" width="1440" height="30"/>
    </g>
    <!-- Mist -->
    <rect x="0" y="340" width="1440" height="60" fill="url(#mistGrad)" opacity="0.4"/>
    <defs>
      <linearGradient id="mistGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#050507" stop-opacity="0"/>
        <stop offset="100%" stop-color="#050507"/>
      </linearGradient>
    </defs>
  </svg>

  <div class="corp-badge">PUFFTON CORPORATION — CLASSIFIED ARCHIVE</div>

  <h1 class="hero-title glitch" data-text="FIRST OF THE FOREST">
    <span>FIRST OF THE</span>
    FOREST
  </h1>

  <p class="hero-sub">SUBJECT FILE — MILON — PROTOTYPE SERIES</p>
  <p class="slogan">"Live a Beautiful Life."</p>

  <div class="scroll-hint">▼ SCROLL TO ACCESS ▼</div>
</section>

<hr class="divider">

<!-- ═══════════════════════════════════════════════════════════════ STORY -->
<div class="section">
  <p class="section-label">01 — HIKAYE / STORY</p>
  <h2 class="section-title">BAŞLANGIÇ KAYDI</h2>

  <div class="timeline">

    <div class="timeline-item">
      <p class="timeline-num">// OLAY — 001</p>
      <h3>UYANIS — TESİS İÇİ KORİDOR</h3>
      <p>Milon gözlerini açar. Uzun, loş bir koridorun ortasında yatmaktadır. Her iki yönde de uzanan koridor boyunca diğer deneklerin hücreleri boştur — bir kısmı ölmüş, bir kısmı ise gizemli bir şekilde götürülmüştür. Yerde parlayan küçük bir nesne dikkatini çeker: <strong style="color:var(--green-bright)">ERİŞİM SEVİYESİ 2 kimlik kartı.</strong> Üzerinde kırmızı harflerle PUFFTON CORPORATION etiketi ve şirketin sloganı: <em>"Live a Beautiful Life."</em></p>
    </div>

    <div class="timeline-item">
      <p class="timeline-num">// OLAY — 002</p>
      <h3>CUTSCENE — JİRKOLİFST KARŞILAŞMASI</h3>
      <p>Milon koridorun sonundaki kapıyı kartıyla açar. İçeride bir kaos sahnesi onu karşılar: 16 kollu, 3 bacaklı insansı bir yaratık — <strong style="color:var(--red)">JİRKOLİFST</strong> — güvenlik personeli ile amansız bir dövüşün içindedir. Yaratık, güvenlik görevlisinin kafasını koparmak suretiyle öldürür. Ardından kanlı gözleriyle Milon'u fark eder ve üzerine koşmaya başlar.</p>
      <p style="margin-top:0.8rem">Tam o anda tiz, cızırtılı bir frekans dalgası tüm alanı kaplar. <strong style="color:var(--amber-bright)">ARIA SİSTEMİ</strong> (Puffton'ın kaçak denek imha frekansı) devreye girmiştir. Jirkolifst anında ölür. Milon, biyolojik modifikasyonu henüz tamamlanmadığı için sağ kalır — ama geçici olarak sağır olur.</p>
    </div>

    <div class="timeline-item">
      <p class="timeline-num">// OLAY — 003</p>
      <h3>EŞYA TOPLANMASI — ÖLÜ GÜVENLİK GÖREVLİSİ</h3>
      <p>Milon kendine geldiğinde artık gece olmuştur. Ölen güvenlik görevlisinin yanına gider, üstünü arar. Üç kritik eşya bulur ve envanterine alır.</p>
    </div>

    <div class="timeline-item">
      <p class="timeline-num">// OLAY — 004</p>
      <h3>KAPIDAN ÇIKIŞ — ORMAN BAŞLIYOR</h3>
      <p>Karşı duvarda bir kapı fark eder. Araştırmacı kartı (LVL 2) bu kapıyı açamaz. Güvenlik görevlisinin <strong style="color:var(--green-bright)">LVL 4 kartı</strong>yla kapı açılır. Dışarıda; ucu bucağı görünmeyen bir deniz ve güneşi bile geçirmeyen yoğun ağaç ve çalılık... Ada. Milon ilk adımını atar. <strong style="color:var(--amber-bright)">Oyun başlar.</strong></p>
    </div>

  </div>
</div>

<hr class="divider">

<!-- ═══════════════════════════════════════════════════════════════ INVENTORY -->
<div class="section">
  <p class="section-label">02 — ENVANTER</p>
  <h2 class="section-title">BULUNAN EŞYALAR</h2>

  <div class="inv-list">

    <div class="inv-item">
      <svg class="inv-icon" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="16" width="24" height="10" rx="2" fill="#1aff7a" opacity="0.8"/>
        <rect x="24" y="18" width="10" height="6" rx="1" fill="#0f8c4a"/>
        <rect x="6" y="12" width="6" height="4" rx="1" fill="#0f8c4a"/>
        <rect x="10" y="26" width="4" height="8" rx="1" fill="#0a5c32"/>
        <circle cx="14" cy="21" r="2" fill="#050507"/>
      </svg>
      <div>
        <div class="inv-name">S İ L A H — LVL 4</div>
        <div class="inv-desc">Puffton Corp. güvenlik sınıfı — ölü güvenlik görevlisinden alındı</div>
      </div>
    </div>

    <div class="inv-item" style="border-left-color: var(--amber)">
      <svg class="inv-icon" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="4" y="8" width="32" height="22" rx="3" fill="none" stroke="#ffb800" stroke-width="1.5"/>
        <rect x="4" y="8" width="32" height="7" rx="3" fill="#c87f00" opacity="0.5"/>
        <text x="20" y="23" font-family="monospace" font-size="7" fill="#ffb800" text-anchor="middle" letter-spacing="1">PUFFTON</text>
        <text x="20" y="32" font-family="monospace" font-size="5" fill="#c87f00" text-anchor="middle">LVL  4  ACCESS</text>
        <rect x="28" y="10" width="5" height="3" rx="1" fill="#ffb800"/>
      </svg>
      <div>
        <div class="inv-name" style="color:var(--amber-bright)">ERİŞİM KARTI — LVL 4</div>
        <div class="inv-desc">Güvenlik personeli sınıfı — tüm tesis kapılarını açar</div>
      </div>
    </div>

    <div class="inv-item" style="border-left-color: var(--red)">
      <svg class="inv-icon" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
        <rect x="8" y="10" width="10" height="24" rx="2" fill="#6b0b0e"/>
        <rect x="9" y="11" width="8" height="3" rx="1" fill="#c0151a"/>
        <rect x="10" y="16" width="6" height="16" rx="1" fill="#3d0608"/>
        <rect x="22" y="10" width="10" height="24" rx="2" fill="#6b0b0e"/>
        <rect x="23" y="11" width="8" height="3" rx="1" fill="#c0151a"/>
        <rect x="24" y="16" width="6" height="16" rx="1" fill="#3d0608"/>
        <text x="20" y="38" font-family="monospace" font-size="5" fill="#c0151a" text-anchor="middle">12/3</text>
      </svg>
      <div>
        <div class="inv-name" style="color:var(--red)">3 × ŞARJÖR — 12/3</div>
        <div class="inv-desc">Her şarjörde 12 mermi — 3 şarjör, toplam 36 atış kapasitesi</div>
      </div>
    </div>

  </div>
</div>

<hr class="divider">

<!-- ═══════════════════════════════════════════════════════════════ ACCESS CARDS -->
<div class="section">
  <p class="section-label">03 — ERİŞİM KARTLARI</p>
  <h2 class="section-title">PUFFTON CORP. ID SİSTEMİ</h2>

  <div class="access-cards-row">

    <!-- LVL 2 -->
    <div>
      <svg class="access-card" viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="card2bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#0d1a0d"/>
            <stop offset="100%" stop-color="#080f08"/>
          </linearGradient>
        </defs>
        <rect width="320" height="200" rx="12" fill="url(#card2bg)"/>
        <rect width="320" height="200" rx="12" fill="none" stroke="#1a4a1a" stroke-width="1.5"/>
        <!-- Chip -->
        <rect x="22" y="70" width="44" height="32" rx="4" fill="#2a3a2a" stroke="#0f8c4a" stroke-width="1"/>
        <line x1="22" y1="82" x2="66" y2="82" stroke="#0f8c4a" stroke-width="0.5" opacity="0.5"/>
        <line x1="22" y1="90" x2="66" y2="90" stroke="#0f8c4a" stroke-width="0.5" opacity="0.5"/>
        <line x1="22" y1="98" x2="66" y2="98" stroke="#0f8c4a" stroke-width="0.5" opacity="0.5"/>
        <line x1="36" y1="70" x2="36" y2="102" stroke="#0f8c4a" stroke-width="0.5" opacity="0.5"/>
        <line x1="50" y1="70" x2="50" y2="102" stroke="#0f8c4a" stroke-width="0.5" opacity="0.5"/>
        <!-- Top strip -->
        <rect x="0" y="0" width="320" height="40" rx="12" fill="#0a1a0a"/>
        <rect x="0" y="28" width="320" height="12" fill="#0a1a0a"/>
        <!-- Logo area -->
        <text x="20" y="26" font-family="Oswald,sans-serif" font-weight="700" font-size="16" fill="#1aff7a" letter-spacing="3">PUFFTON</text>
        <text x="130" y="26" font-family="Share Tech Mono,monospace" font-size="8" fill="#0f8c4a" letter-spacing="1">CORPORATION</text>
        <!-- Level badge -->
        <rect x="248" y="8" width="56" height="24" rx="4" fill="#0f8c4a" opacity="0.2" stroke="#0f8c4a" stroke-width="1"/>
        <text x="276" y="25" font-family="Oswald,sans-serif" font-weight="700" font-size="16" fill="#1aff7a" text-anchor="middle" letter-spacing="1">LVL 2</text>
        <!-- Name -->
        <text x="22" y="62" font-family="Share Tech Mono,monospace" font-size="8" fill="#0f8c4a" letter-spacing="2">SUBJECT ID</text>
        <text x="22" y="52" font-family="Oswald,sans-serif" font-weight="400" font-size="9" fill="#4a7a4a" letter-spacing="2">RESEARCHER CLASS</text>
        <text x="80" y="92" font-family="Oswald,sans-serif" font-weight="700" font-size="22" fill="#c8c4b8" letter-spacing="2">MILON</text>
        <text x="80" y="110" font-family="Share Tech Mono,monospace" font-size="9" fill="#4a7a4a" letter-spacing="1">PROTOTYPE — SERIES 7</text>
        <!-- Barcode -->
        <g opacity="0.6">
          <rect x="20" y="140" width="2" height="30" fill="#1aff7a"/>
          <rect x="24" y="140" width="1" height="30" fill="#1aff7a"/>
          <rect x="27" y="140" width="3" height="30" fill="#1aff7a"/>
          <rect x="32" y="140" width="1" height="30" fill="#1aff7a"/>
          <rect x="35" y="140" width="2" height="30" fill="#1aff7a"/>
          <rect x="39" y="140" width="4" height="30" fill="#1aff7a"/>
          <rect x="45" y="140" width="1" height="30" fill="#1aff7a"/>
          <rect x="48" y="140" width="2" height="30" fill="#1aff7a"/>
          <rect x="52" y="140" width="3" height="30" fill="#1aff7a"/>
          <rect x="57" y="140" width="1" height="30" fill="#1aff7a"/>
          <rect x="60" y="140" width="2" height="30" fill="#1aff7a"/>
          <rect x="64" y="140" width="4" height="30" fill="#1aff7a"/>
          <rect x="70" y="140" width="1" height="30" fill="#1aff7a"/>
          <rect x="73" y="140" width="2" height="30" fill="#1aff7a"/>
        </g>
        <text x="20" y="182" font-family="Share Tech Mono,monospace" font-size="7" fill="#4a7a4a" letter-spacing="1">*PT-S7-0042-LVL2*</text>
        <!-- Slogan -->
        <text x="300" y="182" font-family="Rajdhani,sans-serif" font-size="9" fill="#1a4a1a" text-anchor="end" font-style="italic">"Live a Beautiful Life."</text>
      </svg>
      <p style="font-family:var(--mono);font-size:10px;color:var(--text-dim);margin-top:0.8rem;letter-spacing:2px;text-align:center">ARAŞTIRMACI SINIFI — LVL 2</p>
    </div>

    <!-- LVL 4 -->
    <div>
      <svg class="access-card" viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="card4bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#1a0d0d"/>
            <stop offset="100%" stop-color="#0f0808"/>
          </linearGradient>
        </defs>
        <rect width="320" height="200" rx="12" fill="url(#card4bg)"/>
        <rect width="320" height="200" rx="12" fill="none" stroke="#4a1a1a" stroke-width="1.5"/>
        <!-- Top strip -->
        <rect x="0" y="0" width="320" height="40" rx="12" fill="#150a0a"/>
        <rect x="0" y="28" width="320" height="12" fill="#150a0a"/>
        <!-- Logo area -->
        <text x="20" y="26" font-family="Oswald,sans-serif" font-weight="700" font-size="16" fill="#c0151a" letter-spacing="3">PUFFTON</text>
        <text x="130" y="26" font-family="Share Tech Mono,monospace" font-size="8" fill="#6b0b0e" letter-spacing="1">CORPORATION</text>
        <!-- Level badge -->
        <rect x="248" y="8" width="56" height="24" rx="4" fill="#6b0b0e" opacity="0.4" stroke="#c0151a" stroke-width="1"/>
        <text x="276" y="25" font-family="Oswald,sans-serif" font-weight="700" font-size="16" fill="#c0151a" text-anchor="middle" letter-spacing="1">LVL 4</text>
        <!-- Chip -->
        <rect x="22" y="60" width="44" height="32" rx="4" fill="#2a1a1a" stroke="#c0151a" stroke-width="1"/>
        <line x1="22" y1="72" x2="66" y2="72" stroke="#c0151a" stroke-width="0.5" opacity="0.5"/>
        <line x1="22" y1="80" x2="66" y2="80" stroke="#c0151a" stroke-width="0.5" opacity="0.5"/>
        <line x1="22" y1="88" x2="66" y2="88" stroke="#c0151a" stroke-width="0.5" opacity="0.5"/>
        <line x1="36" y1="60" x2="36" y2="92" stroke="#c0151a" stroke-width="0.5" opacity="0.5"/>
        <line x1="50" y1="60" x2="50" y2="92" stroke="#c0151a" stroke-width="0.5" opacity="0.5"/>
        <text x="22" y="52" font-family="Rajdhani,sans-serif" font-size="9" fill="#6b0b0e" letter-spacing="2">SECURITY CLASS</text>
        <text x="80" y="82" font-family="Oswald,sans-serif" font-weight="700" font-size="20" fill="#c8c4b8" letter-spacing="2">GUARD</text>
        <text x="80" y="100" font-family="Share Tech Mono,monospace" font-size="9" fill="#6b0b0e" letter-spacing="1">UNIT-44 / DECEASED</text>
        <!-- Warning stripe -->
        <g opacity="0.15">
          <rect x="0" y="118" width="320" height="14" fill="none"/>
          <rect x="0" y="118" width="20" height="14" fill="#c0151a"/>
          <rect x="26" y="118" width="20" height="14" fill="#c0151a"/>
          <rect x="52" y="118" width="20" height="14" fill="#c0151a"/>
          <rect x="78" y="118" width="20" height="14" fill="#c0151a"/>
          <rect x="104" y="118" width="20" height="14" fill="#c0151a"/>
          <rect x="130" y="118" width="20" height="14" fill="#c0151a"/>
          <rect x="156" y="118" width="20" height="14" fill="#c0151a"/>
          <rect x="182" y="118" width="20" height="14" fill="#c0151a"/>
          <rect x="208" y="118" width="20" height="14" fill="#c0151a"/>
          <rect x="234" y="118" width="20" height="14" fill="#c0151a"/>
          <rect x="260" y="118" width="20" height="14" fill="#c0151a"/>
          <rect x="286" y="118" width="34" height="14" fill="#c0151a"/>
        </g>
        <!-- Barcode -->
        <g opacity="0.6">
          <rect x="20" y="140" width="2" height="30" fill="#c0151a"/>
          <rect x="24" y="140" width="1" height="30" fill="#c0151a"/>
          <rect x="27" y="140" width="3" height="30" fill="#c0151a"/>
          <rect x="32" y="140" width="1" height="30" fill="#c0151a"/>
          <rect x="35" y="140" width="2" height="30" fill="#c0151a"/>
          <rect x="39" y="140" width="4" height="30" fill="#c0151a"/>
          <rect x="45" y="140" width="1" height="30" fill="#c0151a"/>
          <rect x="48" y="140" width="2" height="30" fill="#c0151a"/>
          <rect x="52" y="140" width="3" height="30" fill="#c0151a"/>
          <rect x="57" y="140" width="1" height="30" fill="#c0151a"/>
          <rect x="60" y="140" width="2" height="30" fill="#c0151a"/>
          <rect x="64" y="140" width="4" height="30" fill="#c0151a"/>
          <rect x="70" y="140" width="1" height="30" fill="#c0151a"/>
          <rect x="73" y="140" width="2" height="30" fill="#c0151a"/>
        </g>
        <text x="20" y="182" font-family="Share Tech Mono,monospace" font-size="7" fill="#6b0b0e" letter-spacing="1">*PT-SEC-UNIT44-LVL4*</text>
        <text x="300" y="182" font-family="Rajdhani,sans-serif" font-size="9" fill="#2a0a0a" text-anchor="end" font-style="italic">"Live a Beautiful Life."</text>
      </svg>
      <p style="font-family:var(--mono);font-size:10px;color:var(--text-dim);margin-top:0.8rem;letter-spacing:2px;text-align:center">GÜVENLİK SINIFI — LVL 4</p>
    </div>

    <!-- ARIA Destruction Card -->
    <div>
      <svg class="access-card" viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="cardAria" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#100d1a"/>
            <stop offset="100%" stop-color="#08080f"/>
          </linearGradient>
        </defs>
        <rect width="320" height="200" rx="12" fill="url(#cardAria)"/>
        <rect width="320" height="200" rx="12" fill="none" stroke="#2a1a4a" stroke-width="1.5"/>
        <!-- Top strip -->
        <rect x="0" y="0" width="320" height="40" rx="12" fill="#100d18"/>
        <rect x="0" y="28" width="320" height="12" fill="#100d18"/>
        <text x="20" y="26" font-family="Oswald,sans-serif" font-weight="700" font-size="16" fill="#8a4aff" letter-spacing="3">PUFFTON</text>
        <text x="130" y="26" font-family="Share Tech Mono,monospace" font-size="8" fill="#4a2a8a" letter-spacing="1">CORPORATION</text>
        <!-- Level badge -->
        <rect x="232" y="8" width="76" height="24" rx="4" fill="#2a1a4a" opacity="0.6" stroke="#8a4aff" stroke-width="1"/>
        <text x="270" y="25" font-family="Oswald,sans-serif" font-weight="700" font-size="13" fill="#8a4aff" text-anchor="middle" letter-spacing="1">IMHA KARTI</text>
        <!-- Warning icon -->
        <polygon points="44,55 24,90 64,90" fill="none" stroke="#8a4aff" stroke-width="2"/>
        <text x="44" y="83" font-family="Oswald,sans-serif" font-weight="700" font-size="18" fill="#8a4aff" text-anchor="middle">!</text>
        <text x="80" y="70" font-family="Oswald,sans-serif" font-weight="700" font-size="16" fill="#c8c4b8" letter-spacing="2">BOMBA ERİŞİM</text>
        <text x="80" y="88" font-family="Share Tech Mono,monospace" font-size="9" fill="#4a2a8a" letter-spacing="1">ADA İMHA PROTOKOLܛ</text>
        <text x="22" y="116" font-family="Share Tech Mono,monospace" font-size="8" fill="#4a2a8a" letter-spacing="1">HEDEF: ADA — TÜM TESİSLER</text>
        <text x="22" y="130" font-family="Share Tech Mono,monospace" font-size="8" fill="#c0151a" letter-spacing="1">⚠  GERİ DÖNÜŞ YOK  ⚠</text>
        <!-- Barcode purple -->
        <g opacity="0.6">
          <rect x="20" y="148" width="2" height="24" fill="#8a4aff"/>
          <rect x="24" y="148" width="1" height="24" fill="#8a4aff"/>
          <rect x="27" y="148" width="3" height="24" fill="#8a4aff"/>
          <rect x="32" y="148" width="1" height="24" fill="#8a4aff"/>
          <rect x="35" y="148" width="2" height="24" fill="#8a4aff"/>
          <rect x="39" y="148" width="4" height="24" fill="#8a4aff"/>
          <rect x="45" y="148" width="1" height="24" fill="#8a4aff"/>
          <rect x="48" y="148" width="3" height="24" fill="#8a4aff"/>
          <rect x="53" y="148" width="2" height="24" fill="#8a4aff"/>
          <rect x="57" y="148" width="1" height="24" fill="#8a4aff"/>
          <rect x="60" y="148" width="4" height="24" fill="#8a4aff"/>
          <rect x="66" y="148" width="1" height="24" fill="#8a4aff"/>
          <rect x="69" y="148" width="2" height="24" fill="#8a4aff"/>
        </g>
        <text x="20" y="186" font-family="Share Tech Mono,monospace" font-size="7" fill="#4a2a8a" letter-spacing="1">*PT-DESTRUCT-OMEGA-AUTH*</text>
        <text x="300" y="186" font-family="Rajdhani,sans-serif" font-size="9" fill="#1a0d2a" text-anchor="end" font-style="italic">"Live a Beautiful Life."</text>
      </svg>
      <p style="font-family:var(--mono);font-size:10px;color:var(--text-dim);margin-top:0.8rem;letter-spacing:2px;text-align:center">OMEGA SINIFI — ADA İMHA</p>
    </div>

  </div>
</div>

<hr class="divider">

<!-- ═══════════════════════════════════════════════════════════════ CREATURE -->
<div class="section">
  <p class="section-label">04 — YARATIKLAR</p>
  <h2 class="section-title">JİRKOLİFST</h2>

  <div class="creature-block">
    <div>
      <!-- Jirkolifst SVG illustration -->
      <svg viewBox="0 0 400 500" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:380px;display:block">
        <defs>
          <radialGradient id="jirkGlow" cx="50%" cy="50%">
            <stop offset="0%" stop-color="#c0151a" stop-opacity="0.15"/>
            <stop offset="100%" stop-color="#050507" stop-opacity="0"/>
          </radialGradient>
        </defs>
        <rect width="400" height="500" fill="url(#jirkGlow)"/>
        <!-- Body -->
        <ellipse cx="200" cy="240" rx="60" ry="85" fill="#1a0808" stroke="#4a1010" stroke-width="1.5"/>
        <!-- Head -->
        <ellipse cx="200" cy="130" rx="48" ry="55" fill="#1a0a0a" stroke="#6b1010" stroke-width="1.5"/>
        <!-- Eyes - 4 of them -->
        <circle cx="182" cy="120" r="8" fill="#c0151a"/>
        <circle cx="218" cy="120" r="8" fill="#c0151a"/>
        <circle cx="188" cy="140" r="5" fill="#ff4040"/>
        <circle cx="212" cy="140" r="5" fill="#ff4040"/>
        <circle cx="182" cy="120" r="3" fill="#050507"/>
        <circle cx="218" cy="120" r="3" fill="#050507"/>
        <!-- Mouth slit -->
        <path d="M175 158 Q200 170 225 158" fill="none" stroke="#6b0b0e" stroke-width="2"/>
        <path d="M183 158 Q200 165 217 158" fill="#2a0505"/>
        <!-- 3 legs -->
        <line x1="170" y1="310" x2="130" y2="430" stroke="#2a0a0a" stroke-width="14" stroke-linecap="round"/>
        <line x1="200" y1="320" x2="200" y2="450" stroke="#2a0a0a" stroke-width="14" stroke-linecap="round"/>
        <line x1="230" y1="310" x2="270" y2="430" stroke="#2a0a0a" stroke-width="14" stroke-linecap="round"/>
        <!-- Leg joints -->
        <circle cx="148" cy="380" r="7" fill="#3a1010" stroke="#6b1010" stroke-width="1"/>
        <circle cx="200" cy="388" r="7" fill="#3a1010" stroke="#6b1010" stroke-width="1"/>
        <circle cx="252" cy="380" r="7" fill="#3a1010" stroke="#6b1010" stroke-width="1"/>
        <!-- Feet -->
        <ellipse cx="128" cy="434" rx="16" ry="8" fill="#1a0505"/>
        <ellipse cx="200" cy="454" rx="16" ry="8" fill="#1a0505"/>
        <ellipse cx="272" cy="434" rx="16" ry="8" fill="#1a0505"/>
        <!-- 16 arms — 8 per side, radiating -->
        <!-- Left side arms -->
        <line x1="150" y1="200" x2="60" y2="150" stroke="#2a0a0a" stroke-width="6" stroke-linecap="round"/>
        <line x1="148" y1="215" x2="50" y2="190" stroke="#2a0a0a" stroke-width="6" stroke-linecap="round"/>
        <line x1="148" y1="230" x2="45" y2="230" stroke="#2a0a0a" stroke-width="5" stroke-linecap="round"/>
        <line x1="150" y1="245" x2="50" y2="270" stroke="#2a0a0a" stroke-width="5" stroke-linecap="round"/>
        <line x1="152" y1="258" x2="60" y2="300" stroke="#2a0a0a" stroke-width="5" stroke-linecap="round"/>
        <line x1="155" y1="270" x2="75" y2="320" stroke="#2a0a0a" stroke-width="4" stroke-linecap="round"/>
        <line x1="158" y1="280" x2="90" y2="340" stroke="#2a0a0a" stroke-width="4" stroke-linecap="round"/>
        <line x1="162" y1="288" x2="110" y2="355" stroke="#2a0a0a" stroke-width="3" stroke-linecap="round"/>
        <!-- Right side arms -->
        <line x1="250" y1="200" x2="340" y2="150" stroke="#2a0a0a" stroke-width="6" stroke-linecap="round"/>
        <line x1="252" y1="215" x2="350" y2="190" stroke="#2a0a0a" stroke-width="6" stroke-linecap="round"/>
        <line x1="252" y1="230" x2="355" y2="230" stroke="#2a0a0a" stroke-width="5" stroke-linecap="round"/>
        <line x1="250" y1="245" x2="350" y2="270" stroke="#2a0a0a" stroke-width="5" stroke-linecap="round"/>
        <line x1="248" y1="258" x2="340" y2="300" stroke="#2a0a0a" stroke-width="5" stroke-linecap="round"/>
        <line x1="245" y1="270" x2="325" y2="320" stroke="#2a0a0a" stroke-width="4" stroke-linecap="round"/>
        <line x1="242" y1="280" x2="310" y2="340" stroke="#2a0a0a" stroke-width="4" stroke-linecap="round"/>
        <line x1="238" y1="288" x2="290" y2="355" stroke="#2a0a0a" stroke-width="3" stroke-linecap="round"/>
        <!-- Arm tips / claws -->
        <circle cx="58" cy="149" r="5" fill="#6b0b0e"/>
        <circle cx="48" cy="189" r="5" fill="#6b0b0e"/>
        <circle cx="43" cy="230" r="4" fill="#6b0b0e"/>
        <circle cx="48" cy="270" r="4" fill="#6b0b0e"/>
        <circle cx="58" cy="300" r="4" fill="#6b0b0e"/>
        <circle cx="342" cy="149" r="5" fill="#6b0b0e"/>
        <circle cx="352" cy="189" r="5" fill="#6b0b0e"/>
        <circle cx="357" cy="230" r="4" fill="#6b0b0e"/>
        <circle cx="352" cy="270" r="4" fill="#6b0b0e"/>
        <circle cx="342" cy="300" r="4" fill="#6b0b0e"/>
        <!-- Label -->
        <text x="200" y="490" font-family="Share Tech Mono,monospace" font-size="11" fill="#6b0b0e" text-anchor="middle" letter-spacing="3">JİRKOLİFST — SPECIES UNKNOWN</text>
      </svg>
    </div>

    <div>
      <p style="font-size:15px;color:var(--text);line-height:1.9;margin-bottom:1.5rem">
        Puffton Corporation'ın tesislerinde gözlemlenen birincil tehdit türüdür. İnsana benzer iskelet yapısı taşır ancak vücudunun her yanından uzanan <strong style="color:var(--red)">16 kolu</strong> ve dengesini sağlayan <strong style="color:var(--red)">3 bacağı</strong> ile tamamen bilinmeyene ait bir türdür. Köken belgelerinde "başarısız biyolojik denek" olarak geçmektedir.
      </p>
      <p style="font-size:15px;color:var(--text);line-height:1.9;margin-bottom:2rem">
        ARIA frekans sistemine karşı son derece hassastır. Puffton bu zayıflığı deneylerin kontrolü için aktif olarak kullanmaktaydı.
      </p>

      <div class="creature-stats">
        <div class="stat-box">
          <span class="stat-box-label">KOLLAR</span>
          <div class="stat-box-val">16</div>
        </div>
        <div class="stat-box">
          <span class="stat-box-label">BACAKLAR</span>
          <div class="stat-box-val">3</div>
        </div>
        <div class="stat-box">
          <span class="stat-box-label">ARIA ZAFIYETI</span>
          <div class="stat-box-val" style="color:var(--green-bright)">+</div>
        </div>
        <div class="stat-box">
          <span class="stat-box-label">TEHLİKE SEVİYESİ</span>
          <div class="stat-box-val">KRİTİK</div>
        </div>
      </div>
    </div>
  </div>
</div>

<hr class="divider">

<!-- ═══════════════════════════════════════════════════════════════ CAVES -->
<div class="section">
  <p class="section-label">05 — MAĞRALAR / CAVES</p>
  <h2 class="section-title">ADA YERALTISI HARİTASI</h2>

  <div class="cave-grid">

    <!-- Cave 1 - Ritol -->
    <div class="cave-card important">
      <div class="cave-header">
        <div>
          <span class="cave-num">CAVE — 01</span>
          <div class="cave-name">RITOL IN THE CAVE</div>
        </div>
        <span class="cave-tag danger">KRİTİK</span>
      </div>
      <div class="cave-body">
        <!-- Cave SVG illustration -->
        <svg viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg" style="width:100%;margin-bottom:1rem;border:1px solid #1a0a0a">
          <rect width="300" height="120" fill="#080508"/>
          <!-- Cave walls -->
          <path d="M0,80 Q30,40 60,70 Q90,30 120,60 Q150,20 180,55 Q210,35 240,65 Q270,45 300,70 L300,120 L0,120 Z" fill="#150a15"/>
          <path d="M0,90 Q40,60 80,85 Q120,55 160,80 Q200,60 240,82 Q270,65 300,80 L300,120 L0,120 Z" fill="#0a0508"/>
          <!-- Stalactites -->
          <polygon points="40,0 30,35 50,35" fill="#120812"/>
          <polygon points="100,0 90,28 110,28" fill="#120812"/>
          <polygon points="160,0 148,40 172,40" fill="#120812"/>
          <polygon points="220,0 210,25 230,25" fill="#120812"/>
          <polygon points="275,0 265,32 285,32" fill="#120812"/>
          <!-- TV glow -->
          <rect x="120" y="55" width="50" height="35" rx="3" fill="#0a0f1a" stroke="#1a2a4a" stroke-width="1"/>
          <rect x="122" y="57" width="46" height="28" rx="2" fill="#0d1525" opacity="0.8"/>
          <!-- Puffton ad on TV -->
          <text x="145" y="68" font-family="monospace" font-size="6" fill="#4a6aaa" text-anchor="middle">PUFFTON</text>
          <text x="145" y="76" font-family="monospace" font-size="4" fill="#2a3a6a" text-anchor="middle">Live a Beautiful Life</text>
          <rect x="140" y="85" width="10" height="8" rx="1" fill="#0a0f1a" stroke="#1a2a4a" stroke-width="0.5"/>
          <!-- Jirkolifst silhouettes -->
          <g fill="#2a0505" opacity="0.7">
            <ellipse cx="30" cy="100" rx="8" ry="12"/>
            <line x1="22" y1="94" x2="10" y2="88" stroke="#2a0505" stroke-width="1.5"/>
            <line x1="22" y1="97" x2="8" y2="95" stroke="#2a0505" stroke-width="1.5"/>
            <line x1="38" y1="94" x2="50" y2="88" stroke="#2a0505" stroke-width="1.5"/>
            <line x1="38" y1="97" x2="52" y2="95" stroke="#2a0505" stroke-width="1.5"/>
            <line x1="30" y1="112" x2="24" y2="120" stroke="#2a0505" stroke-width="2"/>
            <line x1="30" y1="112" x2="36" y2="120" stroke="#2a0505" stroke-width="2"/>
          </g>
          <g fill="#2a0505" opacity="0.7">
            <ellipse cx="270" cy="98" rx="8" ry="12"/>
            <line x1="262" y1="92" x2="250" y2="86" stroke="#2a0505" stroke-width="1.5"/>
            <line x1="262" y1="95" x2="248" y2="93" stroke="#2a0505" stroke-width="1.5"/>
            <line x1="278" y1="92" x2="290" y2="86" stroke="#2a0505" stroke-width="1.5"/>
            <line x1="278" y1="95" x2="292" y2="93" stroke="#2a0505" stroke-width="1.5"/>
            <line x1="270" y1="110" x2="264" y2="120" stroke="#2a0505" stroke-width="2"/>
            <line x1="270" y1="110" x2="276" y2="120" stroke="#2a0505" stroke-width="2"/>
          </g>
          <!-- Bomb/key icon -->
          <circle cx="220" cy="95" r="8" fill="none" stroke="#8a4aff" stroke-width="1.5"/>
          <circle cx="220" cy="95" r="3" fill="#8a4aff"/>
          <line x1="220" y1="87" x2="220" y2="83" stroke="#8a4aff" stroke-width="1.5"/>
          <line x1="218" y1="82" x2="222" y2="82" stroke="#8a4aff" stroke-width="1"/>
        </svg>

        <p>Adanın en uzun mağrasıdır. İçeride aktif <strong style="color:var(--red)">12 Jirkolifst</strong> barınmaktadır. Derinlerde eski bir güvenlik odasında çalışan bir televizyon bulunur — ekranda sürekli Puffton Corporation reklamı döner.</p>
        <p>Mağaranın sonunda bulunan kasada <strong style="color:#8a4aff">ADA İMHA BOMBA ERİŞİM KARTI</strong> saklıdır. Kart alındığında haritaya otomatik olarak <em>İmha Mağarası'nın</em> konumu yüklenir.</p>
        <p style="color:var(--text-dim);font-size:13px;font-family:var(--mono);margin-top:0.5rem">// KAMERA KAYDI: Kurucu Lion'un öldürülmesi buradan izleniyor.</p>
        <div class="cave-stats">
          <div class="cave-stat"><span class="cave-stat-label">JİRKOLİFST</span><span class="cave-stat-val">12</span></div>
          <div class="cave-stat"><span class="cave-stat-label">UZUNLUK</span><span class="cave-stat-val">UZUN</span></div>
          <div class="cave-stat"><span class="cave-stat-label">ÖDÜL</span><span class="cave-stat-val">BOMBA KARTI</span></div>
        </div>
      </div>
    </div>

    <!-- Cave 2 - Energy Explosion -->
    <div class="cave-card important">
      <div class="cave-header">
        <div>
          <span class="cave-num">CAVE — 02</span>
          <div class="cave-name">ENERGY EXPLOSION CAVE</div>
        </div>
        <span class="cave-tag danger">NÜKLEER</span>
      </div>
      <div class="cave-body">
        <svg viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg" style="width:100%;margin-bottom:1rem;border:1px solid #1a0a0a">
          <rect width="300" height="120" fill="#080808"/>
          <path d="M0,80 Q50,50 100,75 Q150,40 200,70 Q250,50 300,75 L300,120 L0,120 Z" fill="#0f0a05"/>
          <!-- Reactor ruins -->
          <rect x="110" y="30" width="80" height="70" rx="5" fill="#150f05" stroke="#3a2505" stroke-width="1"/>
          <!-- Cracked reactor -->
          <ellipse cx="150" cy="65" rx="30" ry="30" fill="#0a0805" stroke="#5a3505" stroke-width="2"/>
          <ellipse cx="150" cy="65" rx="20" ry="20" fill="#150f05" stroke="#7a4505" stroke-width="1.5"/>
          <!-- Cracks -->
          <path d="M150,45 L145,58 L155,58 Z" fill="#c87f00" opacity="0.3"/>
          <path d="M135,65 L145,62 L142,70 Z" fill="#c87f00" opacity="0.3"/>
          <path d="M155,70 L163,65 L160,75 Z" fill="#c87f00" opacity="0.2"/>
          <!-- Radiation symbol -->
          <circle cx="150" cy="65" r="6" fill="none" stroke="#c87f00" stroke-width="1" opacity="0.5"/>
          <line x1="150" y1="55" x2="150" y2="50" stroke="#c87f00" stroke-width="1" opacity="0.5"/>
          <line x1="158" y1="70" x2="163" y2="74" stroke="#c87f00" stroke-width="1" opacity="0.5"/>
          <line x1="142" y1="70" x2="137" y2="74" stroke="#c87f00" stroke-width="1" opacity="0.5"/>
          <!-- Explosion debris -->
          <circle cx="60" cy="70" r="12" fill="#1a0f05" stroke="#3a2505" stroke-width="1"/>
          <circle cx="250" cy="75" r="10" fill="#1a0f05" stroke="#3a2505" stroke-width="1"/>
          <rect x="40" y="85" width="25" height="8" rx="2" fill="#150f05" stroke="#2a1a05" stroke-width="0.5" transform="rotate(-15,52,89)"/>
          <rect x="230" y="88" width="30" height="6" rx="2" fill="#150f05" stroke="#2a1a05" stroke-width="0.5" transform="rotate(10,245,91)"/>
          <!-- Glow -->
          <circle cx="150" cy="65" r="35" fill="#c87f00" opacity="0.03"/>
          <text x="150" y="112" font-family="monospace" font-size="6" fill="#3a2505" text-anchor="middle">REAKTÖR — TERK EDİLDİ</text>
        </svg>

        <p>Tüm ada tesislerinin enerjisini karşılamak amacıyla inşa edilmiştir. Bir kaza sonucu <strong style="color:var(--amber-bright)">nükleer reaktörün çekirdeği, soğutma tankerleri ve türbinleri</strong> eş zamanlı patlama yaşadı.</p>
        <p>Patlama adada <strong style="color:var(--red)">6.7 büyüklüğünde deprem</strong>e yol açtı. Bu depremde 4 prototip denek tesislerden kaçtı. 8 tesisin 3'ü terk edildi — tesis sayısı 5'e düştü.</p>
        <p style="color:var(--amber);font-size:13px;font-family:var(--mono);border-left:2px solid var(--amber);padding-left:0.8rem;margin-top:0.5rem">// 3. TESİS (bizim tesisimiz) bu kaçışta 2 prototip kaybetti. Milon bunlardan biridir.</p>
        <div class="cave-stats">
          <div class="cave-stat"><span class="cave-stat-label">DEPREM</span><span class="cave-stat-val">M 6.7</span></div>
          <div class="cave-stat"><span class="cave-stat-label">KAÇAN DENEK</span><span class="cave-stat-val">4</span></div>
          <div class="cave-stat"><span class="cave-stat-label">TERK TESİS</span><span class="cave-stat-val">3</span></div>
        </div>
      </div>
    </div>

    <!-- Cave 3 -->
    <div class="cave-card">
      <div class="cave-header">
        <div>
          <span class="cave-num">CAVE — 03</span>
          <div class="cave-name">SHADOW PASSAGE</div>
        </div>
        <span class="cave-tag caution">DİKKAT</span>
      </div>
      <div class="cave-body">
        <svg viewBox="0 0 300 100" xmlns="http://www.w3.org/2000/svg" style="width:100%;margin-bottom:1rem;border:1px solid #111">
          <rect width="300" height="100" fill="#060608"/>
          <path d="M0,70 Q60,40 120,65 Q180,35 240,62 Q270,50 300,68 L300,100 L0,100 Z" fill="#0a0a10"/>
          <line x1="0" y1="50" x2="300" y2="50" stroke="#1a1a2a" stroke-width="0.5" stroke-dasharray="8,12"/>
          <circle cx="90" cy="72" r="15" fill="#080a12" stroke="#1a1a2a" stroke-width="1"/>
          <circle cx="200" cy="68" r="12" fill="#080a12" stroke="#1a1a2a" stroke-width="1"/>
          <text x="150" y="90" font-family="monospace" font-size="6" fill="#1a1a2a" text-anchor="middle">KARMAŞIK TÜNEL SİSTEMİ</text>
        </svg>
        <p>Ada'nın en karmaşık tünel sistemine sahip mağrasıdır. Çok sayıda çatallanma ve kör nokta içerir. İçeride kaybolmak kolaydır.</p>
        <div class="cave-stats">
          <div class="cave-stat"><span class="cave-stat-label">DALLANMA</span><span class="cave-stat-val">ÇOK</span></div>
          <div class="cave-stat"><span class="cave-stat-label">JİRKOLİFST</span><span class="cave-stat-val">4</span></div>
        </div>
      </div>
    </div>

    <!-- Cave 4 -->
    <div class="cave-card">
      <div class="cave-header">
        <div>
          <span class="cave-num">CAVE — 04</span>
          <div class="cave-name">THE FLOODED CHAMBER</div>
        </div>
        <span class="cave-tag caution">DİKKAT</span>
      </div>
      <div class="cave-body">
        <svg viewBox="0 0 300 100" xmlns="http://www.w3.org/2000/svg" style="width:100%;margin-bottom:1rem;border:1px solid #111">
          <rect width="300" height="100" fill="#060810"/>
          <path d="M0,65 Q80,45 160,60 Q240,40 300,58 L300,100 L0,100 Z" fill="#08101a"/>
          <!-- Water -->
          <path d="M0,80 Q75,72 150,78 Q225,70 300,76 L300,100 L0,100 Z" fill="#0a1828" opacity="0.8"/>
          <path d="M0,85 Q60,80 120,83 Q200,78 300,82 L300,100 L0,100 Z" fill="#0a1a30" opacity="0.6"/>
          <text x="150" y="94" font-family="monospace" font-size="7" fill="#0a3050" text-anchor="middle">~~~ SU SEVİYESİ ~~~</text>
        </svg>
        <p>Depremden sonra yer altı suları bu mağraya dolmuştur. Kısmen geçilebilir ama alt katlar tamamen su altındadır.</p>
        <div class="cave-stats">
          <div class="cave-stat"><span class="cave-stat-label">SU DURUMU</span><span class="cave-stat-val">KISMI</span></div>
          <div class="cave-stat"><span class="cave-stat-label">JİRKOLİFST</span><span class="cave-stat-val">2</span></div>
        </div>
      </div>
    </div>

    <!-- Cave 5 -->
    <div class="cave-card">
      <div class="cave-header">
        <div>
          <span class="cave-num">CAVE — 05</span>
          <div class="cave-name">ARCHIVE CAVE</div>
        </div>
        <span class="cave-tag clear">GÜVENLİ</span>
      </div>
      <div class="cave-body">
        <svg viewBox="0 0 300 100" xmlns="http://www.w3.org/2000/svg" style="width:100%;margin-bottom:1rem;border:1px solid #111">
          <rect width="300" height="100" fill="#060808"/>
          <path d="M0,70 Q80,55 160,68 Q240,52 300,66 L300,100 L0,100 Z" fill="#0a0f0a"/>
          <!-- File boxes -->
          <rect x="60" y="55" width="22" height="28" rx="2" fill="#0a1208" stroke="#0f8c4a" stroke-width="0.5"/>
          <rect x="86" y="55" width="22" height="28" rx="2" fill="#0a1208" stroke="#0f8c4a" stroke-width="0.5"/>
          <rect x="112" y="55" width="22" height="28" rx="2" fill="#0a1208" stroke="#0f8c4a" stroke-width="0.5"/>
          <line x1="60" y1="62" x2="82" y2="62" stroke="#0f8c4a" stroke-width="0.5" opacity="0.5"/>
          <line x1="86" y1="62" x2="108" y2="62" stroke="#0f8c4a" stroke-width="0.5" opacity="0.5"/>
          <line x1="112" y1="62" x2="134" y2="62" stroke="#0f8c4a" stroke-width="0.5" opacity="0.5"/>
          <text x="150" y="90" font-family="monospace" font-size="6" fill="#0f4a2a" text-anchor="middle">PUFFTON ARŞİV ODASI</text>
        </svg>
        <p>Puffton Corporation'ın eski deney kayıtlarının bir kısmı bu mağarada korunmaktadır. Jirkolifst yoktur — Milon burada şirketin geçmişini öğrenebilir.</p>
        <div class="cave-stats">
          <div class="cave-stat"><span class="cave-stat-label">JİRKOLİFST</span><span class="cave-stat-val" style="color:var(--green-bright)">0</span></div>
          <div class="cave-stat"><span class="cave-stat-label">LOR KARTI</span><span class="cave-stat-val">8</span></div>
        </div>
      </div>
    </div>

    <!-- Cave 6 -->
    <div class="cave-card">
      <div class="cave-header">
        <div>
          <span class="cave-num">CAVE — 06</span>
          <div class="cave-name">COLD STORAGE CAVE</div>
        </div>
        <span class="cave-tag caution">DİKKAT</span>
      </div>
      <div class="cave-body">
        <svg viewBox="0 0 300 100" xmlns="http://www.w3.org/2000/svg" style="width:100%;margin-bottom:1rem;border:1px solid #111">
          <rect width="300" height="100" fill="#060810"/>
          <path d="M0,72 Q80,50 160,67 Q240,48 300,65 L300,100 L0,100 Z" fill="#0a0d18"/>
          <!-- Ice/freeze effects -->
          <line x1="80" y1="40" x2="80" y2="70" stroke="#1a3a5a" stroke-width="0.5" stroke-dasharray="3,5"/>
          <line x1="150" y1="35" x2="150" y2="68" stroke="#1a3a5a" stroke-width="0.5" stroke-dasharray="3,5"/>
          <line x1="220" y1="42" x2="220" y2="65" stroke="#1a3a5a" stroke-width="0.5" stroke-dasharray="3,5"/>
          <!-- Frozen subjects -->
          <rect x="68" y="60" width="14" height="22" rx="2" fill="#0a1a2a" stroke="#1a3a5a" stroke-width="1" opacity="0.8"/>
          <rect x="144" y="58" width="14" height="24" rx="2" fill="#0a1a2a" stroke="#1a3a5a" stroke-width="1" opacity="0.8"/>
          <text x="150" y="92" font-family="monospace" font-size="6" fill="#1a2a4a" text-anchor="middle">DONMUŞ DENEK MUHAFAZA</text>
        </svg>
        <p>Puffton'ın başarısız denek serilerini dondurarak sakladığı tesis. İçeride kriyojenik kapsüller bulunur. Bazı kapsüller patlamıştır.</p>
        <div class="cave-stats">
          <div class="cave-stat"><span class="cave-stat-label">JİRKOLİFST</span><span class="cave-stat-val">6</span></div>
          <div class="cave-stat"><span class="cave-stat-label">KAPSÜL</span><span class="cave-stat-val">KIRIK</span></div>
        </div>
      </div>
    </div>

    <!-- Cave 7 -->
    <div class="cave-card">
      <div class="cave-header">
        <div>
          <span class="cave-num">CAVE — 07</span>
          <div class="cave-name">ARIA CONTROL NODE</div>
        </div>
        <span class="cave-tag danger">TEHLİKELİ</span>
      </div>
      <div class="cave-body">
        <svg viewBox="0 0 300 100" xmlns="http://www.w3.org/2000/svg" style="width:100%;margin-bottom:1rem;border:1px solid #111">
          <rect width="300" height="100" fill="#080608"/>
          <path d="M0,72 Q80,52 160,69 Q240,50 300,66 L300,100 L0,100 Z" fill="#0f0810"/>
          <!-- Signal waves -->
          <circle cx="150" cy="60" r="15" fill="none" stroke="#4a2a6a" stroke-width="1" opacity="0.6"/>
          <circle cx="150" cy="60" r="25" fill="none" stroke="#4a2a6a" stroke-width="0.5" opacity="0.4"/>
          <circle cx="150" cy="60" r="35" fill="none" stroke="#4a2a6a" stroke-width="0.5" opacity="0.2"/>
          <!-- Antenna -->
          <rect x="147" y="35" width="6" height="25" rx="1" fill="#3a1a5a"/>
          <line x1="150" y1="35" x2="140" y2="25" stroke="#4a2a6a" stroke-width="1"/>
          <line x1="150" y1="35" x2="160" y2="25" stroke="#4a2a6a" stroke-width="1"/>
          <text x="150" y="92" font-family="monospace" font-size="6" fill="#3a1a5a" text-anchor="middle">ARIA — FREKANS İSTASYONU</text>
        </svg>
        <p>ARIA sisteminin ada genelindeki kontrol düğümü burada bulunmaktadır. Bu mağara ele geçirilirse Jirkolifst'ler üzerindeki frekans imha sistemi devre dışı bırakılabilir — ama bu onları daha da tehlikeli yapar.</p>
        <div class="cave-stats">
          <div class="cave-stat"><span class="cave-stat-label">JİRKOLİFST</span><span class="cave-stat-val">8</span></div>
          <div class="cave-stat"><span class="cave-stat-label">ARIA NODE</span><span class="cave-stat-val">AKTİF</span></div>
        </div>
      </div>
    </div>

    <!-- Cave 8 - Destruction -->
    <div class="cave-card important">
      <div class="cave-header">
        <div>
          <span class="cave-num">CAVE — 08</span>
          <div class="cave-name">DESTRUCTION CAVE — OMEGA</div>
        </div>
        <span class="cave-tag danger">OMEGA</span>
      </div>
      <div class="cave-body">
        <svg viewBox="0 0 300 100" xmlns="http://www.w3.org/2000/svg" style="width:100%;margin-bottom:1rem;border:1px solid #1a0a1a">
          <rect width="300" height="100" fill="#080608"/>
          <path d="M0,72 Q80,52 160,69 Q240,50 300,66 L300,100 L0,100 Z" fill="#100810"/>
          <!-- Big bomb device -->
          <circle cx="150" cy="62" r="20" fill="#0d0810" stroke="#6b0b6b" stroke-width="1.5"/>
          <circle cx="150" cy="62" r="12" fill="#150a15" stroke="#8a0b8a" stroke-width="1"/>
          <circle cx="150" cy="62" r="5" fill="#4a054a"/>
          <!-- Wires -->
          <path d="M150,42 Q160,35 170,40" fill="none" stroke="#c0151a" stroke-width="1.5"/>
          <path d="M150,42 Q140,35 130,40" fill="none" stroke="#0f8c4a" stroke-width="1.5"/>
          <circle cx="170" cy="40" r="3" fill="#c0151a"/>
          <circle cx="130" cy="40" r="3" fill="#0f8c4a"/>
          <!-- Countdown display -->
          <rect x="118" y="78" width="64" height="14" rx="2" fill="#0a0508" stroke="#6b0b6b" stroke-width="0.5"/>
          <text x="150" y="89" font-family="Share Tech Mono,monospace" font-size="8" fill="#8a0b8a" text-anchor="middle" letter-spacing="2">00:00:00</text>
        </svg>
        <p>Konumu yalnızca Ritol Mağarası'ndaki bomba erişim kartı alındıktan sonra haritaya yüklenir. Ada'nın imha mekanizması bu mağrada bulunur. Aktive edilirse <strong style="color:var(--red)">geri dönüş yoktur.</strong></p>
        <p style="color:var(--text-dim);font-family:var(--mono);font-size:12px;margin-top:0.5rem">// Konum: KART ALINMADAN ÖNCE GİZLİ</p>
        <div class="cave-stats">
          <div class="cave-stat"><span class="cave-stat-label">ERİŞİM</span><span class="cave-stat-val">OMEGA KARTI</span></div>
          <div class="cave-stat"><span class="cave-stat-label">GERİ DÖNÜŞ</span><span class="cave-stat-val" style="color:var(--red)">YOK</span></div>
        </div>
      </div>
    </div>

  </div>
</div>

<hr class="divider">

<!-- ═══════════════════════════════════════════════════════════════ FACILITIES -->
<div class="section">
  <p class="section-label">06 — TESİSLER</p>
  <h2 class="section-title">ADA TESİS DURUMU</h2>

  <div class="facility-map-wrap">
    <svg viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg" style="width:100%">
      <!-- Ada outline -->
      <ellipse cx="450" cy="200" rx="420" ry="180" fill="none" stroke="#1a2a1a" stroke-width="1" stroke-dasharray="6,10"/>
      <ellipse cx="450" cy="200" rx="400" ry="160" fill="#080f08" opacity="0.4"/>

      <!-- Sea texture -->
      <text x="80" y="100" font-family="monospace" font-size="8" fill="#0a1a2a" letter-spacing="4">~ ~ ~ ~</text>
      <text x="740" y="300" font-family="monospace" font-size="8" fill="#0a1a2a" letter-spacing="4">~ ~ ~ ~</text>
      <text x="50" y="320" font-family="monospace" font-size="8" fill="#0a1a2a" letter-spacing="4">~ ~</text>
      <text x="820" y="150" font-family="monospace" font-size="8" fill="#0a1a2a" letter-spacing="4">~ ~</text>

      <!-- TERK EDİLEN tesisler (3) -->
      <!-- Abandoned Facility A -->
      <rect x="120" y="120" width="80" height="55" rx="3" fill="#0f0a08" stroke="#2a1a10" stroke-width="1"/>
      <line x1="120" y1="135" x2="200" y2="135" stroke="#2a1a10" stroke-width="0.5"/>
      <text x="160" y="131" font-family="monospace" font-size="7" fill="#3a2510" text-anchor="middle">TESİS 1</text>
      <text x="160" y="150" font-family="monospace" font-size="6" fill="#3a2510" text-anchor="middle">TERK EDİLDİ</text>
      <text x="160" y="162" font-family="monospace" font-size="6" fill="#2a1505" text-anchor="middle">POST-NÜKLEER</text>
      <!-- X mark -->
      <line x1="130" y1="140" x2="190" y2="168" stroke="#3a1505" stroke-width="1.5" opacity="0.4"/>
      <line x1="190" y1="140" x2="130" y2="168" stroke="#3a1505" stroke-width="1.5" opacity="0.4"/>

      <!-- Abandoned Facility B -->
      <rect x="380" y="60" width="80" height="55" rx="3" fill="#0f0a08" stroke="#2a1a10" stroke-width="1"/>
      <line x1="380" y1="75" x2="460" y2="75" stroke="#2a1a10" stroke-width="0.5"/>
      <text x="420" y="71" font-family="monospace" font-size="7" fill="#3a2510" text-anchor="middle">TESİS 2</text>
      <text x="420" y="90" font-family="monospace" font-size="6" fill="#3a2510" text-anchor="middle">TERK EDİLDİ</text>
      <text x="420" y="102" font-family="monospace" font-size="6" fill="#2a1505" text-anchor="middle">POST-NÜKLEER</text>
      <line x1="390" y1="80" x2="450" y2="108" stroke="#3a1505" stroke-width="1.5" opacity="0.4"/>
      <line x1="450" y1="80" x2="390" y2="108" stroke="#3a1505" stroke-width="1.5" opacity="0.4"/>

      <!-- Abandoned Facility C = TESİS 3 (BİZİM) -->
      <rect x="620" y="140" width="90" height="65" rx="3" fill="#0f0d10" stroke="#2a1a3a" stroke-width="1.5"/>
      <line x1="620" y1="157" x2="710" y2="157" stroke="#2a1a3a" stroke-width="0.5"/>
      <text x="665" y="153" font-family="monospace" font-size="7" fill="#4a2a6a" text-anchor="middle">TESİS 3 ★</text>
      <text x="665" y="170" font-family="monospace" font-size="6" fill="#3a1a5a" text-anchor="middle">TERK EDİLDİ</text>
      <text x="665" y="182" font-family="monospace" font-size="6" fill="#4a2aaa" text-anchor="middle">MILON'UN TESİSİ</text>
      <text x="665" y="196" font-family="monospace" font-size="5" fill="#2a1a4a" text-anchor="middle">2 PROTOTIP KAÇTI</text>
      <line x1="630" y1="162" x2="700" y2="195" stroke="#3a1050" stroke-width="1.5" opacity="0.4"/>
      <line x1="700" y1="162" x2="630" y2="195" stroke="#3a1050" stroke-width="1.5" opacity="0.4"/>

      <!-- ACTIVE facilities (5) -->
      <!-- Facility 4 -->
      <rect x="180" y="250" width="80" height="55" rx="3" fill="#080f08" stroke="#0f4a1a" stroke-width="1.5"/>
      <line x1="180" y1="265" x2="260" y2="265" stroke="#0f4a1a" stroke-width="0.5"/>
      <rect x="184" y="259" width="72" height="6" rx="1" fill="#0a1a0a"/>
      <text x="220" y="263" font-family="monospace" font-size="6" fill="#0f8c4a" text-anchor="middle" letter-spacing="1">AKTIF</text>
      <text x="220" y="277" font-family="monospace" font-size="7" fill="#1aff7a" text-anchor="middle">TESİS 4</text>
      <text x="220" y="290" font-family="monospace" font-size="6" fill="#0f6a3a" text-anchor="middle">ARAŞTIRMA</text>
      <circle cx="196" cy="298" r="3" fill="#0f8c4a" opacity="0.7"/>
      <circle cx="220" cy="298" r="3" fill="#0f8c4a" opacity="0.7"/>
      <circle cx="244" cy="298" r="3" fill="#0f8c4a" opacity="0.7"/>

      <!-- Facility 5 -->
      <rect x="330" y="270" width="80" height="55" rx="3" fill="#080f08" stroke="#0f4a1a" stroke-width="1.5"/>
      <line x1="330" y1="285" x2="410" y2="285" stroke="#0f4a1a" stroke-width="0.5"/>
      <rect x="334" y="279" width="72" height="6" rx="1" fill="#0a1a0a"/>
      <text x="370" y="283" font-family="monospace" font-size="6" fill="#0f8c4a" text-anchor="middle" letter-spacing="1">AKTIF</text>
      <text x="370" y="297" font-family="monospace" font-size="7" fill="#1aff7a" text-anchor="middle">TESİS 5</text>
      <text x="370" y="310" font-family="monospace" font-size="6" fill="#0f6a3a" text-anchor="middle">GÜVENLİK MERKEZİ</text>
      <circle cx="346" cy="318" r="3" fill="#0f8c4a" opacity="0.7"/>
      <circle cx="370" cy="318" r="3" fill="#0f8c4a" opacity="0.7"/>
      <circle cx="394" cy="318" r="3" fill="#0f8c4a" opacity="0.7"/>

      <!-- Facility 6 -->
      <rect x="480" y="260" width="80" height="55" rx="3" fill="#080f08" stroke="#0f4a1a" stroke-width="1.5"/>
      <line x1="480" y1="275" x2="560" y2="275" stroke="#0f4a1a" stroke-width="0.5"/>
      <rect x="484" y="269" width="72" height="6" rx="1" fill="#0a1a0a"/>
      <text x="520" y="273" font-family="monospace" font-size="6" fill="#0f8c4a" text-anchor="middle" letter-spacing="1">AKTIF</text>
      <text x="520" y="287" font-family="monospace" font-size="7" fill="#1aff7a" text-anchor="middle">TESİS 6</text>
      <text x="520" y="300" font-family="monospace" font-size="6" fill="#0f6a3a" text-anchor="middle">BİYO-LAB</text>
      <circle cx="496" cy="308" r="3" fill="#0f8c4a" opacity="0.7"/>
      <circle cx="520" cy="308" r="3" fill="#0f8c4a" opacity="0.7"/>
      <circle cx="544" cy="308" r="3" fill="#0f8c4a" opacity="0.7"/>

      <!-- Facility 7 -->
      <rect x="240" y="150" width="80" height="55" rx="3" fill="#080f08" stroke="#0f4a1a" stroke-width="1.5"/>
      <line x1="240" y1="165" x2="320" y2="165" stroke="#0f4a1a" stroke-width="0.5"/>
      <rect x="244" y="159" width="72" height="6" rx="1" fill="#0a1a0a"/>
      <text x="280" y="163" font-family="monospace" font-size="6" fill="#0f8c4a" text-anchor="middle" letter-spacing="1">AKTIF</text>
      <text x="280" y="177" font-family="monospace" font-size="7" fill="#1aff7a" text-anchor="middle">TESİS 7</text>
      <text x="280" y="190" font-family="monospace" font-size="6" fill="#0f6a3a" text-anchor="middle">DENEK ÜRETIM</text>
      <circle cx="256" cy="198" r="3" fill="#0f8c4a" opacity="0.7"/>
      <circle cx="280" cy="198" r="3" fill="#0f8c4a" opacity="0.7"/>
      <circle cx="304" cy="198" r="3" fill="#0f8c4a" opacity="0.7"/>

      <!-- Facility 8 (HQ) -->
      <rect x="480" y="145" width="100" height="65" rx="3" fill="#0f0808" stroke="#6b0b0e" stroke-width="1.5"/>
      <line x1="480" y1="162" x2="580" y2="162" stroke="#4a0a0a" stroke-width="0.5"/>
      <rect x="484" y="156" width="92" height="6" rx="1" fill="#150808"/>
      <text x="530" y="160" font-family="monospace" font-size="6" fill="#c0151a" text-anchor="middle" letter-spacing="1">AKTIF — MERKEZ</text>
      <text x="530" y="175" font-family="monospace" font-size="7" fill="#ff4040" text-anchor="middle">TESİS 8  ⬛</text>
      <text x="530" y="188" font-family="monospace" font-size="6" fill="#6b0b0e" text-anchor="middle">PUFFTON HQ</text>
      <text x="530" y="200" font-family="monospace" font-size="5" fill="#4a0808" text-anchor="middle">KURUCU LION [†]</text>

      <!-- Legend -->
      <rect x="20" y="345" width="10" height="10" fill="#080f08" stroke="#0f4a1a" stroke-width="1.5"/>
      <text x="36" y="354" font-family="monospace" font-size="8" fill="#0f6a3a">AKTİF TESİS (5)</text>
      <rect x="160" y="345" width="10" height="10" fill="#0f0a08" stroke="#2a1a10" stroke-width="1"/>
      <text x="176" y="354" font-family="monospace" font-size="8" fill="#3a2510">TERK EDİLDİ (3)</text>
      <rect x="310" y="345" width="10" height="10" fill="#0f0d10" stroke="#2a1a3a" stroke-width="1.5"/>
      <text x="326" y="354" font-family="monospace" font-size="8" fill="#4a2a6a">MILON'UN TESİSİ</text>
    </svg>
  </div>

  <div class="cards-grid" style="margin-top:2rem">
    <div class="card">
      <p style="font-family:var(--mono);font-size:10px;color:var(--red);letter-spacing:3px;margin-bottom:0.5rem">TOPLAM TESİS</p>
      <p style="font-family:var(--head);font-size:3rem;font-weight:700;color:var(--text-bright);line-height:1">8</p>
      <p style="font-size:13px;color:var(--text-dim)">Ada'daki başlangıç tesis sayısı</p>
    </div>
    <div class="card">
      <p style="font-family:var(--mono);font-size:10px;color:var(--amber);letter-spacing:3px;margin-bottom:0.5rem">TERK EDİLEN</p>
      <p style="font-family:var(--head);font-size:3rem;font-weight:700;color:var(--amber-bright);line-height:1">3</p>
      <p style="font-size:13px;color:var(--text-dim)">Nükleer patlama sonrası terk edildi</p>
    </div>
    <div class="card">
      <p style="font-family:var(--mono);font-size:10px;color:var(--green-bright);letter-spacing:3px;margin-bottom:0.5rem">AKTIF TESİS</p>
      <p style="font-family:var(--head);font-size:3rem;font-weight:700;color:var(--green-bright);line-height:1">5</p>
      <p style="font-size:13px;color:var(--text-dim)">Hâlâ aktif Puffton operasyonları</p>
    </div>
    <div class="card">
      <p style="font-family:var(--mono);font-size:10px;color:var(--red);letter-spacing:3px;margin-bottom:0.5rem">KAÇAN DENEK</p>
      <p style="font-family:var(--head);font-size:3rem;font-weight:700;color:var(--red);line-height:1">4</p>
      <p style="font-size:13px;color:var(--text-dim)">Depremde 4 prototip denek kaçtı</p>
    </div>
  </div>
</div>

<hr class="divider">

<!-- ═══════════════════════════════════════════════════════════════ LORE -->
<div class="section">
  <p class="section-label">07 — GEÇMİŞ / LORE</p>
  <h2 class="section-title">KURUCU LION & D-01</h2>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:start">
    <div>
      <div class="timeline">
        <div class="timeline-item">
          <p class="timeline-num">// KAYIT — ALPHA</p>
          <h3>PUFFTON'IN KURULUŞU</h3>
          <p>Kurucu Lion, "mükemmel insan" projesiyle Puffton Corporation'ı kurdu. Ada, dış dünyadan izole bir deney alanı olarak seçildi. Slogan: <em>"Live a Beautiful Life"</em> — ironik bir perde.</p>
        </div>
        <div class="timeline-item">
          <p class="timeline-num">// KAYIT — BETA</p>
          <h3>D-01 — İLK DENEK</h3>
          <p>Lion'ın yarattığı ilk denek D-01, gelişimi tamamlandığında beklenmedik bir bilinç kazandı. Puffton'ın yaptıklarını anladı. Kamera kayıtlarına göre tüm araştırmacılarla birlikte Lion'ı öldürdü.</p>
        </div>
        <div class="timeline-item">
          <p class="timeline-num">// KAYIT — GAMMA</p>
          <h3>NÜKLEER KAZA & KAÇIŞ</h3>
          <p>Enerji Patlama Mağarası'ndaki reaktör kazası 6.7'lik depreme yol açtı. Bu kaosta 4 prototip denek (Milon dahil) tesislerden kaçtı. Ada artık kontrolden çıkmıştı.</p>
        </div>
      </div>
    </div>

    <div>
      <!-- D-01 vs Lion scene -->
      <svg viewBox="0 0 380 380" xmlns="http://www.w3.org/2000/svg" style="width:100%;background:#080608;border:1px solid #1a0a1a">
        <!-- Camera frame -->
        <rect x="0" y="0" width="380" height="380" fill="#080608"/>
        <rect x="10" y="10" width="360" height="360" fill="none" stroke="#1a0a1a" stroke-width="1" stroke-dasharray="5,8"/>
        <!-- Camera HUD -->
        <rect x="10" y="10" width="100" height="16" rx="2" fill="#0f080f"/>
        <text x="16" y="22" font-family="monospace" font-size="8" fill="#c0151a">● REC</text>
        <text x="60" y="22" font-family="monospace" font-size="7" fill="#4a0a4a">CAM-07</text>
        <text x="280" y="22" font-family="monospace" font-size="7" fill="#4a0a4a">03:47:22</text>

        <!-- Room background -->
        <rect x="10" y="26" width="360" height="344" fill="#0a080a"/>
        <rect x="10" y="26" width="360" height="2" fill="#150a15"/>

        <!-- Floor perspective lines -->
        <line x1="10" y1="280" x2="370" y2="280" stroke="#150a15" stroke-width="0.5"/>
        <line x1="190" y1="280" x2="10" y2="370" stroke="#130810" stroke-width="0.3"/>
        <line x1="190" y1="280" x2="370" y2="370" stroke="#130810" stroke-width="0.3"/>

        <!-- Lion (standing figure, being attacked) -->
        <!-- Body -->
        <rect x="220" y="160" width="28" height="60" rx="4" fill="#1a1015" stroke="#2a1a20" stroke-width="1"/>
        <!-- Head -->
        <circle cx="234" cy="148" r="18" fill="#1a1015" stroke="#2a1a20" stroke-width="1"/>
        <!-- Lab coat detail -->
        <line x1="234" y1="160" x2="234" y2="220" stroke="#2a1a2a" stroke-width="1"/>
        <rect x="224" y="165" width="8" height="12" rx="1" fill="#150a15"/>
        <!-- Arms falling -->
        <line x1="220" y1="175" x2="190" y2="195" stroke="#1a1015" stroke-width="8" stroke-linecap="round"/>
        <line x1="248" y1="175" x2="275" y2="190" stroke="#1a1015" stroke-width="8" stroke-linecap="round"/>
        <!-- Legs -->
        <line x1="224" y1="220" x2="215" y2="280" stroke="#1a1015" stroke-width="9" stroke-linecap="round"/>
        <line x1="244" y1="220" x2="253" y2="280" stroke="#1a1015" stroke-width="9" stroke-linecap="round"/>
        <!-- Blood -->
        <ellipse cx="220" cy="265" rx="25" ry="8" fill="#2a0505" opacity="0.7"/>
        <path d="M190,240 Q200,255 210,248" fill="none" stroke="#3a0808" stroke-width="2"/>

        <!-- D-01 (attacker, silhouette) -->
        <!-- Body -->
        <ellipse cx="155" cy="200" rx="25" ry="40" fill="#100808" stroke="#3a1010" stroke-width="1"/>
        <!-- Head -->
        <circle cx="155" cy="155" r="22" fill="#100808" stroke="#3a1010" stroke-width="1"/>
        <!-- Multiple eyes -->
        <circle cx="144" cy="150" r="5" fill="#c0151a"/>
        <circle cx="166" cy="150" r="5" fill="#c0151a"/>
        <circle cx="150" cy="162" r="3" fill="#ff2020"/>
        <circle cx="160" cy="162" r="3" fill="#ff2020"/>
        <!-- Extended arm reaching Lion -->
        <path d="M175,190 Q200,175 218,165" fill="none" stroke="#180808" stroke-width="10" stroke-linecap="round"/>
        <circle cx="220" cy="163" r="8" fill="#2a0a0a"/>
        <!-- Other arms -->
        <line x1="138" y1="190" x2="100" y2="170" stroke="#180808" stroke-width="6" stroke-linecap="round"/>
        <line x1="136" y1="205" x2="95" y2="200" stroke="#180808" stroke-width="5" stroke-linecap="round"/>
        <line x1="138" y1="220" x2="100" y2="235" stroke="#180808" stroke-width="5" stroke-linecap="round"/>
        <!-- Legs -->
        <line x1="145" y1="240" x2="130" y2="280" stroke="#180808" stroke-width="8" stroke-linecap="round"/>
        <line x1="165" y1="240" x2="155" y2="282" stroke="#180808" stroke-width="7" stroke-linecap="round"/>
        <line x1="168" y1="238" x2="185" y2="278" stroke="#180808" stroke-width="6" stroke-linecap="round"/>

        <!-- Caption -->
        <rect x="10" y="344" width="360" height="26" fill="#0f080f" opacity="0.9"/>
        <text x="190" y="361" font-family="monospace" font-size="8" fill="#6b0b6b" text-anchor="middle" letter-spacing="2">D-01  KURUCU LION'I ÖLDÜRÜYOR — KAMERA KAYDI</text>
      </svg>
    </div>
  </div>
</div>

<hr class="divider">

<!-- ═══════════════════════════════════════════════════════════════ FOOTER -->
<footer>
  <p style="margin-bottom:0.5rem;font-size:12px;color:var(--text-dim)">PUFFTON CORPORATION — CLASSIFIED ARCHIVE SYSTEM v2.4.1</p>
  <p>"Live a Beautiful Life."</p>
  <p style="margin-top:1rem;color:var(--border)">FIRST OF THE FOREST — PRE-FOREST CHRONICLE — ALL RIGHTS RESERVED</p>
</footer>

</body>
</html>
