import os
import datetime
import random
import time
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# --- SİSTEM ÇEKİRDEK YAPILANDIRMASI ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ggi-ultra-secure-2025-special-vortex-key-x800'

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'ggi.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# --- VERİTABANI MİMARİSİ (GENİŞLETİLDİ) ---
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)
    access_level = db.Column(db.String(20), default="LEVEL_1")

class Visit(db.Model):
    __tablename__ = 'visits'
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_agent = db.Column(db.String(250))

class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500))
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- STRATEJİK ANALİZ MODÜLÜ (HER ÜLKE İÇİN 20+ SATIR GARANTİSİ) ---
def get_long_info(country_name):
    # Bu fonksiyon her çağrıldığında 20 satırı aşacak bir veri yapısı döner
    return f"""
[ERİŞİM KATMANI: ADMİN_LEVEL_5] - ANALİZ NESNESİ: {country_name}
======================================================================
01. JEOPOLİTİK VE KONVANSİYONEL KONUMLANDIRMA:
{country_name}, küresel jeopolitik arenada kritik bir denge unsurudur.
Toprak bütünlüğü, stratejik derinlik prensibiyle korunmaktadır.
Sınır hatları boyunca 7/24 aktif olan otonom gözetleme kuleleri mevcuttur.
Deniz yetki alanları, Mavi Vatan doktrini çerçevesinde izlenmektedir.
Hava sahası, katmanlı savunma sistemleri ile koruma altına alınmıştır.

02. ASKERİ KAPASİTE VE NÜKLEER DOKTRİN ANALİZİ:
Savunma bütçesi, GSYİH içinde %4.8 oranında stratejik paya sahiptir.
Nükleer kapasite, 'Aktif Caydırıcılık' fazından 'Hızlı Yanıt' fazına geçmiştir.
Konvansiyonel kara güçleri, hibrit savaş senaryolarına göre mobilize edilmiştir.
Donanma unsurları, uçak gemisi görev grupları ile okyanus aşırı yetenektedir.
Hava kuvvetleri, 5. nesil görünmezlik teknolojisine sahip jetlerle donatılmıştır.

03. TEKNOLOJİK SİBER SAVUNMA VE VERİ EGEMENLİĞİ:
Milli siber güvenlik kalkanı, kuantum sonrası şifreleme ile modernize edilmiştir.
Kritik devlet altyapıları (Enerji, Su, Finans) izole 'Air-Gap' ağlardadır.
Yapay zeka tabanlı siber timler, proaktif saldırı engelleme yapmaktadır.
Blockchain tabanlı veri saklama sistemleri, kayıtların güvenliğini sağlar.
Yerli işletim sistemi çekirdeği, arka kapılara karşı tamamen taranmıştır.

04. EKONOMİK MANİPÜLASYON DİRENCİ VE REZERVLER:
Dış borç rasyosu, küresel finansal dalgalanmalara karşı stabilize edilmiştir.
Stratejik maden ve nadir element yatakları devlet denetimi altındadır.
Gıda güvenliği için yer altı tarım tesisleri ve stratejik stoklar aktiftir.
Enerji bağımsızlığı için nükleer ve yenilenebilir kaynaklar ana odaktır.
Merkez bankası rezervleri, dijital varlıklarla çeşitlendirilmektedir.

05. GELECEK PROJEKSİYONU VE RİSK ANALİZİ:
2030 uzay programı, Ay yörüngesinde askeri gözlem istasyonunu hedefler.
Demografik değişimler, yapay zeka ve robotik iş gücü ile dengelenmektedir.
Su kaynaklarının korunması, ulusal güvenlik belgesinde 1. sıradadır.
İklim değişikliği senaryolarına karşı kentsel dayanıklılık artırılmaktadır.

VERİ ANALİZİ TAMAMLANMIŞTIR. KAYIT NO: 0x{id(country_name)}C78
======================================================================
"""

COUNTRIES_DATA = []
names = ["TÜRKİYE", "ABD", "RUSYA", "ÇİN", "FRANSA", "İNGİLTERE", "HİNDİSTAN", "PAKİSTAN", "İSRAİL", "KUZEY KORE", "ALMANYA", "JAPONYA", "İRAN", "BREZİLYA", "GÜNEY AFRİKA"]
for i, name in enumerate(names, 1):
    COUNTRIES_DATA.append({"n": f"{i}. {name} STRATEJİK RAPORU", "info": get_long_info(name)})

# --- SİBER ARAYÜZ (HTML/CSS/JS) ---
HTML_SABLON = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GGİ // COMMAND_OS_v8</title>
    <style>
        :root {
            --neon-blue: #00f2ff;
            --neon-red: #ff0055;
            --neon-green: #39ff14;
            --bg-deep: #010203;
            --panel-glass: rgba(5, 10, 20, 0.9);
        }

        body {
            background: var(--bg-deep);
            color: #fff;
            font-family: 'Courier New', monospace;
            margin: 0;
            overflow: hidden;
            background-image: radial-gradient(circle at 50% 50%, #0a111a 0%, #010203 100%);
        }

        /* ÜST BİLGİ BANDI */
        .top-bar {
            background: #000;
            border-bottom: 2px solid var(--neon-blue);
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 0 20px var(--neon-blue);
        }

        .ticker-text {
            background: #000;
            color: var(--neon-green);
            padding: 5px;
            font-size: 11px;
            border-bottom: 1px solid #111;
            overflow: hidden;
            white-space: nowrap;
        }
        .ticker-text span {
            display: inline-block;
            padding-left: 100%;
            animation: ticker-move 35s linear infinite;
        }
        @keyframes ticker-move {
            0% { transform: translate(0, 0); }
            100% { transform: translate(-100%, 0); }
        }

        /* ANA EKRAN DÜZENİ */
        .main-grid {
            display: grid;
            grid-template-columns: 380px 1fr 400px;
            gap: 15px;
            padding: 15px;
            height: calc(100vh - 110px);
        }

        .panel {
            background: var(--panel-glass);
            border: 1px solid #1a2a3a;
            border-radius: 5px;
            display: flex;
            flex-direction: column;
            position: relative;
        }

        .panel-title {
            background: #0d1621;
            padding: 10px;
            font-size: 12px;
            color: var(--neon-blue);
            border-bottom: 1px solid #1a2a3a;
            letter-spacing: 2px;
        }

        /* SOL PANEL */
        .stats-container { padding: 20px; }
        .data-card {
            background: rgba(0,0,0,0.5);
            border-left: 5px solid var(--neon-blue);
            padding: 15px;
            margin-bottom: 20px;
        }
        .data-val { font-size: 32px; color: var(--neon-green); font-weight: bold; }

        /* HESAP MAKİNESİ */
        .calc-wrap { padding: 20px; }
        #calc-display {
            width: 100%;
            background: #000;
            border: 1px solid var(--neon-blue);
            color: var(--neon-green);
            padding: 15px;
            text-align: right;
            margin-bottom: 10px;
            font-size: 20px;
        }
        .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
        .calc-grid button {
            background: #111;
            border: 1px solid #333;
            color: #fff;
            padding: 15px;
            cursor: pointer;
            font-weight: bold;
        }
        .calc-grid button:hover { background: var(--neon-blue); color: #000; }

        /* ORTA PANEL: ARŞİV */
        .archive-scroll {
            flex-grow: 1;
            overflow-y: auto;
            padding: 20px;
        }
        .country-card {
            background: #050a0f;
            border: 1px solid #112233;
            padding: 20px;
            margin-bottom: 20px;
            cursor: pointer;
            transition: 0.3s;
        }
        .country-card:hover { border-color: var(--neon-blue); box-shadow: 0 0 15px rgba(0,242,255,0.2); }
        
        .info-body {
            display: none;
            white-space: pre-wrap;
            font-size: 13px;
            color: var(--neon-green);
            line-height: 1.6;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px dashed #224466;
        }

        /* SAĞ PANEL: TERMİNAL */
        .terminal {
            background: #000;
            flex-grow: 1;
            padding: 15px;
            font-size: 11px;
            color: #4a4a4a;
            overflow-y: hidden;
        }
        .terminal-line { margin-bottom: 5px; }

        /* AYARLAR SLIDER */
        #settings-menu {
            position: fixed;
            right: -450px;
            top: 0;
            width: 400px;
            height: 100%;
            background: #000;
            border-left: 2px solid var(--neon-blue);
            z-index: 1000;
            transition: 0.5s;
            padding: 40px;
        }
        #settings-menu.active { right: 0; }

        .btn-ui {
            width: 100%;
            padding: 15px;
            background: var(--neon-blue);
            color: #000;
            border: none;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 10px;
        }

        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: var(--neon-blue); }
    </style>
</head>
<body>

    <audio id="click-sound" src="https://www.soundjay.com/buttons/button-50.mp3"></audio>

    <div class="ticker-text">
        <span>>>> SİSTEM MESAJI: {datetime.datetime.now().year} GÜVENLİK PROTOKOLLERİ AKTİF... IP TAKİBİ YAPILIYOR... KRİTİK ALTYAPI ANALİZLERİ YÜKLENDİ... <<<</span>
    </div>

    <div class="top-bar">
        <div style="font-size: 24px; font-weight: bold; color: var(--neon-blue); letter-spacing: 5px;">GGİ_CORE_OS</div>
        <div style="display: flex; gap: 30px; align-items: center;">
            <div id="live-clock" style="color: var(--neon-blue);">00:00:00</div>
            <button onclick="toggleSet()" style="background:none; border:none; color:var(--neon-blue); font-size:28px; cursor:pointer;">☰</button>
            {% if current_user.is_authenticated %}
                <a href="/logout" style="color:var(--neon-red); text-decoration:none; font-size:12px;">[DISCONNECT]</a>
            {% else %}
                <a href="/login" style="background:var(--neon-blue); color:#000; padding:5px 15px; text-decoration:none; font-weight:bold;">LOGIN</a>
            {% endif %}
        </div>
    </div>

    <div class="main-grid">
        <div class="panel">
            <div class="panel-title">SYSTEM_METRICS</div>
            <div class="stats-container">
                <div class="data-card">
                    <div style="font-size:10px; color:#555;">TOPLAM ERİŞİM SAYISI</div>
                    <div class="data-val">{{ total_visits }}</div>
                </div>
                <div class="data-card" style="border-left-color: var(--neon-green);">
                    <div style="font-size:10px; color:#555;">AKTİF BAĞLANTI IP</div>
                    <div style="color:var(--neon-blue); font-size:14px; margin-top:5px;">{{ user_ip }}</div>
                </div>
            </div>

            <div class="calc-wrap">
                <div style="color:var(--neon-blue); font-size:11px; margin-bottom:5px;">STRATEJİK HESAPLAYICI</div>
                <input type="text" id="calc-display" readonly value="0">
                <div class="calc-grid">
                    <button onclick="press('/')">/</button><button onclick="press('*')">*</button><button onclick="press('-')">-</button><button onclick="clr()">C</button>
                    <button onclick="press('7')">7</button><button onclick="press('8')">8</button><button onclick="press('9')">9</button><button onclick="press('+')">+</button>
                    <button onclick="press('4')">4</button><button onclick="press('5')">5</button><button onclick="press('6')">6</button><button onclick="exe()">=</button>
                    <button onclick="press('1')">1</button><button onclick="press('2')">2</button><button onclick="press('3')">3</button><button onclick="press('0')">0</button>
                </div>
            </div>
            
            <div style="padding:20px; overflow-y:auto; flex-grow:1;">
                <div style="color:var(--neon-blue); font-size:11px; margin-bottom:10px;">LİDER_OPERATÖRLER</div>
                {% for u in leaders %}
                    <div style="font-size:11px; padding:5px; border-bottom:1px solid #111; display:flex; justify-content:space-between;">
                        <span>{{ u.username }}</span>
                        <span style="color:var(--neon-green);">{{ u.score }} PX</span>
                    </div>
                {% endfor %}
            </div>
        </div>

        <div class="panel">
            <div class="panel-title">GLOBAL_STRATEGY_ARCHIVE</div>
            <div class="archive-scroll">
                {% for c in countries %}
                <div class="country-card" onclick="openArchive(this, {{loop.index}})">
                    <div style="color:var(--neon-blue); font-weight:bold; letter-spacing:2px;">{{ c.n }}</div>
                    <div class="info-body" id="text-{{loop.index}}" data-raw="{{ c.info }}"></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="panel">
            <div class="panel-title">LIVE_TERMINAL_LOGS</div>
            <div class="terminal" id="term-box">
                <div class="terminal-line">> Çekirdek başlatıldı...</div>
                <div class="terminal-line">> IP {{ user_ip }} üzerinden el sıkışma sağlandı...</div>
            </div>
            
            <div style="padding:20px; background:#0a1118; border-top:1px solid #1a2a3a;">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="font-size:11px;">USD/TRY</span>
                    <span id="market-usd" style="color:var(--neon-green);">32.44</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="font-size:11px;">CPU_LOAD</span>
                    <span id="cpu-stat" style="color:var(--neon-blue);">14%</span>
                </div>
            </div>
            
            <div style="padding:15px; font-size:10px; color:#333;">
                <p>> GGI_INTERFACE_v8.0.2</p>
                <p>> SYSTEM_ADMIN: EGE</p>
                <p>> DURUM: KRİTİK ANALİZ MODU</p>
            </div>
        </div>
    </div>

    <div id="settings-menu">
        <h2 style="color:var(--neon-blue); border-bottom:1px solid #222; padding-bottom:10px;">SYSTEM_CONTROL</h2>
        <div style="background:#111; padding:20px; margin-bottom:20px;">
            <p style="color:var(--neon-blue);">ADMİN: EGE (12 YAŞ)</p>
            <p>YETKİ: SİSTEM SAHİBİ</p>
            <p>DİL: PYTHON / SQLITE / JS</p>
        </div>
        <button class="btn-ui" onclick="alert('Sistem Yeniden Kalibre Ediliyor...')">KALİBRASYON</button>
        <button class="btn-ui" style="background:#333; color:#fff;" onclick="toggleSet()">MENÜYÜ KAPAT</button>
    </div>

    <script>
        // Zaman ve Dinamikler
        setInterval(() => {
            const d = new Date();
            document.getElementById('live-clock').innerText = d.getHours().toString().padStart(2,'0')+":"+d.getMinutes().toString().padStart(2,'0')+":"+d.getSeconds().toString().padStart(2,'0');
            document.getElementById('market-usd').innerText = (32.4 + Math.random()*0.1).toFixed(2);
            document.getElementById('cpu-stat').innerText = Math.floor(Math.random()*30 + 5) + "%";
        }, 1000);

        // Hesap Makinesi
        let cd = document.getElementById('calc-display');
        function press(v) { if(cd.value==='0') cd.value=v; else cd.value+=v; }
        function clr() { cd.value='0'; }
        function exe() { try { cd.value=eval(cd.value); } catch { cd.value='HATA'; } }

        // Arşiv ve Daktilo
        function openArchive(card, id) {
            document.getElementById('click-sound').play();
            const el = document.getElementById('text-' + id);
            if(el.style.display === 'block') {
                el.style.display = 'none';
            } else {
                el.style.display = 'block';
                if(el.innerHTML === "") {
                    const raw = el.getAttribute('data-raw');
                    let i = 0;
                    el.innerHTML = '<span id="inner-'+id+'"></span><span style="display:inline-block;width:8px;height:15px;background:var(--neon-green);animation:blink 0.7s infinite;"></span>';
                    const target = document.getElementById('inner-'+id);
                    function typing() {
                        if(i < raw.length) {
                            target.innerHTML += raw.charAt(i);
                            i++;
                            setTimeout(typing, 2);
                        }
                    }
                    typing();
                }
            }
        }

        // Terminal Logları
        const logs = [
            "> Yeni bağlantı isteği kabul edildi...",
            "> Arşiv paketi çözümleniyor...",
            "> IP {{ user_ip }} taranıyor...",
            "> Güvenlik katmanı aktif...",
            "> Veritabanı senkronizasyonu tamam...",
            "> Enerji koridoru verileri alındı..."
        ];
        setInterval(() => {
            const box = document.getElementById('term-box');
            const line = document.createElement('div');
            line.className = 'terminal-line';
            line.innerText = logs[Math.floor(Math.random()*logs.length)];
            box.appendChild(line);
            if(box.childNodes.length > 20) box.removeChild(box.firstChild);
        }, 3000);

        function toggleSet() { document.getElementById('settings-menu').classList.toggle('active'); }
    </script>
</body>
</html>
"""

# --- ROUTERLAR VE KONTROLLER ---
@app.route('/')
def index():
    db.create_all()
    # IP Takibi ve Ziyaret Kaydı
    u_ip = request.remote_addr
    v = Visit(ip_address=u_ip, user_agent=request.user_agent.string)
    db.session.add(v)
    
    # Log Kaydı
    log = SystemLog(message=f"IP {u_ip} bağlandı.", category="INFO")
    db.session.add(log)
    db.session.commit()
    
    total = Visit.query.count()
    leaders = User.query.order_by(User.score.desc()).limit(15).all()
    return render_template_string(HTML_SABLON, leaders=leaders, countries=COUNTRIES_DATA, total_visits=total, user_ip=u_ip)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form['u']; p = generate_password_hash(request.form['p'])
        if not User.query.filter_by(username=u).first():
            user = User(username=u, password=p); db.session.add(user); db.session.commit()
        return redirect('/login')
    return render_template_string('<body style="background:#000;color:#0f0;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace;"><div style="border:2px solid #0f0;padding:50px;"><h2>SİSTEM_KAYIT</h2><form method="post"><input name="u" placeholder="KULLANICI" style="display:block;width:100%;margin:10px 0;background:#000;border:1px solid #0f0;color:#0f0;padding:10px;"><input name="p" type="password" placeholder="ŞİFRE" style="display:block;width:100%;margin:10px 0;background:#000;border:1px solid #0f0;color:#0f0;padding:10px;"><button style="width:100%;background:#0f0;border:none;padding:10px;cursor:pointer;">BAŞLAT</button></form></div></body>')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['u']).first()
        if u and check_password_hash(u.password, request.form['p']): login_user(u); return redirect('/')
    return render_template_string('<body style="background:#000;color:#00f2ff;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace;"><div style="border:2px solid #00f2ff;padding:50px;"><h2>SİSTEM_GİRİŞ</h2><form method="post"><input name="u" placeholder="KULLANICI" style="display:block;width:100%;margin:10px 0;background:#000;border:1px solid #00f2ff;color:#00f2ff;padding:10px;"><input name="p" type="password" placeholder="ŞİFRE" style="display:block;width:100%;margin:10px 0;background:#000;border:1px solid #00f2ff;color:#00f2ff;padding:10px;"><button style="width:100%;background:#00f2ff;border:none;padding:10px;cursor:pointer;">ERİŞİM</button></form></div></body>')

@app.route('/logout')
def logout(): logout_user(); return redirect('/')

if __name__ == "__main__":
    with app.app_context(): db.create_all()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
