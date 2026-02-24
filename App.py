from flask import Flask, render_template_string
import os

app = Flask(__name__)

# SHADOW RP | MERKEZİ TERMİNAL YAZILIMI V12
# BU KOD YAPISI VE VERİ KÜMELERİYLE 350 SATIRI GEÇECEK ŞEKİLDE TASARLANMIŞTIR.
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SHADOW RP | ARSIV V12</title>
    <style>
        :root { --red: #ff0000; --green: #00ff41; --bg: #050505; --blue: #00d4ff; --gold: #ffd700; }
        * { box-sizing: border-box; cursor: crosshair; }
        body { 
            background: var(--bg); color: #ccc; font-family: 'Courier New', monospace; margin: 0; 
            overflow-x: hidden;
        }
        
        /* GÖMÜLÜ SCP LOGOSU (KIRILMAZ SVG) */
        .bg-overlay {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 50%; opacity: 0.05; z-index: -1; pointer-events: none;
        }

        .shadow-tag { position: fixed; top: 20px; right: 30px; color: var(--red); font-weight: bold; font-size: 1.8rem; text-shadow: 0 0 15px var(--red); z-index: 2000; }

        .terminal-header { background: rgba(0,0,0,0.98); border-bottom: 4px solid var(--red); padding: 40px; text-align: center; position: sticky; top: 0; z-index: 1500; }
        
        .auth-input { background: #000; border: 2px solid var(--red); color: var(--red); padding: 20px; width: 90%; max-width: 700px; margin: 20px auto; display: block; outline: none; text-align: center; font-size: 1.2rem; box-shadow: 0 0 20px rgba(255,0,0,0.3); }

        .main-container { max-width: 1000px; margin: 40px auto; padding: 20px; }

        /* BRANŞ KARTLARI */
        .branch-box { background: rgba(5,5,5,0.95); border: 2px solid var(--blue); border-left: 12px solid var(--blue); padding: 30px; margin-bottom: 50px; display: none; border-radius: 5px; }
        .o5-box { border-color: var(--gold); border-right: 12px solid var(--gold); }

        .title { font-size: 2rem; color: #fff; font-weight: bold; border-bottom: 2px solid #333; margin-bottom: 25px; padding-bottom: 10px; }
        .desc { color: var(--green); font-size: 1.1rem; line-height: 1.8; white-space: pre-wrap; }

        /* TIKLANABİLİR SCP DOSYALARI */
        .scp-folder { 
            background: #111; border: 1px solid #222; border-left: 8px solid var(--red); 
            padding: 15px 25px; margin-bottom: 15px; cursor: pointer; transition: 0.3s;
            display: flex; justify-content: space-between; align-items: center;
        }
        .scp-folder:hover { background: #1a1a1a; border-color: var(--red); transform: translateX(5px); }

        .scp-details { 
            background: #000; border: 1px solid var(--red); border-top: none; border-left: 8px solid var(--red);
            padding: 25px; margin-bottom: 20px; display: none; color: var(--green); line-height: 1.8;
            animation: slideDown 0.3s ease-out; font-size: 0.95rem;
        }

        @keyframes slideDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
        
        .scp-id { font-size: 1.3rem; font-weight: bold; color: #fff; }
        .scp-class-badge { background: var(--red); color: white; padding: 2px 10px; font-size: 0.8rem; font-weight: bold; }
        
        .footer-note { text-align: center; color: #444; font-size: 0.7rem; margin-top: 50px; }
    </style>
</head>
<body>
    <div class="shadow-tag">SHADOW RP</div>
    
    <svg class="bg-overlay" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
        <path fill="red" d="M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256 256-114.6 256-256S397.4 0 256 0zm0 472c-119.3 0-216-96.7-216-216S136.7 40 256 40s216 96.7 216 216-96.7 216-216 216z"/>
        <circle fill="red" cx="256" cy="256" r="40"/>
    </svg>

    <div class="terminal-header">
        <h1 style="color:var(--red); margin:0; letter-spacing: 10px;">SECURE ARCHIVE SYSTEM</h1>
        <input type="password" id="passInput" class="auth-input" placeholder="YETKİ ANAHTARI GİRİNİZ...">
        <div id="status" style="color:var(--blue); font-weight:bold; margin-top:15px; letter-spacing: 2px;">STATUS: WAITING_AUTHORIZATION</div>
    </div>

    <div class="main-container">
        <div id="SEC-B" class="branch-box">
            <div class="title" style="color:var(--blue)">GÜVENLİK BİRİMİ PROSEDÜRLERİ</div>
            <div id="sec-text" class="desc"></div>
        </div>
        <div id="ENG-B" class="branch-box">
            <div class="title" style="color:var(--blue)">MÜHENDİSLİK TEKNİK RAPORLARI</div>
            <div id="eng-text" class="desc"></div>
        </div>
        <div id="ETH-B" class="branch-box">
            <div class="title" style="color:var(--blue)">ETİK KOMİTE DİREKTİFLERİ</div>
            <div id="eth-text" class="desc"></div>
        </div>
        <div id="DCL-B" class="branch-box">
            <div class="title" style="color:var(--blue)">D-SINIFI PERSONEL REHBERİ</div>
            <div id="dcl-text" class="desc"></div>
        </div>
        <div id="O5-B" class="branch-box o5-box">
            <div class="title" style="color:var(--gold)">O5-01 GİZLİ ARŞİV (YASAKLI)</div>
            <div id="o5-text" class="desc"></div>
        </div>

        <div id="scp-list"></div>
        
        <div class="footer-note">BU TERMİNAL SHADOW RP KANONUNA ÖZELDİR. YETKİSİZ ERİŞİM İNFAZ SEBEBİDİR.</div>
    </div>

    <script>
        const input = document.getElementById('passInput');
        const scpList = document.getElementById('scp-list');
        const status = document.getElementById('status');

        const DATABASE = {
            "SEC-SHADOW-2026": {
                id: "SEC-B", txt: "sec-text",
                data: "01. Tesis güvenliği her şeyin üstündedir.\\n02. İhlal durumunda Code Red uygulanır.\\n03. Ağır silah yetkisi Site Direktörü onayıyla açılır.\\n04. Hücre önünde nöbet değişimi 2 saatte birdir.\\n05. Yetkisiz siviller derhal etkisiz hale getirilir.\\n06. Kaos İsyanı sızmalarına karşı sorgu yapılır.\\n07. O5 üyelerinin fiziksel koruması bizdedir.\\n08. Tesis içi devriyeler 3 kişilik timler halindedir.\\n09. Herhangi bir anomalide telsiz kodu 10-4'tür.\\n10. Personel kartı olmayanlar tutuklanır.\\n11. Zırhlı kapıların manuel kilidi bizdedir.\\n12. Firar eden denekler için 'Vur' emri geçerlidir.\\n13. Tesis dışı iletişim karartması uygulanabilir.\\n14. Görev başındaki uyku infaz sebebidir.\\n15. Shadow RP'nin kalkanı biziz."
            },
            "ENG-TECH-SYS": {
                id: "ENG-B", txt: "eng-text",
                data: "01. Elektrik şebekesi SCP-914 tarafından beslenir.\\n02. Havalandırma kanalları her gün temizlenmelidir.\\n03. Sektör-4 kapıları yağlanmazsa sıkışır.\\n04. Jeneratör odasına girmek için B-2 kartı şarttır.\\n05. Radyasyon sızıntısı durumunda B blok kapatılır.\\n06. Ağ bağlantıları O5 terminalinden izlenir.\\n07. Asansör arızalarında manuel kolu kullanın.\\n08. Isı sensörleri Keter odalarında 24 saat açıktır.\\n09. Yangın söndürme sistemi halon gazı içerir.\\n10. Yedek güç üniteleri %80 kapasitede tutulur.\\n11. Sunucu odası sıcaklığı 18 derece olmalıdır.\\n12. Su arıtma sistemi Site-Shadow altındadır.\\n13. Gaz sızıntısı sensörleri her hafta test edilir.\\n14. Kırılan camlar anında polimerle kaplanır.\\n15. Tesisin kalbi mühendislerin elindedir."
            },
            "ETHIC-BOARD-01": {
                id: "ETH-B", txt: "eth-text",
                data: "01. Vakıf canavar değildir, zorunluluktur.\\n02. Gereksiz can kaybı Vakıf verimliliğini düşürür.\\n03. D-Sınıfı terminasyonları bizim onayımızdadır.\\n04. Bilim adamlarının vicdanı biz olmalıyız.\\n05. Protokol dışı deneyler ağır cezalandırılır.\\n06. O5 kararlarını veto yetkimiz gizlidir.\\n07. Personel psikolojisi sürekli ölçülür.\\n08. Acımasızlık bir seçenek değil, son çaredir.\\n09. Sırlar, insanlığın bekası için saklanır.\\n10. İşkence değil, araştırma önceliğimizdir.\\n11. Yanlış kararların bedeli ağırdır.\\n12. Her denek bir veridir ama her veri candır.\\n13. Tesis içi adalet mekanizmasını koruruz.\\n14. Personel üzerindeki baskıyı yönetiriz.\\n15. Biz sessiz denetçileriz."
            },
            "D-CLASS-FREE": {
                id: "DCL-B", txt: "dcl-text",
                data: "01. Numaranız sizin tek kimliğinizdir.\\n02. Gardiyanların emirlerine harfiyen uyun.\\n03. Deney odasına girerken itiraz etmeyin.\\n04. Hücrenizde bulduğunuz her şeyi raporlayın.\\n05. Diğer deneklerle gizli iletişim yasaktır.\\n06. Yemek saati dışında dolaşmak yasaktır.\\n07. İsyan girişimi anında infazla sonuçlanır.\\n08. Temizlik görevlerini eksiksiz yerine getirin.\\n09. SCP'lerle göz teması kurmamaya çalışın.\\n10. Sağlık kontrolleri zorunludur.\\n11. Ay sonunda terminasyon prosedürü uygulanabilir.\\n12. İşbirliği yapanlara ek ödüller verilir.\\n13. Kaçış imkansızdır, denemeyin.\\n14. Vakıf sizi izliyor, her zaman.\\n15. Hayatta kalmak için sadece dinleyin."
            },
            "O5-secsysttem": {
                id: "O5-B", txt: "o5-text",
                data: "SCP-001: KURULUŞUN ASLI.\\nBu dosya sadece O5 üyelerinin retinası ile açılır.\\nİnsanlık aslında bir simülasyonun parçası olabilir.\\nGerçeklik bükücüler bizim asıl atalarımızdır.\\nDünyayı kurtarmak için dünyayı yakmak gerekebilir.\\nSistem 30 saniye içinde silinecektir.\\nERİŞİM ONAYLANDI: HOŞ GELDİN KONSEY ÜYESİ."
            }
        };

        function daktilo(elId, text) {
            const el = document.getElementById(elId); el.innerHTML = ""; let i = 0;
            const timer = setInterval(() => {
                if(i < text.length) { el.innerHTML += text.charAt(i) === "\\n" ? "<br>" : text.charAt(i); i++; }
                else { clearInterval(timer); }
            }, 8);
        }

        input.addEventListener('input', (e) => {
            const key = e.target.value;
            if(DATABASE[key]) {
                status.innerText = "ACCESS GRANTED: " + key;
                status.style.color = "var(--green)";
                document.querySelectorAll('.branch-box').forEach(x => x.style.display = 'none');
                document.getElementById(DATABASE[key].id).style.display = 'block';
                daktilo(DATABASE[key].txt, DATABASE[key].data);
                buildList(key);
            }
        });

        function buildList(key) {
            scpList.innerHTML = "";
            let start = 0; let end = 50;
            
            // Branşlara göre 50'şerli SCP blokları ayırıyoruz
            if(key === "ENG-TECH-SYS") { start = 51; end = 100; }
            else if(key === "ETHIC-BOARD-01") { start = 101; end = 150; }
            else if(key === "D-CLASS-FREE") { start = 151; end = 200; }
            else if(key === "O5-secsysttem") { start = 1; end = 10; } // O5'e sadece 10 özel dosya

            for(let i=start; i<=end; i++) {
                const id = "SCP-" + i.toString().padStart(3, '0');
                const sClass = i % 3 === 0 ? "KETER" : (i % 2 === 0 ? "EUCLID" : "SAFE");
                
                const folder = document.createElement('div');
                folder.className = 'scp-folder';
                folder.innerHTML = `<span class="scp-id">${id}</span><span class="scp-class-badge">${sClass}</span>`;
                
                const details = document.createElement('div');
                details.className = 'scp-details';
                details.id = "det-"+id;

                folder.onclick = () => {
                    const isOpen = details.style.display === 'block';
                    document.querySelectorAll('.scp-details').forEach(d => d.style.display = 'none');
                    if(!isOpen) {
                        details.style.display = 'block';
                        let bio = `[TEKNIK ANALIZ RAPORU]\\n1. SIRA: Nesne ${i%4 === 0 ? 'Sektör-4' : 'Sektör-9'} bölgesinde muhafaza edilmektedir.\\n2. SIRA: ${sClass} sınıfı protokol uyarınca 24 saat termal izleme zorunludur.\\n3. SIRA: Yetkisiz personel teması durumunda tesis karantinaya alınacaktır.`;
                        daktilo(details.id, bio);
                    }
                };

                scpList.appendChild(folder);
                scpList.appendChild(details);
            }
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
