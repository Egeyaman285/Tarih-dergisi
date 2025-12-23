from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def ana_sayfa():
    # Burada f-string kullanmıyoruz, böylece {} karakterleri hata vermiyor
    return """
    <html>
        <head>
            <title>Render Uygulamam</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #f4f4f4; }
                .card { background: white; padding: 20px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🚀 Uygulama Yayında!</h1>
                <p>GitHub üzerinden Render'a başarıyla bağlandın.</p>
                <p><b>Durum:</b> Çalışıyor ✅</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    # Render'ın port ayarını otomatik alması için:
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
