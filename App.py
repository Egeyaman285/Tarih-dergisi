import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ggi-gizli-123-special'

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'ggi.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- HER ÜLKE İÇİN 15+ SATIRLIK STRATEJİK ANALİZ (KORUNDU VE GENİŞLETİLDİ) ---
def get_long_info(country_name):
    return f"""
[ERİŞİM İZNİ: YÜKSEK] - ANALİZ NESNESİ: {country_name}
-------------------------------------------------------
01. JEOPOLİTİK KONUMLANDIRMA:
{country_name}, küresel satranç tahtasında kritik bir noktadadır.
Stratejik derinliği, sınır güvenliğiyle doğrudan orantılıdır.
Bölgesel ittifakları, enerji koridorlarını kontrol eder.

02. ASKERİ VE NÜKLEER DOKTRİN:
Askeri harcamalar GSYİH içinde %4.5 paya sahiptir.
Nükleer başlık kapasitesi 'Caydırıcı Eşik' seviyesindedir.
Konvansiyonel güçler modernizasyon sürecindedir.

03. TEKNOLOJİK SİBER SAVUNMA:
Yapay zeka tabanlı savunma sistemleri aktiftir.
Siber ordusu 7/24 aktif saldırı tespiti yapar.
Kuantum şifreleme protokolleri altyapıda yüklüdür.

04. EKONOMİK MANİPÜLASYON DİRENCİ:
Yabancı sermaye akışları devlet tarafından izlenir.
Kritik hammadde yatakları millileştirilmiştir.
Dış borçlanma rasyosu sürdürülebilir limitlerdedir.

05. GELECEK PROJEKSİYONU VE RİSKLER:
2030 vizyonu tam teknolojik bağımsızlığı hedefler.
Demografik değişimler en büyük iç risk faktörüdür.
Uzay çalışmaları askeri gözlem odaklı devam eder.

VERİ ANALİZİ TAMAMLANMIŞTIR. KAYIT NO: 0x{id(country_name)}
-------------------------------------------------------
"""

COUNTRIES_DATA = []
names = ["TÜRKİYE", "ABD", "RUSYA", "ÇİN", "FRANSA", "İNGİLTERE", "HİNDİSTAN", "PAKİSTAN", "İSRAİL", "KUZEY KORE", "ALMANYA", "JAPONYA", "İRAN", "BREZİLYA", "GÜNEY AFRİKA"]
for i, name in enumerate(names, 1):
    COUNTRIES_DATA.append({"n": f"{i}. {name} STRATEJİK ANALİZİ", "info": get_long_info(name)})

HTML_SABLON = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GGİ // SİBER ARŞİV</title>
    <style>
        :root { --neon-blue: #00f2ff; --neon-red: #ff0055; --bg: #010203; --card: #050a0f; }
        body { background: var(--bg); color: #fff; font-family: 'Courier New', monospace; margin: 0; overflow-x: hidden; }
        
        /* NAV */
        .nav { background: #000; padding: 15px; border-bottom: 2px solid var(--neon-blue); display: flex; justify-content: space-between; align-items: center; box-shadow: 0 0 15px var(--neon-blue); }
        
        /* LAYOUT */
        .layout { display: grid; grid-template-columns: 320px 1fr 380px; gap: 10px; padding: 10px; }
        .panel { background: var(--card); border: 1px solid #1a2a3a; padding: 15px; border-radius: 5px; }

        /* SOL PANEL: ARAÇLAR */
        .market-box { background: #000; border-left: 3px solid #0f0; padding: 10px; margin-bottom: 10px; font-size: 12px; }
        .calc { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; margin-top: 15px; }
        .calc input { grid-column: span 4; background: #000; border: 1px solid var(--neon-blue); color: #0f0; padding: 10px; text-align: right; }
        .calc button { background: #111; border: 1px solid #333; color: #fff; padding: 10px; cursor: pointer; }
        .calc button:hover { background: var(--neon-blue); color: #000; }

        /* ORTA PANEL: ARŞİV */
        .archive-scroll { height: 80vh; overflow-y: auto; padding-right: 10px; }
        .country-card { background: #0a1118; border: 1px solid #112233; padding: 15px; margin-bottom: 15px; cursor: pointer; transition: 0.3s; position: relative; }
        .country-card:hover { border-color: var(--neon-blue); box-shadow: 0 0 10px var(--neon-blue); }
        .country-card::before { content: "DATA"; position: absolute; right: 5px; top: 5px; font-size: 8px; color: #333; }
        .text-body { display: none; white-space: pre-wrap; font-size: 12px; color: #00ff00; border-top: 1px dashed #224466; margin-top: 10px; padding-top: 10px; }
        .cursor { display: inline-block; width: 8px; height: 15px; background: #0f0; animation: blink 0.7s infinite; vertical-align: middle; }
        @keyframes blink { 50% { opacity: 0; } }

        /* SAĞ PANEL: OYUN */
        #game-container { position: relative; width: 100%; background: #000; border: 2px solid #1a2a3a; }
        canvas { display: block; margin: 0 auto; background: #000; }
        #game-ui { position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.85); display: flex; flex-direction: column; align-items: center; justify-content: center; }

        /* AYARLAR */
        #settings { position: fixed; right: -350px; top: 0; width: 320px; height: 100%; background: #000; border-left: 2px solid var(--neon-blue); z-index: 1000; transition: 0.5s; padding: 20px; }
        #settings.active { right: 0; }

        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-thumb { background: var(--neon-blue); }
    </style>
</head>
<body>

    <audio id="tick" src="https://www.soundjay.com/buttons/button-50.mp3"></audio>

    <div class="nav">
        <div style="font-size: 20px; font-weight: bold; color: var(--neon-blue); text-shadow: 0 0 10px var(--neon-blue);">
            GGİ // SYSTEM_OS
        </div>
        <div>
            <button onclick="toggleSet()" style="background:none; border:none; color:var(--neon-blue); font-size:24px; cursor:pointer;">⚙</button>
            {% if current_user.is_authenticated %}
                <a href="/logout" style="color:var(--neon-red); text-decoration:none; margin-left:15px;">[DISCONNECT]</a>
            {% else %}
                <a href="/login" class="btn" style="text-decoration:none; background:var(--neon-blue); color:#000; padding:5px 15px; border-radius:3px;">LOGIN</a>
            {% endif %}
        </div>
    </div>

    <div class="layout">
        <div class="panel">
            <h4 style="color:var(--neon-blue); margin-top:0;">FINANCE_WATCH</h4>
            <div class="market-box">USD/TRY: <span id="usd">32.45</span> <span style="color:#0f0;">↑</span></div>
            <div class="market-box">EUR/TRY: <span id="eur">35.12</span> <span style="color:#f00;">↓</span></div>
            <div class="market-box">BTC/USD: <span id="btc">67,432</span> <span style="color:#0f0;">↑</span></div>

            <h4 style="color:var(--neon-blue); margin-top:20px;">SİBER HESAP MAKİNESİ</h4>
            <div class="calc">
                <input type="text" id="display" readonly value="0">
                <button onclick="clearCalc()">C</button><button onclick="press('/')">/</button><button onclick="press('*')">*</button><button onclick="press('-')">-</button>
                <button onclick="press('7')">7</button><button onclick="press('8')">8</button><button onclick="press('9')">9</button><button onclick="press('+')">+</button>
                <button onclick="press('4')">4</button><button onclick="press('5')">5</button><button onclick="press('6')">6</button><button onclick="calculate()">=</button>
                <button onclick="press('1')">1</button><button onclick="press('2')">2</button><button onclick="press('3')">3</button><button onclick="press('0')">0</button>
            </div>
            
            <h4 style="color:var(--neon-blue); margin-top:20px;">AKTİF LİDERLER</h4>
            {% for u in leaders %}
                <div style="font-size:12px; border-bottom:1px solid #111; padding:5px;">
                    {{ loop.index }}. {{ u.username }} <span style="float:right; color:var(--neon-blue);">{{ u.score }} PX</span>
                </div>
            {% endfor %}
        </div>

        <div class="panel">
            <div style="color:#555; font-size:10px; margin-bottom:10px;">> ROOT@GGI_ARCHIVE: LIST COUNTRIES --ALL</div>
            <div class="archive-scroll">
                {% for c in countries %}
                <div class="country-card" onclick="openArchive(this, {{loop.index}})">
                    <div style="color:var(--neon-blue); font-weight:bold;">{{ c.n }}</div>
                    <div class="text-body" id="text-{{loop.index}}" data-info="{{ c.info }}"></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="panel">
            <h4 style="color:var(--neon-blue); margin-top:0;">TRAINING_PROGRAM (v2.0)</h4>
            <div id="game-container">
                <canvas id="game" width="340" height="400"></canvas>
                <div id="game-ui">
                    <h2 style="color:var(--neon-blue);">SİSTEME GİRİŞ</h2>
                    <p style="font-size:12px; text-align:center;">Engellerden kaçmak için<br>BOŞLUK veya DOKUN</p>
                    <button onclick="startGame()" class="btn" style="padding:10px 30px; font-size:16px;">BAŞLAT</button>
                </div>
            </div>
            <div style="margin-top:15px; font-size:11px; color:#444;">
                <p>> Yerçekimi: 0.65</p>
                <p>> Motor: Canvas_Render_v2</p>
                <p>> Durum: Stabil</p>
            </div>
        </div>
    </div>

    <div id="settings">
        <h2 style="color:var(--neon-blue); border-bottom:1px solid #222;">SYSTEM_INFO</h2>
        <div style="background:#111; padding:15px; border-radius:5px; margin-bottom:20px;">
            <p style="color:var(--neon-blue);">ADMIN: EGE</p>
            <p>YAŞ: 12</p>
            <p>CORE_LANG: PYTHON</p>
        </div>
        <h3 style="color:var(--neon-blue);">TEMA</h3>
        <button onclick="toggleMode()" style="width:100%; padding:10px; background:var(--neon-blue); border:none; cursor:pointer; font-weight:bold;">GECE / GÜNDÜZ</button>
        <button onclick="toggleSet()" style="width:100%; padding:10px; background:#222; color:#fff; border:none; margin-top:10px; cursor:pointer;">KAPAT</button>
    </div>

    <script>
        // --- HESAP MAKİNESİ ---
        let d = document.getElementById('display');
        function press(v) { if(d.value == '0') d.value = v; else d.value += v; }
        function clearCalc() { d.value = '0'; }
        function calculate() { try { d.value = eval(d.value); } catch { d.value = 'ERR'; } }

        // --- MARKET SİMÜLASYONU ---
        setInterval(() => {
            document.getElementById('usd').innerText = (32.4 + Math.random()*0.1).toFixed(2);
            document.getElementById('eur').innerText = (35.1 + Math.random()*0.1).toFixed(2);
        }, 3000);

        // --- ARŞİV VE DAKTİLO ---
        function openArchive(card, id) {
            const el = document.getElementById('text-' + id);
            document.getElementById('tick').play();
            if(el.style.display === 'block') {
                el.style.display = 'none';
            } else {
                el.style.display = 'block';
                if(el.innerHTML === "") {
                    const info = el.getAttribute('data-info');
                    let i = 0;
                    el.innerHTML = '<span id="inner-'+id+'"></span><span class="cursor"></span>';
                    const target = document.getElementById('inner-'+id);
                    function type() {
                        if(i < info.length) {
                            target.innerHTML += info.charAt(i);
                            i++;
                            setTimeout(type, 5);
                        }
                    }
                    type();
                }
            }
        }

        // --- OYUN MOTORU (DÜZELTİLDİ) ---
        const canvas = document.getElementById('game');
        const ctx = canvas.getContext('2d');
        let player, obstacles, score, gameActive = false, frame = 0;

        function startGame() {
            document.getElementById('game-ui').style.display = 'none';
            player = { x: 50, y: 300, w: 30, h: 30, dy: 0, jumpPower: -12 };
            obstacles = [];
            score = 0;
            gameActive = true;
            frame = 0;
            animate();
        }

        function animate() {
            if(!gameActive) return;
            ctx.clearRect(0,0,340,400);
            
            // Player
            player.dy += 0.6; // Gravity
            player.y += player.dy;
            if(player.y > 330) { player.y = 330; player.dy = 0; }
            
            ctx.fillStyle = '#00f2ff';
            ctx.shadowBlur = 10; ctx.shadowColor = '#00f2ff';
            ctx.fillRect(player.x, player.y, player.w, player.h);
            ctx.shadowBlur = 0;

            // Ground
            ctx.fillStyle = '#111';
            ctx.fillRect(0, 360, 340, 40);

            // Obstacles
            if(frame % 90 === 0) {
                obstacles.push({ x: 340, w: 20, h: 30 + Math.random()*20, s: 5 + (score/10) });
            }

            obstacles.forEach((o, index) => {
                o.x -= o.s;
                ctx.fillStyle = '#ff0055';
                ctx.fillRect(o.x, 360 - o.h, o.w, o.h);

                // Collision
                if(player.x < o.x + o.w && player.x + player.w > o.x && player.y + player.h > 360 - o.h) {
                    gameOver();
                }

                if(o.x + o.w < 0) {
                    obstacles.splice(index, 1);
                    score++;
                }
            });

            ctx.fillStyle = "#fff";
            ctx.fillText("SCORE: " + score, 10, 20);
            frame++;
            requestAnimationFrame(animate);
        }

        function gameOver() {
            gameActive = false;
            document.getElementById('game-ui').style.display = 'flex';
            document.getElementById('game-ui').innerHTML = `<h2 style="color:red">SİSTEM ÇÖKTÜ</h2><p>SKOR: ${score}</p><button onclick="startGame()" class="btn">REBOOT</button>`;
            fetch('/save', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({s:score})});
        }

        window.addEventListener('keydown', e => { if(e.code === 'Space' && player.y >= 330) player.dy = player.jumpPower; });
        canvas.addEventListener('touchstart', () => { if(player.y >= 330) player.dy = player.jumpPower; });

        function toggleSet() { document.getElementById('settings').classList.toggle('active'); }
        function toggleMode() { document.body.classList.toggle('light-mode'); }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    db.create_all()
    leaders = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template_string(HTML_SABLON, leaders=leaders, countries=COUNTRIES_DATA)

@app.route('/save', methods=['POST'])
@login_required
def save():
    s = request.json.get('s')
    if s and s > current_user.score:
        current_user.score = s
        db.session.commit()
    return '', 204

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form['u']; p = generate_password_hash(request.form['p'])
        if not User.query.filter_by(username=u).first():
            user = User(username=u, password=p); db.session.add(user); db.session.commit()
        return redirect('/login')
    return render_template_string('<body style="background:#000;color:#0f0;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace;overflow:hidden;"><div style="border:1px solid #0f0;padding:50px;box-shadow:0 0 20px #0f0;"><h2 style="text-align:center;">NEW_USER_REGISTRATION</h2><form method="post"><input name="u" placeholder="USERNAME" style="display:block;width:100%;margin:10px 0;background:#000;border:1px solid #0f0;color:#0f0;padding:10px;"><input name="p" type="password" placeholder="PASSWORD" style="display:block;width:100%;margin:10px 0;background:#000;border:1px solid #0f0;color:#0f0;padding:10px;"><button style="width:100%;background:#0f0;color:#000;border:none;padding:10px;font-weight:bold;cursor:pointer;">INITIALIZE</button></form></div></body>')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['u']).first()
        if u and check_password_hash(u.password, request.form['p']):
            login_user(u); return redirect('/')
    return render_template_string('<body style="background:#000;color:#00f2ff;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace;overflow:hidden;"><div style="border:1px solid #00f2ff;padding:50px;box-shadow:0 0 20px #00f2ff;"><h2 style="text-align:center;">SYSTEM_LOGIN</h2><form method="post"><input name="u" placeholder="USERNAME" style="display:block;width:100%;margin:10px 0;background:#000;border:1px solid #00f2ff;color:#00f2ff;padding:10px;"><input name="p" type="password" placeholder="PASSWORD" style="display:block;width:100%;margin:10px 0;background:#000;border:1px solid #00f2ff;color:#00f2ff;padding:10px;"><button style="width:100%;background:#00f2ff;color:#000;border:none;padding:10px;font-weight:bold;cursor:pointer;">ACCESS_SYSTEM</button></form></div></body>')

@app.route('/logout')
def logout():
    logout_user(); return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
