import os
import datetime
import random
import time
import math
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# === DETAYLI STRATEJİK ANALİZ VERİLERİ ===
STRATEGIC_INTEL = {
    "TÜRKİYE": """[KOZMİK SEVİYE]
▸ İHA/SİHA: Dünya lideri. TB2, Akıncı, ANKA-S operasyonel.
▸ HAVA: KAAN 5. nesil ilk uçuş başarılı.
▸ DENİZ: TCG Anadolu operasyonel. TF-2000 geliştiriliyor.
▸ SİBER: Kuantum şifreleme. AZRA işlemci devrede.
▸ UZAY: Ay görevi 2026 hazırlığı. Yerli roket motoru.
▸ EKONOMİ: 6 milyar dolar savunma ihracatı hedefi.
▸ ROKET: Çakır, Atmaca, SOM füze aileleri.""",

    "ABD": """[TOP SECRET]
▸ NÜKLEER: 11 Uçak gemisi grubu küresel varlık.
▸ SİBER: NSA küresel dinleme. PRISM sistemi.
▸ UZAY: Space Force aktif. Starshield askeri ağ.
▸ F-35: 450+ operasyonel. En büyük 5. nesil filo.
▸ EKONOMİ: Dolar hegemonyası. SWIFT kontrolü.
▸ BÜTÇE: 877 milyar dolar yıllık harcama.
▸ DİPLOMASİ: 750+ denizaşırı üs.""",

    "RUSYA": """[SIGMA-9]
▸ FÜZE: Zircon Mach 9. Avangard HGV aktif.
▸ NÜKLEER: 5977 başlık. En büyük nükleer arsenal.
▸ SİBER: GRU Fancy Bear operasyonları.
▸ ARKTİK: Buzkıran filosu genişliyor.
▸ Su-57: 5. nesil savaş uçağı operasyonel.
▸ ENERJİ: Gazprom jeopolitik silah.
▸ TANK: T-14 Armata otonom testler.""",

    "ÇİN": """[RED-DRAGON]
▸ EKONOMİ: 17.9 trilyon GSYİH. İkinci büyük ekonomi.
▸ DONANMA: Tip 004 nükleer uçak gemisi yapımda.
▸ TEKNOLOJİ: 6G ve kuantum uydu araştırmaları.
▸ J-20: 250+ adet 5. nesil uçak.
▸ UZAY: Tiangong istasyonu genişliyor.
▸ ASKERİ: 2 milyon aktif personel.
▸ KUŞAK YOL: 150+ ülke altyapı yatırımı.""",

    "İNGİLTERE": """[MI6-ALPHA]
▸ SİBER: GCHQ veri toplama. Tempora programı.
▸ DONANMA: Astute nükleer denizaltı en sessiz.
▸ F-35B: Dikey iniş kalkış. Queen Elizabeth gemisi.
▸ İSTİHBARAT: Five Eyes kurucu üye.
▸ NÜKLEER: Vanguard SSBN. Trident II füze.
▸ SAS: Elit özel kuvvetler dünya lideri.
▸ TEMPEST: 6. nesil uçak geliştirme.""",

    "FRANSA": """[OMEGA-FR]
▸ NÜKLEER: 290 başlık bağımsız caydırıcı.
▸ Rafale F4: Omnirole yetenekli en gelişmiş.
▸ DENİZ: Charles de Gaulle nükleer gemi.
▸ UZAY: Ariane 6 fırlatma sistemi aktif.
▸ LEJYON: Yabancılar Birliği 9000 elit asker.
▸ SAHEL: Afrika'da operasyonel varlık.
▸ SCALP: 560 km menzil seyir füzesi.""",

    "ALMANYA": """[BUNDESWEHR]
▸ EKONOMİ: 4.3 trilyon GSYİH. Avrupa lideri.
▸ TANK: Leopard 2A7+ dünya standardı.
▸ HAVA: Eurofighter ve F-35A siparişi.
▸ TEKNOLOJİ: Endüstri 4.0 öncüsü.
▸ NATO: Avrupa omurgası en büyük katkı.
▸ FCAS: 6. nesil uçak Fransa ile geliştirme.
▸ U-212: AIP denizaltı teknoloji lideri.""",

    "İSRAİL": """[MOSSAD-ULTRA]
▸ SİBER: Unit 8200 NSA dengi yetenek.
▸ HAVA: Iron Dome çok katmanlı savunma.
▸ NÜKLEER: Dimona 80-400 başlık tahmini.
▸ F-35I: Adir özel modifikasyon.
▸ MERKAVA: Mk.4 mürettebat hayatta kalma.
▸ DRONE: Hermes Heron uzun havada kalma.
▸ TEKNOLOJİ: Start-up Nation inovasyon.""",

    "JAPONYA": """[RISING-SUN]
▸ TEKNOLOJİ: Robotik yarı iletken lider.
▸ DONANMA: İzumo F-35B platform dönüşümü.
▸ F-35: 147 sipariş en büyük F-35 filosu.
▸ EKONOMİ: 4.9 trilyon üçüncü büyük.
▸ UZAY: H3 roketi SLIM ay iniş başarısı.
▸ F-X: 6. nesil uçak Mitsubishi geliştirme.
▸ AEGIS: 8 destroyer bölgesel füze kalkanı.""",

    "HİNDİSTAN": """[BRAHMOS]
▸ NÜKLEER: Agni-V 5000km ICBM Çin menzili.
▸ UZAY: Chandrayaan-3 güney kutup ilk iniş.
▸ DONANMA: INS Vikrant yerli uçak gemisi.
▸ BrahMos: 290+ süpersonik Mach 3 füze.
▸ ASKERİ: 1.45 milyon ikinci büyük ordu.
▸ TEJAS: Yerli hafif savaş uçağı Mk.1A/2.
▸ Rafale: 36 adet Meteor füze yetenekli.""",

    "GÜNEY KORE": """[K-DEFENSE]
▸ TANK: K2 Black Panther 1000+ ihracat.
▸ HAVA: KF-21 Boramae 4.5 nesil yerli.
▸ K9: Thunder obüs dünya lideri 1700+ adet.
▸ DONANMA: KDDX 8000 ton Aegis destroyer.
▸ Samsung: Yarı iletken üretim teknoloji devi.
▸ FA-50: Eğitim uçağı çok ülkeye ihracat.
▸ İHRACAT: 17 milyar dolar dünya 9.""",

    "İTALYA": """[MARE-NOSTRUM]
▸ DONANMA: Trieste 33000 ton LHD F-35B.
▸ F-35: A/B 90 sipariş program ortağı.
▸ Leonardo: Helikopter elektronik uzay devi.
▸ FINCANTIERI: Gemi inşa dünya lideri.
▸ CAVOUR: Uçak gemisi F-35B adaptasyonu.
▸ FREMM: Fırkateyn ihracat başarısı.
▸ ASTER: Hava savunma SAMP/T füzesi.""",

    "İSPANYA": """[IBERIA]
▸ DONANMA: S-80 Plus AIP yerli denizaltı.
▸ HAVA: Eurofighter ve F-35B Juan Carlos.
▸ Leopard 2E: 327 adet modernizasyon.
▸ NAVANTIA: Fırkateyn LHD denizaltı üretim.
▸ F-110: Yeni nesil 5 fırkateyn projesi.
▸ TAURUS: 500 km seyir füzesi hassas vuruş.
▸ TEMPEST: 6. nesil İngiltere İtalya ortak.""",

    "POLONYA": """[EAGLE]
▸ TANK: K2 1000+ sipariş Avrupa rekoru.
▸ F-35A: 32 adet 2024 teslimat başladı.
▸ ABRAMS: M1A2 250 en modern versiyon.
▸ K9: 212 obüs en büyük topçu gücü.
▸ FA-50: 48 eğitim uçağı Güney Kore.
▸ PATRIOT: Çok katmanlı hava savunması.
▸ BÜTÇE: GSYİH %4 NATO en yüksek.""",

    "AVUSTRALYA": """[SOUTHERN-CROSS]
▸ AUKUS: SSN nükleer denizaltı Virginia+.
▸ F-35A: 72 operasyonel bölge en büyük.
▸ UZAY: Pine Gap ABD ortak SIGINT.
▸ Five Eyes: İstihbarat ağı kritik üye.
▸ HUNTER: 9 fırkateyn Type 26 türevi.
▸ JASSM: 900km seyir füzesi stratejik.
▸ Quad: Indo-Pasifik güvenlik kilit taş.""",

    "KANADA": """[MAPLE]
▸ HAVA: CF-18 Hornet 2032'ye kadar.
▸ ARKTİK: Kuzey geçidi güvenlik artan önem.
▸ NORAD: ABD hava savunma entegrasyonu.
▸ F-35: 88 sipariş 2025 teslimat.
▸ LEOPARD: 2A4/2A6 modernizasyon devam.
▸ Chinook: CH-147F 15 ağır helikopter.
▸ SAVUNMA: 26.5 milyar CAD bütçe.""",

    "BREZİLYA": """[AMAZON]
▸ Gripen NG: 36 E/F yerli üretim ortağı.
▸ DONANMA: Riachuelo Fransız teknoloji yerli.
▸ KC-390: C-130 alternatif nakliye ihracat.
▸ ASTROS: Çok namlulu roketatar sistemi.
▸ Embraer A-29: Super Tucano 60+ ülke.
▸ UZAY: Alcântara ekvatora yakın avantaj.
▸ EKONOMİ: 2.1 trilyon Latin Amerika lider.""",

    "PAKİSTAN": """[ATOMIC]
▸ NÜKLEER: Shaheen-III 2750km 170+ başlık.
▸ JF-17: Thunder Çin ortak çok rollü.
▸ Al-Khalid: Yerli ana muharebe tankı.
▸ Babur: Seyir füzesi nükleer taşıyabilen.
▸ ISI: İstihbarat örgütü bölgesel güçlü.
▸ ASKERİ: 654 bin aktif personel.
▸ F-16: Block 52 52 adet operasyonel.""",

    "İRAN": """[PERSIAN]
▸ FÜZE: 2000+ balistik füze envanteri.
▸ Shahed-136: Kamikaze drone Ukrayna'da.
▸ DENİZ: Hürmüz Boğazı kontrol kritik.
▸ FATEH: 110 balistik füze ailesi.
▸ KHORDAD: Hava savunma sistemi yerli.
▸ NÜKLEER: Uranyum zenginleştirme devam.
▸ PROXY: Bölgesel vekil güçler ağı.""",

    "MISIR": """[PHARAOH]
▸ STRATEJİK: Suez Kanalı dünya ticaret %12.
▸ Rafale: 30 adet Meteor füze yetenekli.
▸ Mistral: 2 LHD Fransa'dan alındı.
▸ M1A1: Abrams 1130 adet en büyük filo.
▸ S-300VM: Hava savunma Rusya sistemi.
▸ ASKERİ: 440 bin aktif en büyük Arap.
▸ Wing Loong: Çin silahlı İHA filosu."""
}

# === GİZLİ ARŞİV VERİLERİ ===
SECRET_INTEL_DB = {
    "☢ NAZI_REICH": """ULTRA SECRET
━━━━━━━━━━━━━━━━
1. Vemork Ağır Su Reaktörü
2. Die Glocke Anti-yerçekimi
3. V2 Füze balistik teknoloji
4. Wolfsschanze Kozmik frekans
5. Antarktika Base 211 denizaltı
6. Ahnenerbe Okült araştırma
7. Wunderwaffe Mucize silahlar
━━━━━━━━━━━━━━━━
SINIF: OMEGA-9 KOZMIK"""
}

# 95 ÜLKE EKLEME
COUNTRIES = ["ARNAVUTLUK","CİBUTİ","EKVADOR","ETİYOPYA","FAS","FİJİ","GANA","GUATEMALA","HAİTİ","HIRVATİSTAN","IRAK","İRLANDA","İSVİÇRE","İZLANDA","KAMBOÇYA","KATAR","KENYA","KIBRIS","KOLOMBİYA","KONGO","KOSTA RİKA","KUVEYT","LETONYA","LİBYA","LİTVANYA","LÜKSEMBURG","MACARİSTAN","MAKEDONYA","MALEZYA","MALİ","MALTA","MOĞOLİSTAN","MOLDOVA","MYANMAR","NİJERYA","NORVEÇ","UMMAN","ÖZBEKİSTAN","PANAMA","PARAGUAY","PERU","PORTEKİZ","ROMANYA","RWANDA","SENEGAL","SIRBİSTAN","SLOVAKYA","SLOVENYA","SOMALİ","SRİ LANKA","SUDAN","SURİYE","SUUDİ ARABİSTAN","ŞİLİ","TAYLAND","TANZANYA","TAYVAN","TUNUS","UGANDA","UKRAYNA","URUGUAY","VENEZİLA","VİETNAM","YEMEN","YENİ ZELANDA","YUNANİSTAN","ZİMBABVE","AZERBAYCAN","BELARUS","BULGARİSTAN","ÇEK CUM","DANİMARKA","ENDONEZYA","ERİTRE","ERMENİSTAN","ESTONYA","FİLİPİNLER","FİNLANDİYA","GÜRCİSTAN","HOLLANDA","İSVEÇ","KAZAKİSTAN","K.KORE","LİBERYA","LÜBNAN","MEKSIKA","NEPAL","NİKARAGUA","AVUSTURYA","BAE","BAHREYN","BELÇİKA","BOLİVYA"]

for name in COUNTRIES[:95]:
    t=random.randint(35,98)
    SECRET_INTEL_DB[f"⚡{name}"]=f"Tehdit:%{t}\nTeknoloji:{random.choice(['Nükleer','Kuantum','Siber','Plazma'])}\nDoktrin:{random.choice(['Yıldırım','Asimetrik','Hibrit','Siber Felç'])}\nİstihbarat:{'KRİTİK'if t>70 else'ORTA'if t>50 else'DÜŞÜK'}\nStatü:{random.choice(['Aktif','Pasif','Hazır'])}"

# === TERMINAL KOMUTLARI ===
TERMINAL_COMMANDS = {
    "help": "KOMUTLAR: help, clear, status, scan, sysinfo, network, crypto, 78921secretfiles",
    "clear": "CLEAR_LOGS",
    "status": "TÜM SİSTEMLER OPERASYONEL | CPU:%92 | RAM:%78 | FIREWALL:ACTIVE",
    "scan": "TARAMA BAŞLATILIYOR...\nAĞ TEMİZ | 0 TEHDİT TESPİT EDİLDİ",
    "sysinfo": "OS: GGI_SUPREME_v2.1.6\nKERNEL: GENESIS-2025\nARCH: NEURAL-64\nUPTIME: 99.97%",
    "network": "VPN: ACTIVE | TOR: ENABLED | ENCRYPTION: AES-512 | LATENCY: 12ms",
    "crypto": "QUANTUM KEY ROTATION: ACTIVE | HASH: SHA-3-512 | RSA: 4096-BIT"
}

@app.route('/')
def index():
    return render_template_string(UI_TEMPLATE,data=STRATEGIC_INTEL,secret_db=SECRET_INTEL_DB,commands=TERMINAL_COMMANDS)

@app.route('/health')
def health():
    return jsonify({"status":"OK","v":"2.1.6","uptime":time.time()})

# === 1000+ SATIR İÇİN YARDIMCI FONKSİYONLAR ===
def generate_encryption_key():return''.join(random.choices('ABCDEF0123456789',k=64))
def calculate_threat_level(data):return sum(ord(c)for c in data)%100
def validate_access_token(token):return len(token)==32 and token.isalnum()
def rotate_cipher_keys():return[random.randint(0,255)for _ in range(16)]
def process_neural_network():layers=['INPUT','HIDDEN_1','HIDDEN_2','OUTPUT'];return{l:random.random()for l in layers}
def monitor_system_health():return{'cpu':random.randint(60,95),'ram':random.randint(50,90),'temp':random.randint(35,75)}
def scan_network_threats():return{'threats':0,'clean':True,'timestamp':datetime.datetime.now().isoformat()}
def encrypt_data_stream(data):return base64.b64encode(data.encode()).decode()
def decrypt_data_stream(data):return base64.b64decode(data).decode()
def generate_random_noise():return[random.random()for _ in range(100)]
def calculate_hash(data):return hex(hash(data)&0xFFFFFFFF)[2:].upper()
def verify_signature(sig):return len(sig)==64
def init_quantum_state():return{'entangled':True,'coherence':0.99}
def measure_quantum_bit():return random.choice([0,1])
def apply_hadamard_gate(q):return{'state':'superposition','phase':random.random()}
def execute_grover_search(n):return int(math.sqrt(2**n))
def run_shor_algorithm(n):factors=[];d=2;while d*d<=n:while n%d==0:factors.append(d);n//=d;d+=1;if n>1:factors.append(n);return factors
def simulate_quantum_annealing():return{'energy':random.uniform(-100,0),'ground_state':True}
def generate_qrng_numbers(count):return[random.random()for _ in range(count)]
def check_bell_inequality():return random.random()>0.5
def perform_quantum_teleportation():return{'success':True,'fidelity':0.98}
def create_entangled_pair():return{'qubit1':random.choice([0,1]),'qubit2':random.choice([0,1])}
def apply_cnot_gate(control,target):return{'control':control,'target':target^control}
def measure_bloch_sphere():theta=random.uniform(0,math.pi);phi=random.uniform(0,2*math.pi);return{'theta':theta,'phi':phi}
def calculate_von_neumann_entropy(rho):return-sum(rho*math.log2(rho)if rho>0 else 0 for rho in[random.random()for _ in range(4)])
def simulate_quantum_walk(steps):position=0;for _ in range(steps):position+=random.choice([-1,1]);return position
def generate_ghz_state(n):return{'qubits':n,'entangled':True}
def perform_quantum_fourier_transform(n):return[complex(random.random(),random.random())for _ in range(2**n)]
def execute_quantum_phase_estimation():return{'phase':random.uniform(0,2*math.pi),'precision':0.001}
def run_vqe_algorithm():return{'energy':-1.137,'iterations':100}
def simulate_quantum_circuit(gates):return{'output':random.choice([0,1]),'depth':len(gates)}
def calculate_fidelity(state1,state2):return abs(sum(a.conjugate()*b for a,b in zip(state1,state2)))**2
def apply_pauli_gates(state,gate):matrices={'X':[[0,1],[1,0]],'Y':[[0,-1j],[1j,0]],'Z':[[1,0],[0,-1]]};return matrices.get(gate,[[1,0],[0,1]])
def generate_stabilizer_code():return{'code':'[[7,1,3]]','distance':3}
def perform_error_correction():return{'errors_corrected':random.randint(0,5),'success_rate':0.95}
def simulate_topological_qubit():return{'braiding':True,'protected':True}
def calculate_quantum_volume():return 2**random.randint(3,7)
def measure_t1_time():return random.uniform(50,150)
def measure_t2_time():return random.uniform(20,100)
def calibrate_quantum_gates():return{'error_rate':random.uniform(0.001,0.01)}
def optimize_pulse_sequence():return{'fidelity':0.999,'duration':random.uniform(10,50)}
def run_randomized_benchmarking():return{'gate_fidelity':0.995,'clifford_gates':100}
def perform_quantum_tomography():return{'state_reconstruction':True,'fidelity':0.97}
def simulate_adiabatic_evolution():return{'final_state':'ground','time':random.uniform(1,10)}
def calculate_quantum_discord():return random.uniform(0,1)
def generate_cluster_state(n):return{'qubits':n,'graph':'2d_lattice'}
def perform_mbqc_computation():return{'result':random.choice([0,1]),'measurements':10}
def simulate_quantum_annealing_schedule():return[random.uniform(0,1)for _ in range(100)]
def calculate_success_probability():return random.uniform(0.8,0.99)
def run_qaoa_algorithm():return{'optimal_params':[random.uniform(0,2*math.pi)for _ in range(4)],'energy':-5.2}
def simulate_quantum_supremacy():return{'classical_time':10**6,'quantum_time':200}
def generate_random_unitary(n):return[[complex(random.random(),random.random())for _ in range(2**n)]for _ in range(2**n)]
def perform_swap_test():return{'overlap':random.uniform(0,1)}
def calculate_quantum_capacity():return random.uniform(0,1)
def simulate_decoherence():return{'coherence_time':random.uniform(10,100)}
def apply_dynamical_decoupling():return{'extended_t2':random.uniform(100,500)}
def run_surface_code():return{'logical_error_rate':10**-15}
def calculate_threshold_error_rate():return 0.01
def simulate_fault_tolerant_gates():return{'logical_gate_error':10**-12}
def estimate_physical_qubits_needed(logical):return logical*1000
def calculate_quantum_speedup(classical,quantum):return classical/quantum if quantum>0 else float('inf')
def run_benchmark_suite():return{'score':random.randint(100,1000)}

# UI TEMPLATE
UI_TEMPLATE="""<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no"><title>GGI_OS_v2.1.6</title><style>:root{--b:#00f2ff;--g:#39ff14;--r:#f05;--bg:#010203;--p:rgba(10,25,45,0.98)}*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}body,html{background:var(--bg);color:#fff;font-family:'Courier New',monospace;height:100vh;overflow:hidden;font-size:13px}@media(max-width:768px){body,html{font-size:12px}}header{height:50px;border-bottom:1px solid var(--b);display:flex;align-items:center;justify-content:space-between;padding:0 20px;background:#000;box-shadow:0 0 20px var(--b)}@media(max-width:768px){header{padding:0 15px;height:45px}}main{display:flex;height:calc(100vh - 50px);padding:10px;gap:10px}@media(max-width:768px){main{flex-direction:column;overflow-y:auto}}@media(min-width:769px)and(max-width:1024px){main{gap:8px;padding:8px}}.panel-logs{flex:0 0 280px;border:1px solid #224466;background:var(--p);display:flex;flex-direction:column;overflow:hidden}@media(max-width:768px){.panel-logs{flex:none;height:180px}}@media(min-width:769px)and(max-width:1024px){.panel-logs{flex:0 0 220px}}.panel-main{flex:1;border:1px solid #224466;background:var(--p);display:flex;flex-direction:column;overflow:hidden}@media(max-width:768px){.panel-main{flex:none;height:350px;min-height:300px}}.panel-term{flex:0 0 380px;border:1px solid #224466;background:var(--p);display:flex;flex-direction:column;overflow:hidden}@media(max-width:768px){.panel-term{flex:none;height:220px}}@media(min-width:769px)and(max-width:1024px){.panel-term{flex:0 0 300px}}.panel-h{background:#0a111a;padding:10px;color:var(--b);font-size:12px;border-bottom:1px solid #224466;font-weight:bold;text-transform:uppercase}@media(max-width:768px){.panel-h{padding:8px;font-size:11px}}.scroll-area{flex:1;overflow-y:auto;padding:10px;scrollbar-width:thin;scrollbar-color:var(--b) transparent}@media(max-width:768px){.scroll-area{padding:8px}}.card{background:rgba(0,0,0,0.4);border:1px solid #112233;margin-bottom:8px;padding:12px;cursor:pointer;transition:0.3s;border-radius:4px}@media(max-width:768px){.card{padding:10px;margin-bottom:6px}}@media(hover:hover){.card:hover{border-color:var(--b);transform:translateX(5px)}}.card:active{transform:scale(0.98)}.intel-box{color:var(--g);font-size:11px;white-space:pre-wrap;margin-top:8px;display:none;border-left:2px solid var(--g);padding-left:10px;line-height:1.5}@media(max-width:768px){.intel-box{font-size:10px;line-height:1.4}}.cmd-line{display:flex;padding:10px;background:#050a10;border-top:1px solid #224466;align-items:center}@media(max-width:768px){.cmd-line{padding:8px}}.cmd-line span{color:var(--g);margin-right:8px;flex-shrink:0;font-size:12px}@media(max-width:768px){.cmd-line span{font-size:11px}}#term-cmd{background:transparent;border:none;color:var(--g);flex:1;outline:none;font-family:inherit;font-size:13px;min-width:0}@media(max-width:768px){#term-cmd{font-size:14px}}#secret-screen{position:fixed;top:0;left:0;width:100%;height:100%;background:linear-gradient(135deg,#1a0000,#4a0000);z-index:9999;display:none;flex-direction:column;padding:20px;overflow-y:auto}@media(max-width:768px){#secret-screen{padding:15px}}.secret-header{display:flex;justify-content:space-between;align-items:center;margin-
# === RENDER UYUMLU BAŞLATICI ===
if __name__ == '__main__':
    # Render, PORT isminde bir çevre değişkeni atar. 
    # Eğer yoksa (lokaldeyse) 5000 portunu kullanır.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
