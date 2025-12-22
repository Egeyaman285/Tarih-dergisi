from flask import Flask
import os

app = Flask(__name__)

# CSS ve JavaScript Tasarımı
STYLE = """
<style>
    body {
        background-color: #f4f7f6;
        font-family: 'Times New Roman', serif;
        color: #333;
        margin: 0;
        padding: 0;
    }
    .container {
        max-width: 900px;
        margin: 30px auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 10px solid #2c3e50;
    }
    h1 { text-align: center; color: #2c3e50; font-size: 36px; border-bottom: 2px solid #eee; padding-bottom: 20px; }
    h2 { color: #c0392b; border-left: 5px solid #c0392b; padding-left: 15px; margin-bottom: 20px; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }
    .card { 
        background: #f9f9f9; 
        padding: 20px; 
        border-radius: 10px; 
        text-align: center; 
        text-decoration: none; 
        color: #2980b9; 
        font-weight: bold; 
        border: 1px solid #ddd; 
        transition: 0.3s; 
    }
    .card:hover { background: #eef; transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    img.flag { width: 60px; display: block; margin: 0 auto 10px; border-radius: 5px; box-shadow: 1px 1px 4px rgba(0,0,0,0.2); }
    .typing-text {
        font-size: 19px;
        line-height: 1.8;
        background: #fffdf9;
        padding: 25px;
        border: 1px solid #ddd;
        border-radius: 5px;
        white-space: pre-wrap;
    }
    .back-link { display: block; text-align: center; margin-top: 30px; font-size: 18px; color: #7f8c8d; text-decoration: none; }
    .back-link:hover { color: #2c3e50; }
</style>
<script>
    function typeWriter(elementId, text, speed) {
        let i = 0;
        let element = document.getElementById(elementId);
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

# Çalışan Bayrak Linkleri (FlagCDN kullanıldı)
FLAGS = {
    "OSMANLI": "https://flagcdn.com/w160/tr.png",
    "ALMANYA": "https://flagcdn.com/w160/de.png",
    "TURKIYE": "https://flagcdn.com/w160/tr.png",
    "ROMA": "https://flagcdn.com/w160/it.png",
    "MACARISTAN": "https://flagcdn.com/w160/hu.png",
    "USA": "https://flagcdn.com/w160/us.png"
}

@app.route("/")
def home():
    return f"""
    {STYLE}
    <div class="container">
        <h1>📜 Dünya Enflasyon Tarihi Arşivi</h1>
        <p style="text-align:center; font-style:italic;">Ekonomik krizlerin ve paranın eriyip bittiği tarihi dönemleri keşfedin.</p>
        <div class="grid">
            <a href="/osmanli" class="card"><img src="{FLAGS['OSMANLI']}" class="flag">Osmanlı İmparatorluğu</a>
            <a href="/almanya" class="card"><img src="{FLAGS['ALMANYA']}" class="flag">Weimar Cumhuriyeti</a>
            <a href="/turkiye" class="card"><img src="{FLAGS['TURKIYE']}" class="flag">Modern Türkiye</a>
            <a href="/roma" class="card"><img src="{FLAGS['ROMA']}" class="flag">Antik Roma</a>
            <a href="/macaristan" class="card"><img src="{FLAGS['MACARISTAN']}" class="flag">Macaristan (Dünya Rekoru)</a>
            <a href="/usa" class="card"><img src="{FLAGS['USA']}" class="flag">ABD (Büyük Buhran)</a>
        </div>
    </div>
    """

@app.route("/osmanli")
def osmanli():
    text = """Osmanlı İmparatorluğu'nda enflasyonun temelinde 'Tağşiş' politikası yatmaktadır. 
Padişahlar, savaş masraflarını karşılamak için gümüş paraların içine bakır karıştırarak değerini düşürürdü. 
1580'lerden sonra Amerika'dan gelen ucuz gümüşün Avrupa üzerinden Osmanlı'ya girmesi, fiyat devrimine ve büyük bir hayat pahalılığına yol açmıştır. 
Bu durum, 'Celali İsyanları' gibi toplumsal huzursuzlukların da en büyük tetikleyicisi olmuştur."""
    return f"""{STYLE}<div class="container"><h2>Osmanlı'da Paranın Değer Kaybı</h2><div id="t" class="typing-text"></div><a href="/" class="back-link">← Ana Sayfaya Dön</a></div><script>typeWriter("t", `{text}`, 25);</script>"""

@app.route("/almanya")
def almanya():
    text = """1923 Weimar Cumhuriyeti dönemi, paranın kağıt parçasına dönüştüğü en trajik örnektir. 
Bir somun ekmek 1922'de 160 Mark iken, 1923 sonunda 200 milyar Mark'a çıkmıştır. 
İnsanlar paraları yakarak ısınmanın, kömür almaktan daha ucuz olduğunu fark etmişlerdi. 
Çocuklar sokaklarda değersiz banknotlardan kuleler yaparak oyun oynuyor, işçiler günde üç kez maaş alıp markete koşuyordu."""
    return f"""{STYLE}<div class="container"><h2>Almanya Hiperenflasyonu (1923)</h2><div id="t" class="typing-text"></div><a href="/" class="back-link">← Ana Sayfaya Dön</a></div><script>typeWriter("t", `{text}`, 25);</script>"""

@app.route("/turkiye")
def turkiye():
    text = """Türkiye'nin enflasyon serüveni özellikle 1970'li yıllardaki petrol krizleri ve döviz darlığı ile hız kazanmıştır. 
1994 ve 2001 krizleri, Türk Lirası'nın büyük değer kayıpları yaşadığı ve enflasyonun %100'lerin üzerine çıktığı dönemler olarak tarihe geçmiştir. 
Fiyat istikrarı mücadelesi, Türkiye ekonomi tarihinin en uzun soluklu ve en önemli başlıklarından biri olmaya devam etmektedir."""
    return f"""{STYLE}<div class="container"><h2>Türkiye'nin Ekonomi Mücadelesi</h2><div id="t" class="typing-text"></div><a href="/" class="back-link">← Ana Sayfaya Dön</a></div><script>typeWriter("t", `{text}`, 25);</script>"""

@app.route("/roma")
def roma():
    text = """Antik Roma'da İmparatorlar, ordularını doyurmak için 'Denarius' adlı gümüş paranın içindeki gümüşü kademeli olarak çektiler. 
Neron döneminde gümüş olan paralar, 3. yüzyılda sadece gümüş kaplı bakırlara dönüştü. 
Fiyatlar o kadar yükseldi ki, ticaret çöktü ve halk şehirlere yemek getiremez hale geldi. 
Bu ekonomik erime, Batı Roma İmparatorluğu'nun askeri ve siyasi çöküşünü hızlandıran en büyük faktörlerden biriydi."""
    return f"""{STYLE}<div class="container"><h2>Antik Roma'nın İktisadi Çöküşü</h2><div id="t" class="typing-text"></div><a href="/" class="back-link">← Ana Sayfaya Dön</a></div><script>typeWriter("t", `{text}`, 25);</script>"""

@app.route("/macaristan")
def macaristan():
    text = """Dünya tarihinin en büyük enflasyon rekoru Macaristan'a aittir. 
1946 yılında fiyatlar her 15 saatte bir ikiye katlanıyordu. 
O kadar çok sıfırlı paralar basıldı ki, 'Pengö' birimi tamamen anlamını yitirdi. 
En yüksek banknot olan 100 Kentilyon Pengö tedavüle girdiğinde, insanlar artık parayı saymak yerine tartarak işlem yapıyordu. 
Sonunda sokaklar, değersizliği nedeniyle çöpe atılan paralarla kaplandı."""
    return f"""{STYLE}<div class="container"><h2>Macaristan: Dünya Enflasyon Rekoru</h2><div id="t" class="typing-text"></div><a href="/" class="back-link">← Ana Sayfaya Dön</a></div><script>typeWriter("t", `{text}`, 25);</script>"""

@app.route("/usa")
def usa():
    text = """ABD'de 1929'da başlayan 'Büyük Buhran', başlangıçta paranın yokluğu (deflasyon) ile bilinse de, 1970'lerdeki 'Stagflasyon' dönemi Amerikan ekonomisini derinden sarsmıştır. 
Petrol ambargosuyla birleşen yüksek enflasyon, Amerikan halkının alım gücünü ilk kez bu denli sert düşürmüştür. 
Bu krizler, ABD'nin altın standardından tamamen kopmasına ve modern karşılıksız para sistemine geçmesine neden olmuştur."""
    return f"""{STYLE}<div class="container"><h2>ABD ve Büyük Ekonomik Sarsıntılar</h2><div id="t" class="typing-text"></div><a href="/" class="back-link">← Ana Sayfaya Dön</a></div><script>typeWriter("t", `{text}`, 25);</script>"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
