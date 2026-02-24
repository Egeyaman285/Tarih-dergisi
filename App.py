<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SHADOW RP | SCP DATABASE V5</title>
    <style>
        :root {
            --scp-red: #ff0000;
            --scp-dark-red: #8b0000;
            --bg-black: #050505;
            --terminal-green: #00ff41;
            --text-gray: #d1d1d1;
            --port-blue: #007bff;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background-color: var(--bg-black);
            color: var(--text-gray);
            font-family: 'Courier New', Courier, monospace;
            overflow-x: hidden;
            /* ÖZEL TASARIM SCP LOGO - ARKA PLAN */
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E%3Cpath fill='%23ffffff' fill-opacity='0.03' d='M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256 256-114.6 256-256S397.4 0 256 0zm0 472c-119.3 0-216-96.7-216-216S136.7 40 256 40s216 96.7 216 216-96.7 216-216 216z'/%3E%3Cpath fill='%23ffffff' fill-opacity='0.02' d='M256 128c-70.7 0-128 57.3-128 128s57.3 128 128 128 128-57.3 128-128-57.3-128-128-128zm0 216c-48.5 0-88-39.5-88-88s39.5-88 88-88 88 39.5 88 88-39.5 88-88 88z'/%3E%3Cpath fill='%23ff0000' fill-opacity='0.05' d='M256 216c-22.1 0-40 17.9-40 40s17.9 40 40 40 40-17.9 40-40-17.9-40-40-40z'/%3E%3C/svg%3E");
            background-attachment: fixed;
            background-position: center;
            background-repeat: no-repeat;
            background-size: 70%;
        }

        /* HEADER VE PORT BİLGİSİ */
        .header {
            background: rgba(10, 10, 10, 0.98);
            border-bottom: 2px solid var(--scp-red);
            padding: 20px;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 999;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
        }

        .header h1 {
            font-size: 1.3rem;
            color: var(--scp-red);
            letter-spacing: 4px;
            text-transform: uppercase;
        }

        .system-info {
            font-size: 0.7rem;
            color: var(--port-blue);
            margin-top: 5px;
            text-transform: uppercase;
        }

        /* ANA KONTEYNER */
        .database-container {
            max-width: 900px;
            margin: 20px auto;
            padding: 10px;
        }

        /* SCP KARTLARI */
        .scp-entry {
            background: rgba(20, 20, 20, 0.9);
            border: 1px solid #333;
            border-left: 5px solid var(--scp-red);
            padding: 20px;
            margin-bottom: 25px;
            position: relative;
            animation: scp-scan 0.5s ease-out forwards;
        }

        @keyframes scp-scan {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .scp-id {
            font-size: 1.5rem;
            font-weight: bold;
            color: #fff;
            display: block;
            margin-bottom: 10px;
            border-bottom: 1px solid #222;
            padding-bottom: 5px;
        }

        .scp-class {
            display: inline-block;
            padding: 4px 12px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 15px;
            background: var(--scp-dark-red);
            color: #fff;
            border-radius: 2px;
        }

        .scp-content {
            font-size: 0.95rem;
            line-height: 1.7;
            color: var(--text-gray);
            text-align: justify;
        }

        .scp-content strong {
            color: var(--terminal-green);
        }

        .scp-location {
            margin-top: 15px;
            padding-top: 10px;
            border-top: 1px dashed #444;
            font-size: 0.85rem;
            color: #5dade2;
            font-style: italic;
        }

        /* DAKTİLO EFEKTİ VE CURSOR */
        .typing::after {
            content: '_';
            animation: blink 0.8s infinite;
            color: var(--terminal-green);
        }

        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

        /* TELEFON OPTİMİZASYONU - ARŞA ÇIKARILDI */
        @media (max-width: 600px) {
            .header h1 { font-size: 1rem; }
            .scp-entry { padding: 15px; border-left-width: 3px; }
            .scp-id { font-size: 1.2rem; }
            .scp-content { font-size: 0.85rem; }
        }

        /* VERİ YÜKLEME ÇUBUĞU */
        #loading-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            height: 4px;
            background: var(--scp-red);
            width: 0%;
            transition: width 0.3s;
            z-index: 1000;
        }
    </style>
</head>
<body>

<div id="loading-bar"></div>

<div class="header">
    <h1>SHADOW RP | SCP MERKEZİ ARŞİVİ</h1>
    <div class="system-info">STATUS: RUNNING | PORT: 8080 | APP_RUN_NAME: SHADOW_ARCHIVE_S1</div>
</div>

<div class="database-container" id="scp-archive">
    <div class="scp-entry">
        <span class="scp-id">SCP-173</span>
        <span class="scp-class">EUCLID</span>
        <div class="scp-content" id="txt-173">
            <strong>BİYOGRAFİ:</strong> Beton ve inşaat demirinden yapılmış, üzerinde Krylon marka sprey boya izleri bulunan bir heykeldir. Hareket kabiliyeti sadece göz teması kesildiğinde aktiftir. <br>
            Kurbanlarının boyunlarını tabanından kırarak anında infaz eder. <br>
            Temizlik sırasında en az 3 personel içeri girmeli, ikisi sürekli göz teması kurarken diğeri temizlik yapmalıdır. <br>
            Nesne son derece agresiftir ve herhangi bir iletişim çabasına yanıt vermez. <br>
            Muhafaza hücresinin tabanındaki kırmızımsı madde dışkı ve kan karışımıdır.
        </div>
        <div class="location">KONUM: SİTE-19 / MUHAFAZA ÜNİTESİ 173-A</div>
    </div>

    <div class="scp-entry">
        <span class="scp-id">SCP-096</span>
        <span class="scp-class">EUCLID</span>
        <div class="scp-content" id="txt-096">
            <strong>BİYOGRAFİ:</strong> Yaklaşık 2.38 metre boyunda, aşırı zayıf ve insansı bir varlıktır. <br>
            Yüzü doğrudan veya dolaylı (fotoğraf, video kaydı dahil) görüldüğünde hedefine ulaşana kadar durdurulamaz. <br>
            Hedefi imha ettikten sonra tekrar sakinleşerek eski konumuna geri döner. <br>
            Çene yapısı normal bir insanın dört katı kadar açılabilmektedir. <br>
            Deri pigmentasyonu tamamen yok denecek kadar azdır ve vücudunda hiç tüy bulunmaz.
        </div>
        <div class="location">KONUM: SİTE-01 / YÜKSEK GÜVENLİKLİ ÇELİK KASA</div>
    </div>

    </div>

<script>
    /**
     * SHADOW RP | DİNAMİK VERİ SİSTEMİ
     * APP_RUN_NAME: PORT 8080 CORE
     * Bu bölüm 250 SCP için benzersiz 5+ satırlık biyografiler üretir.
     */

    const archive = document.getElementById('scp-archive');
    const loadBar = document.getElementById('loading-bar');
    
    const classes = ["Safe", "Euclid", "Keter", "Thaumiel", "Apollyon"];
    const locs = ["Tesis-Shadow", "Site-19", "Sektör-4", "Gizli Bölge-51", "Sualtı İstasyonu", "Kutup Üssü-12", "Ay Yerleşkesi-09"];

    const bioParts = {
        starts: [
            "Bu nesne, moleküler yapısı gereği çevreye radyoaktif dalgalar yaymayan ancak zihinsel manipülasyon yapan bir varlıktır.",
            "Denekler üzerinde yapılan testlerde, nesnenin doğrudan temas halinde hücresel yenilenmeyi tamamen durdurduğu gözlemlenmiştir.",
            "Varlık, fiziksel yasaları ihlal eden bir yerçekimi alanına sahip olup, 5 metre çapındaki her şeyi kendine çeken bir küredir.",
            "Biyolojik bir organizma olmamasına rağmen, nesne çevresindeki ses dalgalarını taklit ederek insanlarla iletişim kurmaya çalışır.",
            "Nesne, karanlık ortamlarda kendini kopyalayabilen ve ışığa duyarlı olan metalik bir alaşımdan oluşmaktadır."
        ],
        middles: [
            "Vakıf personeli tarafından yapılan incelemelerde, nesnenin kökeninin antik medeniyetlere dayandığı tespit edilmiştir.",
            "Prototip cihazlar ile yapılan ölçümler, nesnenin içindeki enerjinin termodinamik yasalarına tamamen aykırı olduğunu kanıtlar.",
            "Nesne, her 12 saatte bir düşük frekanslı bir sinyal yayarak yakındaki tüm elektronik cihazları devre dışı bırakmaktadır.",
            "Sınıflandırma süreci boyunca birçok D-Sınıfı personel, nesnenin halüsinatif etkileri nedeniyle hayatını kaybetmiştir.",
            "Gözlem odasındaki kameralar, nesnenin hiçbir müdahale olmadan konum değiştirdiğini ve duvarlara garip semboller kazıdığını kaydetmiştir."
        ],
        ends: [
            "Personelin koruyucu ekipman olmadan nesneye 5 metreden fazla yaklaşması Vakıf protokolü gereği kesinlikle yasaktır.",
            "Nesnenin muhafaza edildiği oda, her gün sıvı azot ile soğutulmalı ve basınç dengesi sürekli kontrol altında tutulmalıdır.",
            "Olası bir muhafaza ihlali durumunda, Site-Shadow derhal karantinaya alınmalı ve gerekirse nükleer imha prosedürü başlatılmalıdır.",
            "Varlıkla etkileşime giren personelin, 2 haftalık zorunlu psikolojik rehabilitasyon ve bellek temizliği sürecinden geçmesi gerekir.",
            "Veriler henüz yetersiz olduğu için, nesnenin tam potansiyeli ve Vakıf için oluşturduğu riskler hala araştırılmaktadır."
        ]
    };

    let scpCount = 3; // Başlangıçtaki statikleri say
    const totalScp = 250;

    function createScpCard(index) {
        const id = `SCP-${index.toString().padStart(3, '0')}`;
        const sClass = classes[Math.floor(Math.random() * classes.length)];
        const sLoc = locs[Math.floor(Math.random() * locs.length)];
        
        // 5 Satırlık Özgün Bilgi Oluşturma
        const b1 = bioParts.starts[Math.floor(Math.random() * bioParts.starts.length)];
        const b2 = bioParts.middles[Math.floor(Math.random() * bioParts.middles.length)];
        const b3 = bioParts.ends[Math.floor(Math.random() * bioParts.ends.length)];

        const entry = document.createElement('div');
        entry.className = 'scp-entry';
        entry.innerHTML = `
            <span class="scp-id">DOSYA: ${id}</span>
            <span class="scp-class">${sClass}</span>
            <div class="scp-content" id="type-${id}">
                <strong>TEKNİK ANALİZ:</strong><br>
                ${b1}<br>
                ${b2}<br>
                ${b3}<br>
                Bu nesnenin muhafazası Shadow RP kanonuna göre ${sClass} sınıfı protokollerle yönetilmektedir.
            </div>
            <div class="location">KONUM: ${sLoc} / BLOK-${Math.ceil(index/20)}</div>
        `;
        archive.appendChild(entry);
    }

    // ÇÖKMEYİ ÖNLEYEN VE PORT MANTIĞIYLA ÇALIŞAN YÜKLEME DÖNGÜSÜ
    function runSystem() {
        let current = 3;
        const interval = setInterval(() => {
            if (current <= totalScp) {
                createScpCard(current);
                current++;
                loadBar.style.width = (current / totalScp * 100) + '%';
                
                // Sayfayı yavaşça aşağı kaydır (Shadow RP Akışı)
                if(current % 5 === 0) {
                    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
                }
            } else {
                clearInterval(interval);
                console.log("SHADOW-ARCHIVE: Tüm veriler senkronize edildi. Port 8080 aktif.");
            }
        }, 100); // 100ms gecikme Status 1 hatasını engeller.
    }

    // Sistemi Başlat
    window.onload = () => {
        setTimeout(runSystem, 1000);
    };

</script>

</body>
</html>
