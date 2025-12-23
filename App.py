from flask import Flask
import random
import os

app = Flask(__name__)

# ==================================================
# TÜM ÜLKELER
# ==================================================
COUNTRIES = [
    "turkiye", "abd", "cin", "rusya", "japonya", "almanya",
    "ingiltere", "fransa", "italya", "ispanya",
    "misir", "iran", "hindistan", "guney_kore",
    "brezilya", "kanada", "avustralya", "meksika",
    "pakistan", "arjantin"
]

# ==================================================
# HER ÜLKE İÇİN 50+ SATIR GERÇEK TARİH ŞABLONU
# ==================================================
BASE_50_LINES = [
    "1. Coğrafi konum ve doğal sınırlar",
    "2. İlk insan yerleşimleri",
    "3. Antik çağ toplulukları",
    "4. Tarımın başlaması",
    "5. İlk şehirleşme süreci",
    "6. Kabile ve aşiret düzeni",
    "7. Erken yönetim biçimleri",
    "8. İnanç sistemlerinin oluşumu",
    "9. Kültürel kimliğin temelleri",
    "10. Antik savaşlar",
    "11. Ticaret yollarının gelişimi",
    "12. Orta çağ siyasi yapıları",
    "13. Krallıklar ve imparatorluklar",
    "14. Feodal sistem",
    "15. Din ve devlet ilişkisi",
    "16. Büyük salgınların etkisi",
    "17. Rönesans ve reform etkileri",
    "18. Bilimsel gelişmeler",
    "19. Keşifler çağı",
    "20. Kolonyal etkiler",
    "21. Halk ayaklanmaları",
    "22. Milliyetçilik akımları",
    "23. Bağımsızlık mücadeleleri",
    "24. İlk anayasalar",
    "25. Devrimci hareketler",
    "26. Sanayi devrimi",
    "27. İşçi sınıfının doğuşu",
    "28. Sosyal hakların gelişimi",
    "29. Modern eğitim sistemi",
    "30. I. Dünya Savaşı etkileri",
    "31. II. Dünya Savaşı etkileri",
    "32. Siyasi rejim değişimleri",
    "33. Soğuk savaş dönemi",
    "34. Askeri bloklaşmalar",
    "35. Ekonomik kalkınma planları",
    "36. Teknolojik dönüşüm",
    "37. Dijital çağ",
    "38. Medya ve propaganda",
    "39. Kültürel küreselleşme",
    "40. Göç hareketleri",
    "41. Nüfus yapısındaki değişim",
    "42. Kadın hakları hareketleri",
    "43. Gençlik hareketleri",
    "44. Demokratikleşme adımları",
    "45. Anayasal reformlar",
    "46. Çevresel sorunlar",
    "47. Enerji politikaları",
    "48. Bölgesel ilişkiler",
    "49. Güncel siyasi durum",
    "50. Gelecek projeksiyonları"
]

def generate_country_text(country):
    header = f"{country.upper()} TARİHSEL GELİŞİM VE DEVRİMLER"
    lines = [header] + BASE_50_LINES
    return "\n".join(lines)

DATA = {c: generate_country_text(c) for c in COUNTRIES}

# ==================================================
# HTML + CSS + JS
# ==================================================
def layout(content, hidden_text=""):
    return f"""
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>GGI Tarih Arşivi</title>
<style>
body {{
    margin:0;
    font-family:Arial;
    display:flex;
    background:#f2f2f2;
}}
.left {{
    width:260px;
    background:#1a1a2e;
    color:white;
    padding:20px;
}}
.right {{
    width:240px;
    background:#0f3460;
    color:white;
    padding:20px;
}}
.main {{
    flex:1;
    padding:40px;
}}
.card {{
    background:#34495e;
    color:white;
    padding:15px;
    margin:10px;
    border-radius:10px;
    text-decoration:none;
    display:inline-block;
    width:160px;
    text-align:center;
}}
.card:hover {{ background:#2c3e50; }}
#text {{
    background:white;
    padding:30px;
    border-left:6px solid #e74c3c;
    min-height:300px;
    white-space:pre-wrap;
    line-height:1.7;
}}
.small {{ font-size:11px; opacity:0.8; }}
</style>

<script>
function animateLines(text) {{
    const lines = text.split("\\n");
    const target = document.getElementById("text");
    target.innerHTML = "";
    let i = 0;

    function addLine() {{
        if (i >= lines.length) return;
        const div = document.createElement("div");
        div.textContent = lines[i];
        div.style.opacity = 0;
        target.appendChild(div);
        setTimeout(() => {{
            div.style.transition = "opacity 0.4s";
            div.style.opacity = 1;
        }}, 20);
        i++;
        setTimeout(addLine, 80);
    }}
    addLine();
}}

window.onload = function() {{
    const hidden = document.getElementById("hidden");
    if (hidden) animateLines(hidden.innerText.trim());
};
</script>
</head>

<body>

<div class="left">
    <h2>GGI</h2>
    <p>Genç Girişimci v3.5</p>
    <p class="small">
    Bu site bilgilendirme amaçlıdır.<br>
    Hiçbir ülkenin, ideolojinin veya
    örgütün tarafı değildir.
    </p>
</div>

<div class="main">
{content}
<div id="hidden" style="display:none;">{hidden_text}</div>
</div>

<div class="right">
    <b>Ayarlar</b><br><br>
    Admin: Ege<br>
    Yaş: 12<br>
    Dil: Python<br>
    Altyapı: GitHub + Render
</div>

</body>
</html>
"""

# ==================================================
# ROUTES
# ==================================================
@app.route("/")
def home():
    selected = random.sample(COUNTRIES, 15)
    cards = "".join(
        f'<a class="card" href="/{c}">{c.upper()}</a>'
        for c in selected
    )
    return layout("<h1>GGI TARİH ARŞİVİ</h1>" + cards)

@app.route("/<country>")
def country(country):
    if country not in DATA:
        return home()
    content = f"""
    <h1>{country.upper()}</h1>
    <div id="text"></div>
    <br>
    <a class="card" href="/">← Geri</a>
    """
    return layout(content, DATA[country])

# ==================================================
# RUN
# ==================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
