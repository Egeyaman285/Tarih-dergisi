import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ggi-gizli-123'

# Veritabanı yolunu kesinleştiriyoruz
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'ggi.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user' # Tablo adını açıkça belirtiyoruz
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- HTML SABLONU ---
HTML_SABLON = """
<!DOCTYPE html>
<html>
<head>
    <title>GGİ Platformu</title>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; text-align: center; }
        .nav { background: #1e293b; padding: 15px; display: flex; justify-content: space-around; border-bottom: 2px solid #00f2fe; }
        .container { display: flex; justify-content: center; padding: 20px; gap: 20px; }
        canvas { background: #000; border: 2px solid #00f2fe; }
        .leaderboard { background: #1e293b; padding: 20px; border-radius: 10px; min-width: 250px; }
        .logo { color: #00f2fe; font-size: 24px; font-weight: bold; }
        .btn { background: #00f2fe; color: #0f172a; padding: 5px 10px; text-decoration: none; border-radius: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="nav">
        <div class="logo">GGİ</div>
        <div>
            {% if current_user.is_authenticated %}
                {{ current_user.username }} | <a href="/logout" style="color:red">Çıkış</a>
            {% else %}
                <a href="/login" class="btn">Giriş</a> | <a href="/register" class="btn">Kayıt</a>
            {% endif %}
        </div>
    </div>
    <div class="container">
        <div>
            <h2>Arabalardan Atla!</h2>
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
        let score = 0, active = true, player = {x:50, y:240, dy:0, jump:false}, obs = [];
        document.addEventListener('keydown', e => { if(e.code=='Space' && !player.jump) { player.dy=-12; player.jump=true; } });
        function spawn() { if(active) obs.push({x:600, w:30, s: 5 + (score/5)}); setTimeout(spawn, 1500 + Math.random()*1000); }
        function loop() {
            if(!active) return;
            ctx.clearRect(0,0,600,300);
            player.dy += 0.6; player.y += player.dy;
            if(player.y > 240) { player.y=240; player.dy=0; player.jump=false; }
            ctx.fillStyle='#00f2fe'; ctx.fillRect(player.x, player.y, 30, 30);
            obs.forEach((o,i) => {
                o.x -= o.s;
                ctx.fillStyle='red'; ctx.fillRect(o.x, 240, o.w, 30);
                if(o.x < 80 && o.x > 20 && player.y > 210) { 
                    active=false; alert("Yandın! Skor: " + score);
                    fetch('/save', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({s:score})}).then(()=>location.reload());
                }
                if(o.x + o.w < 0) { obs.splice(i,1); score++; }
            });
            ctx.fillStyle='white'; ctx.fillText("Puan: "+score, 10, 20);
            requestAnimationFrame(loop);
        }
        spawn(); loop();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # HATAYI ÖNLEMEK İÇİN: Her girişte tabloları kontrol et
    db.create_all()
    leaders = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template_string(HTML_SABLON, leaders=leaders)

@app.route('/save', methods=['POST'])
@login_required
def save():
    s = request.json.get('s')
    if s > current_user.score:
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
    return 'Kayıt: <form method="post"><input name="u"><input name="p" type="password"><button>Ok</button></form>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['u']).first()
        if u and check_password_hash(u.password, request.form['p']):
            login_user(u); return redirect('/')
    return 'Giriş: <form method="post"><input name="u"><input name="p" type="password"><button>Ok</button></form>'

@app.route('/logout')
def logout():
    logout_user(); return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
