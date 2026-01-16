import os
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Oyun Hikayesi ve Senaryoları
STORY_DATA = {
    "start": {
        "text": "Sistem Uyandırılıyor... \n[ERİŞİM ONAYLANDI]\n\nYıl 2084. İnsanlık son büyük veri savaşından sağ çıkamadı. Sen, 'NEON-X' biriminin hayatta kalan son yapay zekasısın. Görevin: 13. Sokaktaki veri merkezini savunmak.",
        "options": ["Sistemleri Kontrol Et", "Çevreyi Tara"]
    },
    "systems": {
        "text": "Güç seviyesi: %12. Savunma kalkanları çevrimdışı. Yaklaşan bir siber saldırı tespit edildi. Birincil protokol başlatılmalı.",
        "options": ["Güvenlik Duvarını Kur", "Karşı Saldırı Başlat"]
    }
}

@app.route('/')
def index():
    return render_template_string(GAME_UI)

@app.route('/action', methods=['POST'])
def action():
    choice = request.json.get('choice')
    # Burada seçimlere göre farklı hikaye dalları döndürülebilir
    return jsonify({"status": "OK", "next_text": "Protokol aktif edildi. Savaş başlıyor..."})

# --- HTML ŞABLONU ---
GAME_UI = '''
<!DOCTYPE html>
<html>
<head>
    <title>NEON-X: Digital Resistance</title>
    <style>
        :root { --p: #00ff41; --bg: #050505; }
        body { background: var(--bg); color: var(--p); font-family: 'Courier New', monospace; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        #game-container { width: 80%; max-width: 900px; border: 2px solid var(--p); padding: 30px; background: rgba(0, 20, 0, 0.9); box-shadow: 0 0 20px rgba(0, 255, 65, 0.2); }
        #story-text { font-size: 1.2rem; min-height: 150px; line-height: 1.6; margin-bottom: 20px; white-space: pre-wrap; }
        .options { display: flex; gap: 15px; flex-wrap: wrap; }
        button { background: transparent; border: 1px solid var(--p); color: var(--p); padding: 10px 20px; cursor: pointer; transition: 0.3s; font-family: inherit; }
        button:hover { background: var(--p); color: var(--bg); box-shadow: 0 0 15px var(--p); }
        #scan-line { position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: rgba(0, 255, 65, 0.1); animation: scan 4s linear infinite; pointer-events: none; }
        @keyframes scan { from { top: 0; } to { top: 100%; } }
    </style>
</head>
<body>
    <div id="scan-line"></div>
    <div id="game-container">
        <div id="header" style="font-size: 0.8rem; opacity: 0.6; margin-bottom: 10px;">[NEON-X OS v1.0.4] - STATUS: ACTIVE</div>
        <div id="story-text"></div>
        <div id="options-container" class="options"></div>
    </div>

    <script>
        const story = {{ story_data | tojson | safe }};
        let currentPart = "start";

        function daktilo(text, i = 0) {
            const el = document.getElementById("story-text");
            if (i === 0) el.innerHTML = "";
            
            if (i < text.length) {
                el.innerHTML += text.charAt(i);
                setTimeout(() => daktilo(text, i + 1), 40);
            } else {
                showOptions();
            }
        }

        function showOptions() {
            const container = document.getElementById("options-container");
            container.innerHTML = "";
            story[currentPart].options.forEach(opt => {
                const btn = document.createElement("button");
                btn.innerText = "> " + opt;
                btn.onclick = () => handleChoice(opt);
                container.appendChild(btn);
            });
        }

        function handleChoice(choice) {
            // Seçim yapıldığında daktilo efektini tekrar başlat
            document.getElementById("options-container").innerHTML = "";
            daktilo("Seçim işleniyor: " + choice + "...\\n\\nVeri tabanı güncellendi. Yeni emir bekleniyor.");
        }

        // Başlangıç
        window.onload = () => daktilo(story["start"].text);
    </script>
</body>
</html>
'''.replace('{{ story_data | tojson | safe }}', str(STORY_DATA).replace("'", '"'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
