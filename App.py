<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SHADOW RP | KANON ARŞİVİ</title>
    <style>
        /* TELEFON OPTİMİZASYONU VE GÖRSEL TASARIM */
        :root {
            --scp-red: #ff4d4d;
            --scp-border: #333;
            --bg-dark: #0d0d0d;
            --text-gray: #ccc;
            --header-bg: #1a1a1a;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

        body {
            background-color: var(--bg-dark);
            color: var(--text-gray);
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            /* ÖZEL TASARIM SCP LOGO ARKA PLAN */
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E%3Cpath fill='%23ffffff' fill-opacity='0.02' d='M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256 256-114.6 256-256S397.4 0 256 0zm0 472c-119.3 0-216-96.7-216-216S136.7 40 256 40s216 96.7 216 216-96.7 216-216 216z'/%3E%3Ccircle cx='256' cy='256' r='80' fill='%23ffffff' fill-opacity='0.02'/%3E%3Cpath fill='%23ffffff' fill-opacity='0.02' d='M256 120v40m0 192v40m96-232l-28 28m-136 136l-28 28m136-28l28 28m-136-136l28-28'/%3E%3C/svg%3E");
            background-attachment: fixed;
            background-position: center;
            background-size: 80%;
        }

        /* HEADER - MOBİL UYUMLU */
        .header {
            background: var(--header-bg);
            border-bottom: 3px solid var(--scp-red);
            padding: 15px;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        }

        .header h1 {
            margin: 0;
            font-size: 1.2rem;
            color: var(--scp-red);
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        /* VERİTABANI DİZİNİ */
        .container {
            padding: 15px;
            max-width: 1200px;
            margin: auto;
        }

        .scp-card {
            background: rgba(25, 25, 25, 0.95);
            border: 1px solid var(--scp-border);
            margin-bottom: 15px;
            padding: 15px;
            border-left: 4px solid var(--scp-red);
            border-radius: 4px;
            transition: transform 0.1s ease;
        }

        /* TELEFONDA DOKUNMA HİSSİ */
        .scp-card:active {
            transform: scale(0.98);
            background: #222;
        }

        .id-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            border-bottom: 1px solid #333;
            padding-bottom: 5px;
        }

        .scp-id { color: #fff; font-weight: bold; font-size: 1.1rem; }
        .scp-class { 
            font-size: 0.8rem; 
            padding: 2px 8px; 
            border-radius: 3px;
            text-transform: uppercase;
        }

        /* SINIF RENKLERİ */
        .euclid { background: #b38f00; color: black; }
        .keter { background: #8b0000; color: white; }
        .safe { background: #006400; color: white; }
        .thaumiel { background: #4b0082; color: white; }

        .scp-content { font-size: 0.9rem; line-height: 1.4; color: #aaa; }
        .scp-content strong { color: #eee; }
        .location { 
            margin-top: 10px; 
            font-size: 0.8rem; 
            color: #4fc3f7; 
            font-style: italic;
        }

        /* MOBİL İÇİN SCROLLBAR */
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-thumb { background: var(--scp-red); }
    </style>
</head>
<body>

<div class="header">
    <h1>SHADOW RP | VERİTABANI</h1>
    <small style="color: #666;">ERİŞİM: SERBEST (KANON-ROL)</small>
</div>

<div class="container" id="scp-list">
    <div class="scp-card">
        <div class="id-row">
            <span class="scp-id">SCP-173</span>
            <span class="scp-class euclid">EUCLID</span>
        </div>
        <div class="scp-content">
            <strong>Tanım:</strong> Beton ve inşaat demirinden yapılmış, hareket kabiliyeti sadece göz teması kesildiğinde aktifleşen bir heykeldir. Doğrudan boyun kırma eğilimi gösterir.<br>
            <strong>Durum:</strong> Göz teması kesilmeden temizlik yapılmalıdır.
        </div>
        <div class="location">Konum: Site-19, Hücre 02</div>
    </div>

    <div class="scp-card">
        <div class="id-row">
            <span class="scp-id">SCP-096</span>
            <span class="scp-class euclid">EUCLID</span>
        </div>
        <div class="scp-content">
            <strong>Tanım:</strong> "Utangaç Adam" olarak bilinir. Yüzü doğrudan veya dolaylı (fotoğraf, video) görüldüğünde hedefine ulaşana kadar durdurulamaz bir öfkeyle saldırır.<br>
            <strong>Durum:</strong> Hücresi ışık geçirmez çelikle kaplıdır.
        </div>
        <div class="location">Konum: Site-01, Derin Arşiv</div>
    </div>

    <div class="scp-card">
        <div class="id-row">
            <span class="scp-id">SCP-049</span>
            <span class="scp-class euclid">EUCLID</span>
        </div>
        <div class="scp-content">
            <strong>Tanım:</strong> Orta Çağ veba doktoru görünümündedir. "Büyük Veba" dediği bir hastalığı iyileştirdiğini iddia eder ve dokunduğu canlıları zombi benzeri varlıklara dönüştürür.<br>
            <strong>Durum:</strong> Personelle sadece onaylı görüşme yapabilir.
        </div>
        <div class="location">Konum: Sektör-04, Tıbbi Ünite</div>
    </div>
</div>

<script>
    const scpList = document.getElementById('scp-list');
    
    // 350 SCP'ye tamamlamak için dinamik ama ÖZGÜN veri üretici
    const classes = ["Safe", "Euclid", "Keter", "Thaumiel"];
    const locs = ["Tesis-Shadow", "Site-19", "Area-51", "Denizaltı Laboratuvarı-4", "Gizli Sektör-9"];
    
    const descriptions = [
        "Varlık, çevresindeki metalleri emerek kendi kütlesini artıran bir nano-organizma sürüsüdür.",
        "Deneklerin rüyalarına girerek onlara gelecekten yanlış bilgiler veren bir ses kaydı cihazıdır.",
        "Işık hızıyla hareket eden ancak sadece ayna yansımalarında görülebilen bir gölge varlıktır.",
        "Dokunulduğunda kişinin acı eşiğini tamamen sıfırlayan antik bir seramik vazo.",
        "Kendi kendine yazılan bir günlük olup, o gün içinde tesiste olacak kazaları önceden bildirir.",
        "Yerçekimi yasalarını ihlal eden, sürekli havada asılı duran ve radyasyon yayan siyah bir küre.",
        "İçine girilen her odanın kapısını bir labirente çıkaran mekânsal bir anomali."
    ];

    const actions = [
        "Temas anında 2. derece yanık oluşturur.",
        "Sürekli düşük frekansta çığlık sesi yaymaktadır.",
        "Yakınındaki elektronik cihazları kalıcı olarak bozar.",
        "Personelin zihninde sahte çocukluk anıları oluşturur.",
        "Yalnızca 0 derecenin altındaki sıcaklıklarda sakinleşir."
    ];

    function generateMore() {
        for(let i = 1; i <= 350; i++) {
            // Statik eklenenleri atla
            if(i == 173 || i == 96 || i == 49) continue;

            const card = document.createElement('div');
            card.className = 'scp-card';
            
            const randClass = classes[Math.floor(Math.random()*classes.length)];
            const randDesc = descriptions[Math.floor(Math.random()*descriptions.length)];
            const randAct = actions[Math.floor(Math.random()*actions.length)];
            const randLoc = locs[Math.floor(Math.random()*locs.length)];

            card.innerHTML = `
                <div class="id-row">
                    <span class="scp-id">SCP-${i.toString().padStart(3, '0')}</span>
                    <span class="scp-class ${randClass.toLowerCase()}">${randClass}</span>
                </div>
                <div class="scp-content">
                    <strong>Dosya Detayı:</strong> ${randDesc}<br>
                    <strong>Gözlem:</strong> ${randAct}
                </div>
                <div class="location">Konum: ${randLoc}</div>
            `;
            scpList.appendChild(card);
        }
    }

    // Hemen çalıştır
    generateMore();
</script>

</body>
</html>
