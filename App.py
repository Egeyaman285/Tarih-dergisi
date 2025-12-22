from flask import Flask
import os

app = Flask(__name__)

# CSS ve JavaScript efektlerini içeren STYLE değişkeni
STYLE = """
<style>
    body {
        background-color: #d1e9ff; /* Açık Mavi Arka Plan */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2c3e50;
        margin: 0;
        padding: 0;
    }
    .container {
        max-width: 800px;
        margin: 50px auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    h1, h2 {
        text-align: center;
        color: #0056b3;
    }
    img.flag {
        width: 45px;
        height: auto;
        border-radius: 4px;
        vertical-align: middle;
        margin-right: 10px;
    }
    /* Yazı efekti için stil */
    .typing-text {
        font-size: 18px;
        line-height: 1.8;
        background: #f8f9fa;
        padding: 20px;
        border-left: 5px solid #2980b9;
        border-radius: 5px;
        min-height: 100px;
        font-family: 'Georgia', serif;
    }
    ul { list-style: none; padding: 0; }
    li { margin: 20px 0; font-size: 22px; text-align: center; }
    a { text-decoration: none; color: #2980b9; font-weight: bold; }
    .back-link { display: block; text-align: center; margin-top: 20px; }
</style>

<script>
    // Yazıları tek tek döken fonksiyon
    function typeWriter(elementId, text, speed) {
        let i = 0;
        let element = document.getElementById(elementId);
        element.innerHTML = ""; // Önce içini temizle
        
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        type();
    }
</script>
"""

OSMANLI_FLAG = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Flag_of_the_Ottoman_Empire_%281840%E2%80%931922%29.svg/320px-Flag_of_the_Ottoman_Empire_%281840%E2%80%931922%29.svg.png"
GERMANY_FLAG = "https://flagcdn.com/w80/de.png"
TURKEY_FLAG = "https://flagcdn.com/w80/tr.png"

@app.route("/")
def home():
    return f"""
    {STYLE}
    <div class="container">
        <h1>📜 Tarih Dergisi</h1>
        <ul>
            <li><img class="flag" src="{OSMANLI_FLAG}"><a href="/osmanli">Osmanlı Enflasyonu</a></li>
            <li><img class="flag" src="{GERMANY_FLAG}"><a href="/almanya">Almanya Enflasyonu</a></li>
            <li><img class="flag" src="{TURKEY_FLAG}"><a href="/turkiye">Türkiye Enflasyonu</a></li>
        </ul>
    </div>
    """

@app.route("/osmanli")
def osmanli():
    text = "Osmanlı'da fiyat artışları genellikle paranın içindeki değerli maden oranının düşürülmesi (tağşiş) ve bitmek bilmeyen savaşların getirdiği mali yükler nedeniyle oluşmuştur. 16. yüzyılda Amerika'dan gelen yoğun gümüş akışı da fiyatları sarsmıştır."
    return f"""
    {STYLE}
    <div class="container">
        <h2><img class="flag" src="{OSMANLI_FLAG}"> Osmanlı Enflasyonu</h2>
        <div id="text-target" class="typing-text"></div>
        <a href="/" class="back-link">← Ana Sayfaya Dön</a>
    </div>
    <script>typeWriter("text-target", "{text}", 40);</script>
    """

@app.route("/almanya")
def almanya():
    text = "1923 yılında Almanya'da yaşanan hiperenflasyon tarihin en uç örneklerinden biridir. Kağıt para o kadar değersizleşti ki, çocuklar banknot desteleriyle oyun oynuyor, insanlar bir somun ekmek alabilmek için el arabası dolusu para taşıyordu."
    return f"""
    {STYLE}
    <div class="container">
        <h2><img class="flag" src="{GERMANY_FLAG}"> Almanya Enflasyonu</h2>
        <div id="text-target" class="typing-text"></div>
        <a href="/" class="back-link">← Ana Sayfaya Dön</a>
    </div>
    <script>typeWriter("text-target", "{text}", 40);</script>
    """

@app.route("/turkiye")
def turkiye():
    text = "Türkiye'nin enflasyon serüveni 1970'li yıllardan günümüze kadar farklı evrelerden geçmiştir. Petrol şokları, bütçe açıkları ve kur hareketleri, Türkiye ekonomisinde fiyat istikrarı mücadelesinin temel taşlarını oluşturur."
    return f"""
    {STYLE}
    <div class="container">
        <h2><img class="flag" src="{TURKEY_FLAG}"> Türkiye Enflasyonu</h2>
        <div id="text-target" class="typing-text"></div>
        <a href="/" class="back-link">← Ana Sayfaya Dön</a>
    </div>
    <script>typeWriter("text-target", "{text}", 40);</script>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)