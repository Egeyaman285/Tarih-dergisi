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

<div id="startScreen">
    <div class="start-logo">SHADOW</div>
    <div class="start-sub">SİTE-SHADOW GİZLİ VERİ TABANI</div>
    <div class="start-sub">ERİŞİM KISITLIDIR — YETKİSİZ GİRİŞ TESPİT EDİLECEKTİR</div>
    <button class="start-btn" onclick="initSystem()">&#9654; SİSTEMİ BAŞLAT</button>
</div>

<div class="shadow-tag">SHADOW RP</div>

<div id="terminalHeader">
    <div class="header-title">&#11041; SECURE TERMINAL V13 &#11041;</div>
    <div id="headerInputArea">
        <input type="password" id="passInput" class="auth-input" placeholder="[ YETKİ ANAHTARI GİRİNİZ ]" autocomplete="off">
        <div id="statusBar">&#9679; STATUS: OFFLINE — YETKİ BEKLENİYOR</div>
    </div>
</div>

<div class="main-container">

    <div id="accessDeniedMsg">
        <div class="denied-title">&#9888; ERİŞİM REDDEDİLDİ &#9888;</div>
        <div style="color:#ff4444; margin:15px 0; font-size:1.1rem; letter-spacing:4px;">DOSYA BULUNAMADI</div>
        <div class="denied-sub">D-SINIFI PERSONEL SİCİL NUMARASI TANIMLANDI</div>
        <div class="denied-sub">BU KİMLİK İLE ERİŞİLEBİLECEK GİZLİ DOSYA MEVCUT DEĞİLDİR</div>
        <div class="denied-sub" style="margin-top:15px; color:#2a2a2a;">GİRİŞİM KAYDEDÜLDÜ — GÜVENLİK BİLGİLENDİRİLDİ</div>
    </div>

    <div id="SEC-B" class="branch-box"><div class="branch-title">GÜVENLİK DEPARTMANI</div><div id="sec-text"></div></div>
    <div id="ENG-B" class="branch-box"><div class="branch-title">MÜHENDİSLİK BİRİMİ</div><div id="eng-text"></div></div>
    <div id="ETH-B" class="branch-box"><div class="branch-title">ETİK KOMİTE</div><div id="eth-text"></div></div>
    <div id="MED-B" class="branch-box"><div class="branch-title">TIBBİ DEPARTMAN</div><div id="med-text"></div></div>
    <div id="IGD-B" class="branch-box"><div class="branch-title">İÇ GÜVENLİK (IGD)</div><div id="igd-text"></div></div>
    <div id="TME-B" class="branch-box"><div class="branch-title">TAKTİKSEL MÜDAHALE (TME)</div><div id="tme-text"></div></div>
    <div id="O5-B" class="branch-box o5-box"><div class="branch-title">O5 KONSEYİ</div><div id="o5-text"></div></div>

    <div id="scpSection">
        <div class="section-header">&#9658; ANOMALİK NESNE ARŞİVİ — YETKİLİ DOSYALAR</div>
        <div id="scp-list"></div>
    </div>
</div>

<script>
var DATABASE = {
    "SEC-SHADOW-2026": {
        type:"dept", boxId:"SEC-B", textId:"sec-text", dept:"SEC",
        allowed:["SAFE","EUCLID"],
        info:[
            "GÜVENLİK PROTOKOLÜ AKTİF",
            "► Yetki Seviyesi   : BETA-3",
            "► Müdahale Kapsamı : Safe ve Euclid sınıfı anomaliler",
            "► Keter İhlali     : TME müdahalesi çağrılır, personel bölgeden çekilir",
            "► Vardiya Süresi   : 8 saatlik rotasyon, 3 peron / vardiya",
            "► Silah Protokolü  : Standart ateşli silah — Thaumiel için yasak",
            "► Öncelik          : Tesis güvenliği, sivil kayıp SIFIR politikası",
            "► Uyarı            : İhlal anında kod KIRMIZI butonu tetiklenecek"
        ]
    },
    "ENG-TECH-SYS": {
        type:"dept", boxId:"ENG-B", textId:"eng-text", dept:"ENG",
        allowed:["SAFE","EUCLID","KETER","THAUMIEL"],
        info:[
            "MÜHENDİSLİK SİSTEM RAPORU",
            "► Yetki Seviyesi   : DELTA-4",
            "► Bakım Kapsamı    : Safe, Euclid, Keter, Thaumiel sınıfları",
            "► Güç Sistemi      : Jeneratör denetimi her 24 saatte bir zorunlu",
            "► Containment Sys  : Thaumiel muhafaza cihazları aktif izleme altında",
            "► Acil Kapatma     : EMP-7 protokolü — yetkili mühendis imzası gerekli",
            "► Malzeme Yönetimi : Anomalik bileşen stoku haftalık raporlanır",
            "► Uyarı            : İzinsiz sistem değişikliği otomatik alarm tetikler"
        ]
    },
    "ETHIC-BOARD-01": {
        type:"dept", boxId:"ETH-B", textId:"eth-text", dept:"ETH",
        allowed:["SAFE","EUCLID","KETER","THAUMIEL","APOLLYON"],
        info:[
            "ETİK KOMİTE DİREKTİFİ",
            "► Yetki Seviyesi   : OMEGA-5 — Tüm sınıflar üzerinde denetim",
            "► Denetim Kapsamı  : Tüm deney protokolleri etik onay gerektirir",
            "► İnsan Deneyleri  : D-sınıfı kullanımı kota ve limit dahilinde",
            "► Amnezik Kullanımı: Yalnızca komite onayı ile uygulanabilir",
            "► Komitenin Gücü   : O5 kararlarını etik ihlal gerekçesiyle durdurabilir",
            "► Rapor Dönemi     : Aylık etik değerlendirme raporu zorunludur",
            "► Uyarı            : İnsan onuruna aykırı deney derhal durdurulur"
        ]
    },
    "MED-DEPT-99": {
        type:"dept", boxId:"MED-B", textId:"med-text", dept:"MED",
        allowed:["SAFE","EUCLID","KETER"],
        info:[
            "TIBBİ DEPARTMAN ANALİZİ",
            "► Yetki Seviyesi   : GAMMA-3",
            "► Biyolojik Tehdit : Sınıf-A biyohazmat protokolü daima hazır",
            "► Personel Sağlığı : Temas sonrası 72 saat karantina zorunlu",
            "► Amnezik Stok     : A-klası, B-klası ve C-klası mevcut",
            "► Antidot Veri     : Anomalik maruziyete karşı 14 formül arşivde",
            "► D-Sınıfı Tıbbi   : Tıbbi kayıt tutulur; ölüm protokolü ayrı dosyada",
            "► Uyarı            : Bulaşıcı anomali tespitinde tesis karantinaya alınır"
        ]
    },
    "IGD-INTERNAL-00": {
        type:"dept", boxId:"IGD-B", textId:"igd-text", dept:"IGD",
        allowed:["SAFE","EUCLID","KETER","THAUMIEL","APOLLYON"],
        info:[
            "İÇ GÜVENLİK DİREKTİFİ — GİZLİ",
            "► Yetki Seviyesi   : SIGMA-5 — Tüm departmanlar üzerinde",
            "► Görev            : Vakıf içi sızıntı, casusluk, ihanet tespiti",
            "► İzleme           : Tüm personel iletişimi pasif izleme altında",
            "► Ajan Ağı         : Her departmanda en az 1 gizli IGD ajanı bulunur",
            "► Gözaltı Yetkisi  : Şüpheli personel mahkemesiz tutulabilir 72 saat",
            "► Dosya Erişimi    : IGD tüm gizli dosyalara erişim hakkına sahiptir",
            "► Uyarı            : Bu dosyayı okuduğunuz kaydedildi"
        ]
    },
    "TME-TACTICAL-X": {
        type:"dept", boxId:"TME-B", textId:"tme-text", dept:"TME",
        allowed:["SAFE","EUCLID","KETER","THAUMIEL","APOLLYON"],
        info:[
            "TAKTİKSEL MÜDAHALE PLANI — GİZLİ",
            "► Yetki Seviyesi   : KAPPA-4 — Ağır silahlı operasyon birimi",
            "► Müdahale Hızı    : Alarm sonrası sahaya iniş 3 dakika altında",
            "► Keter Protokolü  : Nötralizasyon emri O5 onayı olmadan verilemez",
            "► Apollyon Durumu  : Olay yeri boşaltma — TME son savunma hattı",
            "► Ekipman          : Anomalik karşı silahlar, Thaumiel destekli zırh",
            "► Kayıp Politikası : Operasyon önceliklidir; kayıp ikincil kabul edilir",
            "► Uyarı            : TME emirleri yazılı olmadan sözlü kabul edilmez"
        ]
    },
    "O5-secsysttem": {
        type:"dept", boxId:"O5-B", textId:"o5-text", dept:"O5",
        allowed:["SAFE","EUCLID","KETER","THAUMIEL","APOLLYON"],
        info:[
            "O5 KONSEYİ — MUTLAK GİZLİLİK SEVİYESİ",
            "► Yetki Seviyesi   : BEYOND-5 — Mutlak otorite",
            "► Kimlik           : O5 üyeleri kimliklerini hiç kimseyle paylaşmaz",
            "► Karar Yetkisi    : Vakfın tüm kaynakları konseyin emrinde",
            "► XK Protokolü     : Dünya sonu senaryosu kararları bu konseye aittir",
            "► İletişim         : Sadece şifreli kanal — yüz yüze görüşme yasak",
            "► Veto Hakkı       : Herhangi bir etik IGD veya TME kararı veto edilir",
            "► Uyarı            : Bu veriye erişim otomatik olarak O5'e bildirildi"
        ]
    },
    "D-CLASS-PERS":  { type:"dclass" },
    "D-SINIF-001":   { type:"dclass" },
    "D-PERSONEL":    { type:"dclass" },
    "D-4829":        { type:"dclass" },
    "D-SINIFI":      { type:"dclass" }
};

function getSCPLines(num, cls, dept) {
    var sites = ["Site-Shadow","Site-19","Site-17","Site-23","Site-17"];
    var site = sites[num % sites.length];
    var yil = "20" + (10 + (num % 14));

    var data = {
        "SEC": [
            "Siniflandirma   : " + cls,
            "Muhafaza Tesisi : " + site + " — B Kati Güvenli Bölge",
            "Güvenlik Cemberi: 3 katli manyetik kilit, 24 saat silahli nöbet",
            "Personel Izni   : En az Güvenlik Yetki-2 gerektirir",
            "Ihlal Protokolü : Alarm kodu KIRMIZI, tesis otomatik kilitlenir",
            "Son Ihlal       : " + (num % 5 === 0 ? "Kayit YOK" : yil + " — personel kayiplari mühürlendi"),
            "Güvenlik Notu   : Nesneye 5 metreden fazla yaklasmak yasaktir"
        ],
        "ENG": [
            "Siniflandirma   : " + cls,
            "Muhafaza Tesisi : " + site + " — Mühendislik Kanadi",
            "Muhafaza Sistemi: " + (cls === "THAUMIEL" ? "Thaumiel destekli reaktif çevre" : "Standart çelik-beton oda"),
            "Güç Tüketimi    : Günlük " + ((num * 17) % 400 + 50) + " kWh — kesintisiz izleme",
            "Bakim Periyodu  : Her " + (num % 3 + 1) + " günde bir zorunlu kontrol",
            "Son Bakim       : " + yil + "-0" + ((num % 9) + 1) + "-" + (10 + num % 18),
            "Mühendislik Notu: Sistem arizasinda acil kapatma EMP-7 devreye girer"
        ],
        "ETH": [
            "Siniflandirma   : " + cls,
            "Muhafaza Tesisi : " + site,
            "Deney Durumu    : " + (num % 3 === 0 ? "Deneyler etik komite onayi bekliyor" : "Onaylandi — sinirli deney izni verildi"),
            "D-Sinifi Kullanim: " + (num % 4 === 0 ? "Zorunlu — haftada 1 denekle sinirli" : "Yasak — bilgisayar simülasyonu yeterli"),
            "Insan Etkisi    : " + (cls === "APOLLYON" ? "Toplu etkilenme riski — etik ihlal sayilir" : "Bireysel — kontrollü ortamda kabul edilebilir"),
            "Komite Karari   : " + yil + " tarihli etik raporu onaylandi",
            "Etik Notu       : Tüm deneyler komite karari olmadan baslatilamamaz"
        ],
        "MED": [
            "Siniflandirma   : " + cls,
            "Muhafaza Tesisi : " + site + " — Tibbi Karantina Bölgesi",
            "Biyolojik Risk  : " + (cls === "KETER" ? "Sinif-A Biyohazmat — tam koruyucu zorunlu" : "Düsük — standart maske yeterli"),
            "Temas Protokolü : " + (cls === "APOLLYON" ? "Temas KESINLIKLE YASAK — uzaktan izleme" : "72 saat karantina zorunlu"),
            "Anomalik Belirti: Maruziyet sonrasi hafiza bozuklugu rapor edildi",
            "Tedavi Yöntemi  : " + (num % 2 === 0 ? "A-sinifi amnezik + destekleyici bakim" : "Henüz bilinen tedavi mevcut degil"),
            "Tibbi Notu      : " + (cls === "KETER" || cls === "APOLLYON" ? "Tüm kayiplar gizli tutulmaktadir" : "Personel sagligi sürekli takip altinda")
        ],
        "IGD": [
            "Siniflandirma   : " + cls,
            "Muhafaza Tesisi : " + site + " — GIZLI BÖLGE",
            "IGD Izleme      : Nesne etrafinda gizli kamera agi 7/24 aktif",
            "Personel Tarama : Her 48 saatte bir psikolojik degerlendirme zorunlu",
            "Etki Süphesi    : " + (num % 3 === 0 ? "Nesnenin personel kararlarini etkiledigi süpheleniliyor" : "Herhangi bir zihinsel etki tespit edilmedi"),
            "Sizinti Riski   : " + (cls === "APOLLYON" || cls === "KETER" ? "YÜKSEK — SOK protokolü devreye girer" : "DÜSÜK"),
            "IGD Notu        : Bu dosyayi açan tüm personel kaydedilmektedir"
        ],
        "TME": [
            "Siniflandirma   : " + cls,
            "Muhafaza Tesisi : " + site,
            "Müdahale Birimi : TME-" + ((num % 4) + 1) + " — " + (cls === "APOLLYON" ? "Kiyamet Timi" : "Standart Müdahale Ekibi"),
            "Nötralizasyon   : " + (cls === "KETER" || cls === "APOLLYON" ? "Agir silah — termit + anomalik patlayici" : "Standart atisli silah yeterli"),
            "Sahaya Inis     : " + (num % 3 + 2) + " dakika alti — daima hazir durumda",
            "Son Operasyon   : " + yil + " — " + (num % 2 === 0 ? "basariyla kontrol altina alindi" : "kayiplar mühürlendi"),
            "Operasyon Notu  : " + (cls === "APOLLYON" ? "Nötralizasyon emirsiz verilmez — O5 onayi sart" : "Standart protokol geçerli")
        ],
        "O5": [
            "Siniflandirma   : " + cls,
            "Muhafaza Tesisi : [MÜHÜRLÜ — O5 SEVİYESİ]",
            "Konsey Karari   : Nesne O5'in dogrudan denetiminde bulunmaktadir",
            "Erisim Izni     : Yalnizca O5 üyeleri ve onaylı temsilciler",
            "Thaumiel Kullanim: " + (cls === "APOLLYON" ? "Aktif — XK önlemesi için devreye alindi" : "Degerlendirme asamasinda"),
            "Gerceklik Riski : " + (cls === "APOLLYON" ? "OMEGA SEVIYE — varolussal tehdit aktif" : "Kontrol altinda — periyodik degerlendirme yapiliyor"),
            "O5 Notu         : Bu belgenin varligi resmi kanallar tarafindan kabul edilmeyecektir"
        ]
    };

    return data[dept] || data["SEC"];
}

var audioCtx;
function ensureAudio() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
}
function playBeep(freq, dur, vol) {
    if (!audioCtx) return;
    freq = freq || 150; dur = dur || 0.02; vol = vol || 0.012;
    var osc = audioCtx.createOscillator();
    var gain = audioCtx.createGain();
    osc.type = 'square';
    osc.frequency.value = freq;
    gain.gain.value = vol;
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + dur);
}

function initSystem() {
    document.getElementById('startScreen').style.display = 'none';
    ensureAudio();
    document.getElementById('statusBar').textContent = 'STATUS: ONLINE — YETKİ ANAHTARI BEKLENİYOR';
    document.getElementById('statusBar').style.color = '#1a3d1a';
}

document.getElementById('passInput').addEventListener('input', function() {
    var key = this.value.trim().toUpperCase();
    var dbKey = null;
    var keys = Object.keys(DATABASE);
    for (var i = 0; i < keys.length; i++) {
        if (keys[i].toUpperCase() === key) { dbKey = keys[i]; break; }
    }
    if (!dbKey) return;

    var entry = DATABASE[dbKey];

    var boxes = document.querySelectorAll('.branch-box');
    for (var i = 0; i < boxes.length; i++) boxes[i].style.display = 'none';
    document.getElementById('accessDeniedMsg').style.display = 'none';
    document.getElementById('scpSection').style.display = 'none';
    document.getElementById('scp-list').innerHTML = '';
    document.getElementById('terminalHeader').classList.add('collapsed');

    if (entry.type === 'dclass') {
        document.getElementById('accessDeniedMsg').style.display = 'block';
        document.getElementById('statusBar').textContent = 'STATUS: ERİŞİM REDDEDİLDİ — D-SINIFI KİMLİK';
        document.getElementById('statusBar').style.color = '#8b0000';
        playBeep(80, 0.4, 0.04);
    } else {
        document.getElementById(entry.boxId).style.display = 'block';
        daktilo(entry.textId, entry.info);
        buildSCPList(entry.allowed, entry.dept);
        document.getElementById('statusBar').textContent = 'STATUS: YETKİ ONAYLANDI';
        document.getElementById('statusBar').style.color = '#00ff41';
        playBeep(440, 0.05, 0.015);
    }
});

function daktilo(elId, lines) {
    var el = document.getElementById(elId);
    el.innerHTML = '';
    var lineIndex = 0;
    var charIndex = 0;

    var timer = setInterval(function() {
        if (lineIndex >= lines.length) { clearInterval(timer); return; }
        if (!el.children[lineIndex]) {
            var div = document.createElement('div');
            div.className = 'branch-desc-line';
            el.appendChild(div);
        }
        var line = lines[lineIndex];
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

function buildSCPList(allowed, dept) {
    var scpSection = document.getElementById('scpSection');
    var scpList = document.getElementById('scp-list');
    scpList.innerHTML = '';

    var allClasses = ["SAFE","EUCLID","KETER","THAUMIEL","APOLLYON"];

    var indices = [];
    for (var i = 1; i <= 50; i++) indices.push(i);

    // Fisher-Yates shuffle
    for (var i = indices.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = indices[i]; indices[i] = indices[j]; indices[j] = tmp;
    }

    var count = 0;
    indices.forEach(function(num) {
        var cls = allClasses[num % allClasses.length];
        if (allowed.indexOf(cls) === -1) return;
        count++;

        var id = "SCP-" + (num + 100);

        var folder = document.createElement('div');
        folder.className = 'scp-folder';
        folder.innerHTML =
            '<span class="scp-name">' + id + '</span>' +
            '<span class="scp-right">' +
            '<span class="badge badge-' + cls.toLowerCase() + '">' + cls + '</span>' +
            '<span class="scp-arrow">&#9658;</span>' +
            '</span>';

        var det = document.createElement('div');
        det.className = 'scp-details';

        (function(folderEl, detEl, n, c, d) {
            folderEl.onclick = function() {
                var isOpen = detEl.style.display === 'block';
                var allDets = document.querySelectorAll('.scp-details');
                var allFolders = document.querySelectorAll('.scp-folder');
                for (var i = 0; i < allDets.length; i++) allDets[i].style.display = 'none';
                for (var i = 0; i < allFolders.length; i++) allFolders[i].classList.remove('active');

                if (!isOpen) {
                    detEl.style.display = 'block';
                    folderEl.classList.add('active');
                    detEl.innerHTML = '';
                    var lines = getSCPLines(n, c, d);
                    lines.forEach(function(line) {
                        var div = document.createElement('div');
                        div.className = 'scp-detail-line';
                        div.textContent = line;
                        detEl.appendChild(div);
                    });
                    playBeep(220, 0.04, 0.012);
                }
            };
        })(folder, det, num, cls, dept);

        scpList.appendChild(folder);
        scpList.appendChild(det);
    });

    if (count > 0) scpSection.style.display = 'block';
}
</script>
</body>
</html>
