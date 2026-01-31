from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time

# --- AYARLAR VE DİL DESTEĞİ ---
diller = {
    "tr": {"basla": "Oyuna Başla", "ayarlar": "Ayarlar", "mesaj": "Yardım edin..."},
    "en": {"basla": "Start Game", "ayarlar": "Settings", "mesaj": "Help me..."},
    "de": {"basla": "Spiel Starten", "ayarlar": "Einstellungen", "mesaj": "Hilf mir..."}
}
secili_dil = "tr"

app = Ursina()

# --- ANA MENÜ ---
def oyunu_baslat():
    menu_parent.disable()
    oyun_kur()

def dil_degistir(dil_kodu):
    global secili_dil
    secili_dil = dil_kodu
    print(f"Dil değiştirildi: {dil_kodu}")
    # Burada buton metinlerini güncelleyecek bir fonksiyon tetiklenebilir

menu_parent = Entity(enabled=True)
Text("KORKU ÇAĞRISI: 991", parent=menu_parent, scale=3, origin=(0, -3), color=color.red)

Button(text=diller[secili_dil]["basla"], color=color.black66, scale=(.3, .1), y=0, parent=menu_parent, on_click=oyunu_baslat)
Button(text=diller[secili_dil]["ayarlar"], color=color.black66, scale=(.3, .1), y=-.15, parent=menu_parent)

# Dil Seçenekleri Butonları
Button(text="TR", scale=(.05, .05), x=-.1, y=-.3, parent=menu_parent, on_click=Func(dil_degistir, "tr"))
Button(text="EN", scale=(.05, .05), x=0, y=-.3, parent=menu_parent, on_click=Func(dil_degistir, "en"))
Button(text="DE", scale=(.05, .05), x=.1, y=-.3, parent=menu_parent, on_click=Func(dil_degistir, "de"))

# --- OYUN İÇERİĞİ VE DÜNYA ---
def oyun_kur():
    # Zemin ve Gökyüzü
    Entity(model='plane', scale=100, texture='grass', texture_scale=(100,100), collider='box')
    Sky()

    # Işıklandırma (Korku atmosferi için düşük ışık)
    DirectionalLight(y=2, z=3, shadows=True)

    # SENİN KARAKTERİN (Meshy_AI... .glb dosyası)
    # Not: .glb dosyanın bu script ile aynı klasörde olması gerekir.
    player_model = Entity(
        model='Meshy_AI_This_3D_character_des_0131141733_texture.glb',
        scale=1,
        position=(0, 0, 5),
        collider='mesh'
    )

    # Birinci Şahıs Kontrolcü (Hareket Etme: WASD + Mouse)
    player = FirstPersonController()
    player.cursor.visible = False

    # Hikaye Girişi (Senin yazdığın daktilo efekti ekranın altında belirecek)
    alt_yazi = Text(text='', origin=(0, 4), color=color.yellow, background=True)
    
    async def daktilo_efekti_ekran(metin):
        alt_yazi.text = ""
        for harf in metin:
            alt_yazi.text += harf
            await wait(0.05)

    # Oyuna girişte mesajı göster
    invoke(daktilo_efekti_ekran, "991 ÇAĞRISI ALINDI: 5359. CADDEYE GİT.", delay=2)

app.run()

if __name__ == '__main__':
    # Render veya yerel sunucu için otomatik port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
