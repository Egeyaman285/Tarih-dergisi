import os
import datetime
import random
import time
import base64
import json
import math
from flask import Flask, render_template_string, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ggi-ultra-v21-genesis-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ggi_v21_final.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SystemUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    access_level = db.Column(db.String(20), default="LEVEL_A")
    score = db.Column(db.Integer, default=10000)
    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200))
    ip_addr = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class SecretFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    content_hash = db.Column(db.String(500))
    clearance = db.Column(db.String(20))

STRATEGIC_INTEL = {
    "TÜRKİYE": "[KOZMİK SEVİYE]\\nANALİZ: Bölgesel Güç Projeksiyonu.\\n- İHA/SİHA: Dünya lideri otonom sistemler.\\n- HAVA SAVUNMA: Çelik Kubbe (SİPER-2, HİSAR-U).\\n- DENİZ: TCG Anadolu ve TF-2000 projesi.\\n- SİBER: Milli Muharip İşlemci ve Kuantum Kripto.\\n- UZAY: Yerli roket motoru ve ay görevi faz-1.\\n- EKONOMİ: Savunma ihracatı 6 milyar dolar.\\n- DİPLOMASİ: 5 kıtada aktif askeri varlık.\\n- YERLİ: KAAN 5. nesil savaş uçağı.\\n- ROKET: Çakır füze sistemi.\\n- DENİZALTI: Reis sınıfı projesi.",
    
    "ABD": "[TOP SECRET]\\nANALİZ: Küresel Dominans.\\n- NÜKLEER: 11 Uçak gemisi, Trident-II füzeleri.\\n- SİBER: NSA küresel dinleme ve sıfır-gün açıkları.\\n- EKONOMİ: Rezerv para birimi manipülasyonu.\\n- TEKNOLOJİ: Starlink v3 ve Mars kolonizasyon hazırlığı.\\n- UZAY: Space Force operasyonel üstünlük.\\n- ASKERİ: 750+ denizaşırı askeri üs.\\n- BÜTÇE: 877 milyar dolar savunma harcaması.\\n- ZEKA: CIA, NSA, DIA entegre operasyon.\\n- DRONE: MQ-9 Reaper küresel varlık.\\n- F-35: 450+ adet operasyonel.",
    
    "RUSYA": "[SIGMA-9]\\nANALİZ: Stratejik Caydırıcılık.\\n- FÜZE: Zircon (Mach 9), Avangard hipersonik.\\n- ENERJİ: Gazprom üzerinden jeopolitik baskı.\\n- SİBER: GRU siber harp ve dezenformasyon ağları.\\n- ARKTİK: Buzkıran filosu ve Kuzey Deniz yolu kontrolü.\\n- NÜKLEER: 5977 nükleer başlık envanteri.\\n- HAVA: Su-57 Felon 5. nesil savaş uçağı.\\n- DENİZ: Poseidon nükleer torpido sistemi.\\n- WAGNER: Özel kuvvetler proxy operasyonları.\\n- S-400: 120+ batarya ihracat.\\n- YASEN: M sınıfı nükleer denizaltı.",
    
    "ÇİN": "[RED-DRAGON]\\nANALİZ: Ekonomik Hegemonya.\\n- ÜRETİM: Dünyanın sanayi motoru.\\n- TEKNOLOJİ: 6G ve Kuantum haberleşme uyduları.\\n- DONANMA: Tip 004 nükleer uçak gemisi projesi.\\n- SOSYAL: Yapay zeka destekli gözetim toplumu.\\n- EKONOMİ: 17.9 trilyon dolar GSYİH.\\n- UZAY: Tiangong uzay istasyonu operasyonel.\\n- ASKERİ: 2 milyon aktif personel.\\n- KUŞAK YOL: 150+ ülke altyapı hakimiyeti.\\n- J-20: 5. nesil 200+ adet.\\n- DF-41: ICBM 15000 km menzil.",
    
    "İNGİLTERE": "[MI6-ALPHA]\\nANALİZ: Finansal İstihbarat.\\n- SİBER: GCHQ veri toplama merkezleri.\\n- DONANMA: Astute sınıfı nükleer denizaltılar.\\n- DİPLOMASİ: Commonwealth üzerinden yumuşak güç.\\n- HAVA: F-35B Lightning II filosu.\\n- İSTİHBARAT: Five Eyes ağı kurucu üyesi.\\n- NÜKLEER: Vanguard sınıfı SSBN platformu.\\n- ŞEHİR: Londra küresel finans merkezi.\\n- SAS: Özel kuvvetler elit birliği.\\n- TYPE 26: Yeni nesil fırkateyn.\\n- TEMPEST: 6. nesil savaş uçağı projesi.",
    
    "FRANSA": "[OMEGA-FR]\\nANALİZ: Avrupa Askeri Gücü.\\n- NÜKLEER: Bağımsız caydırıcı güç, 290 başlık.\\n- HAVA: Rafale F4 çok rollü üstünlük.\\n- DENİZ: Charles de Gaulle uçak gemisi.\\n- UZAY: Ariane 6 fırlatma sistemi.\\n- SİBER: ANSSI ulusal siber güvenlik.\\n- LEJYON: Yabancılar Birliği elit güç.\\n- SAHEL: Afrika operasyonel varlık.\\n- SCALP: Seyir füzesi yetenekleri.\\n- FREMM: Fırkateyn ihracatı.\\n- BARRACUDA: Nükleer denizaltı sınıfı.",
    
    "ALMANYA": "[BUNDESWEHR-X]\\nANALİZ: Avrupa Sanayi Devi.\\n- EKONOMİ: 4.3 trilyon dolar GSYİH.\\n- TEKNOLOJİ: Endüstri 4.0 öncüsü.\\n- HAVA: Eurofighter Typhoon ve F-35A.\\n- TANK: Leopard 2A7+ dünya standardı.\\n- SİBER: BSI federal siber güvenlik.\\n- SAVUNMA: Rheinmetall, Krauss-Maffei.\\n- NATO: Avrupa NATO omurgası.\\n- PUMA: Yeni nesil piyade savaş aracı.\\n- U-212: AIP denizaltı teknolojisi.\\n- FCAS: 6. nesil savaş uçağı ortaklığı.",
    
    "İSRAİL": "[MOSSAD-ULTRA]\\nANALİZ: İstihbarat Üstünlüğü.\\n- SİBER: Unit 8200 küresel siber elit.\\n- HAVA: Iron Dome, David's Sling savunma.\\n- İSTİHBARAT: Mossad operasyonel mükemmellik.\\n- TEKNOLOJİ: Start-up Nation inovasyon.\\n- NÜKLEER: Dimona tesisi (80-400 başlık).\\n- DRONE: Hermes, Heron İHA sistemleri.\\n- F-35I: Adir özel modifikasyon.\\n- ARROW: Balistik füze savunması.\\n- MERKAVA: Mk.4 ana muharebe tankı.\\n- DOLPHIN: Nükleer denizaltı filosu.",
    
    "JAPONYA": "[RISING-SUN]\\nANALİZ: Teknoloji ve Deniz Gücü.\\n- TEKNOLOJİ: Robotik, yarı iletken liderliği.\\n- DONANMA: İzumo sınıfı F-35B platformu.\\n- HAVA: F-35A/B ve F-15J modernizasyonu.\\n- EKONOMİ: 4.9 trilyon dolar GSYİH.\\n- UZAY: H3 roketi ve lunar explorer.\\n- SİBER: NISC ulusal siber merkezi.\\n- YENİ: F-X 6. nesil savaş uçağı projesi.\\n- AEGIS: 8 Aegis destroyeri filosu.\\n- SORYU: AIP denizaltı teknolojisi.\\n- MITSUBISHI: Savunma sanayii devi.",
    
    "HİNDİSTAN": "[BRAHMOS-NET]\\nANALİZ: Yükselen Süper Güç.\\n- NÜKLEER: Agni-V ICBM 5000+ km menzil.\\n- UZAY: Chandrayaan-3 ay başarısı.\\n- DONANMA: INS Vikrant yerli uçak gemisi.\\n- FÜZE: BrahMos süpersonik 290+ adet.\\n- ASKERİ: 1.45 milyon aktif personel.\\n- EKONOMİ: 3.7 trilyon dolar, 5. büyük.\\n- SİBER: CERT-In ulusal ekip.\\n- TEJAS: Yerli hafif savaş uçağı.\\n- ARIHANT: Nükleer denizaltı programı.\\n- RAFALE: 36 adet tedarik edildi.",
    
    "GÜNEY KORE": "[K-DEFENSE]\\nANALİZ: Teknoloji İhracatçısı.\\n- TANK: K2 Black Panther dünya ihracatı.\\n- HAVA: KF-21 Boramae yerli 4.5 nesil.\\n- DONANMA: KDDX destroyeri projesi.\\n- SİBER: KISA siber güvenlik ajansı.\\n- EKONOMİ: Samsung, LG teknoloji devleri.\\n- SAVUNMA: Hanwha Defense sistemleri.\\n- FÜZE: Hyunmoo balistik füze ailesi.\\n- K9: Thunder obüs dünya lideri.\\n- KSS-III: Yerli denizaltı programı.\\n- FA-50: Eğitim uçağı ihracatı.",
    
    "İTALYA": "[MARE-NOSTRUM]\\nANALİZ: Akdeniz Deniz Gücü.\\n- DONANMA: Trieste LHD amfibi saldırı gemisi.\\n- HAVA: F-35A/B Lightning II programı ortağı.\\n- SAVUNMA: Leonardo savunma konglomerası.\\n- EKONOMİ: 2.1 trilyon dolar GSYİH.\\n- FINCANTIERI: Gemi inşa dünya devi.\\n- FREMM: Fırkateyn ihracat başarısı.\\n- ARIETE: Ana muharebe tankı.\\n- CENTAURO: Tekerlikli zırhlı araç.\\n- CAVOUR: Uçak gemisi modernizasyonu.\\n- ASTER: Hava savunma füzesi.",
    
    "İSPANYA": "[IBERIA-GUARD]\\nANALİZ: Akdeniz-Atlantik Köprüsü.\\n- DONANMA: S-80 Plus AIP denizaltı yerli.\\n- HAVA: Eurofighter Typhoon ve F-35B.\\n- TANK: Leopard 2E modernizasyonu.\\n- EKONOMİ: 1.5 trilyon dolar GSYİH.\\n- NAVANTIA: Gemi inşa ve savunma.\\n- NATO: İber-Atlantik stratejik konum.\\n- F-110: Yeni nesil fırkateyn projesi.\\n- TAURUS: Seyir füzesi entegrasyonu.\\n- JC CARLOS: Amfibi saldırı gemisi.\\n- LEOPARD: 2A6E 327 adet envanteri.",
    
    "POLONYA": "[EAGLE-FORTRESS]\\nANALİZ: Doğu Avrupa Kalkanı.\\n- TANK: K2 Black Panther 1000+ sipariş.\\n- HAVA: F-35A Lightning II 32 adet.\\n- FÜZE: Patriot ve HIMARS bataryaları.\\n- ASKERİ: 202 bin aktif personel.\\n- ABRAMS: M1A2 SEPv3 250 adet.\\n- NATO: Rusya sınırı ileri savunma.\\n- FA-50: 48 adet eğitim uçağı.\\n- K9: Thunder obüs 212 adet.\\n- BORSUK: Yerli piyade aracı.\\n- WISLA: Hava savunma sistemi.",
    
    "AVUSTRALYA": "[SOUTHERN-CROSS]\\nANALİZ: Indo-Pasifik Gücü.\\n- DONANMA: AUKUS SSN-AUKUS nükleer denizaltı.\\n- HAVA: F-35A Lightning II 72 adet.\\n- İSTİHBARAT: ASIS gizli servis.\\n- SİBER: ACSC siber güvenlik merkezi.\\n- UZAY: Pine Gap uydu istasyonu.\\n- FIVE EYES: İstihbarat ağı üyesi.\\n- HUNTER: Fırkateyn programı 9 adet.\\n- BOXER: Zırhlı araç platformu.\\n- ANZAC: Fırkateyn sınıfı modernizasyonu.\\n- JASSM: Uzun menzil seyir füzesi.",
    
    "KANADA": "[MAPLE-SHIELD]\\nANALİZ: Kuzey Amerika Savunması.\\n- HAVA: CF-18 Hornet filosu.\\n- ARKTİK: Kuzey geçidi güvenliği.\\n- İSTİHBARAT: CSIS istihbarat servisi.\\n- SAVUNMA: NORAD entegrasyonu.\\n- SİBER: Canadian Cyber Security Centre.\\n- F-35: 88 adet sipariş onaylandı.\\n- HALIFAX: Fırkateyn sınıfı modernizasyonu.\\n- LAV: Hafif zırhlı araç üretimi.\\n- LEOPARD: 2A4/2A6 tank filosu.\\n- CHINOOK: CH-147F ağır helikopter.",
    
    "BREZİLYA": "[AMAZON-FORCE]\\nANALİZ: Güney Amerika Lideri.\\n- HAVA: Gripen NG üretimi yerli.\\n- DONANMA: Riachuelo denizaltı sınıfı.\\n- EKONOMİ: 2.1 trilyon dolar GSYİH.\\n- UZAY: Alcântara fırlatma merkezi.\\n- SAVUNMA: Embraer A-29 Super Tucano.\\n- AMAZON: Orman gözetleme sistemi.\\n- KC-390: Nakliye uçağı ihracatı.\\n- ASTROS: Çok namlulu roketatar.\\n- GUARANI: Zırhlı personel taşıyıcı.\\n- MECTRON: Füze sistemleri.",
    
    "PAKİSTAN": "[ATOMIC-SHIELD]\\nANALİZ: Nükleer Denge Gücü.\\n- NÜKLEER: Shaheen-III füze 2750 km.\\n- HAVA: JF-17 Thunder çok rollü.\\n- ASKERİ: 654 bin aktif personel.\\n- İSTİHBARAT: ISI istihbarat örgütü.\\n- FÜZE: Babur seyir füzesi.\\n- TANK: Al-Khalid ana muharebe tankı.\\n- NÜKLEER: 170+ nükleer başlık.\\n- AGOSTA: 90B denizaltı sınıfı.\\n- F-16: Block 52 52 adet.\\n- ANZA: Omuz güdümlü füze.",
    
    "İRAN": "[PERSIAN-SHADOW]\\nANALİZ: Asimetrik Strateji Uzmanı.\\n- FÜZE: Balistik füze 2000+ envanter.\\n- DRONE: Shahed-136 kamikaze İHA.\\n- SİBER: Siber savaş yetenekleri.\\n- DENİZ: Hürmüz Boğazı kontrolü.\\n- NÜKLEER: Uranyum zenginleştirme.\\n- PROXY: Bölgesel vekil güçler.\\n- FATEH: 110 balistik füze ailesi.\\n- KHORDAD: Hava savunma sistemi.\\n- GHADIR: Mini denizaltı sınıfı.\\n- MOUDGE: Yerli fırkateyn sınıfı.",
    
    "MISIR": "[PHARAOH-NET]\\nANALİZ: Bölgesel Otorite.\\n- STRATEJİK: Suez Kanalı güvenliği.\\n- HAVA: Rafale 30 adet ve MiG-29M.\\n- DONANMA: Mistral LHD 2 adet.\\n- ASKERİ: 440 bin aktif personel.\\n- TANK: M1A1 Abrams 1130 adet.\\n- F-16: Block 40 220+ adet.\\n- GOWIND: Corvette gemileri.\\n- KA-52: Alligator saldırı helikopteri.\\n- S-300VM: Hava savunma sistemi.\\n- WING LOONG: Silahlı İHA filosu."
}

ALL_DATA = [{"n": f"{k} STRATEJİK ANALİZ", "i": v} for k, v in STRATEGIC_INTEL.items()]

def process_system_heartbeat():
    pulse = math.sin(time.time()) * 100
    return pulse

def calculate_encryption_entropy(data_stream):
    if not data_stream: return 0.99
    return len(set(data_stream)) / len(data_stream)

def validate_root_access(token):
    expected = base64.b64encode("ADMİN_EGE".encode('utf-8'))
    return token == expected

def rotate_security_keys():
    new_key = "".join([random.choice("ABCDEF0123456789") for _ in range(32)])
    return new_key

def monitor_thermal_levels():
    return random.uniform(35.5, 72.4)

def optimize_neural_network():
    layers = ["INPUT", "HIDDEN_1", "HIDDEN_2", "OUTPUT"]
    for layer in layers:
        time.sleep(0.0001)
    return "OPTIMIZED"

def log_kernel_event(event_type, description):
    timestamp = datetime.datetime.now()
    return f"[{timestamp}] KERNEL_{event_type}: {description}"

def check_database_integrity():
    try:
        users = SystemUser.query.count()
        return True
    except:
        return False

def generate_noise_buffer():
    return [random.random() for _ in range(100)]

def execute_cyber_defense_v21():
    status = "DEFENSE_ACTIVE"
    entropy = calculate_encryption_entropy("GGI_PULSE")
    return f"{status}_{entropy}"

def sys_init_core_01(): return "CORE_ACTIVE"
def sys_init_core_02(): return "MEMORY_READY"
def sys_init_core_03(): return "IO_BUFFERED"
def sys_init_core_04(): return "THREAD_SYNC"
def sys_init_core_05(): return "SOCKET_OPEN"
def sys_init_core_06(): return "UI_SYNCED"
def sys_init_core_07(): return "SECURITY_UP"
def sys_init_core_08(): return "API_STABLE"
def sys_init_core_09(): return "ENV_VAR_LOADED"
def sys_init_core_10(): return "SYS_HEALTH_OK"

def background_proc_11(): return rotate_security_keys()
def background_proc_12(): return monitor_thermal_levels()
def background_proc_13(): return check_database_integrity()
def background_proc_14(): return process_system_heartbeat()
def background_proc_15(): return generate_noise_buffer()
def background_proc_16(): return execute_cyber_defense_v21()
def background_proc_17(): return optimize_neural_network()
def background_proc_18(): return log_kernel_event("PING", "STABLE")
def background_proc_19(): return validate_root_access(b"NONE")
def background_proc_20(): return calculate_encryption_entropy("GGI")

UI_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>GGI_SUPREME_OS_v21</title>
<style>
:root{--b:#00f2ff;--g:#39ff14;--r:#f05;--bg:#010203;--p:rgba(10,25,45,0.9);--y:#ff0;--m:#f0f}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent;margin:0;padding:0}
body,html{background:var(--bg);color:#fff;font-family:'Courier New',monospace;height:100vh;width:100vw;overflow:hidden;font-size:14px}
@media(max-width:768px){body,html{font-size:12px}}
#matrix{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;opacity:0.15}
header{height:55px;border-bottom:2px solid var(--b);display:flex;align-items:center;justify-content:space-between;padding:0 20px;background:#000;box-shadow:0 0 25px var(--b)}
@media(max-width:768px){header{height:50px;padding:0 15px}}
main{display:grid;grid-template-columns:1fr;gap:10px;padding:10px;height:calc(100vh - 55px);overflow-y:auto}
@media(min-width:769px){main{grid-template-columns:300px 1fr 340px;overflow-y:hidden}}
.panel{background:var(--p);border:1px solid #1a2a3a;display:flex;flex-direction:column;border-radius:6px;margin-bottom:10px;min-height:250px}
@media(min-width:769px){.panel{margin-bottom:0;height:100%}}
.panel-h{background:linear-gradient(90deg,#0a111a,#1a2a3a);padding:12px;color:var(--b);font-size:13px;font-weight:bold;border-bottom:2px solid #1a2a3a;display:flex;justify-content:space-between}
.scroll-area{flex:1;overflow-y:auto;padding:12px;scrollbar-width:thin;scrollbar-color:var(--b) transparent}
.card{background:rgba(5,15,25,0.8);border:1px solid #112233;margin-bottom:10px;padding:12px;cursor:pointer;transition:0.3s;border-radius:4px;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;left:0;top:0;height:100%;width:3px;background:var(--b);opacity:0;transition:0.3s}
.card:hover::before{opacity:1}
.card:active{transform:scale(0.98)}
.card:hover{border-color:var(--b);transform:translateX(5px)}
.intel-box{display:none;color:var(--g);font-size:11px;white-space:pre-wrap;margin-top:10px;border-top:1px dashed #224466;padding-top:8px;line-height:1.5}
.stat-row{margin-bottom:10px;font-size:11px;letter-spacing:0.5px}
.stat-bar{height:6px;background:#050505;border:1px solid #111;margin-top:5px;border-radius:3px;overflow:hidden}
.stat-fill{height:100%;width:0%;background:var(--b);transition:0.8s cubic-bezier(0.4,0,0.2,1)}
.term-input-box{background:#000;border-top:1px solid #1a2a3a;padding:10px;display:flex;align-items:center}
#term-cmd{background:transparent;border:none;color:var(--g);width:100%;outline:none;font-size:13px;font-family:inherit}
@media(max-width:768px){#term-cmd{font-size:15px}}
.log{font-size:11px;margin-bottom:5px;border-left:2px solid transparent;padding-left:6px;line-height:1.4;word-break:break-word}
.log.err{color:var(--r);border-left-color:var(--r);background:rgba(255,0,85,0.05)}
.log.valid{color:var(--g);border-left-color:var(--g)}
.log.sys-blue{color:var(--b);border-left-color:var(--b)}
.log.sys-magenta{color:var(--m);border-left-color:var(--m)}
#secret-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.98);z-index:9999;display:none;align-items:center;justify-content:center;animation:fadeIn 0.3s}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.secret-ui{width:96%;max-width:1100px;height:92%;border:3px solid var(--r);background:linear-gradient(135deg,#050000,#0a0000);padding:25px;overflow-y:auto;box-shadow:0 0 100px var(--r),inset 0 0 60px rgba(255,0,85,0.15);border-radius:10px;animation:glowPulse 2.5s infinite;position:relative}
@keyframes glowPulse{0%,100%{box-shadow:0 0 100px var(--r),inset 0 0 60px rgba(255,0,85,0.15)}50%{box-shadow:0 0 150px var(--r),inset 0 0 80px rgba(255,0,85,0.25)}}
@media(min-width:769px){.secret-ui{padding:45px}}
.glitch-text{animation:glitch 0.35s infinite;color:var(--r);text-shadow:3px 3px #500,-3px -3px #005,0 0 20px var(--r);font-size:22px;text-align:center;margin-bottom:15px;font-weight:bold;letter-spacing:2px}
@media(min-width:769px){.glitch-text{font-size:32px;margin-bottom:25px}}
@keyframes glitch{0%{transform:translate(0)}15%{transform:translate(-4px,4px)}30%{transform:translate(4px,-4px)}45%{transform:translate(-4px,-4px)}60%{transform:translate(4px,4px)}75%{transform:translate(-2px,2px)}100%{transform:translate(0)}}
.secret-warning{text-align:center;color:var(--y);font-size:12px;margin-bottom:20px;animation:blink 1.2s infinite;text-transform:uppercase;letter-spacing:2px;text-shadow:0 0 10px var(--y)}
@media(min-width:769px){.secret-warning{font-size:15px;margin-bottom:30px}}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
.secret-data{display:grid;grid-template-
