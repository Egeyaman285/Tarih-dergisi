import os
import random
from flask import Flask, render_template_string

app = Flask(__name__)

# === OYUN VERİLERİ ===
BUILDINGS_DATA = []
for i in range(1, 101):
    BUILDINGS_DATA.append({
        "id": i,
        "x": i * 400 + 500, # Binalar arası mesafe
        "height": random.randint(300, 600),
        "accessible": i % 2 == 0,
        "color": "#1a1a1a" if i != 53 else "#4a0000" # Görev binası farklı renk
    })

@app.route('/')
def index():
    return render_template_string(GAME_TEMPLATE, buildings=BUILDINGS_DATA)

# === OYUN ŞABLONU ===
GAME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>GGI PROTOKOL: NEON-X</title>
    <style>
        :root { --p: #00ff41; --bg: #000; --danger: #ff003c; }
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: #000; }
        
        /* Başlangıç Ekranı */
        #start-screen {
            position: fixed; inset: 0; background: #000; z-index: 1000;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            color: var(--p); text-align: center; font-family: 'Courier New', monospace;
        }
        #protocol-title { font-size: 50px; text-shadow: 0 0 20px var(--p); margin-bottom: 20px; border: 2px solid var(--p); padding: 20px; }
        #mission-brief { width: 600px; min-height: 100px; font-size: 18px; margin-bottom: 40px; }
        .start-btn { 
            background: transparent; border: 1px solid var(--p); color: var(--p); 
            padding: 15px 40px; font-size: 20px; cursor: pointer; transition: 0.3s;
        }
        .start-btn:hover { background: var(--p); color: #000; box-shadow: 0 0 20px var(--p); }

        /* Oyun Alanı */
        canvas { display: block; }
        #ui { 
            position: absolute; top: 20px; left: 20px; z-index: 100; 
            font-family: 'Courier New', monospace; color: var(--p); pointer-events: none;
        }
        .hud-box { background: rgba(0,20,0,0.8); border: 1px solid var(--p); padding: 10px; margin-bottom: 10px; }
    </style>
</head>
<body>

    <div id="start-screen">
        <div id="protocol-title">GGİ PROTOKOL v3.0</div>
        <div id="mission-brief"></div>
        <button class="start-btn" id="start-btn" style="display:none">SİSTEMİ BAŞLAT</button>
    </div>

    <div id="ui">
        <div class="hud-box">
            BİRİM: NEON-X [AKTİF]<br>
            KONUM: <span id="ui-street">1. Sokak</span><br>
            HEDEF: 13. SOKAK NO:53
        </div>
        <div class="hud-box" id="interaction-msg" style="color:var(--danger); display:none;">
            [E] BİNAYA SIZ / DİRENİŞİ KIR
        </div>
    </div>

    <canvas id="gameCanvas"></canvas>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const startScreen = document.getElementById('start-screen');
        const briefBox = document.getElementById('mission-brief');
        const startBtn = document.getElementById('start-btn');

        // --- HİKAYE DAKTİLO ---
        const briefText = "EMİR: 13. Sokak'taki insan direnişini imha et. Kuantum çekirdeğini koru. Merhamet protokolü devre dışı bırakıldı. Başarı tek seçenek.";
        let charIdx = 0;
        function typeBrief() {
            if(charIdx < briefText.length) {
                briefBox.textContent += briefText.charAt(charIdx);
                charIdx++;
                setTimeout(typeBrief, 50);
            } else {
                startBtn.style.display = "block";
            }
        }

        // --- OYUN AYARLARI ---
        const buildings = {{ buildings|tojson }};
        const world = { width: 50000, height: canvas.height, gravity: 0.8 };
        const player = {
            x: 100, y: 500, width: 40, height: 64,
            velX: 0, velY: 0, speed: 7, jumpPower: -18,
            grounded: false, color: "#00ff41"
        };
        const camera = { x: 0 };
        const keys = {};

        // --- ÇİZİM VE FİZİK ---
        function init() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            typeBrief();
        }

        startBtn.onclick = () => {
            startScreen.style.display = "none";
            gameLoop();
        };

        window.addEventListener('keydown', e => keys[e.code] = true);
        window.addEventListener('keyup', e => keys[e.code] = false);

        function update() {
            // Hareket
            if (keys['KeyD']) player.velX = player.speed;
            else if (keys['KeyA']) player.velX = -player.speed;
            else player.velX *= 0.8;

            // Zıplama (Mario Tarzı)
            if (keys['Space'] && player.grounded) {
                player.velY = player.jumpPower;
                player.grounded = false;
            }

            player.velY += world.gravity;
            player.x += player.velX;
            player.y += player.velY;

            // Zemin Kontrolü
            const groundY = canvas.height - 100;
            if (player.y + player.height > groundY) {
                player.y = groundY - player.height;
                player.velY = 0;
                player.grounded = true;
            }

            // Kamera Takibi
            camera.x = player.x - canvas.width / 3;
            
            // Etkileşim Kontrolü
            let near = false;
            buildings.forEach(b => {
                if(player.x > b.x && player.x < b.x + 200) {
                    if(b.accessible) near = true;
                }
            });
            document.getElementById('interaction-msg').style.display = near ? "block" : "none";
            document.getElementById('ui-street').textContent = Math.floor(player.x / 4000) + 1 + ". Sokak";
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Arka Plan (Derinlik Hissi için Yıldızlar)
            ctx.fillStyle = "#050505";
            ctx.fillRect(0,0, canvas.width, canvas.height);
            
            // Uzaktaki Binalar (Parallax - Yavaş hareket eder)
            ctx.fillStyle = "#0a0a0a";
            buildings.forEach(b => {
                ctx.fillRect((b.x * 0.5) - (camera.x * 0.5), canvas.height - b.height - 100, 150, b.height);
            });

            // Zemin
            ctx.fillStyle = "#111";
            ctx.fillRect(0, canvas.height - 100, canvas.width, 100);
            ctx.strokeStyle = varColor('--p');
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(0, canvas.height - 100);
            ctx.lineTo(canvas.width, canvas.height - 100);
            ctx.stroke();

            // Öndeki Binalar (Ana Katman)
            buildings.forEach(b => {
                const screenX = b.x - camera.x;
                if(screenX > -300 && screenX < canvas.width + 300) {
                    // Bina Gövdesi
                    ctx.fillStyle = b.color;
                    ctx.fillRect(screenX, canvas.height - b.height - 100, 200, b.height);
                    
                    // Bina Kontür
                    ctx.strokeStyle = b.accessible ? varColor('--p') : "#333";
                    ctx.strokeRect(screenX, canvas.height - b.height - 100, 200, b.height);

                    // Pencereler
                    ctx.fillStyle = b.accessible ? "rgba(0, 255, 65, 0.2)" : "rgba(255,0,0,0.1)";
                    for(let r=1; r<5; r++) {
                        for(let c=1; c<3; c++) {
                            ctx.fillRect(screenX + c*60, canvas.height - b.height - 100 + r*60, 30, 30);
                        }
                    }

                    // No Yazısı
                    ctx.fillStyle = "#fff";
                    ctx.font = "14px Courier";
                    ctx.fillText("NO: " + b.id, screenX + 10, canvas.height - b.height - 80);
                }
            });

            // Oyuncu (2D Karakter)
            ctx.shadowBlur = 15;
            ctx.shadowColor = player.color;
            ctx.fillStyle = player.color;
            ctx.fillRect(player.x - camera.x, player.y, player.width, player.height);
            
            // Robot Kafa/Göz Detayı
            ctx.fillStyle = "#000";
            ctx.fillRect(player.x - camera.x + 5, player.y + 10, 30, 8);
            ctx.fillStyle = "red";
            ctx.fillRect(player.x - camera.x + 10 + (player.velX * 2), player.y + 12, 10, 4);

            ctx.shadowBlur = 0;
        }

        function varColor(name) {
            return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        init();
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
