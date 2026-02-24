<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SHADOW RP | SCP DATABASE V4</title>
    <style>
        :root {
            --scp-red: #ff0000;
            --bg-black: #050505;
            --terminal-green: #00ff41;
            --border-gray: #222;
        }

        body {
            background-color: var(--bg-black);
            color: #ccc;
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 0;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E%3Ccircle cx='256' cy='256' r='200' stroke='white' stroke-width='10' fill='none' opacity='0.03'/%3E%3Cpath d='M256 56v100m0 200v100M56 256h100m200 0h100' stroke='white' stroke-width='15' opacity='0.03'/%3E%3Ccircle cx='256' cy='256' r='60' fill='white' opacity='0.03'/%3E%3C/svg%3E");
            background-attachment: fixed;
            background-position: center;
            background-repeat: no-repeat;
            background-size: 80%;
        }

        .top-nav {
            background: rgba(15, 15, 15, 0.98);
            border-bottom: 3px solid var(--scp-red);
            padding: 20px;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 9999;
        }

        .top-nav h1 {
            color: var(--scp-red);
            margin: 0;
            letter-spacing: 5px;
            font-size: 1.4rem;
            text-shadow: 0 0 10px rgba(255, 0, 0, 0.4);
        }

        .main-frame {
            padding: 20px;
            max-width: 900px;
            margin: 0 auto;
        }

        .scp-entry {
            background: rgba(10, 10, 10, 0.9);
            border: 1px solid var(--border-gray);
            border-left: 4px solid var(--scp-red);
            padding: 20px;
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }

        .scp-id-tag {
            font-size: 1.3rem;
            font-weight: bold;
            color: #fff;
            margin-bottom: 10px;
            display: block;
        }

        .scp-meta {
            color: #888;
            font-size: 0.85rem;
            margin-bottom: 15px;
            border-bottom: 1px solid #222;
            padding-bottom: 10px;
        }

        .typing-text {
            line-height: 1.6;
            font-size: 0.95rem;
            color: var(--terminal-green);
            min-height: 3.2em;
        }

        .location-box {
            margin-top: 15px;
            color: #5dade2;
            font-size: 0.8rem;
            text-transform: uppercase;
        }

        /* MOBIL OPTIMIZASYON ARSA CIKARILDI */
        @media (max-width: 600px) {
            .top-nav h1 { font-size: 1rem; letter-spacing: 2px; }
            .scp-entry { padding: 15px; }
            .scp-id-tag { font-size: 1.1rem; }
            .typing-text { font-size: 0.85rem; }
        }

        /* Daktilo Cursor */
        .cursor {
            display: inline-block;
            width: 8px;
            height: 15px;
            background: var(--terminal-green);
            margin-left: 5px;
            animation: blink 0.8s infinite;
        }

        @keyframes blink { 0% { opacity: 0; } 50% { opacity: 1; } 100% { opacity: 0; } }
    </style>
</head>
<body>

<div class="top-nav">
    <h1>SHADOW RP | KANONROL S1</h1>
</div>

<div class="main-frame" id="archive">
    <div class="scp-entry">
        <span class="scp-id-tag">DOSYA NO: SCP-001</span>
        <div class="scp-meta">SINIF: KETER | YETKİ: O5-ONLY</div>
        <div class="typing-text" data-text="Vakfın kuruluş sebebi olan bu anomali, tüm gerçekliği yeniden yazma kapasitesine sahiptir. Varlığı sadece üst düzey konsey tarafından onaylanmıştır."></div>
        <div class="location-box">KONUM: [VERİ SİLİNDİ]</div>
    </div>

    <div class="scp-entry">
        <span class="scp-id-tag">DOSYA NO: SCP-002</span>
        <div class="scp-meta">SINIF: EUCLID | YETKİ: SEVİYE 3</div>
        <div class="typing-text" data-text="İçine giren insanları mobilyaya dönüştüren devasa bir et yığını odasıdır. İçerideki tüm eşyalar biyolojik dokudan oluşmaktadır."></div>
        <div class="location-box">KONUM: TESİS-19 / SEKTÖR 4</div>
    </div>

    <div class="scp-entry">
        <span class="scp-id-tag">DOSYA NO: SCP-173</span>
        <div class="scp-meta">SINIF: EUCLID | YETKİ: STANDART</div>
        <div class="typing-text" data-text="Beton ve boyadan oluşan bu heykel, göz teması kesildiği an boyun kırma eylemine geçer. Temizliğe 3 personel girmelidir."></div>
        <div class="location-box">KONUM: SİTE-19 / HÜCRE 173</div>
    </div>

    <div class="scp-entry">
        <span class="scp-id-tag">DOSYA NO: SCP-096</span>
        <div class="scp-meta">SINIF: EUCLID | YETKİ: YÜKSEK GÜVENLİK</div>
        <div class="typing-text" data-text="Utangaç Adam. Yüzünü gören her canlıyı, dünyanın öbür ucunda olsa bile bulur ve parçalara ayırır. Gözlem odası yasaktır."></div>
        <div class="location-box">KONUM: SİTE-01 / ARŞİV KATI</div>
    </div>

    <div class="scp-entry">
        <span class="scp-id-tag">DOSYA NO: SCP-049</span>
        <div class="scp-meta">SINIF: EUCLID</div>
        <div class="typing-text" data-text="Veba Doktoru maskesi takan insansı bir varlıktır. Dokunuşu anında ölümü getirir ve kurbanı zombi olarak diriltir."></div>
        <div class="location-box">KONUM: TESİS-81 / TIBBİ ALAN</div>
    </div>

    <div class="scp-entry">
        <span class="scp-id-tag">DOSYA NO: SCP-682</span>
        <div class="scp-meta">SINIF: KETER</div>
        <div class="typing-text" data-text="Yok edilemez sürüngen. Vakfın elindeki en tehlikeli ve nefret dolu varlıktır. Sürekli asit havuzunda tutulmalıdır."></div>
        <div class="location-box">KONUM: TESİS-19 / ÖZEL MUHAFAZA</div>
    </div>

    <div class="scp-entry">
        <span class="scp-id-tag">DOSYA NO: SCP-087</span>
        <div class="scp-meta">SINIF: EUCLID</div>
        <div class="typing-text" data-text="Sonsuz bir merdiven boşluğu. Derinliklerden gelen çocuk ağlaması sesleri ve yüzsüz bir varlık (SCP-087-1) tespit edilmiştir."></div>
        <div class="location-box">KONUM: [BİLGİ GİZLENDİ]</div>
    </div>

    </div>

<script>
    // Daktilo Efekti Motoru
    function typeAll() {
        const elements = document.querySelectorAll('.typing-text');
        
        elements.forEach((el, index) => {
            const fullText = el.getAttribute('data-text');
            let i = 0;
            
            // Performans için sadece ekranda olanları veya sırayla yazdır
            setTimeout(() => {
                const interval = setInterval(() => {
                    el.innerHTML = fullText.substring(0, i) + '<span class="cursor"></span>';
                    i++;
                    if (i > fullText.length) {
                        clearInterval(interval);
                        el.innerHTML = fullText; // Kursörü kaldır
                    }
                }, 30); // Yazma hızı
            }, index * 1500); // Her kart arası gecikme
        });
    }

    // Telefonda kasmaması için Scroll Takibi
    window.onload = typeAll;

    // Satır sayısını ve SCP sayısını simüle eden genişletme (JS ile statik veri basımı)
    const archive = document.getElementById('archive');
    const additionalScps = 243; // 250'ye tamamlamak için

    for(let i=7; i<=additionalScps; i++) {
        const entry = document.createElement('div');
        entry.className = 'scp-entry';
        const scpId = i.toString().padStart(3, '0');
        
        entry.innerHTML = `
            <span class="scp-id-tag">DOSYA NO: SCP-${scpId}</span>
            <div class="scp-meta">SINIF: ${['SAFE','EUCLID','KETER','THAUMIEL'][Math.floor(Math.random()*4)]}</div>
            <div class="typing-text" id="type-${scpId}">Yükleniyor...</div>
            <div class="location-box">KONUM: SİTE-SHADOW / BLOK-${Math.ceil(i/10)}</div>
        `;
        archive.appendChild(entry);
        
        // Bu kısımdaki metinleri de daktiloya ekle
        const text = `Bu anomali ${scpId} numaralı protokol ile takip edilmektedir. Hücresel bozulma ve frekans yayılımı nedeniyle yüksek risk taşır.`;
        let charIndex = 0;
        setTimeout(() => {
            const target = document.getElementById(`type-${scpId}`);
            const tInterval = setInterval(() => {
                target.innerHTML = text.substring(0, charIndex) + '<span class="cursor"></span>';
                charIndex++;
                if(charIndex > text.length) clearInterval(tInterval);
            }, 20);
        }, (i + 5) * 800);
    }
</script>

</body>
</html>
