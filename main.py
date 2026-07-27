import customtkinter as ctk
import random
import string
import pyperclip
import json
import os
import subprocess
import sys



def ayar_yukle():
    if os.path.exists("settings.json"):
        with open("settings.json", "r", encoding="utf-8") as dosya:
            return json.load(dosya)

    return {"language": ""}


def ayar_kaydet(dil):
    with open("settings.json", "w", encoding="utf-8") as dosya:
        json.dump(
            {"language": dil},
            dosya,
            indent=4
        )


def dil_sec():

    print("==============================")
    print("      Password Generator")
    print("==============================")
    print("1 - Türkçe")
    print("2 - English")
    print("3 - Deutsch")
    print("4 - Español")
    print("5 - Français")

    secim = input("Language: ")

    diller = {
        "1": "tr",
        "2": "en",
        "3": "de",
        "4": "es",
        "5": "fr"
    }

    secilen = diller.get(secim, "en")

    ayar_kaydet(secilen)

    return secilen


def aktif_dil():

    ayarlar = ayar_yukle()

    if ayarlar["language"] == "":
        return dil_sec()

    return ayarlar["language"]

def dil_yukle():
    secilen_dil = aktif_dil()

    dosya_yolu = os.path.join(
        "languages",
        secilen_dil + ".json"
    )

    with open(dosya_yolu, "r", encoding="utf-8") as dosya:
        return json.load(dosya)


dil = dil_yukle()


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.title(dil["title"])
app.iconbitmap("icon.ico")
app.geometry("650x850")
app.resizable(False, False)


def sifre_olustur():
    try:
        min_deger = int(minimum.get())
        max_deger = int(maksimum.get())

    except ValueError:
        sonuc.configure(text=dil["error_number"])
        return


    if min_deger > max_deger:
        sonuc.configure(text=dil["error_range"])
        return


    karakterler = ""

    if kucuk.get():
        karakterler += string.ascii_lowercase

    if buyuk.get():
        karakterler += string.ascii_uppercase

    if sayi.get():
        karakterler += string.digits

    if sembol.get():
        karakterler += "!@#$%^&*()-_=+"


    if karakterler == "":
        sonuc.configure(text=dil["error_select"])
        return


    for karakter in haric.get():
        karakterler = karakterler.replace(karakter, "")


    if karakterler == "":
        sonuc.configure(text=dil["error_empty"])
        return


    uzunluk = random.randint(
        min_deger,
        max_deger
    )


    sifre = ""

    for i in range(uzunluk):
        sifre += random.choice(karakterler)


    sifre_kutusu.delete(
        0,
        "end"
    )

    sifre_kutusu.insert(
        0,
        sifre
    )


    guc = 0

    if len(sifre) >= 12:
        guc += 1

    if any(x.islower() for x in sifre):
        guc += 1

    if any(x.isupper() for x in sifre):
        guc += 1

    if any(x.isdigit() for x in sifre):
        guc += 1

    if any(x in "!@#$%^&*()-_=+" for x in sifre):
        guc += 1


    seviyeler = {
        1: dil["very_weak"],
        2: dil["weak"],
        3: dil["medium"],
        4: dil["strong"],
        5: dil["very_strong"]
    }


    guc_label.configure(
        text=dil["strength"] + " " + seviyeler.get(guc, dil["weak"])
    )


def kopyala():
    metin = sifre_kutusu.get()

    if metin:
        pyperclip.copy(metin)
        sonuc.configure(text=dil["copied"])


def ayarlar_ac():

    pencere = ctk.CTkToplevel(app)

    pencere.title(dil["settings"])
    pencere.iconbitmap("icon.ico")
    pencere.geometry("350x350")

    ctk.CTkLabel(
        pencere,
        text=dil["language"],
        font=("Arial",20,"bold")
    ).pack(pady=20)
	

    secenek = ctk.StringVar()


    diller = {
        "Türkçe": "tr",
        "English": "en",
        "Deutsch": "de",
        "Español": "es",
        "Français": "fr"
    }


    mevcut = ayar_yukle()["language"]


    for isim, kod in diller.items():

        ctk.CTkRadioButton(
            pencere,
            text=isim,
            variable=secenek,
            value=kod
        ).pack(
            pady=5
        )


    secenek.set(mevcut)


    def kaydet():
    
        ayar_kaydet(
            secenek.get()
        )
    
        pencere.destroy()
        app.destroy()
    
        subprocess.Popen(
            [sys.executable] + sys.argv
        )


    ctk.CTkButton(
        pencere,
        text=dil["save"],
        command=kaydet
    ).pack(
        pady=20
    )

ana = ctk.CTkFrame(app)

ana.pack(
    padx=40,
    pady=30,
    fill="both",
    expand=True
)


baslik = ctk.CTkLabel(
    ana,
    text=dil["title"],
    font=("Arial",30,"bold")
)

baslik.pack(
    pady=25
)


sifre_kutusu = ctk.CTkEntry(
    ana,
    width=450,
    height=50,
    font=("Arial",20),
    justify="center"
)

sifre_kutusu.pack(
    pady=10
)


kopya = ctk.CTkButton(
    ana,
    text=dil["copy"],
    width=200,
    command=kopyala
)

kopya.pack(
    pady=5
)

ayarlar = ctk.CTkButton(
    ana,
    text="⚙ " + dil["settings"],
    width=200,
    command=ayarlar_ac
)

ayarlar.pack(
    pady=5
)

guc_label = ctk.CTkLabel(
    ana,
    text=dil["strength"],
    font=("Arial",16)
)

guc_label.pack(
    pady=15
)


ctk.CTkLabel(
    ana,
    text=dil["length"],
    font=("Arial",18,"bold")
).pack()


uzunluk = ctk.CTkFrame(ana)

uzunluk.pack(
    pady=10
)


minimum = ctk.CTkEntry(
    uzunluk,
    placeholder_text=dil["minimum"],
    width=180
)

minimum.grid(
    row=0,
    column=0,
    padx=10
)


maksimum = ctk.CTkEntry(
    uzunluk,
    placeholder_text=dil["maximum"],
    width=180
)

maksimum.grid(
    row=0,
    column=1,
    padx=10
)


secimler = ctk.CTkFrame(ana)

secimler.pack(
    pady=15
)


kucuk = ctk.CTkCheckBox(
    secimler,
    text=dil["lowercase"]
)

kucuk.grid(
    row=0,
    column=0,
    padx=30,
    pady=10
)


buyuk = ctk.CTkCheckBox(
    secimler,
    text=dil["uppercase"]
)

buyuk.grid(
    row=0,
    column=1,
    padx=30,
    pady=10
)


sayi = ctk.CTkCheckBox(
    secimler,
    text=dil["number"]
)

sayi.grid(
    row=1,
    column=0,
    padx=30,
    pady=10
)


sembol = ctk.CTkCheckBox(
    secimler,
    text=dil["symbol"]
)

sembol.grid(
    row=1,
    column=1,
    padx=30,
    pady=10
)


ctk.CTkLabel(
    ana,
    text=dil["exclude"],
    font=("Arial",18,"bold")
).pack(
    pady=10
)


haric = ctk.CTkEntry(
    ana,
    width=400,
    placeholder_text=dil["exclude_example"]
)

haric.pack()


olustur = ctk.CTkButton(
    ana,
    text=dil["generate"],
    width=350,
    height=50,
    font=("Arial",18,"bold"),
    command=sifre_olustur
)

olustur.pack(
    pady=30
)


sonuc = ctk.CTkLabel(
    ana,
    text=""
)

sonuc.pack()


app.mainloop()