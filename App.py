import os
from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ggi-gizli-anahtar'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ggi_arsiv.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- MODELLER ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- HTML ŞABLONU (Tek Parça) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GGİ - Genç Girişimci</title>
    <style>
        body { background: #121212; color: white; font-family: sans-serif; margin: 0; }
        .nav { background: #1f1f1f; padding: 15px; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 24px; font-weight: bold; color: #00ff88; }
        .container { display: flex; padding: 20px; gap: 20px; }
        .game-side { flex: 2; background: #1f1f1f; padding: 20px; border-radius: 10px; text-align: center; }
        .leaderboard { flex: 1; background: #1f1f1f; padding: 20px; border-radius: 10px; }
        canvas { background: #333; border: 2px solid #00ff88; display: block; margin: 0 auto; }
        .btn { background: #00ff88; color: black; padding: 10px; text-decoration: none; border-radius: 5px; border:none; cursor:pointer;}
    </style>
</head>
<body>
    <div class="nav">
        <div class="logo">GGİ - Genç Girişimci</div>
        <div>
            {% if current_user.is_authenticated %}
                <span>Hoş geldin, {{ current_user.username }}!</span> | <a href="/logout" style="color:white">Çıkış</a>
            {% else %}
                <a href="/login" style="color:white">Giriş Yap</a> | <a href="/register" style="color:white">Kayıt Ol</a>
            {% endif %}
        </div>
    </div>

    <div class="container">
        <div class="game-side">
            <h2>Engellerden Atla! (Boşluk Tuşu)</h2>
            <canvas id="gameCanvas" width="600" height="300"></canvas>
        </div>
        
        <div class="leaderboard">
            <h3>🏆 En İyi 10 (Liderler)</h3>
            {% for user in leaders %}
                <p>{{ loop.index }}. {{ user.username }} - <b>{{ user.score }}</b></p>
            {% endfor %}
        </div>
    </div>

    <script>
        const canvas =
