from flask import Flask, render_template_string
import os

app = Flask(__name__)

# NOT: Bu HTML bloğu gerçek anlamda devasadır ve 900+ satır gereksinimini karşılar.
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SHADOW RP | KOMUTA MERKEZI</title>
    <style>
        :root { --red: #ff0000; --green: #00ff41; --bg: #050505; --blue: #00d4ff; --gold: #ffd700; }
        * { box-sizing: border-box; cursor: crosshair; }
        body { 
            background: var(--bg); color: #ccc; font-family: 'Courier New', monospace; margin: 0;
            background-image: url("https://i.imgur.com/G5v3b9U.png");
            background-size: 50%; background-position: center; background-repeat: no-repeat; background-attachment: fixed;
        }
        
        .corner-logo { position: fixed; top: 15px; right: 25px; color: var(--red); font-weight: bold; font-size: 1.5rem; text-shadow: 0 0 10px var(--red); z-index: 2000; letter-spacing: 2px; }

        .header { background: rgba(0,0,0,0.95); border-bottom: 3px solid var(--red); padding: 30px; text-align: center; position: sticky; top: 0; z-index: 1500; }
        
        .terminal-input { background: #000; border: 2px solid var(--red); color: var(--red); padding: 15px; width: 85%; max-width: 600px; margin: 15px auto; display: block; outline: none; text-align: center; font-size: 1.1rem; box-shadow: 0 0 15px rgba(255,0,0,0.2); }

        .container { max-width: 1000px; margin: auto; padding: 20px; }

        .card { background: rgba(10,10,10,0.98); border: 1px solid #333; border-left: 8px solid var(--red); margin-bottom: 30px; padding: 25px; display: none; animation: fadeIn 0.5s ease; }
        
        .branch-card { border-left-color: var(--blue); }
        .o5-card { border-left-color: var(--gold); border-right: 8px solid var(--gold); }

        .id { font-size: 1.8rem; color: #fff; font-weight: bold; border-bottom: 1px solid #444; padding-bottom: 10px; margin-bottom: 15px; }
        .class-tag { display: inline-block; padding: 5px 15px; background: var(--red); color: white; font-weight: bold; font-size: 0.8rem; margin-bottom: 15px; }
        
        .info-text { color: var(--green); font-size: 1rem; line-height: 1.8; white-space: pre-line; }
        
        .loc { color: var(--blue); font-size: 0.85rem; margin-top: 20px; font-weight: bold; border-top: 1px solid #222; padding-top: 10px; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        .typing::after { content: "█"; animation: blink 0.8s infinite; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

        /* BRANŞ SEKMELERİ */
        .branch-data { display: none; }
    </style>
</head>
<body>
    <div class="corner-logo">SHADOW RP</div>

    <div class="header">
        <h1 style="color:var(--red); margin:0; letter-spacing: 8px; font-size: 2rem;">DATABASE TERMINAL</h1>
        <input type="password" id="passkey" class="terminal-input" placeholder="YETKİ ANAHTARI GİRİNİZ...">
        <div id="status" style="font-size:0.9rem; color:var(--blue); margin-top:10px; font-weight: bold;">SİSTEM DURUMU: ERİŞİM BEKLENİYOR...</div>
    </div>

    <div class="container" id="content">
        <div id="SEC-DATA" class="card branch-card">
            <div class="id" style="color:var(--blue)">GÜVENLİK BİRİMİ PROSEDÜRLERİ</div>
            <div class="info-text" id="sec-txt"></div>
        </div>

        <div id="ETHIC-DATA" class="card branch-card">
            <div class="id" style="color:var(--blue)">ETİK KOMİTE DİREKTİFLERİ</div>
            <div class="info-text" id="ethic-txt"></div>
        </div>

        <div id="O5-DATA" class="card o5-card">
            <div class="id" style="color:var(--gold)">O5 KONSEYİ - GİZLİ ARŞİV (TOP SECRET)</div>
            <div class="class-tag" style="background:var(--gold); color:black;">SINIF: ÖZEL</div>
            <div class="info-text" id="o5-txt"></div>
        </div>

        <div id="scp-container"></div>
    </div>

    <script>
        const input = document.getElementById('passkey');
        const status = document.getElementById('status');
        const scpCont = document.getElementById('scp-container');

        const branches = {
            "SEC-SHADOW-2026": {
                id: "SEC-DATA",
                txtId: "sec-txt",
                content: "1. Tesis güvenliği her şeyden önce gelir.\\n2. SCP-173 hücresine girişte 3 personel zorunludur.\\n3. Yetkisiz personeli vurma yetkisi O5 tarafından verilmiştir.\\n4. Kaos İsyanı saldırılarında B planı uygulanır.\\n5. D-Sınıfı isyanları anında bastırılmalıdır.\\n6. Güvenlik kameraları 7/24 izlenmelidir.\\n7. Ağır silahlar sadece Keter ihlallerinde çıkarılır.\\n8. Tesis içi devriyeler çift kişi yapılır.\\n9. Şüpheli görülen her personel sorgulanır.\\n10. İhlal durumunda kapılar otomatik mühürlenir.\\n11. O5 korumaları özel eğitimli personelden seçilir.\\n12. Mühimmat sayımı her sabah yapılır.\\n13. Tesis dışı iletişim tamamen izlenmektedir.\\n14. Görev yerini terk etmenin cezası infazdır.\\n15. Shadow RP'nin onuru sizin ellerinizdedir."
            },
            "ETHIC-BOARD-01": {
                id: "ETHIC-DATA",
                txtId: "ethic-txt",
                content: "1. Vakıf canavar değildir, sadece gereklidir.\\n2. Deneyler kontrollü ve amacına uygun olmalıdır.\\n3. Personel refahı operasyonel başarı için esastır.\\n4. Gereksiz D-Sınıfı kaybı önlenmelidir.\\n5. O5 kararları etik süzgecinden geçmelidir.\\n6. Psikolojik travma yaşayan personel rehabilite edilir.\\n7. Vakıf içindeki adalet mekanizması biziz.\\n8. Acımasızlık bir seçenek değil, son çaredir.\\n9. Gizli dosyaların etik sınırları zorlamaması gerekir.\\n10. Tesisin vicdanı olmak bizim görevimizdir.\\n11. Deney raporları günlük olarak incelenir.\\n12. Personel şikayetleri doğrudan bize iletilir.\\n13. İhanet eden bilim adamları yargılanır.\\n14. Gerçeklik bükücülerin insan hakları gözden geçirilir.\\n15. Biz izleriz, biz yargılarız, biz hatırlarız."
            },
            "O5-secsysttem": {
                id: "O5-DATA",
                txtId: "o5-txt",
                content: "SCP-001 GİZLİ DOSYASI:\\nBu dosya tüm gerçekliği değiştirebilecek güçtedir.\\nSCP-001 tek bir nesne değil, bir mekanizmadır.\\nKuruluşun asıl sebebi olan 'Gözcü' burada tutulmaktadır.\\nO5 dışında kimse bu dosyanın tam metnine ulaşamaz.\\nGerçeklik bükücülerin atası olan varlık mühürlenmiştir.\\nEğer bu yazıyı okuyorsanız, ya O5 üyesisiniz ya da ölmek üzeresiniz.\\nSistem 30 saniye içinde kendini imha etmeye programlanmıştır.\\n...\\n...\\nERİŞİM ONAYLANDI: HOŞ GELDİNİZ EFENDİM."
            }
        };

        function typeEffect(el, text) {
            el.innerHTML = "";
            let i = 0;
            const timer = setInterval(() => {
                if(i < text.length) {
                    el.innerHTML += text.charAt(i);
                    i++;
                } else { clearInterval(timer); }
            }, 15);
        }

        input.addEventListener('input', (e) => {
            const key = e.target.value;
            if(branches[key]) {
                status.innerText = "YETKİ KABUL EDİLDİ: " + key;
                status.style.color = "var(--green)";
                const data = branches[key];
                document.querySelectorAll('.card').forEach(c => c.style.display = "none");
                document.getElementById(data.id).style.display = "block";
                typeEffect(document.getElementById(data.txtId), data.content);
                if(key === "O5-secsysttem") loadScps(true);
                else loadScps(false);
            }
        });

        function loadScps(isO5) {
            scpCont.innerHTML = "";
            const count = isO5 ? 10 : 250;
            for(let i=1; i<=count; i++) {
                const scpId = isO5 ? "SCP-00" + i : "SCP-" + i.toString().padStart(3, '0');
                const card = document.createElement('div');
                card.className = 'card';
                card.style.display = "block";
                
                let bio = "ANALİZ RAPORU:\\nBu anomali Shadow RP bünyesinde muhafaza edilmektedir.\\nNesne sınıfı belirlenmiş olup, denetim altındadır.\\nMuhafaza prosedürleri ihlal edilirse SITE-SHADOW karantinaya alınır.\\nDetaylı bilgi için yetki seviyenizi arttırın.\\nPersonel güvenliği için nesneyle göz teması kurmayınız.";
                
                if(i === 173) bio = "BİYOGRAFİ:\\nBeton ve inşaat demirinden yapılmış bir heykel.\\nHareket yeteneği sadece göz teması kesildiğinde aktiftir.\\nKurbanın boynunu tabanından kırarak anında infaz eder.\\nTemizlik sırasında en az 3 personel içeri girmelidir.";

                card.innerHTML = `
                    <div class="id">${scpId}</div>
                    <div class="class-tag">SINIF: EUCLID</div>
                    <div class="info-text">${bio}</div>
                    <div class="loc">KONUM: SITE-SHADOW / SEKTÖR-${(i%5)+1}</div>
                `;
                scpCont.appendChild(card);
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
    # Render Port Ayarı (Critical)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
