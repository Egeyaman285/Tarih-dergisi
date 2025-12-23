import os
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ggi-gizli-123'

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

# --- HER ÜLKE İÇİN GARANTİLENMİŞ 15+ SATIRLIK ANALİZ (BOZULMADI) ---
def get_long_info(country_name):
    return f"""
[GİZLİLİK DERECESİ: ÇOK GİZLİ] - ANALİZ: {country_name}
----------------------------------------------------------------------
1. TARİHSEL VE DEVRİMSEL TEMELLER:
{country_name}, modern tarih sahnesine büyük toplumsal kırılmalar ve devrimsel süreçlerle çıkmıştır. 
Kuruluş felsefesi, bölgesel hakimiyet ve teknolojik bağımsızlık üzerine inşa edilmiştir. 
Geçmişte yaşanan büyük savaşlar, ülkenin savunma doktrinini tamamen 'caydırıcılık' üzerine kurmasına neden olmuştur.

2. NÜKLEER KAPASİTE VE STRATEJİK ENERJİ:
Ülke, nükleer eşik değerine ulaşmak için son yirmi yılda devasa AR-GE yatırımları gerçekleştirmiştir. 
Uranyum zenginleştirme kapasitesi ve gelişmiş reaktör tasarımları, uluslararası denetçilerin radarındadır. 
Nükleer enerji kullanımı, sadece sivil ihtiyaçlar için değil, askeri caydırıcılık için de kritik bir unsurdur.

3. JEOPOLİTİK VE SİBER SAVUNMA KATMANLARI:
Bulunduğu coğrafyanın enerji ve lojistik hatları üzerindeki etkisi, bu devleti vazgeçilmez bir aktör kılar. 
Savunma sanayiinde yapay zeka entegreli sistemler ve İHA teknolojileri ön plandadır. 
Siber ordusu, nükleer tesisleri ve dijital altyapıyı korumak adına 'Aktif Savunma' modunda çalışmaktadır.

4. GİZLİ PROTOKOLLER VE GELECEK VİZYONU:
Yürütülen 'Karanlık Laboratuvar' projeleri, yeni nesil hipersonik füze sistemlerini kapsamaktadır. 
Küresel güç dengelerinde, bu ülkenin hamleleri statükoyu değiştirecek potansiyele sahiptir. 
Gelecek on yılda, nükleer modernizasyonun %100 tamamlanması ve tam bağımsızlık hedeflenmektedir.

DURUM: ARŞİV DOSYASI TAMAMLANDI. KAYITLAR GÜNCELDİR.
----------------------------------------------------------------------
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
    <title>GGİ STRATEJİK ARŞİV</title>
    <style>
        :root { --neon-blue: #38bdf8; --neon-red: #f43f5e; --bg-dark: #020617; --card-bg: #0f172a; --text-color: #e2e8f0; }
        .light-mode { --bg-dark: #f1f5f9; --card-bg: #ffffff; --text-color: #0f172a; }

        body { background: var(--bg-dark); color: var(--text-color); font-family: 'Courier New', Courier, monospace; margin: 0; transition: 0.3s; }
        .nav { background: #0f172a; padding: 15px; border-bottom: 2px solid var(--neon-blue); display: flex; justify-content: space-between; align-items: center; position: sticky; top:0; z-index:100; }
        
        .layout { display: grid; grid-template-columns: 280px 1fr 350px; min-height: 100vh; }
        .sidebar { background: var(--card-bg); border-right: 1px solid #1e293b; padding: 20px; }
        .content { padding: 20px; }
        .game-panel { background: var(--card-bg); border-left: 1px solid #1e293b; padding: 20px; text-align: center; }

        .country-card { background: var(--card-bg); border: 1px solid #1e293b; padding: 20px; margin-bottom: 20px; border-radius: 8px; cursor: pointer; transition: 0.2s; position: relative; overflow: hidden; }
        .country-card:hover { border-color: var(--neon-blue); transform: scale(1.01); box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); }
        .country-card:active { animation: glitch 0.2s infinite; }
        
        @keyframes glitch {
            0% { left: -2px; } 25% { left: 2px; } 50% { left: -1px; } 75% { left: 1px; } 100% { left: 0; }
        }

        .title { color: var(--neon-blue); font-size: 16px; font-weight: bold; }
        .text-body { display: none; line-height: 1.6; font-size: 13px; text-align: left; white-space: pre-wrap; color: #94a3b8; border-top: 1px solid #334155; margin-top: 10px; padding-top: 10px; }
        .cursor { display: inline-block; width: 8px; height: 15px; background: var(--neon-blue); animation: blink 0.6s infinite; vertical-align: middle; }
        @keyframes blink { 50% { opacity: 0; } }

        #settings-panel { position: fixed; right: -320px; top: 0; width: 300px; height: 100%; background: #0f172a; border-left: 2px solid var(--neon-blue); z-index: 1000; transition: 0.4s; padding: 20px; color: white; }
        #settings-panel.active { right: 0; }
        .info-box { background: #1e293b; padding: 15px; border-radius: 8px; margin-bottom: 15px; font-size: 14px; border-left: 3px solid var(--neon-blue); }
        
        #game-wrapper { position: relative; width: 100%; max-width: 310px; height: 350px; margin: 0 auto; }
        canvas { background: #000; border: 2px solid #334155; border-radius: 8px; width: 100%; }
        #game-ui { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(2,6,23,0.9); color: var(--neon-blue); display: flex; align-items: center; justify-content: center; text-align: center; padding: 20px; border-radius: 8px; }

        @media (max-width: 1024px) { .layout { grid-template-columns: 1fr; } .sidebar { order: 2; } .content { order: 1; } .game-panel { order: 3; } }
        .btn { background: var(--neon-blue); color: #000; padding: 8px 15px; border-radius: 4px; font-weight: bold; font-size: 12px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <audio id="tickSound" src="https://www.soundjay.com/buttons/button-50.mp3" preload="auto"></audio>

    <div class="nav">
        <div style="color:var(--neon-blue); font-weight:bold; letter-spacing:2px;">GGİ // ARŞİV</div>
        <div style="display: flex; align-items: center; gap: 15px;">
            <button onclick="toggleSettings()" style="background:none; border:none; color:var(--neon-blue); font-size:20px; cursor:pointer;">⚙️</button>
            {% if current_user.is_authenticated %} <a href="/logout" style="color:var(--neon-red); text-decoration:none; font-size:12px;">[KAPAT]</a>
            {% else %} <a href="/login" class="btn">GİRİŞ</a> {% endif %}
        </div>
    </div>

    <div id="settings-panel">
        <h3>SİSTEM AYARLARI</h3>
        <p style="color:var(--neon-blue); font-size:11px;">ADMİN BİLGİLERİ</p>
        <div class="info-box">İSİM: EGE<br>YAŞ: 12<br>DİL: PYTHON</div>
        <button onclick="toggleTheme()" class="btn" style="width:100%;">TEMA DEĞİŞTİR</button>
        <button onclick="toggleSettings()" class="btn" style="width:100%; margin-top:10px; background:#475569;">PANELİ KAPAT</button>
    </div>

    <div class="layout">
        <div class="sidebar">
            <h4 style="color:var(--neon-blue);">LİDERLER</h4>
            {% for u in leaders %}
                <div style="background:#1e293b; padding:8px; margin-bottom:8px; border-radius:4px; font-size:13px; color:white;">
                    {{ u.username }} <span style="float:right; color:var(--neon-blue);">{{ u.score }}</span>
                </div>
            {% endfor %}
        </div>

        <div class="content">
            <div style="margin-bottom:20px; padding:10px; background:var(--card-bg); border-left:3px solid var(--neon-blue); font-size:11px; color:#94a3b8;">
                > VERİ TABANI ERİŞİLDİ... ANALİZLER YÜKLENİYOR...
            </div>
            {% for c in countries %}
            <div class="country-card" onclick="toggleArchive(this, {{loop.index}})">
                <div class="title">{{ c.n }}</div>
                <div class="text-body" id="type-{{loop.index}}" data-text="{{ c.info }}"></div>
            </div>
            {% endfor %}
        </div>

        <div class="game-panel">
            <h4 style="color:var(--neon-blue);">EĞİTİM SAHASI</h4>
            <div id="game-wrapper" onclick="gameInput()">
                <canvas id="game" width="310" height="350"></canvas>
                <div id="game-ui">BAŞLAT</div>
            </div>
        </div>
    </div>

    <script>
        function toggleSettings() { document.getElementById('settings-panel').classList.toggle('active'); }
        function toggleTheme() { document.body.classList.toggle('light-mode'); }
        function playTick() { const s = document.getElementById('tickSound'); s.currentTime = 0; s.play(); }

        function toggleArchive(card, id) {
            const el = document.getElementById('type-' + id);
            playTick();
            
            if(el.style.display === "block") {
                el.style.display = "none";
            } else {
                el.style.display = "block";
                if(el.innerHTML === "") {
                    const fullText = el.getAttribute('data-text');
                    let i = 0;
                    el.innerHTML = '<span id="inner-'+id+'"></span><span class="cursor"></span>';
                    const target = document.getElementById('inner-'+id);
                    
                    function type() {
                        if (i < fullText.length) {
                            target.innerHTML += fullText.charAt(i);
                            i++;
                            setTimeout(type, 5); // Yazım hızı
                        } else {
                            // Yazım bitince imleci kaldırabiliriz veya kalsın
                        }
                    }
                    type();
                }
            }
        }

        // Oyun Motoru (Bozulmadı)
        const canvas = document.getElementById('game'); const ctx = canvas.getContext('2d'); const ui = document.getElementById('game-ui');
        let score = 0, active = false, player = {x:40, y:290, dy:0, jump:false}, obs = [];
        function gameInput() { if(!active) { ui.style.display="none"; startGame(); } else if(!player.jump) { player.dy = -10; player.jump = true; } }
        function startGame() { score = 0; obs = []; player.y = 290; active = true; spawn(); loop(); }
        function spawn() { if(active) { obs.push({x:310, w:25, s: 4 + (score/15)}); setTimeout(spawn, 1300 + Math.random()*700); } }
        function loop() {
            if(!active) return;
            ctx.clearRect(0,0,310,350);
            ctx.fillStyle = '#1e293b'; ctx.fillRect(0, 320, 310, 30);
            player.dy += 0.5; player.y += player.dy;
            if(player.y > 290) { player.y=290; player.dy=0; player.jump=false; }
            ctx.fillStyle='#38bdf8'; ctx.fillRect(player.x, player.y, 30, 30);
            obs.forEach((o,i) => {
                o.x -= o.s; ctx.fillStyle='#f43f5e'; ctx.fillRect(o.x, 290, o.w, 30);
                if(o.x < player.x + 25 && o.x + o.w > player.x && player.y > 260) {
                    active = false; ui.style.display="flex"; ui.innerHTML = "BAŞARISIZ<br>SKOR: "+score;
                    fetch('/save', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({s:score})});
                }
                if(o.x + o.w < 0) { obs.splice(i,1); score++; }
            });
            ctx.fillStyle='white'; ctx.fillText("SKOR: "+score, 10, 25);
            requestAnimationFrame(loop);
        }
    </script>
</body>
</html>
"""

# Flask Route'ları (Login, Register, Logout, Save) aynen korunmuştur...
@app.route('/')
def index():
    db.create_all()
    leaders = User.query.order_by(User.score.desc()).limit(10).all()
    return render_template_string(HTML_SABLON, leaders=leaders, countries=COUNTRIES_DATA)

@app.route('/save', methods=['POST'])
@login_required
def save():
    s = request.json.get('s'); 
    if s and s > current_user.score: current_user.score = s; db.session.commit()
    return '', 204

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form['u']; p = generate_password_hash(request.form['p'])
        if not User.query.filter_by(username=u).first():
            user = User(username=u, password=p); db.session.add(user); db.session.commit()
        return redirect('/login')
    return render_template_string('<body style="background:#020617;color:white;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace;"><form method="post" style="border:2px solid #38bdf8;padding:40px;border-radius:10px;text-align:center;"><h2>KAYIT</h2><input name="u" placeholder="KOD ADI" style="display:block;margin:10px auto;padding:10px;"><input name="p" type="password" placeholder="ŞİFRE" style="display:block;margin:10px auto;padding:10px;"><button style="background:#38bdf8;padding:10px 20px;border:none;font-weight:bold;">ONAYLA</button></form></body>')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['u']).first()
        if u and check_password_hash(u.password, request.form['p']): login_user(u); return redirect('/')
    return render_template_string('<body style="background:#020617;color:white;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace;"><form method="post" style="border:2px solid #38bdf8;padding:40px;border-radius:10px;text-align:center;"><h2>GİRİŞ</h2><input name="u" placeholder="KOD ADI" style="display:block;margin:10px auto;padding:10px;"><input name="p" type="password" placeholder="ŞİFRE" style="display:block;margin:10px auto;padding:10px;"><button style="background:#38bdf8;padding:10px 20px;border:none;font-weight:bold;">SİSTEME GİR</button></form></body>')

@app.route('/logout')
def logout(): logout_user(); return redirect('/')

if __name__ == "__main__":
    with app.app_context(): db.create_all()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
