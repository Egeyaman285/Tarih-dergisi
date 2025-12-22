from flask import Flask
import os

app = Flask(__name__)

# CSS ve Tasarım (Yan Menü ve İçerik Alanı Dahil)
STYLE = """
<style>
    body { font-family: 'Times New Roman', serif; background-color: #f0f2f5; margin: 0; display: flex; color: #333; }
    
    /* Yan Menü (Sidebar) */
    .sidebar { width: 320px; background: #2c3e50; color: white; height: 100vh; padding: 25px; position: fixed; overflow-y: auto; box-shadow: 2px 0 10px rgba(0,0,0,0.2); }
    .sidebar h2 { border-bottom: 2px solid #34495e; padding-bottom: 10px; font-size: 22px; color: #ecf0f1; }
    
    /* Ana İçerik Alanı */
    .main-content { margin-left: 360px; padding: 40px; flex-grow: 1; display: flex; justify-content: center; }
    .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); width: 100%; max-width: 900px; }
    
    /* Kartlar ve Izgara */
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }
    .card { background: #fff; border: 1px solid #ddd; padding: 20px; border-radius: 10px; text-decoration: none; text-align: center; transition: 0.3s; color: #2c3e50; display: block; }
    .card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); border-color: #3498db; }
    .card img { width: 60px; margin-bottom: 15px; border-radius: 5px; }
    
    /* Hesap Makinesi Kutusu */
    .tool-box { background: #34495e; padding: 15px; border-radius: 8px; margin-top: 25px; border-left: 5px solid #27ae60; }
    .tool-box h4 { margin-top: 0; color: #2ecc71; }
    .tool-box input { width: 100%; padding: 10px; margin: 10px 0; border-radius: 4px; border: none; box-sizing: border-box; }
    .calc-btn { background: #27ae60; color: white; border: none; padding: 12px; width: 100%; cursor: pointer; border-radius: 4px; font-weight: bold; }
    .calc-btn:hover { background: #2ecc71; }
    
    /* Yazı ve Efektler */
    .typing-text { line-height: 1.9; font-size: 18px; background: #fffdf9; padding: 25px; border-left: 6px solid #c0392b; border-radius: 4px; white-space: pre-wrap; font-family: 'Georgia', serif; }
    .back-link { display: block; margin-top: 30px; text-align: center; color: #3498db; text-decoration: none; font-weight: bold; font-size: 18px; }
</style>

<script>
    function typeWriter(elementId, text, speed) {
        let i = 0; let el = document.getElementById(elementId);
        function type() { if (i < text.length) { el.innerHTML += text.charAt(i); i++; setTimeout(type, speed); } }
        type();
    }
    
    function hesaplaEnflasyon() {
        let para = document.getElementById('para').value;
        let oran = document.getElementById('oran').value;
        if(para && oran) {
            let sonuc = para * Math.pow((1 + oran/100), 10);
            document.getElementById('calc-result').innerHTML = "10 Yıl Sonraki Tahmini Değer: " + sonuc.toLocaleString() + " Birim";
        }
    }
</script>
"""

# Yan Menü Şablonu
def layout(content):
    sidebar = f"""
    <div class="sidebar">
        <h2>🛠️ Ekonomi Araçları</h2>
        
        <div class="tool-box">
            <h4>🧮 Enflasyon Ölçer</h4>
            <p style="font-size: 13px;">Bugünkü paranın 10 yıl sonraki alım gücü kaybını görün:</p>
            <input type="number" id="para" placeholder="Miktar (Örn: 1000)">
            <input type="number" id="oran" placeholder="Yıllık Enflasyon %">
            <button class="calc-btn" onclick="hesaplaEnflasyon()">Analiz Et</button>
            <p id="calc-result" style="margin-top:10px; font-weight:bold; font-size:14px; color: #fff;"></p>
        </div>

        <div class="tool-box" style="border-left-color: #f1c40f;">
            <h4>💵 Canlı Döviz (Simüle)</h4>
            <div style="font-size: 15px;">
                <p>🇺🇸 USD/TRY: <b>34.52</b> <span style="color:#2ecc71;">▲</span></p>
                <p>🇪🇺 EUR/TRY: <b>37.18</b> <span style="color:#e74c3c;">▼</span></p>
                <p>🇬🇧 GBP/TRY: <b>43.85</b> <span style="color:#2ecc71;">▲</span></p>
            </div>
        </div>

        <div style="margin-top: 30px; font-size: 12px; color: #95a5a6; text-align: center;">
            <p>© 2025 Tarih Dergisi Portal</p>
        </div>
    </div>
    """
    return f"{STYLE} {sidebar} <div class='main-content'>{content}</div>"

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
    content = f"""
    <div class="container">
        <h1 style="font-size: 42px;">📜 Dünya Tarih & Ekonomi Portalı</h1>
        <p style="text-align:center; font-style:italic; font-size: 18px;">Büyük imparatorlukların kuruluşundan, paranın yok oluşuna uzanan bir yolculuk.</p>
        <div class="grid">
            <a href="/osmanli" class="card"><img src="{FLAGS['OSMANLI']}"><b>Osmanlı İmparatorluğu</b><br><small>Kuruluş: 1299 | Çöküş: 1922</small></a>
            <a href="/almanya" class="card"><img src="{FLAGS['ALMANYA']}"><b>Almanya (Weimar)</b><br><small>Kuruluş: 1919 | Bitiş: 1933</small></a>
            <a href="/turkiye" class="card"><img src="{FLAGS['TURKIYE']}"><b>Türkiye Cumhuriyeti</b><br><small>Kuruluş: 1923 | Devam Ediyor</small></a>
            <a href="/roma" class="card"><img src="{FLAGS['ROMA']}"><b>Antik Roma İmparatorluğu</b><br><small>Kuruluş: M.Ö. 753</small></a>
            <a href="/macaristan" class="card"><img src="{FLAGS['MACARISTAN']}"><b>Macaristan Krallığı</b><br><small>Kuruluş: 895</small></a>
            <a href="/usa" class="card"><img src="{FLAGS['USA']}"><b>ABD (Amerikan Rüyası)</b><br><small>Kuruluş: 1776</small></a>
        </div>
    </div>
    """
    return layout(content)

@app.route("/osmanli")
def osmanli():
    text = """KURULUŞ: 1299 (Söğüt)
TARİHÇE: Bilecik ilinin Söğüt ilçesinde kurulan bir uç beyliğinden, üç kıtaya yayılan bir imparatorluğa dönüşmüştür. Fatih Sultan Mehmet ile bir dünya imparatorluğu haline gelen devlet, 6 yüzyıl boyunca dünya siyasetine yön vermiştir.

EKONOMİK ÇÖKÜŞ VE ENFLASYON: 
Osmanlı'da enflasyon denilince akla gelen ilk terim 'Tağşiş'tir. Padişahlar, savaşların ağır yüklerini karşılamak için altın ve gümüş akçelerin içine bakır ve tunç karıştırarak paranın değerini kağıt üzerinde düşürmüşlerdir. 
Bu durum, maaşlarını akçe ile alan Yeniçeriler arasında büyük isyanlara (Vaka-i Vakvakiye gibi) yol açmıştır. 
1580 yılından itibaren Amerika kıtasından Avrupa'ya gelen yoğun gümüş girişi, Osmanlı pazarlarında fiyatların bir anda 3-4 katına çıkmasına neden olmuş, bu da tarihteki ilk büyük Osmanlı ekonomik buhranını tetiklemiştir. 
Dönemin ekonomistleri bu durumu 'Fiyat Devrimi' olarak adlandırır. Osmanlı, borçlarını ödeyemeyince 1881'de ekonomik bağımsızlığını Duyun-u Umumiye'ye kaptırmıştır..."""
    
    content = f"""<div class="container"><h2>📜 Osmanlı İmparatorluğu Tarihi Arşivi</h2><div id="target" class="typing-text"></div><a href="/" class="back-link">← Ana Sayfaya Dön</a></div><script>typeWriter("target", `{text}`, 20);</script>"""
    return layout(content)

@app.route("/roma")
def roma():
    text = """KURULUŞ: M.Ö. 753 (Romulus ve Remus)
TARİHÇE: Efsaneye göre Tiber nehri kıyısında kurulan Roma, bir cumhuriyetten devasa bir imparatorluğa evrilmiştir. Akdeniz'i bir 'Roma Gölü' haline getiren bu medeniyet, hukuk ve mimaride temelleri atmıştır.

EKONOMİK ÇÖKÜŞ VE ENFLASYON: 
Roma'nın yıkılışı sadece barbar akınlarıyla değil, içeriden gelen ekonomik çürüme ile başlamıştır. 
İmparatorlar, lejyonerlerin maaşlarını ödeyebilmek için gümüş para olan 'Denarius'un saflığını sürekli bozmuşlardır. 
M.S. 200 yılında %90 gümüş içeren paralar, M.S. 270 yılına gelindiğinde sadece %2 gümüş içeriyordu. 
Halk artık devletin parasına güvenmediği için ticaret durma noktasına gelmiş, insanlar köylere kaçarak takas usulüne (feodalizmin temelleri) geri dönmüşlerdir. 
İmparator Diokletianus'un fiyatları sabitleme çabaları başarısız olmuş ve büyük Roma ekonomisi hiperenflasyon altında ezilerek tarih sahnesinden çekilmiştir..."""
    
    content = f"""<div class="container"><h2>🏛️ Antik Roma'nın İktisadi Tarihi</h2><div id="target" class="typing-text"></div><a href="/" class="back-link">← Ana Sayfaya Dön</a></div><script>typeWriter("target", `{text}`, 20);</script>"""
    return layout(content)

# Diğer ülkeler için (almanya, macaristan, usa, turkiye) yukarıdaki yapıya göre 
# rota eklemeye devam edebilirsin.

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
