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
    "TÜRKİYE": "[KOZMİK SEVİYE]\nANALİZ: Bölgesel Güç Projeksiyonu.\n- İHA/SİHA: Dünya lideri otonom sistemler.\n- HAVA SAVUNMA: Çelik Kubbe (SİPER-2, HİSAR-U).\n- DENİZ: TCG Anadolu ve TF-2000 projesi.\n- SİBER: Milli Muharip İşlemci ve Kuantum Kripto.\n- UZAY: Yerli roket motoru ve ay görevi faz-1.\n- EKONOMİ: Savunma ihracatı 6 milyar dolar.\n- DİPLOMASİ: 5 kıtada aktif askeri varlık.",
    "ABD": "[TOP SECRET]\nANALİZ: Küresel Dominans.\n- NÜKLEER: 11 Uçak gemisi, Trident-II füzeleri.\n- SİBER: NSA küresel dinleme ve sıfır-gün açıkları.\n- EKONOMİ: Rezerv para birimi manipülasyonu.\n- TEKNOLOJİ: Starlink v3 ve Mars kolonizasyon hazırlığı.\n- UZAY: Space Force operasyonel üstünlük.\n- ASKERİ: 750+ denizaşırı askeri üs.\n- BÜTÇE: 877 milyar dolar savunma harcaması.",
    "RUSYA": "[SIGMA-9]\nANALİZ: Stratejik Caydırıcılık.\n- FÜZE: Zircon (Mach 9), Avangard.\n- ENERJİ: Gazprom üzerinden jeopolitik baskı.\n- SİBER: GRU siber harp ve dezenformasyon ağları.\n- ARKTİK: Buzkıran filosu ve Kuzey Deniz yolu kontrolü.\n- NÜKLEER: 5977 nükleer başlık envanteri.\n- HAVA: Su-57 Felon 5. nesil savaş uçağı.\n- DENİZ: Poseidon nükleer torpido sistemi.",
    "ÇİN": "[RED-DRAGON]\nANALİZ: Ekonomik Hegemonya.\n- ÜRETİM: Dünyanın sanayi motoru.\n- TEKNOLOJİ: 6G ve Kuantum haberleşme uyduları.\n- DONANMA: Tip 004 nükleer uçak gemisi projesi.\n- SOSYAL: Yapay zeka destekli gözetim toplumu.\n- EKONOMİ: 17.9 trilyon dolar GSYİH.\n- UZAY: Tiangong uzay istasyonu operasyonel.\n- ASKERİ: 2 milyon aktif personel.",
    "İNGİLTERE": "[MI6-ALPHA]\nANALİZ: Finansal İstihbarat.\n- SİBER: GCHQ veri toplama merkezleri.\n- DONANMA: Astute sınıfı nükleer denizaltılar.\n- DİPLOMASİ: Commonwealth üzerinden yumuşak güç.\n- HAVA: F-35B Lightning II filosu.\n- İSTİHBARAT: Five Eyes ağı kurucu üyesi.\n- NÜKLEER: Vanguard sınıfı SSBN platformu.",
    "FRANSA": "[NIVEAU_OMEGA]\nANALİZ: Avrupa Gücü.\n- NÜKLEER: Bağımsız caydırıcı güç.\n- HAVA: Rafale çok rollü üstünlük.\n- DENİZ: Charles de Gaulle uçak gemisi.\n- UZAY: Ariane 6 fırlatma sistemi.\n- SİBER: ANSSI ulusal siber güvenlik.\n- ASKERİ: Lejyon Yabancılar Birliği elit güç.",
    "ALMANYA": "[BUNDESWEHR_CLASSIFIED]\nANALİZ: Sanayi Devi.\n- EKONOMİ: Avrupa'nın ekonomik motoru.\n- TEKNOLOJİ: Endüstri 4.0 öncüsü.\n- HAVA: Eurofighter Typhoon programı.\n- TANK: Leopard 2A7+ dünya standardı.\n- SİBER: BSI federal siber güvenlik.\n- SAVUNMA: Rheinmetall savunma sanayii devi.",
    "İSRAİL": "[MOSSAD_ULTRA]\nANALİZ: İstihbarat Üstünlüğü.\n- SİBER: Unit 8200 küresel siber elit.\n- HAVA: Iron Dome hava savunma.\n- İSTİHBARAT: Mossad operasyonel mükemmellik.\n- TEKNOLOJİ: Start-up Nation inovasyon.\n- NÜKLEER: Dimona tesisi (resmi olmayan).\n- ASKERİ: Zorunlu askerlik sistemi.",
    "JAPONYA": "[RISING_SUN_CLASSIFIED]\nANALİZ: Teknoloji Lideri.\n- TEKNOLOJİ: Robotik ve yarı iletken hakimiyeti.\n- DONANMA: İzumo sınıfı helikopter destroyeri.\n- HAVA: F-35A/B programı katılımcısı.\n- EKONOMİ: 4.9 trilyon dolar GSYİH.\n- UZAY: H3 roketi geliştirme.\n- SİBER: NISC ulusal siber merkezi.\n- SAVUNMA: Mitsubishi F-X 6. nesil proje.",
    "HİNDİSTAN": "[BRAHMOS_PROTOCOL]\nANALİZ: Yükselen Güç.\n- NÜKLEER: Agni-V ICBM kapasitesi.\n- UZAY: Chandrayaan ay programı.\n- DONANMA: INS Vikrant yerli uçak gemisi.\n- FÜZE: BrahMos süpersonik füze.\n- ASKERİ: 1.4 milyon aktif personel.\n- EKONOMİ: 3.7 trilyon dolar GSYİH.\n- SİBER: CERT-In ulusal siber ekip.",
    "GÜNEY KORE": "[K-DEFENSE_CLASSIFIED]\nANALİZ: Teknoloji İhracatçısı.\n- TANK: K2 Black Panther tank ihracatı.\n- HAVA: KF-21 Boramae yerli savaş uçağı.\n- DONANMA: KDDX destroyeri projesi.\n- SİBER: KISA siber güvenlik ajansı.\n- EKONOMİ: Samsung, LG teknoloji devleri.\n- SAVUNMA: Hanwha Defense sistemleri.\n- FÜZE: Hyunmoo balistik füze ailesi.",
    "İRAN": "[PERSIAN_SHADOW]\nANALİZ: Asimetrik Strateji.\n- FÜZE: Balistik füze envanteri.\n- DRONE: Shahed serisi İHA/SİHA.\n- SİBER: Siber savaş yetenekleri.\n- DENİZ: Hürmüz Boğazı kontrolü.\n- NÜKLEER: Uranyum zenginleştirme programı.\n- PROXY: Bölgesel vekil güçler ağı.",
    "PAKİSTAN": "[ATOMIC_SHIELD]\nANALİZ: Nükleer Denge.\n- NÜKLEER: Shaheen serisi füzeler.\n- HAVA: JF-17 Thunder çok rollü.\n- ASKERİ: 654 bin aktif personel.\n- İSTİHBARAT: ISI istihbarat örgütü.\n- FÜZE: Babur seyir füzesi.\n- TANK: Al-Khalid ana muharebe tankı.",
    "BREZİLYA": "[AMAZON_PROTOCOL]\nANALİZ: Güney Amerika Lideri.\n- HAVA: Gripen NG üretimi.\n- DONANMA: Riachuelo sınıfı denizaltı.\n- EKONOMİ: 2.1 trilyon dolar GSYİH.\n- UZAY: Alcântara fırlatma merkezi.\n- SAVUNMA: Embraer savunma sistemleri.",
    "KANADA": "[MAPLE_SHIELD]\nANALİZ: NATO Ortağı.\n- HAVA: CF-18 Hornet filosu.\n- ARKTİK: Kuzey geçidi güvenliği.\n- İSTİHBARAT: CSIS istihbarat servisi.\n- SAVUNMA: NORAD entegrasyonu.\n- SİBER: Canadian Centre for Cyber Security.",
    "AVUSTRALYA": "[SOUTHERN_CROSS]\nANALİZ: Indo-Pasifik Gücü.\n- DONANMA: AUKUS Paktı SSN-AUKUS denizaltı.\n- HAVA: F-35A Lightning II filosu.\n- İSTİHBARAT: ASIS istihbarat örgütü.\n- SİBER: ACSC siber güvenlik merkezi.\n- UZAY: Pine Gap uydu istasyonu.",
    "İTALYA": "[MARE_NOSTRUM]\nANALİZ: Akdeniz Gücü.\n- DONANMA: Trieste LHD ve PPA gemileri.\n- HAVA: F-35A/B programı ortağı.\n- SAVUNMA: Leonardo savunma konglomerası.\n- EKONOMİ: 2.1 trilyon dolar GSYİH.",
    "POLONYA": "[EAGLE_FORTRESS]\nANALİZ: Doğu Kalkanı.\n- TANK: K2 ve M1A2 Abrams alımları.\n- HAVA: F-35A sipariş 32 adet.\n- FÜZE: Patriot hava savunma bataryaları.\n- ASKERİ: 202 bin aktif personel.",
    "MISIR": "[PHARAOH_PROTOCOL]\nANALİZ: Bölgesel Güç.\n- STRATEJİK: Suez Kanalı güvenliği.\n- HAVA: Rafale ve MiG-29 karması.\n- DONANMA: Mistral sınıfı LHD gemileri.\n- ASKERİ: 440 bin aktif personel.",
    "AZERBAYCAN": "[KARABAKH_VICTORY]\nANALİZ: Drone Savaşı Öncüsü.\n- DRONE: Akıncı ve TB2 entegrasyonu.\n- HAVA: Su-25 yakın hava desteği.\n- EKONOMİ: Enerji ihracatı merkezi.\n- ASKERİ: 2020 zafer tecrübesi.",
    "KATAR": "[GAS_GIANT]\nANALİZ: Enerji Süper Gücü.\n- ENERJİ: LNG dünya üretiminde lider.\n- HAVA: Rafale ve F-15QA filosu.\n- DİPLOMASİ: Arabuluculuk merkezi.\n- EKONOMİ: Kişi başı en yüksek gelir.",
    "UKRAYNA": "[TRIDENT_RESILIENCE]\nANALİZ: Savaş Tecrübesi.\n- DRONE: Deniz drone sistemleri öncüsü.\n- HAVA: F-16 entegrasyonu devam ediyor.\n- SİBER: IT Army of Ukraine.\n- ASKERİ: Aktif savaş tecrübesi.",
    "YUNANİSTAN": "[HELLENIC_SHIELD]\nANALİZ: Doğu Akdeniz Dengesi.\n- HAVA: Rafale ve F-35 programı.\n- DONANMA: FDI tipi fırkateynler.\n- SAVUNMA: S-300PMU1 hava savunma.\n- ASKERİ: 130 bin aktif personel."
}

DETAILED_META = {
    "İSPANYA": "S-80 Plus denizaltı projesi // Leopard 2E tankları // NH90 helikopter filosu",
    "NORVEÇ": "F-35 operasyonel merkezi // Nasams hava savunma // Fritjof Nansen sınıfı fırkateyn",
    "İSVEÇ": "Gotland sınıfı AIP denizaltılar // JAS 39 Gripen E/F // Carl Gustaf piyade silahı",
    "HOLLANDA": "AIVD siber operasyonlar // De Zeven Provinciën sınıfı // Patriot hava savunma",
    "İSVİÇRE": "Yeraltı sığınak ağları // F/A-18 Hornet filosu // Nötr statü avantajı",
    "BELÇİKA": "NATO merkez güvenliği // F-16 modernizasyonu // FN Herstal silah üretimi",
    "AVUSTURYA": "Terma elektronik harp sistemleri // Pandur zırhlı araç // Glock tabanca üretimi",
    "MEKSİKA": "Kartel karşıtı operasyonlar // Deniz piyadeleri özel kuvvetleri // F-5 Tiger II",
    "ARJANTİN": "Güney Atlantik lojistiği // A-4AR Fightinghawk // Almirante Brown destroyerleri",
    "VİETNAM": "Su-30MK2 Flanker // Kilo sınıfı denizaltılar // S-300PMU1 hava savunma",
    "ENDONEZYA": "KF-21 Boramae ortaklığı // Su-27/30 karması // Strategic location Malacca",
    "GÜNEY AFRİKA": "Rooivalk saldırı helikopteri // G6 Rhino obüs sistemi // Denel dinamikleri",
    "SUUDİ ARABİSTAN": "Vizyon 2030 Savunma // F-15SA Strike Eagle // Patriot ve THAAD entegrasyonu",
    "BAE": "EDGE Group otonom sistemler // F-35A siparişi // Baynunah sınıfı korvet",
    "KAZAKİSTAN": "Baykonur Uzay Üssü // Su-30SM filosu // Stratejik konumu Orta Asya",
    "ÖZBEKİSTAN": "HAVA savunma dijitalleşme // Su-27 Flanker // Özbekistan-ABD ortaklığı",
    "MACARİSTAN": "Lynx KF41 üretimi // JAS 39 Gripen C/D // NATO üyeliği avantajı",
    "ROMANYA": "Aegis Ashore Karadeniz // F-16 Fighting Falcon // IAR-99 Șoim eğitim",
    "SIRBİSTAN": "Balkan denge stratejisi // Pantsir-S1 hava savunma // MiG-29 modernizasyonu",
    "PORTEKİZ": "C-PROC Siber Suçlar Merkezi // F-16AM/BM MLU // Vasco da Gama fırkateyn",
    "FİNLANDİYA": "Geniş topçu envanteri // F-35A siparişi 64 adet // Hamina sınıfı füze botu",
    "DANİMARKA": "Arktik komutanlığı // F-35A Lightning II // Iver Huitfeldt sınıfı fırkateyn",
    "SİNGAPUR": "F-35B dikey kalkış // Formidable sınıfı fırkateyn // Teknoloji merkezi Güneydoğu Asya",
    "MALEZYA": "Malakka Boğazı kontrolü // Su-30MKM Flanker // Scorpene sınıfı denizaltı",
    "TAYLAND": "S26T Yuan sınıfı denizaltı // JAS 39 Gripen // Chakri Naruebet uçak gemisi",
    "CEZAYİR": "T-90SA tank filosu // Su-30MKA Flanker // S-300PMU2 hava savunma",
    "FAS": "Cebelitarık Boğazı gözetleme // F-16V Viper // Mohammed VI frigate programı",
    "IRAK": "Rafale planları // M1A1M Abrams // F-16IQ Fighting Falcon",
    "LÜBNAN": "Kentsel savaş taktikleri // M60A3 tankları // A-29 Super Tucano",
    "ÜRDÜN": "Özel kuvvetler eğitim merkezi // F-16AM/BM MLU // Challenger 1 tankları",
    "KUVEYT": "Patriot hava savunma // F/A-18E/F Super Hornet // Eurofighter Typhoon",
    "UMMAN": "Hürmüz Boğazı kontrolü // F-16C/D Block 50 // Al Ofouq sınıfı korvet",
    "BAHREYN": "ABD 5. Filo ev sahipliği // F-16V Viper // Al-Manama sınıfı korvet",
    "AFGANİSTAN": "Bölgesel istihbarat havuzu // Geçmiş savaş tecrübesi // Stratejik konum",
    "GÜRCİSTAN": "Kafkasya geçiş güvenliği // Su-25 Frogfoot // NATO ortaklık programı",
    "ERMENİSTAN": "Pinaka MLRS tedariki // Su-30SM siparişi // Rusya askeri üssü",
    "İZLANDA": "NATO ASW hattı // Hava polisi NATO rotasyonu // Stratejik Atlantik konumu",
    "YENİ ZELANDA": "Five Eyes ağı üyesi // P-8A Poseidon // ANZAC sınıfı fırkateyn",
    "KIBRIS": "Doğu Akdeniz enerji güvenliği // İngiliz Egemen Üs Alanları // HAW sistemi",
    "SUDAN": "Kızıldeniz lojistik hatları // MiG-29 Fulcrum // Stratejik Port Sudan",
    "ETİYOPYA": "Gerd Barajı siber koruma // Su-27 Flanker // Bölgesel güç Doğu Afrika",
    "KÜBA": "Siber direniş birimleri // MiG-29 ve MiG-23 // Lourdes SIGINT tesisi",
    "VENEZUELA": "S-300VM hava savunma // Su-30MKV Flanker // F-16A/B Fighting Falcon",
    "ŞİLİ": "Antarktika lojistik projeksiyonu // F-16AM/BM MLU // Scorpene denizaltı",
    "KOLOMBİYA": "Anti-narkotik siber ağı // Kfir C.10/C.12 // ARC Almirante Padilla fırkateyn",
    "NİJERYA": "Boko Haram karşıtı drone // Alpha Jets // Aradu sınıfı korvet",
    "KENYA": "Sınır gözetleme teknolojileri // F-5E/F Tiger II // Maritim güvenlik Hint Okyanusu",
    "LÜKSEMBURG": "Askeri uydu haberleşmesi // NATO AWACS programı // SES uydu operatörü",
    "FİLİPİNLER": "BrahMos süpersonik füze // FA-50 Fighting Eagle // Jose Rizal sınıfı fırkateyn",
    "BANGLADEŞ": "Kuvvet Hedefi 2030 // J-10C Vigorous Dragon // Type 035G denizaltı",
    "TAYVAN": "Kirpi doktrini // F-16V Viper // Indigeno us Defense Fighter",
    "PERU": "And Dağları radar ağları // MiG-29SMT Fulcrum // Carvajal sınıfı fırkateyn",
    "İRLANDA": "Deniz altı kablo güvenliği // PC-9M Pilatus // Eithne sınıfı devriye",
    "ÇEK CUMHURİYETİ": "NÚKIB Siber Güvenlik // JAS 39 Gripen C/D // Pandur II zırhlı",
    "SLOVAKYA": "Zuzana 2 obüs sistemleri // F-16V Viper // BVP-2 piyade savaş",
    "SLOVENYA": "Adriyatik lojistik güvenliği // PC-9M Swift // Pandur II 8x8",
    "MAKEDONYA": "Balkan barış koruma // Su-25 Frogfoot // NATO üyelik 2020",
    "ARNAVUTLUK": "NATO Kuçova Hava Üssü // Eurocopter AS532 // NATO üyelik 2009",
    "BOSNA HERSEK": "Yerli mühimmat üretim // Igman-BH üretim // EUFOR Althea misyonu",
    "HIRVATİSTAN": "Rafale F3R geçişi // Patria AMV zırhlı // NATO üyelik 2009",
    "ESTONYA": "e-Savunma NATO CCDCOE // Javelin füze sistemleri // NATO siber merkezi",
    "LETONYA": "Patria 6x6 zırhlı araç // Stinger MANPADS // NATO eFP bataryası",
    "LİTVANYA": "Suwalki boşluğu savunması // NASAMS hava savunma // NATO eFP öncü",
    "BEYAZ RUSYA": "Polonez MLRS sistemleri // Su-30SM Flanker // Rusya Birlik Devleti",
    "MOLDOVA": "Sınır güvenliği dijitalleşme // MiG-29 Fulcrum // AB ortaklık anlaşması",
    "MOĞOLİSTAN": "İHA gözetleme ağları // MiG-29 Fulcrum // Stratejik konum Asya",
    "BOLİVYA": "Lityum tesisleri güvenliği // K-8 Karakorum // Çin askeri işbirliği",
    "PARAGUAY": "Bölgesel istihbarat paylaşımı // Embraer EMB 314 // Merkosur üyeliği",
    "URUGUAY": "Deniz yetki alanları radar // A-37B Dragonfly // Artigas Üssü Antarktika",
    "PANAMA": "Kanal geçiş siber güvenlik // UH-1H Iroquois // Stratejik su yolu",
    "KOSTA RİKA": "Siber suçlarla mücadele // Ordu yok sivil güvenlik // Barış anayasası",
    "KAMBOÇYA": "Ream Deniz Üssü modernizasyonu // J-7 Fishbed // Çin askeri üssü",
    "LAOS": "İletişim altyapısı siber koruma // MiG-21 Fishbed // Çin-Laos demiryolu",
    "MYANMAR": "İç güvenlik sinyal istihbaratı // JF-17 Thunder // Yak-130 eğitim",
    "SENEGAL": "Deniz devriye OPV gemileri // CASA C-295 // ECOWAS liderliği",
    "GANA": "Körfez güvenliği deniz // C-295 uçak // Kofi Annan merkezi",
    "FİLDİŞİ SAHİLİ": "Terörle mücadele merkezi // Su-25 Frogfoot // ECOWAS gücü",
    "BELARus": "S-400 Triumph entegrasyonu // Su-30SM Flanker // Rusya entegrasyonu",
    "SURİYE": "Hibrit savaş tecrübesi // S-300 ve Pantsir // Rusya Hmeimim üssü",
    "LİBYA": "Akdeniz kıyı devriyeleri // Bayraktar TB2 // Wagner varlığı",
    "TUNUS": "Sınır dijital bariyerleri // F-5E/F Tiger II // AB ortaklığı",
    "MOLİ": "Taktik İHA ağları // Su-25 Frogfoot // Rusya Wagner varlığı"
}

# Tüm ülkeleri STRATEGIC_INTEL'e ekle
OTHER_COUNTRIES = list(DETAILED_META.keys())
for c in OTHER_COUNTRIES:
    if c not in STRATEGIC_INTEL:
        threat_level = random.randint(40, 95)
        STRATEGIC_INTEL[c] = f"[DOSYA KODU: {c[:3]}-2025]\n- Tehdit Seviyesi: {threat_level}/100\n- Analiz: {DETAILED_META[c]}\n- Son Güncelleme: {datetime.datetime.now().strftime('%Y-%m-%d')}\n- Kategori: {'YÜKSEK RİSK' if threat_level > 70 else 'ORTA RİSK' if threat_level > 50 else 'DÜŞÜK RİSK'}"

ALL_DATA = [{"n": f"{k} STRATEJİK ANALİZİ", "i": v} for k, v in STRATEGIC_INTEL.items()]

UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>GGİ_SUPREME_OS_v21_GENESIS</title>
    <style>
        :root { 
            --b: #00f2ff; --g: #39ff14; --r: #ff0055; --bg: #010203; 
            --p: rgba(10, 25, 45, 0.9); --y: #ffff00; --m: #ff00ff; --cyan: #00ffff; 
        }
        * { box-sizing: border-box; cursor: crosshair; -webkit-tap-highlight-color: transparent; }
        body, html { 
            margin: 0; padding: 0; background: var(--bg); color: #fff; 
            font-family: 'Courier New', monospace; height: 100vh; width: 100vw;
            overflow: hidden; touch-action: none;
        }
        #matrix { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; opacity: 0.15; }
        .os-wrapper { display: flex; flex-direction: column; height: 100vh; width: 100vw; }
        header { 
            height: 50px; border-bottom: 2px solid var(--b); 
            display: flex; align-items: center; justify-content: space-between; 
            padding: 0 15px; background: #000; flex-shrink: 0;
            box-shadow: 0 0 25px var
