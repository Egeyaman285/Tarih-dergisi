import os
import random
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# === OYUN VERİLERİ VE HARİTA YAPILANDIRMASI ===
# 100 Bina, Sokaklar ve Görevler
BUILDINGS = []
for i in range(1, 101):
    street_num = (i // 15) + 1
    is_accessible = i % 2 == 0 # Sadece 50 tanesine (çift numaralılar) girilebilir
    BUILDINGS.append({
        "id": i,
        "name": f"Bina No:{i}",
        "street": street_num,
        "accessible": is_accessible,
        "x": random.randint(100, 4000), # Geniş bir harita alanı
        "y": random.randint(100, 4000),
        "has_enemy": is_accessible and random.random() > 0.7,
        "has_loot": not is_accessible or random.random() > 0.5
    })

STORY_EVENTS = [
    "SİSTEM: Birim NEON-X aktif edildi.",
    "GÖREV 1: 13. Sokak, 53 numaralı binadaki rejim karşıtı varlıkları temizle.",
    "BİLGİ: İnsan direnişçiler yapay zekaya karşı sabotaj planlıyor.",
    "GÖREV 2: Rejim sokağına git, mühimmat ve enerji (yemek) ikmali yap.",
    "KONTROLLER: [W,A,S,D] Hareket | [E] Etkileşim | [SPACE] Ateş"
]

@app.route('/')
def index():
    return render_template_string(GAME_ENGINE, buildings=BUILDINGS, story=STORY_EVENTS)

# === OYUN MOTORU (HTML/JS/CSS) ===
GAME_ENGINE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>NEON-X: REJİM MUHAFIZI</title>
    <style>
        :root { --p: #00ff41; --bg: #020502; --danger: #ff003c; }
        body { background: var(--bg); color: var(--p); font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }
        
        #game-ui { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; display: flex; flex-direction: column; padding: 15px; box-sizing: border-box; }
        #terminal { background: rgba(0, 10, 0, 0.9); border: 1px solid var(--p); padding: 10px; width: 400px; height: 180px; overflow-y: auto; font-size: 12px; }
        
        canvas { display: block; background: #000; }
        
        #hud { margin-top: auto; display: flex; justify-content: space-between; background: rgba(0,0,0,0.8); border: 1px solid var(--p); padding: 10px; pointer-events: auto; }
        .stat-val { color: #fff; font-weight: bold; }
        .scanlines { position: fixed; inset: 0; background: linear-gradient(rgba(18,16,16,0) 50%, rgba(0,0,0,0.1) 50%), linear-gradient(90deg, rgba(255,0,0,0.03), rgba(0,255,0,0.01), rgba(0,0,255,0.03)); z-index: 100; pointer-events: none; background-size: 100% 3px, 3px 100%; }
        
        #interaction-prompt { position: absolute; top: 60%; left: 50%; transform: translate(-50%, -50%); color: var(--danger); font-size: 20px; display: none; text-shadow: 0 0 10px var(--danger); }
    </style>
</head>
<body>
    <div class="scanlines"></div>
    <div id="interaction-prompt">[E] BİNAYA GİRİŞ YAP</div>
    
    <div id="game-ui">
        <div id="terminal"></div>
        <div id="hud">
            <div>BİRİM: <span class="stat-val">NEON-X</span></div>
            <div>ENERJİ: <span class="stat-val" id="hp">100</span></div>
            <div>KONUM: <span class="stat-val" id="loc">1. Sokak</span></div>
            <div>HEDEF: <span class="stat-val" id="target">Bina 53</span></div>
        </div>
    </div>

    <canvas id="screen"></canvas>

    <script>
        const canvas = document.getElementById('screen');
        const ctx = canvas.getContext('2d');
        const terminal = document.getElementById('terminal');
        const prompt = document.getElementById('interaction-prompt');
        
        // --- DATA ---
        const buildings = {{ buildings|tojson }};
        const story = {{ story|tojson }};
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // --- PLAYER / CAMERA ---
        const player = {
            x: 500, y: 500,
            width: 32, height: 48,
            speed: 6,
            hp: 100,
            ammo: 50,
            color: "#00ff41"
        };

        const camera = { x: 0, y: 0 };
        const keys = {};

        // --- HİKAYE BAŞLATICI ---
        let lineIdx = 0;
        function logToTerminal(text) {
            const div = document.createElement('div');
            div.textContent = "> " + text;
            terminal.appendChild(div);
            terminal.scrollTop = terminal.scrollHeight;
        }

        function initStory() {
            if(lineIdx < story.length) {
                logToTerminal(story[lineIdx]);
                lineIdx++;
                setTimeout(initStory, 1500);
            }
        }

        // --- KONTROLLER ---
        window.addEventListener('keydown', e => keys[e.code] = true);
        window.addEventListener('keyup', e => keys[e.code] = false);

        // --- ÇİZİM FONKSİYONLARI ---
        function drawPlayer() {
            // Karakter Gövdesi (Basit Robot Görünümü)
            ctx.shadowBlur = 10;
            ctx.shadowColor = player.color;
            ctx.fillStyle = player.color;
            ctx.fillRect(player.x - camera.x, player.y - camera.y, player.width, player.height);
            
            // Gözler (Vizör)
            ctx.fillStyle = "black";
            ctx.fillRect(player.x - camera.x + 5, player.y - camera.y + 10, 22, 5);
            ctx.shadowBlur = 0;
        }

        function drawMap() {
            buildings.forEach(b => {
                const screenX = b.x - camera.x;
                const screenY = b.y - camera.y;

                if(screenX > -200 && screenX < canvas.width + 200 && screenY > -200 && screenY < canvas.height + 200) {
                    // Bina Çizimi
                    ctx.strokeStyle = b.accessible ? varColor('--p') : "#333";
                    ctx.lineWidth = 2;
                    ctx.strokeRect(screenX, screenY, 120, 180);
                    
                    // Bina Detayları
                    ctx.fillStyle = b.accessible ? "rgba(0, 255, 65, 0.1)" : "rgba(50,50,50,0.1)";
                    ctx.fillRect(screenX, screenY, 120, 180);
                    
                    ctx.fillStyle = ctx.strokeStyle;
                    ctx.font = "10px monospace";
                    ctx.fillText(b.name, screenX + 5, screenY - 5);
                    ctx.fillText("Sokak: " + b.street, screenX + 5, screenY + 195);
                    
                    // Giriş Kapısı İşareti
                    if(b.accessible) {
                        ctx.fillStyle = varColor('--p');
                        ctx.fillRect(screenX + 45, screenY + 160, 30, 20);
                    }
                }
            });
        }

        function varColor(name) {
            return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
        }

        // --- GÜNCELLEME ---
        function update() {
            if (keys['KeyW']) player.y -= player.speed;
            if (keys['KeyS']) player.y += player.speed;
            if (keys['KeyA']) player.x -= player.speed;
            if (keys['KeyD']) player.x += player.speed;

            // Kamera takibi
            camera.x = player.x - canvas.width / 2;
            camera.y = player.y - canvas.height / 2;

            // Etkileşim Kontrolü
            let nearBuilding = false;
            buildings.forEach(b => {
                const dist = Math.hypot(player.x - b.x, player.y - b.y);
                if(dist < 150 && b.accessible) {
                    nearBuilding = true;
                    if(keys['KeyE']) {
                        if(b.id === 53) {
                            logToTerminal("KRİTİK GÖREV: Bina 53'e girildi. Hedefler imha ediliyor...");
                            player.hp -= 5;
                        } else {
                            logToTerminal(b.name + " tarandı. Rejim karşıtı unsur yok.");
                        }
                        keys['KeyE'] = false; // Spam engelleme
                    }
                }
            });
            prompt.style.display = nearBuilding ? "block" : "none";

            // HUD Güncelleme
            document.getElementById('hp').textContent = player.hp;
            const currentStreet = Math.floor(player.y / 800) + 1; // Basit sokak hesabı
            document.getElementById('loc').textContent = currentStreet + ". Sokak";
        }

        function draw() {
            ctx.fillStyle = "black";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Izgara Arka Plan
            ctx.strokeStyle = "rgba(0, 255, 65, 0.05)";
            ctx.beginPath();
            for(let i = -camera.x % 100; i < canvas.width; i += 100) {
                ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height);
            }
            for(let i = -camera.y % 100; i < canvas.height; i += 100) {
                ctx.moveTo(0, i); ctx.lineTo(canvas.width, i);
            }
            ctx.stroke();

            drawMap();
            drawPlayer();
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        window.onload = () => {
            initStory();
            loop();
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
