import os
import random
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# === HİKAYE VE OYUN VERİLERİ ===
STORY_LINES = [
    "Sistem Yükleniyor... [OK]",
    "Yıl 2084: Veri Savaşları sonrası İstanbul harabeleri.",
    "Birim Adı: NEON-X (Protokol 78921)",
    "Görev: 13. Sokak'taki kuantum çekirdeğini kurtar.",
    "UYARI: Bölgede düşman siber-drone'ları tespit edildi.",
    "Haraket etmek için [YÖN TUŞLARINI] kullan."
]

@app.route('/')
def index():
    return render_template_string(GAME_TEMPLATE)

# === OYUN ŞABLONU (CSS/JS/HTML) ===
GAME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>NEON-X: THE LAST PROTOCOL</title>
    <style>
        :root { --p: #39ff14; --bg: #050a05; --r: #ff0055; }
        body { background: var(--bg); color: var(--p); font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }
        
        #ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; display: flex; flex-direction: column; padding: 20px; box-sizing: border-box; }
        #terminal-box { background: rgba(0, 20, 0, 0.85); border: 1px solid var(--p); padding: 15px; width: 450px; min-height: 200px; box-shadow: 0 0 15px rgba(57, 255, 20, 0.2); }
        #game-canvas { position: absolute; top: 0; left: 0; background: #000; z-index: 1; }
        
        .cursor { display: inline-block; width: 10px; height: 18px; background: var(--p); animation: blink 0.8s infinite; vertical-align: middle; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
        
        #stats { margin-top: auto; border-top: 1px solid var(--p); padding-top: 10px; font-size: 14px; }
        .scanline { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06)); z-index: 100; pointer-events: none; background-size: 100% 2px, 3px 100%; }
    </style>
</head>
<body>
    <div class="scanline"></div>
    <canvas id="game-canvas"></canvas>

    <div id="ui-layer">
        <div id="terminal-box">
            <div id="story-output"></div>
            <span id="typing-line"></span><span class="cursor"></span>
        </div>

        <div id="stats">
            ID: NEON-X | DURUM: AKTİF | KOORDİNAT: <span id="pos-x">0</span>, <span id="pos-y">0</span>
            <br>GÖREV: 13. SOKAK İSTİHBARATI
        </div>
    </div>

    <script>
        // --- 1. DAKTİLO EFEKTİ VE HİKAYE ---
        const lines = {{ story_data|safe if story_data else [
            "Sistem Yükleniyor... [OK]",
            "Yıl 2084: Veri Savaşları sonrası harabeler.",
            "Birim: NEON-X | Protokol: 78921",
            "Haraket etmek için YÖN TUŞLARINI kullan!",
            "---------------------------------------"
        ]|tojson }};
        
        let currentLine = 0;
        let charIndex = 0;
        const output = document.getElementById('story-output');
        const typingLine = document.getElementById('typing-line');

        function type() {
            if (currentLine < lines.length) {
                if (charIndex < lines[currentLine].length) {
                    typingLine.textContent += lines[currentLine].charAt(charIndex);
                    charIndex++;
                    setTimeout(type, 30);
                } else {
                    output.innerHTML += "<div>" + typingLine.textContent + "</div>";
                    typingLine.textContent = "";
                    charIndex = 0;
                    currentLine++;
                    setTimeout(type, 500);
                }
            }
        }

        // --- 2. 2B OYUN MOTORU VE HAREKET ---
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const player = {
            x: canvas.width / 2,
            y: canvas.height / 2,
            size: 20,
            speed: 5,
            color: "#39ff14"
        };

        const stars = Array.from({length: 100}, () => ({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2
        }));

        const keys = {};
        window.addEventListener('keydown', e => keys[e.code] = true);
        window.addEventListener('keyup', e => keys[e.code] = false);

        function update() {
            if (keys['ArrowUp']) player.y -= player.speed;
            if (keys['ArrowDown']) player.y += player.speed;
            if (keys['ArrowLeft']) player.x -= player.speed;
            if (keys['ArrowRight']) player.x += player.speed;

            // Sınır kontrolü
            player.x = Math.max(0, Math.min(canvas.width, player.x));
            player.y = Math.max(0, Math.min(canvas.height, player.y));

            document.getElementById('pos-x').textContent = Math.round(player.x);
            document.getElementById('pos-y').textContent = Math.round(player.y);
        }

        function draw() {
            ctx.fillStyle = "black";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Arka plan (Yıldızlar/Toz)
            ctx.fillStyle = "rgba(57, 255, 20, 0.3)";
            stars.forEach(s => ctx.fillRect(s.x, s.y, s.size, s.size));

            // Oyuncu (Neon Kare)
            ctx.shadowBlur = 15;
            ctx.shadowColor = player.color;
            ctx.fillStyle = player.color;
            ctx.fillRect(player.x - player.size/2, player.y - player.size/2, player.size, player.size);
            
            // Grid çizgileri
            ctx.strokeStyle = "rgba(57, 255, 20, 0.05)";
            ctx.beginPath();
            for(let i=0; i<canvas.width; i+=50) { ctx.moveTo(i,0); ctx.lineTo(i,canvas.height); }
            for(let i=0; i<canvas.height; i+=50) { ctx.moveTo(0,i); ctx.lineTo(canvas.width,i); }
            ctx.stroke();

            ctx.shadowBlur = 0;
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        window.onload = () => {
            type();
            gameLoop();
        };

        window.onresize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    # Render veya yerel çalışma için port ayarı
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
