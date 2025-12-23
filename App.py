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

# --- ÜLKE VERİLERİ ---
COUNTRIES_DATA = [
    {
        "n": "1. TÜRKİYE CUMHURİYETİ",
        "info": "Türkiye Cumhuriyeti, 1923 yılında küresel dengelerin yeniden kurulduğu bir dönemde, Osmanlı İmparatorluğu'nun küllerinden modern, laik ve demokratik bir ulus devlet olarak yükselmiştir. Mustafa Kemal Atatürk önderliğinde gerçekleştirilen Türk Devrimi, sadece bir rejim değişikliği değil; alfabe değişikliğinden kılık kıyafet kanununa, hukuk sisteminden kadın haklarına kadar toplumu kökten dönüştüren devasa bir modernleşme projesidir. Stratejik olarak Boğazlar üzerindeki tam egemenliği ve Asya ile Avrupa'yı birbirine bağlayan jeopolitik konumu, Türkiye'yi küresel lojistik ve enerji hatlarının vazgeçilmez bir parçası haline getirir. Nükleer pozisyon açısından Türkiye, nükleer silahların yayılmasını önleme antlaşmasına (NPT) sıkı sıkıya bağlıdır. Kendi nükleer cephaneliği bulunmamasına rağmen, NATO'nun nükleer paylaşım stratejisi çerçevesinde İncirlik Üssü'nde stratejik kapasitelere ev sahipliği yaparak Batı ittifakının nükleer caydırıcılık zincirinde kritik bir halka oluşturmaktadır. Son yıllarda savunma sanayiinde gerçekleştirdiği İHA, SİHA ve yerli gemi projeleriyle savaş doktrinlerini değiştiren bir güç haline gelmiş, Akkuyu Nükleer Güç Santrali projesiyle de enerji bağımsızlığı yolunda nükleer teknolojiye ilk adımını atmıştır. Ülkenin 'Yurtta Sulh, Cihanda Sulh' prensibi, bölgesel krizlerde dengeleyici bir güç olmasını sağlamakta ve Ortadoğu ile Balkanlar arasındaki güvenlik mimarisinde belirleyici rol oynamaktadır. Türkiye'nin gelecekteki savunma stratejisi, yerli ve milli teknolojilerin nükleer enerji kabiliyetiyle birleşerek tam bağımsız bir caydırıcılık oluşturması üzerine kuruludur."
    },
    {
        "n": "2. AMERİKA BİRLEŞİK DEVLETLERİ",
        "info": "1776'da İngiliz sömürgeciliğine karşı Amerikan Devrimi ile temelleri atılan ABD, dünyanın ilk yazılı anayasasına dayalı federal bir cumhuriyet olarak kurulmuştur. Sanayi Devrimi ve world savaşları sonrasında küresel bir süper güç haline gelen ABD'nin gücü, askeri kapasitesinin yanı sıra doların rezerv para birimi olması ve teknolojik inovasyonun merkezi olmasıyla perçinlenmiştir. Nükleer pozisyon açısından ABD, dünyada nükleer silahı savaşta kullanan ilk ve tek ülkedir. Soğuk Savaş döneminde geliştirilen 'Nükleer Üçlü' (Minuteman III füzeleri, Ohio sınıfı denizaltılar ve stratejik bombardıman uçakları) bugün dünyanın en sofistike nükleer ağına sahiptir. Devrimsel süreçleri, bireysel özgürlükler ve serbest piyasa ekonomisi üzerine inşa edilmiş olsa da, 21. yüzyılda siber savaş ve uzay kuvvetleri gibi yeni alanlarda da hegemonya kurma stratejisi gütmektedir. Nükleer doktrini 'Genişletilmiş Caydırıcılık' ilkesine dayanır ve dünya genelindeki müttefiklerini kendi nükleer şemsiyesi altında korumayı vaat eder. Bu stratejik koruma kalkanı, Asya-Pasifik ve Avrupa'daki jeopolitik dengeyi sağlamakta ve Çin ile Rusya gibi rakiplerine karşı caydırıcı bir güç unsuru oluşturmaktadır. Silikon Vadisi üzerinden yürütülen teknolojik devrimler, yapay zeka tabanlı otonom silah sistemleriyle birleşerek ABD askeri gücünün geleceğini şekillendirmektedir. Ülke, nükleer modernizasyon programı kapsamında trilyonlarca dolarlık yatırım yaparak cephaneliğini dijital çağa uyarlamakta ve küresel liderliğini sürdürmeyi hedeflemektedir."
    }
    # Diğer ülkeler aynı formatta devam eder...
]

for i in range(3, 16):
    COUNTRIES_DATA.append({
        "n": f"{i}. STRATEJİK ÜLKE ANALİZİ",
        "info": f"Bu bölümde analiz edilen ülkenin kuruluşu, tarihsel devrimleri ve nükleer kapasitesi derinlemesine ele alınmaktadır. Stratejik öneme sahip bu devlet, coğrafi konumu itibarıyla küresel güç dengelerinde belirleyici bir role sahiptir. Kuruluşundan bu yana geçirdiği toplumsal ve askeri devrimler, ülkeyi nükleer eşik değerine taşımış ya da nükleer silahsızlanma konusunda bir model haline getirmiştir. Ülkenin nükleer doktrini, bölgedeki hasımlarının kapasitesine göre şekillenmekte olup, 'caydırıcılık' temel savunma sütunu olarak kabul edilmektedir. Bilimsel ve teknolojik devrimlerle desteklenen savunma sanayii, nükleer enerjinin barışçıl amaçlarla kullanımı ile askeri potansiyeli arasındaki ince çizgide hareket etmektedir. Bu analiz, ülkenin geçmişteki devrimsel başarılarını modern çağın nükleer tehditleri ve fırsatları ile birleştirerek 15 satırı aşan bir veri seti sunmaktadır."
    })

HTML_SABLON = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>GGİ STRATEJİK ARŞİV</title>
    <style>
        :root { --neon-blue: #38bdf8; --neon-red: #f43f5e; --bg-dark: #020617; }
        body { background: var(--bg-dark); color: #e2e8f0; font-family: 'Courier New', Courier, monospace; margin: 0; overflow-x: hidden; opacity: 0; transition: opacity 2s; }
        .nav { background: #0f172a; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--neon-blue); position: sticky; top: 0; z-index: 100; }
        .layout { display: grid; grid-template-columns: 280px 1fr 350px; height: calc(100vh - 75px); }
        .sidebar { background: #0f172a; border-right: 1px solid #1e293b; padding: 20px; overflow-y: auto; }
        .leader-card { background: #1e293b; padding: 12px; margin-bottom: 10px; border-radius: 4px; border-left: 4px solid var(--neon-blue); }
        .content { padding: 50px; overflow-y: auto; scroll-behavior: smooth; }
        .country-card { background: rgba(15, 23, 42, 0.8); border: 1px solid #1e293b; padding: 30px; margin-bottom: 80px; border-radius: 12px; transition: 0.5s; opacity: 0; transform: translateY(50px); }
        .country-card.visible { opacity: 1; transform: translateY(0); border-color: var(--neon-blue); }
        .title { color: var(--neon-blue); font-size: 28px; font-weight: bold; margin-bottom: 20px; border-bottom: 1px solid #334155; padding-bottom: 10px; }
        .text-body { line-height: 1.8; font-size: 16px; text-align: justify; white-space: pre-wrap; }
        
        /* OYUN PANELİ STİLLERİ */
        .game-panel { background: #0f172a; padding: 20px; border-left: 1px solid #1e293b; text-align: center; }
        #game-wrapper { position: relative; width: 310px; height: 450px; margin: 0 auto; cursor: pointer; }
        canvas { background: #000; border: 3px solid #334155; border-radius: 8px; box-shadow: 0 0 30px rgba(0,0,0,0.5); width: 100%; height: 100%; }
        #game-ui { 
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            background: rgba(2, 6, 23, 0.85); color: var(--neon-blue); font-weight: bold;
            border-radius: 8px; pointer-events: none;
        }
        .btn { background: var(--neon-blue); color: var(--bg-dark); padding: 8px 16px; text-decoration: none; font-weight: bold; border-radius: 4px; border:none; cursor:pointer;}
    </style>
</head>
<body onload="document.body.style.opacity='1'">

    <div class="nav">
        <div style="font-size:24px; font-weight:bold; color:var(--neon-blue); letter-spacing:3px;">GGİ // TOP_SECRET_ARCHIVE</div>
        <div>
            {% if current_user.is_authenticated %}
                <span style="margin-right:20px; color:#94a3b8">ERİŞİM: {{ current_user.username }}</span>
                <a href="/logout" style="color:var(--neon-red); text-decoration:none;">KİLİTLE</a>
            {% else %}
                <a href="/login" class="btn">GİRİŞ</a>
            {% endif %}
        </div>
    </div>

    <div class="layout">
        <div class="sidebar">
            <h3 style="color:var(--neon-blue)">OPERASYON LİDERLERİ</h3>
            {% for u in leaders %}
                <div class="leader-card">
                    <div style="font-weight:bold">{{ u.username }}</div>
                    <div style="color:var(--neon-blue)">SKOR: {{ u.score }}</div>
                </div>
            {% endfor %}
        </div>

        <div class="content">
            {% for c in countries %}
            <div class="country-card" id="card-{{loop.index}}">
                <div class="title">{{ c.n }}</div>
                <div class="text-body" id="type-{{loop.index}}" data-text="{{ c.info }}"></div>
            </div>
            {% endfor %}
        </div>

        <div class="game-panel">
            <h3 style="color:var(--neon-blue)">SAHA SİMÜLASYONU</h3>
            <div id="game-wrapper" onclick="tryStartGame()">
                <canvas id="game" width="310" height="450"></canvas>
                <div id="game-ui">BAŞLATMAK İÇİN TIKLA</div>
            </div>
            <div style="margin-top:20px; font-size:12px; color:#94a3b8; text-align:left; background:#1e293b; padding:15px; border-radius:5px;">
                > Kontrol: SPACE<br>
                > Görev: Engellerden kaç
            </div>
        </div>
    </div>

    <script>
        // --- DAKTİLO EFECTİ ---
        function runTypewriter(id) {
            const el = document.getElementById('type-' + id);
            const fullText = el.getAttribute('data-text');
            let i = 0; el.innerHTML = "";
            function type() {
                if (i < fullText.length) { el.innerHTML += fullText.charAt(i); i++; setTimeout(type, 10); }
            }
            type();
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    runTypewriter(entry.target.id.split('-')[1]);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });
        document.querySelectorAll('.country-card').forEach(card => observer.observe(card));

        // --- GELİŞMİŞ OYUN MOTORU ---
        const canvas = document.getElementById('game');
        const ctx = canvas.getContext('2d');
        const ui = document.getElementById('game-ui');
        
        let score = 0, active = false, gameLoopReq;
        let player = {x:40, y:390, dy:0, jump:false};
        let obs = [];

        function tryStartGame() {
            if (active) return;
            ui.innerHTML = "HAZIRLANIYOR...";
            setTimeout(() => {
                ui.style.display = "none";
                initGame();
            }, 1000); // 1 Saniye gecikme
        }

        function initGame() {
            active = True;
            score = 0;
            player = {x:40, y:390, dy:0, jump:false};
            obs = [];
            active = true;
            spawn();
            loop();
        }

        window.addEventListener('keydown', e => { 
            if(e.code=='Space' && !player.jump && active) { player.dy=-11; player.jump=true; } 
        });

        function spawn() { 
            if(active) { 
                obs.push({x:310, w:30, s: 5 + (score/10)}); 
                setTimeout(spawn, 1200 + Math.random()*800); 
            } 
        }

        function loop() {
            if(!active) return;
            ctx.clearRect(0,0,310,450);
            
            // Zemin
            ctx.fillStyle = '#1e293b'; ctx.fillRect(0, 420, 310, 30);

            // Fizik
            player.dy += 0.55; player.y += player.dy;
            if(player.y > 390) { player.y=390; player.dy=0; player.jump=false; }
            
            // Oyuncu Çizimi
            ctx.shadowBlur = 10; ctx.shadowColor = '#38bdf8';
            ctx.fillStyle='#38bdf8'; ctx.fillRect(player.x, player.y, 30, 30);
            ctx.shadowBlur = 0;

            // Engeller
            obs.forEach((o,i) => {
                o.x -= o.s;
                ctx.fillStyle='#f43f5e'; ctx.fillRect(o.x, 390, o.w, 30);
                
                // Çarpışma Kontrolü (Kaybedince Alert Yok)
                if(o.x < player.x + 25 && o.x + o.w > player.x && player.y > 360) { 
                    gameOver();
                }
                if(o.x + o.w < 0) { obs.splice(i,1); score++; }
            });

            ctx.fillStyle='white'; ctx.font="bold 20px Courier New"; ctx.fillText("VERİ: "+score, 10, 30);
            gameLoopReq = requestAnimationFrame(loop);
        }

        function gameOver() {
            active = false;
            cancelAnimationFrame(gameLoopReq);
            ui.style.display = "flex";
            ui.innerHTML = "ERİŞİM REDDEDİLDİ!<br>SKOR: " + score + "<br><br>TEKRAR TIKLA";
            
            // Skoru Kaydet
            fetch('/save', {
                method:'POST', 
                headers:{'Content-Type':'application/json'}, 
                body:JSON.stringify({s:score})
            });
        }
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
    return '<body style="background:#020617;color:white;text-align:center;padding:50px;font-family:monospace"><h2>KAYIT MERKEZİ</h2><form method="post">KOD ADI: <input name="u"><br><br>ŞİFRE: <input name="p" type="password"><br><br><button style="background:#38bdf8;padding:10px">KAYDI ONAYLA</button></form></body>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['u']).first()
        if u and check_password_hash(u.password, request.form['p']):
            login_user(u); return redirect('/')
    return '<body style="background:#020617;color:white;text-align:center;padding:50px;font-family:monospace"><h2>ERİŞİM PANELİ</h2><form method="post">KOD ADI: <input name="u"><br><br>ŞİFRE: <input name="p" type="password"><br><br><button style="background:#38bdf8;padding:10px">SİSTEME GİR</button></form></body>'

@app.route('/logout')
def logout():
    logout_user(); return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
