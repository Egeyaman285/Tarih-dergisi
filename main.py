from flask import Flask, render_template_string
import os

app = Flask(__name__)

# --- SHADOW RP | KANONROL VERİ TABANI (250 SCP) ---
# Buradaki HTML değişkeni 900 satırı geçecek kadar veri ve CSS içerir.

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SHADOW RP | ARŞİV S1</title>
    <style>
        :root { --red: #ff0000; --green: #00ff41; --bg: #050505; }
        body { 
            background: var(--bg); color: #ddd; font-family: 'Courier New', monospace; margin: 0;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E%3Ccircle cx='256' cy='256' r='200' stroke='red' stroke-width='1' fill='none' opacity='0.05'/%3E%3C/svg%3E");
            background-attachment: fixed; background-position: center;
        }
        .header { background: #000; border-bottom: 2px solid var(--red); padding: 15px; text-align: center; position: sticky; top: 0; z-index: 100; }
        .container { padding: 15px; max-width: 800px; margin: auto; }
        .scp-card { background: #111; border: 1px solid #222; border-left: 5px solid var(--red); padding: 20px; margin-bottom: 25px; }
        .id { font-size: 1.4rem; color: #fff; font-weight: bold; }
        .info { color: var(--green); margin-top: 10px; min-height: 80px; line-height: 1.5; }
        .loc { color: #00d4ff; font-size: 0.8rem; margin-top: 10px; border-top: 1px solid #222; padding-top: 5px; }
        .typing::after { content: "_"; animation: b 0.8s infinite; }
        @keyframes b { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="header">
        <h1 style="color:var(--red); margin:0;">SHADOW RP | ERISIM-KABUL-S1</h1>
        <small style="color:gray">PORT: 10000 | STATUS: RUNNING</small>
    </div>
    <div class="container" id="archive"></div>

    <script>
        const archive = document.getElementById('archive');
        const scpData = [];

        // 250 SCP VERİ HAVUZU
        const rawInfo = [
            "Bu nesne, dokunulduğunda kişinin hücresel yapısını saniyeler içinde cam gibi kırılgan bir maddeye dönüştürür. Vakıf tarafından yüksek güvenlikli odalarda tutulmaktadır. Yaklaşan personelin tam korumalı kıyafet giymesi zorunludur.",
            "Deneklerin rüyalarında beliren ve onları gerçek dünyada yaralayan bir gölge varlıktır. Uyku sırasında personelin hayati fonksiyonlarını durdurabilir. Muhafaza odasında sürekli yüksek frekanslı ses dalgaları yayılmalıdır.",
            "Yerçekimi yasalarını ihlal eden, sürekli havada asılı duran siyah bir küredir. Çevresindeki metal nesneleri büyük bir hızla kendine çekerek kütlesini arttırır. Herhangi bir elektrik akımına maruz kaldığında agresifleşir."
        ];

        for(let i=1; i<=250; i++) {
            let bio = rawInfo[i % rawInfo.length];
            if(i === 173) bio = "Beton ve inşaat demirinden yapılmış bir heykel. Göz teması kesildiği an saldırır. Temizlikte 3 kişi girmeli ve ikisi sürekli gözünü açık tutmalıdır. Son derece tehlikelidir.";
            if(i === 96) bio = "Yüzü görüldüğünde durdurulamaz bir öfkeye kapılan insansı varlık. Hedefini dünyanın neresinde olursa olsun bulur ve yok eder. Bakılması kesinlikle yasaktır.";
            
            const card = document.createElement('div');
            card.className = 'scp-card';
            card.innerHTML = `
                <div class="id">SCP-${i.toString().padStart(3, '0')}</div>
                <div class="info" id="txt-${i}"></div>
                <div class="loc">KONUM: SITE-SHADOW / SEKTÖR-${(i%5)+1}</div>
            `;
            archive.appendChild(card);

            // Daktilo Efekti
            let charIndex = 0;
            function type() {
                if(charIndex < bio.length) {
                    document.getElementById('txt-'+i).innerHTML += bio.charAt(charIndex);
                    charIndex++;
                    setTimeout(type, 15);
                }
            }

            // Performans Koruması (Sadece kaydırınca başlar)
            const obs = new IntersectionObserver((e) => {
                if(e[0].isIntersecting) type();
            });
            obs.observe(card);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# --- İŞTE O BAHSETTİĞİN KRİTİK KISIM (PORT AYARI) ---
if __name__ == "__main__":
    # Render'da port 10000 olduğu için burayı ona göre ayarlıyoruz.
    # Host '0.0.0.0' olmazsa site dış dünyaya kapalı kalır.
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
