# ==========================================
# SHADOW RP | KANONROL MERKEZI VERITABANI
# ACCESS CODE: ERISIM-KABUL-S1
# PORT CONFIG: 10000
# ==========================================

from flask import Flask, render_template_string
import os

app = Flask(__name__)

# GÖRSEL TASARIM VE SCP VERİLERİ (900+ SATIR MANTIĞI İÇİN STATİK VERİ HAVUZU)
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SHADOW RP | SCP DB</title>
    <style>
        :root { --red: #ff0000; --green: #00ff41; --bg: #050505; --blue: #00d4ff; }
        * { box-sizing: border-box; }
        body { 
            background: var(--bg); color: #ccc; font-family: 'Courier New', monospace; margin: 0; 
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E%3Ccircle cx='256' cy='256' r='200' stroke='red' stroke-width='1' fill='none' opacity='0.05'/%3E%3Cpath d='M256 40v80M256 392v80M40 256h80M392 256h80' stroke='red' stroke-width='5' opacity='0.1'/%3E%3C/svg%3E");
            background-attachment: fixed; background-position: center;
        }
        .header { background: #000; border-bottom: 3px solid var(--red); padding: 25px; text-align: center; position: sticky; top: 0; z-index: 100; }
        .card { background: rgba(15,15,15,0.9); border: 1px solid #222; border-left: 6px solid var(--red); margin: 25px; padding: 20px; }
        .scp-id { font-size: 1.6rem; color: #fff; font-weight: bold; border-bottom: 1px solid #333; padding-bottom: 10px; }
        .scp-info { color: var(--green); margin-top: 15px; font-size: 0.95rem; line-height: 1.6; min-height: 120px; }
        .scp-loc { color: var(--blue); font-size: 0.8rem; margin-top: 15px; font-weight: bold; text-transform: uppercase; }
        .typing::after { content: "_"; animation: blink 0.7s infinite; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="header">
        <h1 style="color:var(--red); margin:0; letter-spacing: 5px;">SHADOW RP | KANONROL</h1>
        <div style="font-size:0.7rem; color:var(--blue); margin-top:10px;">SYSTEM STATUS: ONLINE | PORT: 10000 | KEY: ERISIM-KABUL-S1</div>
    </div>
    <div id="main-db"></div>

    <script>
        const db = document.getElementById('main-db');
        const bios = [
            "BİYOGRAFİ: Bu nesne, moleküler yapısı gereği çevresindeki radyasyonu emen canlı bir dokudur. Denekler üzerinde yapılan testlerde %90 oranında hücre ölümü gözlemlenmiştir. Nesneye 3 metreden fazla yaklaşmak yasaktır. Personel koruyucu kurşun levhalarla korunmalıdır.",
            "BİYOGRAFİ: Sadece aynalar ve yansıtıcı yüzeyler üzerinden hareket eden boyutsal bir parazittir. Kurbanın yansımasını ele geçirerek fiziksel dünyadaki bedenini felç eder. Muhafaza odasında hiçbir parlak yüzeye izin verilmez. Personel göz bandı kullanmalıdır.",
            "BİYOGRAFİ: Yerçekimi kurallarını ihlal eden ve dokunulduğunda zaman kaymasına sebep olan antik bir küredir. Deneklerin 1940'lı yıllara ait anılarla geri döndüğü saptanmıştır. Nesne sürekli elektromanyetik kalkanlarla izole edilmektedir.",
            "BİYOGRAFİ: Konuşan herkesin sesini kaydedip 12 saat sonra farklı bir dilde yayınlayan radyoaktif bir cihazdır. Dinleyen personelde kronik uykusuzluk ve halüsinasyonlar baş gösterir. Cihazın güç kaynağı hala keşfedilememiştir."
        ];
        const locations = ["SITE-SHADOW / SEKTÖR-09", "TESİS-19 / DERİN MAHZEN", "ALAN-102 / GİZLİ KANAT", "SİTE-01 / ARŞİV KATI"];

        for(let i=1; i<=250; i++) {
            const id = "SCP-" + i.toString().padStart(3, '0');
            const card = document.createElement('div');
            card.className = 'card';
            
            let text = (i === 173) ? "BİYOGRAFİ: Beton ve inşaat demirinden yapılmış bir heykel. Göz teması kesildiği an saldırır. Kurbanın boyun kemiğini tabanından kırarak saniyeler içinde infaz eder. Temizlikte 3 personel girmeli, ikisi göz kırpmadan izlemelidir." :
                       (i === 096) ? "BİYOGRAFİ: Yüzü görüldüğünde durdurulamaz bir öfkeye kapılan insansı varlık. Hedefini dünyanın neresinde olursa olsun bulur. Fotoğrafı veya video kaydı dahi tetikleyicidir. Çelik kasa içerisinde tutulmalıdır." :
                       bios[i % bios.length];

            card.innerHTML = `<div class="scp-id">${id}</div><div class="scp-info" id="t-${i}"></div><div class="scp-loc">KONUM: ${locations[i % 4]} / BLOK-${(i%5)+1}</div>`;
            db.appendChild(card);

            let idx = 0;
            function type() {
                if(idx < text.length) {
                    document.getElementById('t-'+i).innerHTML += text.charAt(idx);
                    idx++;
                    setTimeout(type, 15);
                }
            }

            const obs = new IntersectionObserver((e) => { if(e[0].isIntersecting) type(); });
            obs.observe(card);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)

# MAYMUNA ANLATIR GİBİ: RENDER'I ÇALIŞTIRAN PORT KODU BURASI
if __name__ == "__main__":
    # Render'da 'PORT' ismindeki ortam değişkenini alır, yoksa 10000 yapar.
    # '0.0.0.0' demek siteyi internete açmak demektir.
    name = "shadow-rp-kanonrol"
    port_val = int(os.environ.get("PORT", 10000))
    print(f"Sistem Baslatiliyor: {name} Port: {port_val}")
    app.run(host='0.0.0.0', port=port_val)
