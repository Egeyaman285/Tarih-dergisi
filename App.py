import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# 1. UYGULAMA AYARLARI
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ggi-gizli-anahtar-123')
# Render'da veritabanının düzgün yazılması için path'i belirleyelim
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'ggi_arsiv.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 2. VERİTABANI MODELİ
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 3. HTML TASARIMI (Tek Parça)
HTML_SABLON = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>GGİ - Genç Girişimci Platformu</title>
    <style>
        body { background: #0f172a; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; }
        .nav { background: #1e293b; padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #00f2fe; }
        .logo { font-size: 28px; font-weight: bold; color: #00f2fe; text-shadow: 0 0 10px #00f2fe; }
        .container { display: flex; padding: 20px; gap: 20px; max-width: 1200px; margin: auto; }
        .game-box { flex: 2; background: #1e293b; padding: 20px; border-radius: 15px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .leaderboard { flex: 1; background: #1e293b; padding: 20px; border-radius: 15px; border: 1px solid #334155; }
        canvas { background: #000; border: 2px solid #00f2fe; border-radius: 8px; width: 100%; max-width: 600px; }
        .btn { background: #00f2fe; color: #0f172a; padding: 8px 15px; text-decoration: none; border-radius: 5px; font-weight: bold; }
        .user-info { font-size: 14px; }
        h3 { color: #00f2fe; border-bottom: 1px solid #334155; padding-bottom: 10px; }
    </style>
</head>
<body>
    <div class="nav">
        <div class="logo">GGİ</div>
        <div class="user-info">
            {% if current_user.is_authenticated %}
                <span>👤 {{ current_user.username }} | Skor: {{ current_user.score }}</span> | 
                <a href="/logout" style="color:#ff4b2b">Çıkış Yap</a>
            {% else %}
                <a href="/login" class="btn">Giriş Yap</a>
                <a href="/register" class="btn" style="background:#fff">Kayıt Ol</a>
            {% endif %}
        </div>
    </div>

    <div class="container">
        <div class="game-box">
            <h3>🎮 Araba Yarışı - Engellerden Atla</h3>
            <canvas id="gameCanvas" width="600" height="300"></canvas>
            <p style="color: #94a3b8; margin-top: 10px;">Zıplamak için <b>BOŞLUK (SPACE)</b> tuşuna bas!</p>
        </div>
        
        <div class="leaderboard">
            <h3>🏆 TOP 10 LİDERLER</h3>
            {% for u in leaders %}
                <div style="display:flex; justify-content:space-between; margin-bottom:8px; padding:5px; border-bottom:1px solid #334155">
                    <span>{{ loop.index }}. {{ u.username }}</span>
                    <span style="color:#00f2fe; font-weight:bold;">{{ u.score }}</span>
                </div>
            {% endfor %}
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        let score = 0, gameActive = true;
        let player = { x: 50, y: 240, w: 30, h: 30, dy: 0, jump: -12, grounded: false };
        let obstacles = [];

        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && player.grounded) {
                player.dy = player.jump;
                player.grounded = false;
            }
        });

        function createObs() {
            if(!gameActive) return;
            obstacles.push({ x: 650, w: 40, h: 40, speed: 5 + (score/10) });
            setTimeout(createObs, 1500 + Math.random() * 1000);
        }

        function update() {
            if (!gameActive) return;
            
            player.dy += 0.7; // Yerçekimi
            player.y += player.dy;

            if (player.y > 240) {
                player.y = 240;
                player.dy = 0;
                player.grounded = true;
            }

            obstacles.forEach((o, i) => {
                o.x -= o.speed;
                // Çarpışma Kontrolü
                if (player.x < o.x + o.w && player.x + 30 > o.x && player.y < 240 + o.h && player.y + 30 > 240) {
                    gameActive = false;
                    alert("OYUN BİTTİ! Skorun: " + score);
                    saveScore(score);
                }
                if (o.x + o.w < 0) {
                    obstacles.splice(i, 1);
                    score++;
                }
            });

            draw();
            requestAnimationFrame(update);
        }

        function draw() {
            ctx.clearRect(0, 0, 600, 300);
            // Yol
            ctx.strokeStyle = '#334155'; ctx.strokeRect(0, 270, 600, 1);
            // Oyuncu
            ctx.fillStyle = '#00f2fe'; ctx.fillRect(player.x, player.y, 30, 30);
            // Engeller
            ctx.fillStyle = '#f43f5e'; obstacles.forEach(o => ctx.fillRect(o.x, 240, o.w, o.h));
            // Skor
            ctx.fillStyle = 'white'; ctx.font = '20px Arial'; ctx.fillText("Puan: " + score, 20, 30);
        }

        function saveScore(s) {
            fetch('/save-score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ score: s })
            }).then(() => location.reload());
        }

        createObs();
        update();
    </script>
</body>
</html>
"""

# 4. YOLLAR (ROUTES)
@app.route('/')
def index():
    leaders = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template_string(HTML_SABLON, leaders=leaders)

@app.route('/save-score', methods=['POST'])
@login_required
def save_score():
    data = request.get_json()
    if data and data.get('score', 0) > current_user.score:
        current_user.score = data['score']
        db.session.commit()
    return '', 204

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form.get('u')
        p = request.form.get('p')
        if User.query.filter_by(username=u).first():
            return "Bu kullanıcı adı alınmış!"
        user = User(username=u, password=generate_password_hash(p))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return '<h2>Kayıt Ol</h2><form method="post">Kullanıcı: <input name="u"><br>Şifre: <input name="p" type="password"><button>Kayıt</button></form>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('u')
        p = request.form.get('p')
        user = User.query.filter_by(username=u).first()
        if user and check_password_hash(user.password, p):
            login_user(user)
            return redirect(url_for('index'))
    return '<h2>Giriş Yap</h2><form method="post">Kullanıcı: <input name="u"><br>Şifre: <input name="p" type="password"><button>Giriş</button></form>'

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# 5. VERİTABANI OLUŞTURMA VE BAŞLATMA
if __name__ == "__main__":
    # Flask 3.0+ için veritabanını uygulama bağlamında oluşturuyoruz
    with app.app_context():
        db.create_all()
        print("Tablolar oluşturuldu/kontrol edildi.")
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
