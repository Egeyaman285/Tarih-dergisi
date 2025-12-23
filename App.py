from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Güvenlik için SECRET_KEY gerekli
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cokgizlibirkey') 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db') # Veritabanı
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Giriş yapılmamışsa yönlendirilecek sayfa

# Kullanıcı Modeli (Veritabanı Tablosu)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    high_score = db.Column(db.Integer, default=0) # Kullanıcının en yüksek skoru

# Kullanıcı yükleyici (Flask-Login için zorunlu)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROUTES (Sayfalar) ---

@app.before_first_request
def create_tables():
    db.create_all() # Uygulama ilk çalıştığında veritabanı tablolarını oluştur

@app.route('/')
def index():
    # Ana sayfa: GGİ logosu, oyun ve skor tablosu için iskelet
    top_scores = User.query.order_by(User.high_score.desc()).limit(10).all()
    return render_template('index.html', top_scores=top_scores)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        
        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Hesabınız başarıyla oluşturuldu! Giriş yapabilirsiniz.', 'success')
            return redirect(url_for('login'))
        except:
            flash('Bu kullanıcı adı zaten alınmış!', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Giriş başarısız. Kullanıcı adı veya şifre hatalı.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/settings')
@login_required
def settings():
    # Ayarlar sayfası (şu an boş, sonra eklenecek)
    return render_template('settings.html')

@app.route('/submit_score', methods=['POST'])
@login_required
def submit_score():
    score = int(request.form.get('score'))
    if score > current_user.high_score:
        current_user.high_score = score
        db.session.commit()
        flash('Yeni yüksek skorunuz kaydedildi!', 'success')
    return redirect(url_for('index'))

# --- Uygulamayı Çalıştır ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True) # debug=True sadece geliştirme aşamasında kullanılır)
