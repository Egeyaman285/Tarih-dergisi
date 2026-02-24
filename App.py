rom flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SHADOW RP | SECURE TERMINAL V13</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

        :root {
            --red: #ff0000;
            --red-dim: #8b0000;
            --green: #00ff41;
            --bg: #030303;
            --blue: #00d4ff;
            --gold: #ffd700;
            --panel: #080808;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: var(--bg);
            color: #aaa;
            font-family: 'Share Tech Mono', monospace;
            overflow-x: hidden;
            min-height: 100vh;
        }
        body::before {
            content: '';
            position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.07) 2px, rgba(0,0,0,0.07) 4px);
            pointer-events: none;
            z-index: 9999;
        }

        /* BAŞLANGIÇ EKRANI */
        #startScreen {
            position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            background: #000; z-index: 5000;
            display: flex; flex-direction: column;
            justify-content: center; align-items: center; gap: 30px;
        }
        .start-logo {
            font-family: 'Orbitron', monospace;
            font-size: 3rem; font-weight: 900;
            color: var(--red); letter-spacing: 12px;
            text-shadow: 0 0 30px var(--red), 0 0 60px var(--red-dim);
            animation: flicker 4s infinite;
        }
        .start-sub { color: #444; letter-spacing: 4px; font-size: 0.8rem; text-align: center; }
        .start-btn {
            padding: 16px 55px;
            background: transparent;
            border: 2px solid var(--red);
            color: var(--red);
            font-family: 'Share Tech Mono', monospace;
            font-size: 1.1rem; cursor: pointer;
            letter-spacing: 5px; transition: all 0.3s;
        }
        .start-btn:hover { background: var(--red); color: #fff; box-shadow: 0 0 40px var(--red); }

        /* HEADER */
        #terminalHeader {
            background: rgba(0,0,0,0.97);
            border-bottom: 3px solid var(--red);
            padding: 25px 30px; text-align: center;
            position: sticky; top: 0; z-index: 1500;
            transition: all 0.5s;
        }
        #terminalHeader.collapsed {
            padding: 8px 30px;
            border-bottom: 1px solid var(--red-dim);
        }
        .header-title {
            font-family: 'Orbitron', monospace;
            color: var(--red); font-size: 1.5rem; font-weight: 700;
            letter-spacing: 8px; text-shadow: 0 0 20px var(--red);
            margin-bottom: 15px; transition: all 0.5s;
        }
        #terminalHeader.collapsed .header-title {
            font-size: 0.75rem; margin-bottom: 0; letter-spacing: 3px; opacity: 0.4;
        }
        #headerInputArea {
            transition: all 0.5s; overflow: hidden; max-height: 120px;
        }
        #terminalHeader.collapsed #headerInputArea {
            max-height: 0; opacity: 0;
        }
        .auth-input {
            background: #000;
            border: 1px solid var(--red-dim);
            border-bottom: 2px solid var(--red);
            color: var(--red); padding: 12px 20px;
            width: 80%; max-width: 550px;
            margin: 10px auto; display: block;
            outline: none; text-align: center;
            font-size: 1rem; font-family: 'Share Tech Mono', monospace;
            letter-spacing: 4px; transition: 0.3s;
        }
        .auth-input:focus { border-color: var(--red); box-shadow: 0 0 20px rgba(255,0,0,0.3); }
        #statusBar { font-size: 0.75rem; color: #333; margin-top: 8px; letter-spacing: 3px; }

        .shadow-tag {
            position: fixed; top: 18px; right: 25px;
            color: var(--red); font-family: 'Orbitron', monospace;
            font-size: 0.85rem; font-weight: 700;
            letter-spacing: 3px; text-shadow: 0 0 10px var(--red);
            z-index: 2000; opacity: 0.6;
        }

        /* ANA CONTAINER */
        .main-container { max-width: 950px; margin: 30px auto; padding: 0 20px 60px; }

        /* ERİŞİM REDDEDİLDİ */
        #accessDeniedMsg {
            display: none;
            background: #050000; border: 2px solid var(--red);
            padding: 50px; text-align: center;
            margin-bottom: 30px; animation: fadeIn 0.4s;
        }
        .denied-title {
            font-family: 'Orbitron', monospace;
            color: var(--red); font-size: 2rem; margin-bottom: 15px;
            text-shadow: 0 0 20px var(--red); animation: pulse 1.5s infinite;
        }
        .denied-sub { color: #555; letter-spacing: 2px; font-size: 0.85rem; margin-top: 8px; }

        /* DEPARTMAN KUTUSU */
        .branch-box {
            background: var(--panel); border: 1px solid #111;
            border-left: 6px solid var(--blue);
            padding: 25px; margin-bottom: 30px;
            display: none; animation: slideIn 0.4s ease;
        }
        .o5-box { border-left-color: var(--gold); }
        .branch-title {
            font-family: 'Orbitron', monospace;
            font-size: 1rem; color: #fff; letter-spacing: 4px;
            border-bottom: 1px solid #1a1a1a;
            padding-bottom: 12px; margin-bottom: 18px;
        }
        .branch-desc-line { color: var(--green); font-size: 0.88rem; line-height: 2; }

        /* SCP LİSTESİ */
        #scpSection { margin-top: 10px; display: none; }
        .section-header {
            font-family: 'Orbitron', monospace;
            font-size: 0.75rem; color: #333; letter-spacing: 5px;
            margin-bottom: 15px; border-top: 1px solid #111; padding-top: 20px;
        }
        .scp-folder {
            background: #050505; border: 1px solid #111;
            border-left: 4px solid var(--red-dim);
            padding: 14px 20px; margin-bottom: 6px;
            cursor: pointer; display: flex;
            justify-content: space-between; align-items: center;
            transition: all 0.2s;
        }
        .scp-folder:hover { background: #0a0a0a; border-left-color: var(--red); transform: translateX(6px); }
        .scp-folder.active { border-left-color: var(--red); background: #0c0000; }
        .scp-name { color: #ccc; font-size: 0.9rem; letter-spacing: 2px; }
        .scp-right { display: flex; align-items: center; gap: 12px; }
        .scp-arrow { color: #333; font-size: 0.8rem; transition: 0.2s; }
        .scp-folder.active .scp-arrow { color: var(--red); transform: rotate(90deg); }

        .badge {
            padding: 3px 10px; font-size: 0.65rem; font-weight: bold;
            font-family: 'Orbitron', monospace; letter-spacing: 1px; border-radius: 2px;
        }
        .badge-safe     { background: #1a3d1a; color: #00ff41; border: 1px solid #00ff41; }
        .badge-euclid   { background: #3d3500; color: #ffd700; border: 1px solid #ffd700; }
        .badge-keter    { background: #3d0000; color: #ff4444; border: 1px solid #ff4444; }
        .badge-thaumiel { background: #1e0033; color: #cc88ff; border: 1px solid #cc88ff; }
        .badge-apollyon { background: #000; color: var(--red); border: 1px solid var(--red); animation: pulse 1.2s infinite; }

        .scp-details {
            background: #000; border: 1px solid #1a0000;
            border-left: 4px solid var(--red); border-top: none;
            padding: 20px 25px; margin-bottom: 10px;
            display: none; animation: fadeIn 0.3s;
        }
        .scp-detail-line {
            color: var(--green); font-size: 0.82rem; line-height: 2;
            border-bottom: 1px solid #080808; padding: 2px 0;
        }
        .scp-detail-line:last-child { border-bottom: none; }

        /* ANİMASYONLAR */
        @keyframes fadeIn { from { opacity: 0; transform: translateY(-5px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
        @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }
        @keyframes flicker {
            0%,100% { opacity: 1; } 92% { opacity: 1; } 93% { opacity: 0.4; }
            94% { opacity: 1; } 96% { opacity: 0.7; } 97% { opacity: 1; }
        }

        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: #000; }
        ::-webkit-scrollbar-thumb { background: var(--red-dim); }
    </style>
</head>
<body>

<!-- BAŞLANGIÇ EKRANI -->
<div id="startScreen">
    <div class="start-logo">SHADOW</div>
    <div class="start-sub">SİTE-SHADOW GİZLİ VERİ TABANI</div>
    <div class="start-sub">ERİŞİM KISITLIDIR — YETKİSİZ GİRİŞ TESPİT EDİLECEKTİR</div>
    <button class="start-btn" onclick="initSystem()">▶ SİSTEMİ BAŞLAT</button>
</div>

<div class="shadow-tag">SHADOW RP</div>

<!-- HEADER -->
<div id="terminalHeader">
    <div class="header-title">⬡ SECURE TERMINAL V13 ⬡</div>
    <div id="headerInputArea">
        <input type="password" id="passInput" class="auth-input" placeholder="[ YETKİ ANAHTARI GİRİNİZ ]" autocomplete="off">
        <div id="statusBar">● STATUS: OFFLINE — YETKİ BEKLENİYOR</div>
    </div>
</div>

<!-- ANA İÇERİK -->
<div class="main-container">

    <!-- D-SINIFI UYARI -->
    <div id="accessDeniedMsg">
        <div class="denied-title">⚠ ERİŞİM REDDEDİLDİ ⚠</div>
        <div style="color:#ff4444; margin:15px 0; font-size:1.1rem; letter-spacing:4px;">DOSYA BULUNAMADI</div>
        <div class="denied-sub">D-SINIFI PERSONEL SİCİL NUMARASI TANIMLANDI</div>
        <div class="denied-sub">BU KİMLİK İLE ERİŞİLEBİLECEK GİZLİ DOSYA MEVCUT DEĞİLDİR</div>
        <div class="denied-sub" style="margin-top:15px; color:#2a2a2a;">GİRİŞİM KAYDEDÜLDÜ — GÜVENLİK BİLGİLENDİRİLDİ</div>
    </div>

    <!-- DEPARTMAN KUTULARI -->
    <div id="SEC-B" class="branch-box"><div class="branch-title">🔒 GÜVENLİK DEPARTMANI</div><div id="sec-text"></div></div>
    <div id="ENG-B" class="branch-box"><div class="branch-title">⚙ MÜHENDİSLİK BİRİMİ</div><div id="eng-text"></div></div>
    <div id="ETH-B" class="branch-box"><div class="branch-title">⚖ ETİK KOMİTE</div><div id="eth-text"></div></div>
    <div id="MED-B" class="branch-box"><div class="branch-title">✚ TIBBİ DEPARTMAN</div><div id="med-text"></div></div>
    <div id="IGD-B" class="branch-box"><div class="branch-title">👁 İÇ GÜVENLİK (IGD)</div><div id="igd-text"></div></div>
    <div id="TME-B" class="branch-box"><div class="branch-title">⚔ TAKTİKSEL MÜDAHALE (TME)</div><div id="tme-text"></div></div>
    <div id="O5-B" class="branch-box o5-box"><div class="branch-title">★ O5 KONSEYİ</div><div id="o5-text"></div></div>

    <!-- SCP LİSTESİ -->
    <div id="scpSection">
        <div class="section-header">▸ ANOMALİK NESNE ARŞİVİ — YETKİLİ DOSYALAR</div>
        <div id="scp-list"></div>
    </div>
</div>

<script>
// =============================================
//  VERİTABANI
// =============================================
const DATABASE = {
    // --- DEPARTMAN ŞİFRELERİ ---
    "SEC-SHADOW-2026": {
        type:"dept", boxId:"SEC-B", textId:"sec-text",
        dept:"SEC", allowed:["SAFE","EUCLID"],
        info:"GÜVENLİK PROTOKOLÜ AKTİF\\n► Yetki Seviyesi   : BETA-3\\n► Müdahale Kapsamı : Safe ve Euclid sınıfı anomaliler\\n► Keter İhlali     : TME müdahalesi çağrılır, personel bölgeden çekilir\\n► Vardiya Süresi   : 8 saatlik rotasyon, 3 peron / vardiya\\n► Silah Protokolü  : Standart ateşli silah — Thaumiel için yasak\\n► Öncelik          : Tesis güvenliği, sivil kayıp SIFIR politikası\\n► Uyarı            : İhlal anında kod KIRMIZI butonu tetiklenecek"
    },
    "ENG-TECH-SYS": {
        type:"dept", boxId:"ENG-B", textId:"eng-text",
        dept:"ENG", allowed:["SAFE","EUCLID","KETER","THAUMIEL"],
        info:"MÜHENDİSLİK SİSTEM RAPORU\\n► Yetki Seviyesi   : DELTA-4\\n► Bakım Kapsamı    : Safe, Euclid, Keter, Thaumiel sınıfları\\n► Güç Sistemi      : Jeneratör denetimi her 24 saatte bir zorunlu\\n► Containment Sys  : Thaumiel muhafaza cihazları aktif izleme altında\\n► Acil Kapatma     : EMP-7 protokolü — yetkili mühendis imzası gerekli\\n► Malzeme Yönetimi : Anomalik bileşen stoku haftalık raporlanır\\n► Uyarı            : İzinsiz sistem değişikliği otomatik alarm tetikler"
    },
    "ETHIC-BOARD-01": {
        type:"dept", boxId:"ETH-B", textId:"eth-text",
        dept:"ETH", allowed:["SAFE","EUCLID","KETER","THAUMIEL","APOLLYON"],
        info:"ETİK KOMİTE DİREKTİFİ\\n► Yetki Seviyesi   : OMEGA-5 — Tüm sınıflar üzerinde denetim\\n► Denetim Kapsamı  : Tüm deney protokolleri etik onay gerektirir\\n► İnsan Deneyleri  : D-sınıfı kullanımı kota ve limit dahilinde\\n► Amnezik Kullanımı: Yalnızca komite onayı ile uygulanabilir\\n► Komitenin Gücü   : O5 kararlarını etik ihlal gerekçesiyle durdurabilir\\n► Rapor Dönemi     : Aylık etik değerlendirme raporu zorunludur\\n► Uyarı            : İnsan onuruna aykırı deney derhal durdurulur"
    },
    "MED-DEPT-99": {
        type:"dept", boxId:"MED-B", textId:"med-text",
        dept:"MED", allowed:["SAFE","EUCLID","KETER"],
        info:"TIBBİ DEPARTMAN ANALİZİ\\n► Yetki Seviyesi   : GAMMA-3\\n► Biyolojik Tehdit : Sınıf-A biyohazmat protokolü daima hazır\\n► Personel Sağlığı : Temas sonrası 72 saat karantina zorunlu\\n► Amnezik Stok     : A-klası, B-klası ve C-klası mevcut\\n► Antidot Veri     : Anomalik maruziyete karşı 14 formül arşivde\\n► D-Sınıfı Tıbbi   : Tıbbi kayıt tutulur; ölüm protokolü ayrı dosyada\\n► Uyarı            : Bulaşıcı anomali tespitinde tesis karantinaya alınır"
    },
    "IGD-INTERNAL-00": {
        type:"dept", boxId:"IGD-B", textId:"igd-text",
        dept:"IGD", allowed:["SAFE","EUCLID","KETER","THAUMIEL","APOLLYON"],
        info:"İÇ GÜVENLİK DİREKTİFİ — GİZLİ\\n► Yetki Seviyesi   : SIGMA-5 — Tüm departmanlar üzerinde\\n► Görev            : Vakıf içi sızıntı, casusluk, ihanet tespiti\\n► İzleme           : Tüm personel iletişimi pasif izleme altında\\n► Ajan Ağı         : Her departmanda en az 1 gizli IGD ajanı bulunur\\n► Gözaltı Yetkisi  : Şüpheli personel mahkemesiz tutulabilir, 72 saat\\n► Dosya Erişimi    : IGD tüm gizli dosyalara erişim hakkına sahiptir\\n► Uyarı            : Bu dosyayı okuduğunuz kaydedildi"
    },
    "TME-TACTICAL-X": {
        type:"dept", boxId:"TME-B", textId:"tme-text",
        dept:"TME", allowed:["SAFE","EUCLID","KETER","THAUMIEL","APOLLYON"],
        info:"TAKTİKSEL MÜDAHALE PLANI — GİZLİ\\n► Yetki Seviyesi   : KAPPA-4 — Ağır silahlı operasyon birimi\\n► Müdahale Hızı    : Alarm sonrası sahaya iniş < 3 dakika\\n► Keter Protokolü  : Nötralizasyon emri O5 onayı olmadan verilemez\\n► Apollyon Durumu  : Olay yeri boşaltma — TME son savunma hattı\\n► Ekipman          : Anomalik karşı silahlar, Thaumiel destekli zırh\\n► Kayıp Politikası : Operasyon önceliklidir; kayıp ikincil kabul edilir\\n► Uyarı            : TME emirleri yazılı olmadan sözlü kabul edilmez"
    },
    "O5-secsysttem": {
        type:"dept", boxId:"O5-B", textId:"o5-text",
        dept:"O5", allowed:["SAFE","EUCLID","KETER","THAUMIEL","APOLLYON"],
        info:"O5 KONSEYİ — MUTLAK GİZLİLİK SEVİYESİ\\n► Yetki Seviyesi   : BEYOND-5 — Mutlak otorite\\n► Kimlik           : O5 üyeleri kimliklerini hiç kimseyle paylaşmaz\\n► Karar Yetkisi    : Vakfın tüm kaynakları konseyin emrinde\\n► XK Protokolü     : Dünya sonu senaryosu kararları bu konseye aittir\\n► İletişim         : Sadece şifreli kanal — yüz yüze görüşme yasak\\n► Veto Hakkı       : Herhangi bir etik, IGD veya TME kararı veto edilir\\n► Uyarı            : Bu veriye erişim otomatik olarak O5'e bildirildi"
    },

    // --- D-SINIFI ŞİFRELERİ (erişim yok) ---
    "D-CLASS-PERS":  { type:"dclass" },
    "D-SINIF-001":   { type:"dclass" },
    "D-PERSONEL":    { type:"dclass" },
    "D-4829":        { type:"dclass" },
    "D-SINIFI":      { type:"dclass" }
};

// =============================================
//  SCP BİLGİLERİ — Departmana göre 7 satır
// =============================================
function getSCPLines(num, cls, dept) {
    const sites = ["Site-Shadow", "Site-19", "Site-17", "Site-23", "Site-██"];
    const site = sites[num % sites.length];
    const yil = "20" + String(10 + (num % 14)).padStart(2,'0');

    const data = {
        "SEC": [
            `► Sınıflandırma   : ${cls}`,
            `► Muhafaza Tesisi : ${site} — B Katı Güvenli Bölge`,
            `► Güvenlik Çemberi: 3 katlı manyetik kilit, 24 saat silahlı nöbet`,
            `► Personel İzni   : En az Güvenlik Yetki-2 gerektirir`,
            `► İhlal Protokolü : Alarm kodu KIRMIZI, tesis otomatik kilitlenir`,
            `► Son İhlal       : ${num % 5 === 0 ? "Kayıt YOK" : yil + " — personel kayıpları mühürlendi"}`,
            `► Güvenlik Notu   : Nesneye 5 metreden fazla yaklaşmak yasaktır`
        ],
        "ENG": [
            `► Sınıflandırma   : ${cls}`,
            `► Muhafaza Tesisi : ${site} — Mühendislik Kanadı`,
            `► Muhafaza Sistemi: ${cls === "THAUMIEL" ? "Thaumiel-destekli reaktif çevre" : "Standart çelik-beton oda"}`,
            `► Güç Tüketimi    : Günlük ${(num * 17) % 400 + 50} kWh — kesintisiz izleme`,
            `► Bakım Periyodu  : Her ${num % 3 + 1} günde bir zorunlu kontrol`,
            `► Son Bakım       : ${yil}-0${(num % 9) + 1}-${10 + num % 18}`,
            `► Mühendislik Notu: Sistem arızasında acil kapatma EMP-7 devreye girer`
        ],
        "ETH": [
            `► Sınıflandırma   : ${cls}`,
            `► Muhafaza Tesisi : ${site}`,
            `► Deney Durumu    : ${num % 3 === 0 ? "Deneyler etik komite onayı bekliyor" : "Onaylı — sınırlı deney izni verildi"}`,
            `► D-Sınıfı Kullanım: ${num % 4 === 0 ? "Zorunlu — haftalık 1 denekle sınırlı" : "Yasak — bilgisayar simülasyonu yeterli"}`,
            `► İnsan Etkisi    : ${cls === "APOLLYON" ? "Toplu etkilenme riski — etik ihlal sayılır" : "Bireysel — kontrollü ortamda kabul edilebilir"}`,
            `► Komite Kararı   : ${yil} tarihli etik raporu onaylandı`,
            `► Etik Notu       : Tüm deneyler komite kararı olmadan başlatılamaz`
        ],
        "MED": [
            `► Sınıflandırma   : ${cls}`,
            `► Muhafaza Tesisi : ${site} — Tıbbi Karantina Bölgesi`,
            `► Biyolojik Risk  : ${cls === "KETER" ? "Sınıf-A Biyohazmat — tam koruyucu zorunlu" : "Düşük — standart maske yeterli"}`,
            `► Temas Protokolü : ${cls === "APOLLYON" ? "Temas KESİNLİKLE YASAK — uzaktan izleme" : "72 saat karantina zorunlu"}`,
            `► Anomalik Belirti: Maruziyet sonrası hafıza bozukluğu rapor edildi`,
            `► Tedavi Yöntemi  : ${num % 2 === 0 ? "A-sınıfı amnezik + destekleyici bakım" : "Henüz bilinen tedavi mevcut değil"}`,
            `► Tıbbi Notu      : ${cls === "KETER" || cls === "APOLLYON" ? "Tüm kayıplar gizli tutulmaktadır" : "Personel sağlığı sürekli takip altında"}`
        ],
        "IGD": [
            `► Sınıflandırma   : ${cls}`,
            `► Muhafaza Tesisi : ${site} — GİZLİ BÖLGE`,
            `► IGD İzleme      : Nesne etrafında gizli kamera ağı 7/24 aktif`,
            `► Personel Tarama : Her 48 saatte bir psikolojik değerlendirme zorunlu`,
            `► Etki Şüphesi    : ${num % 3 === 0 ? "Nesnenin personel kararlarını etkilediği şüpheleniliyor" : "Herhangi bir zihinsel etki tespit edilmedi"}`,
            `► Sızıntı Riski   : ${cls === "APOLLYON" || cls === "KETER" ? "YÜKSEK — bilgi sızıntısı SOK protokolü devreye girer" : "DÜŞÜK"}`,
            `► IGD Notu        : Bu dosyayı açan tüm personel kaydedilmektedir`
        ],
        "TME": [
            `► Sınıflandırma   : ${cls}`,
            `► Muhafaza Tesisi : ${site}`,
            `► Müdahale Birimi : TME-${(num % 4) + 1} — ${cls === "APOLLYON" ? "Kıyamet Timi" : "Standart Müdahale Ekibi"}`,
            `► Nötralizasyon   : ${cls === "KETER" || cls === "APOLLYON" ? "Ağır silah — termit + anomalik patlayıcı" : "Standart ateşli silah yeterli"}`,
            `► Sahaya İniş     : < ${num % 3 + 2} dakika — daima hazır durumda`,
            `► Son Operasyon   : ${yil} — ${num % 2 === 0 ? "başarıyla kontrol altına alındı" : "kayıplar mühürlendi, dosya kilitlendi"}`,
            `► Operasyon Notu  : ${cls === "APOLLYON" ? "Nötralizasyon emirsiz verilmez — O5 onayı şart" : "Standart protokol geçerli"}`
        ],
        "O5": [
            `► Sınıflandırma   : ${cls}`,
            `► Muhafaza Tesisi : [MÜHÜRLÜ — O5 SEVİYESİ]`,
            `► Konsey Kararı   : Nesne O5'in doğrudan denetiminde bulunmaktadır`,
            `► Erişim İzni     : Yalnızca O5 üyeleri ve onaylı temsilciler`,
            `► Thaumiel Kullanım: ${cls === "APOLLYON" ? "Aktif — XK önlemesi için devreye alındı" : "Değerlendirme aşamasında"}`,
            `► Gerçeklik Riski : ${cls === "APOLLYON" ? "OMEGA SEVİYE — varoluşsal tehdit aktif" : "Kontrol altında — periyodik değerlendirme yapılıyor"}`,
            `► O5 Notu         : Bu belgenin varlığı resmi kanallar tarafından kabul edilmeyecektir`
        ]
    };

    return data[dept] || data["SEC"];
}

// =============================================
//  SES
// =============================================
let audioCtx;
function ensureAudio() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
}
function playBeep(freq = 150, dur = 0.02, vol = 0.012) {
    if (!audioCtx) return;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'square';
    osc.frequency.value = freq;
    gain.gain.value = vol;
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + dur);
}

// =============================================
//  BAŞLANGIÇ
// =============================================
function initSystem() {
    document.getElementById('startScreen').style.display = 'none';
    ensureAudio();
    document.getElementById('statusBar').textContent = '● STATUS: ONLINE — YETKİ ANAHTARI BEKLENİYOR';
    document.getElementById('statusBar').style.color = '#1a3d1a';
}

// =============================================
//  YETKİ GİRİŞİ
// =============================================
document.getElementById('passInput').addEventListener('input', function() {
    const key = this.value.trim().toUpperCase();
    const dbKey = Object.keys(DATABASE).find(k => k.toUpperCase() === key);
    if (!dbKey) return;

    const entry = DATABASE[dbKey];

    // Her şeyi sıfırla
    document.querySelectorAll('.branch-box').forEach(b => b.style.display = 'none');
    document.getElementById('accessDeniedMsg').style.display = 'none';
    document.getElementById('scpSection').style.display = 'none';
    document.getElementById('scp-list').innerHTML = '';

    // Header'ı kapat
    document.getElementById('terminalHeader').classList.add('collapsed');

    if (entry.type === 'dclass') {
        document.getElementById('accessDeniedMsg').style.display = 'block';
        document.getElementById('statusBar').textContent = '● STATUS: ERİŞİM REDDEDİLDİ — D-SINIFI KİMLİK TANIMLANDI';
        document.getElementById('statusBar').style.color = '#8b0000';
        playBeep(80, 0.4, 0.04);
    } else {
        document.getElementById(entry.boxId).style.display = 'block';
        daktilo(entry.textId, entry.info);
        buildSCPList(entry.allowed, entry.dept);
        document.getElementById('statusBar').textContent = '● STATUS: YETKİ ONAYLANDI';
        document.getElementById('statusBar').style.color = '#00ff41';
        playBeep(440, 0.05, 0.015);
    }
});

// =============================================
//  DAKTİLO EFEKTİ
// =============================================
function daktilo(elId, text) {
    const el = document.getElementById(elId);
    el.innerHTML = '';
    const lines = text.split('\\n');
    let lineIndex = 0;
    let charIndex = 0;

    const timer = setInterval(() => {
        if (lineIndex >= lines.length) { clearInterval(timer); return; }
        if (!el.children[lineIndex]) {
            const div = document.createElement('div');
            div.className = 'branch-desc-line';
            el.appendChild(div);
        }
        const line = lines[lineIndex];
        if (charIndex < line.length) {
            el.children[lineIndex].textContent += line[charIndex];
            charIndex++;
            if (charIndex % 4 === 0) playBeep(100 + Math.random() * 50, 0.015, 0.007);
        } else {
            lineIndex++;
            charIndex = 0;
        }
    }, 10);
}

// =============================================
//  SCP LİSTESİNİ OLUŞTUR — RASTGELE SIRALI
// =============================================
function buildSCPList(allowed, dept) {
    const scpSection = document.getElementById('scpSection');
    const scpList = document.getElementById('scp-list');
    scpList.innerHTML = '';

    const allClasses = ["SAFE", "EUCLID", "KETER", "THAUMIEL", "APOLLYON"];

    // 1-50 arası indeksleri üret
    let indices = Array.from({length: 50}, (_, i) => i + 1);

    // Fisher-Yates shuffle — RASTGELE SIRALAMA
    for (let i = indices.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [indices[i], indices[j]] = [indices[j], indices[i]];
    }

    let count = 0;
    indices.forEach(i => {
        const cls = allClasses[i % allClasses.length];
        if (!allowed.includes(cls)) return;
        count++;

        const id = "SCP-" + (i + 100);

        const folder = document.createElement('div');
        folder.className = 'scp-folder';
        folder.innerHTML = `
            <span class="scp-name">${id}</span>
            <span class="scp-right">
                <span class="badge badge-${cls.toLowerCase()}">${cls}</span>
                <span class="scp-arrow">▶</span>
            </span>
        `;

        const det = document.createElement('div');
        det.className = 'scp-details';

        folder.onclick = () => {
            const isOpen = det.style.display === 'block';
            document.querySelectorAll('.scp-details').forEach(d => d.style.display = 'none');
            document.querySelectorAll('.scp-folder').forEach(f => f.classList.remove('active'));

            if (!isOpen) {
                det.style.display = 'block';
                folder.classList.add('active');
                det.innerHTML = '';

                const lines = getSCPLines(i, cls, dept);
                lines.forEach(line => {
                    const div = document.createElement('div');
                    div.className = 'scp-detail-line';
                    div.textContent = line;
                    det.appendChild(div);
                });

                playBeep(220, 0.04, 0.012);
            }
        };

        scpList.appendChild(folder);
        scpList.appendChild(det);
    });

    if (count > 0) scpSection.style.display = 'block';
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
