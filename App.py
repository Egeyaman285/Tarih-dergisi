<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SHADOW RP | ARSIV S1</title>
    <style>
        :root {
            --scp-red: #ff0000;
            --bg: #080808;
            --green: #00ff41;
        }

        body {
            background-color: var(--bg);
            color: #ccc;
            font-family: 'Courier New', Courier, monospace;
            margin: 0; padding: 0;
            /* ÖZEL SCP LOGOSU */
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E%3Ccircle cx='256' cy='256' r='180' stroke='white' stroke-width='5' fill='none' opacity='0.05'/%3E%3Cpath d='M256 20v100M256 392v100M20 256h100M392 256h100' stroke='white' stroke-width='10' opacity='0.05'/%3E%3C/svg%3E");
            background-attachment: fixed;
            background-position: center;
            background-repeat: no-repeat;
        }

        .header {
            background: #000;
            border-bottom: 2px solid var(--scp-red);
            padding: 15px;
            text-align: center;
            position: sticky; top: 0; z-index: 100;
            box-shadow: 0 0 20px rgba(255,0,0,0.2);
        }

        .container { padding: 10px; max-width: 700px; margin: auto; }

        .scp-box {
            background: rgba(15, 15, 15, 0.95);
            border: 1px solid #222;
            border-left: 4px solid var(--scp-red);
            margin-bottom: 20px;
            padding: 15px;
            min-height: 120px;
        }

        .id { color: #fff; font-weight: bold; font-size: 1.2rem; display: block; margin-bottom: 5px; }
        .info { color: var(--green); font-size: 0.9rem; line-height: 1.4; }
        .loc { color: #5dade2; font-size: 0.8rem; margin-top: 10px; text-transform: uppercase; }

        /* Mobil Optimizasyon */
        @media (max-width: 480px) {
            .id { font-size: 1rem; }
            .info { font-size: 0.8rem; }
        }

        .typing::after { content: '_'; animation: blink 0.8s infinite; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
    </style>
</head>
<body>

<div class="header">
    <h1 style="color: var(--scp-red); margin:0; font-size: 1.2rem;">SHADOW RP | MERKEZI VERITABANI</h1>
</div>

<div class="container" id="main">
    <div class="scp-box">
        <span class="id">SCP-173</span>
        <div class="info" data-text="Beton ve insaat demiri karisimi bir heykeldir. Goz temasi kesildiginde saniyeler icinde boyun kirar."></div>
        <div class="loc">KONUM: SITE-19 / HUCRE 01</div>
    </div>

    <div class="scp-box">
        <span class="id">SCP-096</span>
        <div class="info" data-text="Yuzu goruldugunde durdurulamaz bir ofkeye kapilan insansi varlik. Hedefini dunya uzerinde her yerde bulur."></div>
        <div class="loc">KONUM: SITE-01 / OZEL KASA</div>
    </div>
</div>

<script>
    const main = document.getElementById('main');
    
    // 250 SCP VERİ HAVUZU (SİSTEMİ YORMAYAN DİNAMİK YAPILANDIRMA)
    const descs = [
        "Temas halinde canli dokuyu aninda kristalize eden antik bir mucevher kutusu.",
        "Sadece aynalarda gorunen ve insanlari kendi boyutuna ceken golge organizma.",
        "Yercekimi kurallarini tamamen yok sayan, dokunuldugunda zaman kaymasi yaratan kure.",
        "Radyo frekanslari uzerinden insan bilincini kontrol eden yapay zeka paraziti.",
        "Hic bitmeyen bir ciglik sesi yayan ve cevresindeki personeli delirten heykel.",
        "Gece yarisi beliren ve icine girenleri 1920'lere isinlayan mekan anomalisi.",
        "Kendi kendine yazilan ve okuyan kisinin olum tarihini gosteren lanetli gunluk."
    ];
    const locs = ["TESIS-19", "SITE-SHADOW", "ALAN-102", "SEKTOR-4", "GIZLI BOLGE-12"];

    // 250 SCP'yi sisteme ekle
    for(let i=1; i<=250; i++) {
        if(i==173 || i==96) continue;
        const div = document.createElement('div');
        div.className = 'scp-box';
        const d = descs[Math.floor(Math.random()*descs.length)];
        const l = locs[Math.floor(Math.random()*locs.length)];
        
        div.innerHTML = `
            <span class="id">SCP-${i.toString().padStart(3, '0')}</span>
            <div class="info" data-text="${d} Bu nesne yuksek risk tasimaktadir."></div>
            <div class="loc">KONUM: ${l}</div>
        `;
        main.appendChild(div);
    }

    // ÇÖKME KORUMALI DAKTİLO (Sadece ekrandakini yazar)
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if(entry.isIntersecting) {
                const target = entry.target;
                const text = target.getAttribute('data-text');
                if(!target.classList.contains('done')) {
                    typeWriter(target, text);
                    target.classList.add('done');
                }
            }
        });
    }, { threshold: 0.1 });

    function typeWriter(element, text) {
        let i = 0;
        element.classList.add('typing');
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, 20);
            } else {
                element.classList.remove('typing');
            }
        }
        type();
    }

    document.querySelectorAll('.info').forEach(info => observer.observe(info));
</script>

</body>
</html>
