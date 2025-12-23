import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ggi-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ggi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# HTML BURADA BAŞLIYOR - Syntax hatası olmaması için f-string kullanmıyoruz
HTML_SABLON = """
<!DOCTYPE html>
<html>
<head>
    <title>GGI Oyun</title>
    <style>
        body { background: #1a1a1a; color: white; font-family: sans-serif; text-align: center; }
        .nav { background: #333; padding: 10px; display: flex; justify-content: space-around; }
        .container { display: flex; justify-content: center; padding: 20px; }
        canvas { background: #000; border: 3px solid #00ff88; cursor: pointer; }
        .leaderboard { margin-left: 20px; background: #222; padding: 15px; border-radius: 10px; min-width: 200px; }
        .logo { color: #00ff88; font-size: 24px; font-weight: bold; }
        a { color: #00ff88; text-decoration: none; }
    </style>
</head>
<body>
    <div class="nav">
        <div class="logo">GGİ</div>
        <div>
            {% if current_user.is_authenticated %}
                {{ current_user.username }} | <a href="/logout">Çıkış</a>
            {% else %}
                <a href="/login">Giriş</a> | <a href="/register">Kayıt</a>
            {% endif %}
        </div>
    </div>

    <div class="container">
        <div>
            <h2>Kareyi Zıplat (Space)</h2>
            <canvas id="game" width="600" height="300"></canvas>
        </div>
        <div class="leaderboard">
            <h3>🏆 TOP 10</h3>
            {% for u in leaders %}
                <p>{{ loop.index }}. {{ u.username }} - {{ u.score }}</p>
            {% endfor %}
        </div>
    </div>

    <script>
        const canvas = document.getElementById('game');
        const ctx = canvas.getContext('2d');
        let score = 0, active = true, player = {x:50, y:250, dy:0}, obs = [];

        document.addEventListener('keydown', e => { if(e.code=='Space' && player.y==270) player.dy=-12; });

        function loop() {
            if(!active) return;
            ctx.clearRect(0,0,600,300);
            player.dy += 0.6; player.y += player.dy;
            if(player.y > 270) { player.y=270; player.dy=0; }
            
            ctx.fillStyle='#00ff88'; ctx.fillRect(player.x, player.y, 30, 30);
            
            if(Math.random()<0.02) obs.push({x:600, w:30});
            obs.forEach((o,i) => {
                o.x -= 5;
                ctx.fillStyle='red'; ctx.fillRect(o.x, 270, o.w, 30);
                if(o.x<80 && o.x>20 && player.y>240) {
                    active=false;
                    fetch('/save', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({s:score})})
                    .then(() => location.reload());
                }
                if(o.x == 0) score++;
            });
            ctx.fillStyle='white'; ctx.fillText('Puan: '+score, 10, 20);
            requestAnimationFrame(loop);
        }
        loop();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    leaders = User.query.order_by(User.score.desc()).limit(10).all()
