<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>SHADOW RP - SCP DATABASE</title>
    <style>
        :root {
            --scp-red: #9e1a1a;
            --scp-gold: #c5a028;
            --bg-dark: #0a0a0a;
            --terminal-green: #00ff41;
        }

        body {
            background-color: var(--bg-dark);
            color: #d1d1d1;
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 20px;
            /* Arka plana özel tasarım SCP Logosu */
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" opacity="0.05"><path fill="white" d="M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256 256-114.6 256-256S397.4 0 256 0zm0 472c-119.3 0-216-96.7-216-216S136.7 40 256 40s216 96.7 216 216-96.7 216-216 216zm-80-216c0-44.1 35.9-80 80-80s80 35.9 80 80-35.9 80-80 80-80-35.9-80-80zm112 0c0-17.7-14.3-32-32-32s-32 14.3-32 32 14.3 32 32 32 32-14.3 32-32zM256 80c-97.2 0-176 78.8-176 176s78.8 176 176 176 176-78.8 176-176S353.2 80 256 80zm0 320c-79.5 0-144-64.5-144-144s64.5-144 144-144 144 64.5 144 144-64.5 144-144 144z"/></svg>');
            background-attachment: fixed;
            background-position: center;
            background-repeat: no-repeat;
            background-size: 60%;
        }

        header {
            border-bottom: 2px solid var(--scp-red);
            padding-bottom: 10px;
            margin-bottom: 30px;
            text-align: center;
        }

        .database-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }

        .scp-card {
            background: rgba(20, 20, 20, 0.9);
            border: 1px solid #333;
            padding: 15px;
            border-left: 5px solid var(--scp-red);
            transition: transform 0.2s;
        }

        .scp-card:hover {
            border-color: var(--scp-gold);
            transform: scale(1.02);
        }

        .scp-id { color: var(--scp-red); font-weight: bold; font-size: 1.2em; }
        .scp-class { color: var(--scp-gold); font-style: italic; margin-bottom: 10px; }
        .scp-location { color: #5dade2; font-size: 0.9em; margin-top: 10px; }
        .scp-bio { line-height: 1.5; font-size: 0.95em; text-align: justify; }
        
        .loading { text-align: center; font-size: 2em; color: var(--terminal-green); }
    </style>
</head>
<body>

<header>
    <h1>SHADOW RP: KANON-ROL VERİTABANI</h1>
    <p>ERİŞİM SEVİYESİ 4 - GİZLİ BELGE</p>
</header>

<div id="app" class="database-container">
    <div class="loading">SİSTEM YÜKLENİYOR... [LOGIN: O5-█]</div>
</div>

<script>
/** * SCP VERİ ÜRETİM MOTORU 
 * Bu bölüm 1000+ nesne için benzersiz biyografiler oluşturur.
 */

const classes = ["Safe", "Euclid", "Keter", "Thaumiel", "Neutralized", "Apollyon", "Archon"];

const bioParts = {
    starts: [
        "Bu nesne, moleküler yapısı gereği çevreye radyasyon yaymayan ancak zihinsel manipülasyon yapan bir yapıdadır.",
        "Denekler üzerinde yapılan testlerde, nesnenin doğrudan temas halinde hücresel yenilenmeyi durdurduğu gözlemlenmiştir.",
        "Varlık, fiziksel yasaları ihlal eden bir yerçekimi alanına sahip olup, 5 metre çapındaki her şeyi kendine çeker.",
        "Biyolojik bir organizma olmamasına rağmen, nesne çevresindeki ses dalgalarını taklit ederek iletişim kurmaya çalışır.",
        "Nesne, karanlık ortamlarda kendini kopyalayabilen ve ışığa duyarlı olan metalik bir alaşımdan oluşmaktadır."
    ],
    middles: [
        "Vakıf personeli tarafından yapılan incelemelerde, nesnenin kökeninin antik Sümer metinlerine dayandığı tespit edilmiştir.",
        "Prototip S-12 cihazı ile yapılan ölçümler, nesnenin içindeki enerjinin termodinamik yasalarına aykırı olduğunu kanıtlar.",
        "Nesne, her 48 saatte bir düşük frekanslı bir sinyal yayarak yakındaki elektronik cihazları devre dışı bırakmaktadır.",
        "Sınıflandırma süreci boyunca 3 D-Sınıfı personel, nesnenin halüsinatif etkileri nedeniyle hayatını kaybetmiştir.",
        "Gözlem odasındaki kameralar, nesnenin hiçbir müdahale olmadan konum değiştirdiğini defalarca kaydetmiştir."
    ],
    ends: [
        "Personelin koruyucu ekipman olmadan nesneye 2 metreden fazla yaklaşması kesinlikle yasaktır.",
        "Nesnenin muhafaza edildiği oda, her gün sıvı azot ile soğutulmalı ve basınç dengelenmelidir.",
        "Olası bir muhafaza ihlali durumunda, Tesis-19 derhal karantinaya alınmalı ve nükleer imha prosedürü başlatılmalıdır.",
        "Varlıkla etkileşime giren personelin, 2 haftalık zorunlu psikolojik rehabilitasyon sürecinden geçmesi gerekir.",
        "Veriler henüz yetersiz olduğu için, nesnenin tam potansiyeli hala bir araştırma konusudur."
    ],
    locations: [
        "Tesis-19, Gizli Yeraltı Kanadı - Kat 4",
        "Sektör-07, Yüksek Güvenlikli Kasa",
        "Tesis-104, Biyolojik Tehlike Alanı",
        "Site-Shadow, Derin Dondurucu Ünitesi",
        "Tesis-81, Gözlem Odası B-12",
        "Site-17, İnsan-dışı Varlıklar Bölümü",
        "Sektör-4, Radyoaktif İzole Alanı"
    ]
};

function generateScp(id) {
    const sClass = classes[Math.floor(Math.random() * classes.length)];
    const start = bioParts.starts[Math.floor(Math.random() * bioParts.starts.length)];
    const middle = bioParts.middles[Math.floor(Math.random() * bioParts.middles.length)];
    const end = bioParts.ends[Math.floor(Math.random() * bioParts.ends.length)];
    const loc = bioParts.locations[Math.floor(Math.random() * bioParts.locations.length)];

    return {
        id: `SCP-${id.toString().padStart(3, '0')}`,
        class: sClass,
        bio: `${start} ${middle} ${end}`,
        location: loc
    };
}

// 1000+ Veriyi Render Etme (Hız için DocumentFragment kullanımı)
const app = document.getElementById('app');
const fragment = document.createDocumentFragment();

for (let i = 1; i <= 1050; i++) {
    const scp = generateScp(i);
    const card = document.createElement('div');
    card.className = 'scp-card';
    
    card.innerHTML = `
        <div class="scp-id">${scp.id}</div>
        <div class="scp-class">Sınıflandırma: ${scp.class}</div>
        <div class="scp-bio">
            <strong>Biyografi:</strong><br>
            ${scp.bio}
        </div>
        <div class="scp-location"><strong>Konum:</strong> ${scp.location}</div>
    `;
    fragment.appendChild(card);
}

// Yükleme ekranını temizle ve içeriği bas
setTimeout(() => {
    app.innerHTML = '';
    app.appendChild(fragment);
}, 1500);

</script>

</body>
</html>

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
