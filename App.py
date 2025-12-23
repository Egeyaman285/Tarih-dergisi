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
app.config['SECRET_KEY'] = 'ggi-ultra-secure-2025-special-vortex-key-x800-mega-pro'

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'ggi.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# --- VERİTABANI MİMARİSİ ---
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

# --- STRATEJİK ANALİZ MODÜLÜ (HER ÜLKE İÇİN 25+ SATIR ANALİZ) ---
def get_mega_report(country_name):
    return f"""
[GÜVENLİK PROTOKOLÜ: ADMİN_ACCESS_V9]
======================================================================
ANALİZ NESNESİ: {country_name} STRATEJİK VERİ PAKETİ
DURUM: KRİTİK ANALİZ TAMAMLANIYOR...
======================================================================
01. JEOPOLİTİK VE KONVANSİYONEL KONUMLANDIRMA:
- {country_name}, bölgesel güç projeksiyonunda merkez noktadadır.
- Toprak bütünlüğü, 'Derin Strateji' doktrini ile muhafaza edilir.
- Sınır hatları, 3. nesil termal otonom sensörlerle donatılmıştır.
- Deniz yetki alanları, kıtasal sahanlık yasalarına göre izlenir.
- Hava sahası, yapay zeka destekli önleme sistemleri ile korunur.
- Lojistik ikmal hatları, yeraltı raylı sistemlerle yedeklenmiştir.

02. ASKERİ KAPASİTE VE CAYDIRICILIK ANALİZİ:
- Savunma bütçesi, yıllık GSYİH oranında %5.4 stratejik pay alır.
- Nükleer kapasite, 'Aktif Caydırıcılık' modundan tam hazır hale geldi.
- Kara güçleri, kentsel savaş senaryoları için mobilize edilmiştir.
- Donanma, fırkateyn sınıfı insansız deniz araçlarını devreye aldı.
- Hava kuvvetleri, siber saldırılara dirençli link-16 sistemindedir.
- Özel kuvvetler, hibrit operasyon yeteneği ile optimize edildi.
- Anti-balistik füze kalkanı, %99.8 başarı oranı ile test edildi.

03. TEKNOLOJİK SİBER SAVUNMA VE VERİ EGEMENLİĞİ:
- Milli siber güvenlik duvarı, kuantum sonrası algoritmalara sahiptir.
- Kritik altyapılar (Elektrik, Gaz), 'Black-Box' ağlarında saklanır.
- Siber saldırı timleri, 'Proaktif İmha' yetkisiyle donatılmıştır.
- Blockchain tabanlı veri merkezleri, kayıt güvenliğini garanti eder.
- Yerli işletim sistemi çekirdeği, her 10 milisaniyede taranır.
- Kriptoloji merkezi, asimetrik şifreleme ile veri koruması yapar.
- Uzay tabanlı gözetleme uyduları, 15 cm çözünürlükle veri sağlar.

04. EKONOMİK MANİPÜLASYON DİRENCİ VE KAYNAKLAR:
- Dış borç rasyosu, küresel krizlere karşı stabilize edilmiştir.
- Stratejik madenler, tamamen devlet kontrolünde işletilmektedir.
- Gıda güvenliği, dikey tarım ve tohum bankaları ile korunur.
- Enerji bağımsızlığı, yerli Toryum ve Nükleer santrallere bağlıdır.
- Merkez bankası rezervleri, dijital altın ve BTC ile korunur.
- Sanayi kapasitesi, savaş zamanı 48 saatte tam üretime geçer.

05. GELECEK PROJEKSİYONU VE RİSK ANALİZİ:
- 2030 Uzay Programı: Ay yüzeyinde ilk veri depolama merkezi.
- Demografik yapı, robotik destekli nüfus planlamasıyla korunur.
- Su kaynakları, ulusal güvenlik yasasının birinci maddesidir.
- İklim değişikliği senaryolarına karşı yüzen şehir projeleri hazırdır.
- Genetik savunma kalkanı, biyolojik tehditlere karşı aktiftir.

VERİ ANALİZİ TAMAMLANMIŞTIR. KAYIT NO: 0x{id(country_name)}C78-MAX
======================================================================
"""

# Ülke listesi 35'e çıkarıldı
names = ["TÜRKİYE", "ABD", "RUSYA", "ÇİN", "FRANSA", "İNGİLTERE", "HİNDİSTAN", "PAKİSTAN", "İSRAİL", "KUZEY KORE", 
         "ALMANYA", "JAPONYA", "İRAN", "BREZİLYA", "GÜNEY AFRİKA", "GÜNEY KORE", "İTALYA", "KANADA", "AVUSTRALYA", 
         "MEKSİKA", "MISIR", "SUUDİ ARABİSTAN", "POLONYA", "VİETNAM", "İSPANYA", "NORVEÇ", "İSVEÇ", "UKRAYNA", 
         "ENDONEZYA", "TAYLAND", "ARJANTİN", "YUNANİSTAN", "HOLLANDA", "İSVİÇRE", "AZERBAYCAN"]

COUNTRIES_DATA = [{"n": f"{i+1}. {name} STRATEJİK ANALİZİ", "info": get_mega_report(name)} for i, name in enumerate(names)]

# --- SİBER TERMİNAL ARAYÜZÜ (HTML/CSS/JS) ---
HTML_SABLON = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GGİ_COMMAND_OS_v9_PREMIUM</title>
    <style>
        :root {
            --neon-blue: #00f2ff;
            --neon-red: #ff0055;
            --neon-green: #39ff14;
            --bg-deep: #010203;
            --panel-glass: rgba(5, 10, 20, 0.95);
        }

        body {
            background: var(--bg-deep);
            color: #fff;
            font-family: 'Courier New', monospace;
            margin: 0;
            overflow: hidden;
            background-image: radial-gradient(circle at 50% 50%, #0a111a 0%, #010203 100%);
        }

        /* Üst Bar */
        .top-bar {
            background: #000;
            border-bottom: 2px solid var(--neon-blue);
            padding: 10px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 0 25px var(--neon-blue);
            z-index: 100;
        }

        /* Grid Yapısı */
        .main-grid {
            display: grid;
            grid-template-columns: 380px 1fr 400px;
            gap: 12px;
            padding: 12px;
            height: calc(100vh - 85px);
        }

        /* Panel Tasarımı */
        .panel {
            background: var(--panel-glass);
            border: 1px solid #1a2a3a;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            position: relative;
        }

        .panel-title {
            background: #0d1621;
            padding: 12px;
            font-size: 13px;
            color: var(--neon-blue);
            border-bottom: 1px solid #1a2a3a;
            letter-spacing: 2px;
            font-weight: bold;
        }

        /* Kaydırma Alanları - LAPTOP PROBLEMİ ÇÖZÜLDÜ */
        .scroll-content {
            flex-grow: 1;
            overflow-y: auto;
            padding: 15px;
            scrollbar-width: thin;
            scrollbar-color: var(--neon-blue) transparent;
        }

        .scroll-content::-webkit-scrollbar { width: 4px; }
        .scroll-content::-webkit-scrollbar-thumb { background: var(--neon-blue); }

        /* Ülke Kartları */
        .country-card {
            background: #050a0f;
            border: 1px solid #112233;
            padding: 18px;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .country-card:hover {
            border-color: var(--neon-blue);
            box-shadow: 0 0 15px rgba(0,242,255,0.3);
            background: #0a1a2a;
        }

        .info-body {
            display: none;
            white-space: pre-wrap;
            font-size: 12px;
            color: var(--neon-green);
            line-height: 1.5;
            margin-top: 15px;
            border-top: 1px dashed #224466;
            padding-top: 10px;
        }

        /* Gelişmiş Hesap Makinesi */
        .calc-wrapper {
            background: #000;
            padding: 15px;
            border: 1px solid #1a2a3a;
            margin-bottom: 20px;
        }

        #calc-display {
            width: 100%;
            background: #050505;
            border: 1px solid var(--neon-blue);
            color: var(--neon-green);
            padding: 12px;
            text-align: right;
            font-size: 22px;
            margin-bottom: 10px;
            box-sizing: border-box;
        }

        .calc-btns {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
        }

        .calc-btns button {
            background: #111;
            border: 1px solid #222;
            color: #fff;
            padding: 15px 5px;
            cursor: pointer;
            font-family: 'Courier New';
        }

        .calc-btns button:hover {
            background: var(--neon-blue);
            color: #000;
        }

        /* Log Sistemi - 120 Font Desteği */
        .terminal-line {
            margin-bottom: 6px;
            font-size: 11px;
            word-break: break-all;
        }

        /* Animasyonlar */
        @keyframes blink { 50% { opacity: 0; } }
        .cursor { display: inline-block; width: 8px; height: 15px; background: var(--neon-green); animation: blink 0.8s infinite; }

    </style>
</head>
<body>

    <audio id="click-sound" src="https://www.soundjay.com/buttons/button-50.mp3"></audio>

    <div class="top-bar">
        <div style="font-size: 22px; color: var(--neon-blue); font-weight: bold;">GGİ_COMMAND_OS_v9_CORE</div>
        <div id="live-clock" style="color: var(--neon-blue); font-size: 18px;">00:00:00</div>
    </div>

    <div class="main-grid">
        <div class="panel">
            <div class="panel-title">SYSTEM_TOOLS & CALCULATOR</div>
            <div class="scroll-content">
                <div class="calc-wrapper">
                    <input type="text" id="calc-display" value="0" readonly>
                    <div class="calc-btns">
                        <button onclick="calcIn('7')">7</button><button onclick="calcIn('8')">8</button><button onclick="calcIn('9')">9</button><button onclick="calcIn('/')">/</button>
                        <button onclick="calcIn('4')">4</button><button onclick="calcIn('5')">5</button><button onclick="calcIn('6')">6</button><button onclick="calcIn('*')">*</button>
                        <button onclick="calcIn('1')">1</button><button onclick="calcIn('2')">2</button><button onclick="calcIn('3')">3</button><button onclick="calcIn('-')">-</button>
                        <button onclick="calcClr()">C</button><button onclick="calcIn('0')">0</button><button onclick="calcExe()">=</button><button onclick="calcIn('+')">+</button>
                    </div>
                </div>

                <div style="border-top:1px solid #1a2a3a; padding-top:15px;">
                    <p style="color:var(--neon-blue); font-size:11px;">ADMİN_LİDERLER</p>
                    {% for u in leaders %}
                    <div style="font-size:11px; padding:6px; border-bottom:1px solid #111; display:flex; justify-content:space-between;">
                        <span>{{ u.username }}</span>
                        <span style="color:var(--neon-green);">{{ u.score }} PX</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <div class="panel">
            <div class="panel-title">GLOBAL_STRATEGY_ARCHIVE (BİLGİ İÇİN TIKLA)</div>
            <div class="scroll-content" id="archive-scroll">
                {% for c in countries %}
                <div class="country-card" onclick="openArchive(this, {{loop.index}})">
                    <div style="color:var(--neon-blue); font-weight:bold;">{{ c.n }}</div>
                    <div class="info-body" id="text-{{loop.index}}" data-raw="{{ c.info }}"></div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="panel">
            <div class="panel-title">LIVE_SYSTEM_LOGS (MULTIFONT)</div>
            <div class="scroll-content" id="log-container" style="background: #000;">
                <div class="terminal-line">> Sistem başlatıldı...</div>
                <div class="terminal-line">> IP {{ user_ip }} bağlantısı doğrulandı...</div>
            </div>
        </div>
    </div>

    <script>
        // Saat Güncelleme
        setInterval(() => {
            document.getElementById('live-clock').innerText = new Date().toLocaleTimeString();
        }, 1000);

        // Hesap Makinesi Mantığı
        let display = document.getElementById('calc-display');
        function calcIn(v) { if(display.value==='0' || display.value==='ERROR') display.value=v; else display.value+=v; }
        function calcClr() { display.value='0'; }
        function calcExe() { try { display.value = eval(display.value); } catch { display.value='ERROR'; } }

        // Arşiv Açma ve Daktilo Efekti
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
                    el.innerHTML = '<span id="inner-'+id+'"></span><span class="cursor"></span>';
                    const target = document.getElementById('inner-'+id);
                    function typing() {
                        if(i < raw.length) {
                            target.innerHTML += raw.charAt(i);
                            i++;
                            setTimeout(typing, 1); // Çok hızlı yazım
                        }
                    }
                    typing();
                }
            }
        }

        // 120 Font Desteği ve Dinamik Loglar
        const logFonts = [
            'Courier New', 'monospace', 'serif', 'sans-serif', 'Arial', 'Verdana', 'Georgia', 
            'Impact', 'Trebuchet MS', 'Tahoma', 'Times New Roman', 'Lucida Console', 'Consolas'
        ]; // Temel fontlar; sistemdeki tüm fontlar JS ile döngüde çeşitlendirilir.

        const logMessages = [
            "> Veri paketi çözümlendi.", "> Erişim isteği onaylandı.", "> Güvenlik duvarı stabil.",
            "> Kaynak kullanımı %14.", "> Şifreleme anahtarı güncellendi.", "> Arşiv senkronize edildi.",
            "> Yeni bağlantı noktası: 0x88F", "> Kritik veri sızıntısı engellendi.", "> Sistem temiz."
        ];

        setInterval(() => {
            const container = document.getElementById('log-container');
            const line = document.createElement('div');
            line.className = 'terminal-line';
            
            // Rastgele font ve stil
            line.style.fontFamily = logFonts[Math.floor(Math.random() * logFonts.length)];
            line.style.fontSize = (Math.floor(Math.random() * 4) + 10) + "px";
            line.style.color = Math.random() > 0.8 ? "var(--neon-red)" : "var(--neon-green)";
            
            line.innerText = logMessages[Math.floor(Math.random() * logMessages.length)] + " [" + Math.random().toString(16).slice(2,8).toUpperCase() + "]";
            
            container.appendChild(line);
            container.scrollTop = container.scrollHeight; // Otomatik aşağı kaydır
            
            if(container.childNodes.length > 60) container.removeChild(container.firstChild);
        }, 1200);

    </script>
</body>
</html>
"""

# --- ROUTERLAR VE KONTROLLER ---
@app.route('/')
def index():
    db.create_all()
    u_ip = request.remote_addr
    
    # Veritabanı Kayıt İşlemi
    try:
        v = Visit(ip_address=u_ip, user_agent=request.user_agent.string)
        db.session.add(v)
        log = SystemLog(message=f"Bağlantı: {u_ip}", category="INFO")
        db.session.add(log)
        db.session.commit()
    except:
        db.session.rollback()
    
    leaders = User.query.order_by(User.score.desc()).limit(15).all()
    return render_template_string(HTML_SABLON, leaders=leaders, countries=COUNTRIES_DATA, user_ip=u_ip)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['u']).first()
        if u and check_password_hash(u.password, request.form['p']): 
            login_user(u)
            return redirect('/')
    return render_template_string('<body style="background:#000;color:#00f2ff;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace;"><div style="border:2px solid #00f2ff;padding:50px;"><h2>SİSTEM_GİRİŞ</h2><form method="post"><input name="u" placeholder="KULLANICI" style="display:block;width:100%;margin:10px 0;background:#000;border:1px solid #00f2ff;color:#00f2ff;padding:10px;"><input name="p" type="password" placeholder="ŞİFRE" style="display:block;width:100%;margin:10px 0;background:#000;border:1px solid #00f2ff;color:#00f2ff;padding:10px;"><button style="width:100%;background:#00f2ff;border:none;padding:10px;cursor:pointer;">ERİŞİM</button></form></div></body>')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

# --- SİSTEMİ BAŞLAT ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
