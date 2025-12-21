from flask import Flask

app = Flask(__name__)

STYLE = """
<style>
    body {
        background-color: #f4f1ec;
        font-family: Georgia, serif;
        color: #2c2c2c;
        margin: 0;
        padding: 0;
    }
    .container {
        max-width: 900px;
        margin: 40px auto;
        background-color: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 0 15px rgba(0,0,0,0.1);
    }
    h1, h2 {
        text-align: center;
    }
    ul {
        list-style: none;
        padding: 0;
        text-align: center;
    }
    li {
        margin: 20px 0;
        font-size: 20px;
    }
    img.flag {
        width: 36px;
        vertical-align: middle;
        margin-right: 10px;
        border: 1px solid #ccc;
    }
    a {
        text-decoration: none;
        color: #7a1f1f;
        font-weight: bold;
    }
    a:hover {
        text-decoration: underline;
    }
    pre {
        white-space: pre-wrap;
        line-height: 1.6;
        font-size: 15px;
    }
</style>
"""

OSMANLI_FLAG = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Flag_of_the_Ottoman_Empire_%281840%E2%80%931922%29.svg/320px-Flag_of_the_Ottoman_Empire_%281840%E2%80%931922%29.svg.png"
GERMANY_FLAG = "https://flagcdn.com/w40/de.png"
TURKEY_FLAG = "https://flagcdn.com/w40/tr.png"

@app.route("/")
def home():
    return f"""
    {STYLE}
    <div class="container">
        <h1>📜 Tarih Dergisi</h1>
        <ul>
            <li>
                <img class="flag" src="{OSMANLI_FLAG}">
                <a href="/osmanli">Osmanlı Enflasyonu</a>
            </li>
            <li>
                <img class="flag" src="{GERMANY_FLAG}">
                <a href="/almanya">Almanya Enflasyonu</a>
            </li>
            <li>
                <img class="flag" src="{TURKEY_FLAG}">
                <a href="/turkiye">Türkiye Enflasyonu</a>
            </li>
        </ul>
    </div>
    """

@app.route("/osmanli")
def osmanli():
    return f"""
    {STYLE}
    <div class="container">
        <h2>
            <img class="flag" src="{OSMANLI_FLAG}">
            Osmanlı Enflasyonu
        </h2>
        <pre>
Osmanlı İmparatorluğu’nda enflasyon, modern anlamda tanımlanmasa da
fiyatlar genel seviyesindeki uzun süreli artışlarla kendini göstermiştir.

Enflasyonun temel nedenleri:
- Akçe tağşişi
- Sürekli savaşlar
- Artan askerî ve bürokratik harcamalar
- Amerika’dan gelen gümüş bolluğu

Devlet bütçe açıklarını kapatmak için paranın içindeki gümüş oranını düşürmüş,
bu durum halkın satın alma gücünü azaltmıştır.

Yeniçerilerin maaşlarının değer kaybetmesi isyanlara yol açmış,
devlet bu isyanları daha fazla para dağıtarak bastırmış,
bu da enflasyonu kronik hale getirmiştir.
        </pre>
        <a href="/">← Ana Sayfa</a>
    </div>
    """

@app.route("/almanya")
def almanya():
    return f"""
    {STYLE}
    <div class="container">
        <h2>
            <img class="flag" src="{GERMANY_FLAG}">
            Almanya Enflasyonu
        </h2>
        <pre>
1923 Weimar Cumhuriyeti döneminde Almanya’da hiperenflasyon yaşanmıştır.
Para neredeyse tamamen değersiz hale gelmiş,
ekonomik ve sosyal düzen çökmüştür.
        </pre>
        <a href="/">← Ana Sayfa</a>
    </div>
    """

@app.route("/turkiye")
def turkiye():
    return f"""
    {STYLE}
    <div class="container">
        <h2>
            <img class="flag" src="{TURKEY_FLAG}">
            Türkiye Enflasyonu
        </h2>
        <pre>
2018 sonrası dönemde Türkiye’de enflasyon,
kur şokları ve ekonomi politikaları nedeniyle yükselmiştir.
Sıkı para politikalarıyla düşürülmesi hedeflenmiştir.
        </pre>
        <a href="/">← Ana Sayfa</a>
    </div>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)
