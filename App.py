import os
import random
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# ==========================================
# OYUN VERİ YÖNETİMİ VE DÜNYA OLUŞTURMA
# ==========================================

def generate_world():
    world_data = []
    # 13 Farklı Sokak (Level)
    for street_id in range(1, 14):
        buildings = []
        danger_factor = street_id * 1.2
        
        # Her sokakta 10-15 bina
        num_buildings = 12
        for i in range(num_buildings):
            global_id = (street_id - 1) * num_buildings + i + 1
            
            # 5. Bina ve çift numaralı binalar girilebilir
            is_accessible = (global_id == 5) or (global_id % 2 == 0)
            
            buildings.append({
                "id": global_id,
                "x_pos": global_id * 600,
                "height": random.randint(400, 700),
                "accessible": is_accessible,
                "locked": True if is_accessible else False,
                "has_zombies": True if global_id >= 5 else False,
                "zombie_density": int(danger_factor + random.randint(0, 3)),
                "loot": "Mühimmat" if random.random() > 0.6 else "Enerji"
            })
        
        world_data.append({
            "street_name": f"{street_id}. Sokak",
            "danger_level": street_id,
            "buildings": buildings
        })
    return world_data

WORLD_MAP = generate_world()

@app.route('/')
def index():
    # Jinja2 hatalarını önlemek için güvenli render
    return render_template_string(GAME_SOURCE, map_data=WORLD_MAP)

# ==========================================
# OYUN MOTORU: HTML5, CSS3 VE JAVASCRIPT
# ==========================================

GAME_SOURCE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>GGİ PROTOKOL: NEON-X SIZMA</title>
    <style>
        :root { 
            --neon: #00ff41; 
            --dark: #000800; 
            --danger: #ff003c; 
            --gold: #ffcc00;
        }

        body, html { 
            margin: 0; padding: 0; width: 100%; height: 100%; 
            background: #000; overflow: hidden; 
            font-family: 'Courier New', Courier, monospace;
        }

        /* --- BAŞLANGIÇ EKRANI (GGI PROTOKOL) --- */
        #loading-screen {
            position: fixed; inset: 0; background: var(--dark);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            z-index: 9999; color: var(--neon); text-align: center;
            border: 20px solid #001100;
        }

        #protocol-title {
            font-size: 4rem; text-shadow: 0 0 20px var(--neon);
            margin-bottom: 30px; letter-spacing: 15px; font-weight: 900;
        }

        #briefing-text {
            width: 70%; max-width: 800px; height: 150px;
            font-size: 1.2rem; line-height: 1.5; color: #aaffaa;
            border-left: 2px solid var(--neon); padding-left: 20px;
        }

        #btn-initialize {
            margin-top: 50px; padding: 15px 60px;
            background: transparent; border: 2px solid var(--neon);
            color: var(--neon); font-size: 1.5rem; cursor: pointer;
            display: none; transition: all 0.3s;
        }
        #btn-initialize:hover { background: var(--neon); color: #000; box-shadow: 0 0 30px var(--neon); }

        /* --- MAYMUNCUK (LOCKPICK) UI --- */
        #lockpick-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85); display: none;
            flex-direction: column; align-items: center; justify-content: center;
            z-index: 5000;
        }

        .lock-mechanism {
            width: 300px; height: 300px; border: 8px double var(--gold);
            border-radius: 50%; position: relative;
            display: flex; align-items: center; justify-content: center;
        }

        .lock-core {
            width: 50px; height: 50px; background: var(--gold);
            border-radius: 5px; box-shadow: 0 0 20px var(--gold);
        }

        .pick-indicator {
            position: absolute; width: 100%; height: 100%;
            border-radius: 50%; border: 4px solid transparent;
            border-top: 10px solid var(--neon);
            animation: spin 1s infinite linear;
        }

        @keyframes spin { 100% { transform: rotate(360deg); } }

        /* --- HUD VE UI --- */
        #game-canvas { display: block; }

        #hud {
            position: absolute; top: 20px; left: 20px; pointer-events: none;
            display: flex; flex-direction: column; gap: 10px; z-index: 1000;
        }

        .hud-panel {
            background: rgba(0, 15, 0, 0.9); border: 1px solid var(--neon);
            padding: 15px; color: var(--neon); min-width: 250px;
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
        }

        .status-bar { height: 10px; background: #111; margin-top: 5px; border: 1px solid #333; }
        .bar-fill { height: 100%; background: var(--neon); width: 100%; transition: width 0.3s; }

        .interaction-hint {
            position: fixed; bottom: 50px; left: 50%; transform: translateX(-50%);
            color: var(--danger); font-size: 1.5rem; display: none;
            text-shadow: 0 0 10px var(--danger);
        }
    </style>
</head>
<body>

    <div id="loading-screen">
        <div id="protocol-title">GGI PROTOKOL V.4</div>
        <div id="briefing-text"></div>
        <button id="btn-initialize">SİSTEMİ YÜKLE</button>
    </div>

    <div id="lockpick-overlay">
        <h2 style="color:var(--gold)">MAYMUNCUK AKTİF - BİNA SIZMASI</h2>
        <div class="lock-mechanism">
            <div class="lock-core"></div>
            <div class="pick-indicator"></div>
        </div>
        <p style="color:#fff; margin-top:20px;">KİLİDİ KIRMAK İÇİN [F] TUŞUNA HIZLICA BAS!</p>
        <div class="status-bar" style="width: 300px;"><div id="pick-progress" class="bar-fill" style="width:0%; background:var(--gold);"></div></div>
    </div>

    <div id="hud">
        <div class="hud-panel">
            <strong>BİRİM:</strong> NEON-X (OPERATÖR)<br>
            <strong>GÖREV:</strong> <span id="mission-target">13. Sokak No:53</span>
            <div class="status-bar"><div id="energy-bar" class="bar-fill"></div></div>
        </div>
        <div class="hud-panel">
            <strong>KONUM:</strong> <span id="hud-location">1. Sokak</span><br>
            <strong>TEHLİKE:</strong> <span id="hud-danger" style="color:var(--neon)">DÜŞÜK</span><br>
            <strong>MÜHİMMAT:</strong> <span id="hud-ammo">24/24</span>
        </div>
    </div>

    <div id="interaction-hint">[E] MAYMUNCUKLA SIZ</div>

    <canvas id="gameCanvas"></canvas>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const mapData = {{ map_data|tojson }};

        // --- VARLIKLAR (GÖRSELLER) ---
        const sprites = {
            player: new Image(),
            zombie: new Image()
        };
        sprites.player.src = 'https://i.ibb.co/XfXkY9p/player.png';
        sprites.zombie.src = 'https://i.ibb.co/Zz0N7h4/zombie.png';

        // --- OYUN AYARLARI ---
        let state = 'LOADING';
        let camX = 0;
        let lockpicking = false;
        let pickPower = 0;
        let currentStreetIdx = 0;

        const player = {
            x: 300, y: 0, w: 70, h: 110,
            vX: 0, vY: 0, speed: 8,
            jump: -18, grounded: false,
            energy: 100, ammo: 24
        };

        const keys = {};

        // --- DAKTİLO EFECT ---
        const storyLines = [
            "SİSTEM UYARISI: Rejim karşıtı yapay zeka birimleri 13. Sokak'a kadar yayıldı.",
            "ANALİZ: İnsan-Zombi hibritleri tüm sivil binaları işgal etmiş durumda.",
            "GÖREV: 53 numaralı binadaki ana bilgisayara sız ve temizliği başlat.",
            "KONTROL: Maymuncuğunla kapıları kır, zombileri imha et. İyi şanslar NEON-X."
        ];
        
        let line = 0, char = 0;
        function typeStory() {
            const box = document.getElementById('briefing-text');
            if (line < storyLines.length) {
                if (char < storyLines[line].length) {
                    box.innerHTML += storyLines[line][char++];
                    setTimeout(typeStory, 30);
                } else {
                    box.innerHTML += "<br>";
                    line++; char = 0;
                    setTimeout(typeStory, 500);
                }
            } else {
                document.getElementById('btn-initialize').style.display = 'block';
            }
        }

        // --- BAŞLATMA ---
        document.getElementById('btn-initialize').onclick = () => {
            document.getElementById('loading-screen').style.display = 'none';
            state = 'PLAY';
            requestAnimationFrame(gameLoop);
        };

        window.addEventListener('keydown', e => {
            keys[e.code] = true;
            if(e.code === 'KeyF' && lockpicking) {
                pickPower += 15;
                if(pickPower >= 100) successLockpick();
            }
        });
        window.addEventListener('keyup', e => keys[e.code] = false);

        // --- MAYMUNCUK MANTIĞI ---
        function startLockpick() {
            lockpicking = true;
            pickPower = 0;
            document.getElementById('lockpick-overlay').style.display = 'flex';
        }

        function successLockpick() {
            lockpicking = false;
            document.getElementById('lockpick-overlay').style.display = 'none';
            alert("SİSTEME SIZILDI: Bina güvenliği devre dışı.");
        }

        // --- MOTOR DÖNGÜSÜ ---
        function update() {
            if (state !== 'PLAY' || lockpicking) return;

            // Hareket
            if (keys['KeyD']) player.vX = player.speed;
            else if (keys['KeyA']) player.vX = -player.speed;
            else player.vX *= 0.85;

            // Zıplama
            if (keys['Space'] && player.grounded) {
                player.vY = player.jump;
                player.grounded = false;
            }

            player.vY += 0.9; // Yerçekimi
            player.x += player.vX;
            player.y += player.vY;

            // Zemin Kontrolü
            const ground = canvas.height - 120;
            if (player.y + player.h > ground) {
                player.y = ground - player.h;
                player.vY = 0;
                player.grounded = true;
            }

            camX = player.x - canvas.width / 4;

            // Bina Kontrolü
            let canEnter = false;
            mapData.forEach(street => {
                street.buildings.forEach(b => {
                    const dist = Math.abs(player.x - b.x_pos);
                    if (dist < 100 && b.accessible) {
                        canEnter = true;
                        if (keys['KeyE']) startLockpick();
                    }
                });
            });
            document.getElementById('interaction-hint').style.display = canEnter ? 'block' : 'none';

            // HUD
            currentStreetIdx = Math.min(12, Math.floor(player.x / 7500));
            document.getElementById('hud-location').textContent = (currentStreetIdx + 1) + ". Sokak";
            document.getElementById('hud-danger').style.color = currentStreetIdx > 6 ? 'var(--danger)' : 'var(--neon)';
            document.getElementById('hud-danger').textContent = currentStreetIdx > 6 ? 'YÜKSEK' : 'DÜŞÜK';
            document.getElementById('energy-bar').style.width = player.energy + "%";
            
            if(lockpicking) {
                document.getElementById('pick-progress').style.width = pickPower + "%";
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // --- ARKA PLAN (Parallax) ---
            ctx.fillStyle = '#050505';
            ctx.fillRect(0,0, canvas.width, canvas.height);

            // Zemin
            ctx.fillStyle = '#111';
            ctx.fillRect(0, canvas.height - 120, canvas.width, 120);
            ctx.strokeStyle = varColor('--neon');
            ctx.lineWidth = 2;
            ctx.strokeRect(-10, canvas.height - 120, canvas.width + 20, 5);

            // --- DÜNYA OBJELERİ ---
            mapData.forEach(street => {
                street.buildings.forEach(b => {
                    const sx = b.x_pos - camX;
                    if (sx > -400 && sx < canvas.width + 400) {
                        // Bina Çizimi
                        ctx.strokeStyle = (b.id === 53) ? varColor('--danger') : varColor('--neon');
                        ctx.strokeRect(sx, canvas.height - b.height - 120, 250, b.height);
                        
                        // İç Işıklandırma
                        ctx.fillStyle = b.accessible ? 'rgba(0, 255, 65, 0.05)' : 'rgba(255,0,0,0.05)';
                        ctx.fillRect(sx, canvas.height - b.height - 120, 250, b.height);

                        // Bina Etiketi
                        ctx.fillStyle = '#fff';
                        ctx.font = '14px Courier';
                        ctx.fillText(`NO: ${b.id}`, sx + 10, canvas.height - b.height - 130);
                        if(b.id === 53) ctx.fillText("!!! HEDEF !!!", sx + 10, canvas.height - b.height - 150);

                        // Pencereler
                        ctx.fillStyle = 'rgba(255,255,255,0.1)';
                        for(let i=0; i<3; i++) {
                            for(let j=0; j<4; j++) {
                                ctx.fillRect(sx + 30 + i*70, canvas.height - b.height - 100 + j*80, 40, 40);
                            }
                        }

                        // Zombiler (Düşmanlar)
                        if (b.has_zombies) {
                            for(let z=0; z < b.zombie_density; z++) {
                                const zX = sx + 150 + (z * 30);
                                ctx.drawImage(sprites.zombie, zX, canvas.height - 210, 60, 90);
                            }
                        }
                    }
                });
            });

            // --- OYUNCU ---
            ctx.shadowBlur = 15;
            ctx.shadowColor = varColor('--neon');
            ctx.drawImage(sprites.player, player.x - camX, player.y, player.w, player.h);
            ctx.shadowBlur = 0;
        }

        function varColor(name) {
            return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
        }

        function gameLoop() {
            update();
            draw();
            if (state === 'PLAY') requestAnimationFrame(gameLoop);
        }

        window.onload = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            typeStory();
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
    # Render veya yerel sunucu için otomatik port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
