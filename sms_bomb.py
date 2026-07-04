from colorama import Fore, Style
from time import sleep
from os import system
from sms import SendSms
import threading
import re
import sys

def temizle_numara(num):
    """Numarayı standart 10 haneli forma çevirir"""
    if not num:
        return None
    # Tüm non-digit karakterleri sil
    num = re.sub(r'\D', '', num)
    # +90 veya 90 ile başlıyorsa kaldır
    if num.startswith('90'):
        num = num[2:]
    elif num.startswith('0'):
        num = num[1:]
    if len(num) == 10:
        return num
    return None

# Servisleri bir kere al, sonra kullan
def get_servisler():
    servisler = []
    for attr in dir(SendSms):
        if not attr.startswith('__') and callable(getattr(SendSms, attr)):
            servisler.append(attr)
    return servisler

servisler_sms = get_servisler()

def clear_screen():
    system("cls||clear")

while True:
    clear_screen()
    print(f"""{Fore.LIGHTCYAN_EX}
    ____   ____  _       ______   _________  _______     ________  _____       ______   ____    ____   ______   
|_  _| |_  _|/ \    .' ____ \ |  _   _  ||_   __ \   |_   __  ||_   _|    .' ____ \ |_   \  /   _|.' ____ \  
  \ \   / / / _ \   | (___ \_||_/ | | \_|  | |__) |    | |_ \_|  | |      | (___ \_|  |   \/   |  | (___ \_| 
   \ \ / / / ___ \   _.____`.     | |      |  __ /     |  _| _   | |   _   _.____`.   | |\  /| |   _.____`.  
    \ ' /_/ /   \ \_| \____) |   _| |_    _| |  \ \_  _| |__/ | _| |__/ | | \____) | _| |_\/_| |_ | \____) | 
     \_/|____| |____|\______.'  |_____|  |____| |___||________||________|  \______.'|_____||_____| \______.' 
    {Style.RESET_ALL}
    Sms Servis Sayısı: {Fore.LIGHTGREEN_EX}{len(servisler_sms)}{Style.RESET_ALL}           {Fore.LIGHTRED_EX}by @Vastrel{Style.RESET_ALL}
    """)
    
    try:
        menu = input(Fore.LIGHTGREEN_EX + " 1- SMS Gönder (Normal)\n 2- SMS Gönder (Turbo)\n 3- Çıkış\n\n Seçim: " + Fore.LIGHTYELLOW_EX)
        if not menu.strip():
            continue
        menu = int(menu)
    except ValueError:
        clear_screen()
        print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın kral, tekrar dene.")
        sleep(2)
        continue

    if menu == 3:
        clear_screen()
        print(Fore.LIGHTRED_EX + "Çıkış yapılıyor... Güle güle kral.")
        break

    # ===================== NORMAL MOD =====================
    if menu == 1:
        clear_screen()
        print(Fore.LIGHTYELLOW_EX + "[1] Tek numara\n[2] Çoklu numara (dosya veya liste)" + Fore.LIGHTGREEN_EX)
        secim = input("Seçim: ").strip()

        tel_liste = []
        if secim == "1":
            clear_screen()
            tel_input = input(Fore.LIGHTYELLOW_EX + "Telefon numarasını gir (her format olur): " + Fore.LIGHTGREEN_EX).strip()
            cleaned = temizle_numara(tel_input)
            if cleaned:
                tel_liste.append(cleaned)
            else:
                print(Fore.LIGHTRED_EX + "Geçersiz numara.")
                sleep(2)
                continue

        elif secim == "2":
            clear_screen()
            print(Fore.LIGHTYELLOW_EX + "Numaraları gir (her satıra bir tane, bitince boş satır veya dosya yolu):")
            while True:
                line = input().strip()
                if not line:
                    break
                if line.lower().endswith(('.txt', '.csv')) or any(c in line for c in '/\\'):
                    try:
                        with open(line, "r", encoding="utf-8") as f:
                            for raw in f.readlines():
                                cleaned = temizle_numara(raw.strip())
                                if cleaned:
                                    tel_liste.append(cleaned)
                    except Exception as e:
                        print(Fore.LIGHTRED_EX + f"Dosya okuma hatası: {e}")
                    break
                else:
                    cleaned = temizle_numara(line)
                    if cleaned:
                        tel_liste.append(cleaned)
        else:
            print(Fore.LIGHTRED_EX + "Yanlış seçim.")
            sleep(2)
            continue

        if not tel_liste:
            print(Fore.LIGHTRED_EX + "Hiç numara girmedin.")
            sleep(2)
            continue

        # Mail
        clear_screen()
        mail = input(Fore.LIGHTYELLOW_EX + "Mail adresi (enter ile boş): " + Fore.LIGHTGREEN_EX).strip()
        if mail and ("@" not in mail or "." not in mail):
            print(Fore.LIGHTRED_EX + "Mail formatı hatalı.")
            sleep(2)
            continue

        # Adet ve aralık
        clear_screen()
        kere_input = input(Fore.LIGHTYELLOW_EX + "Kaç adet SMS (sonsuz için enter): " + Fore.LIGHTGREEN_EX).strip()
        kere = int(kere_input) if kere_input.isdigit() else None

        clear_screen()
        try:
            aralik = int(input(Fore.LIGHTYELLOW_EX + "Kaç saniye aralıkla göndersin: " + Fore.LIGHTGREEN_EX))
        except ValueError:
            aralik = 1

        # Gönderme
        for tel in tel_liste:
            clear_screen()
            print(Fore.LIGHTCYAN_EX + f"[{tel}] numarasına gönderiliyor...")
            sms = SendSms(tel, mail)
            
            try:
                if kere is None:  # Sonsuz
                    while True:
                        for servis in servisler_sms:
                            try:
                                getattr(sms, servis)()
                            except Exception as e:
                                print(Fore.LIGHTRED_EX + f"Servis hatası ({servis}): {e}")
                            sleep(aralik)
                else:  # Belirli adet
                    while sms.adet < kere:
                        for servis in servisler_sms:
                            if sms.adet >= kere:
                                break
                            try:
                                getattr(sms, servis)()
                            except Exception:
                                pass
                            sleep(aralik)
            except KeyboardInterrupt:
                print(Fore.LIGHTYELLOW_EX + "\nDurduruldu.")
                break

        input(Fore.LIGHTRED_EX + "\nMenüye dönmek için enter'a bas...")

    # ===================== TURBO MOD =====================
    elif menu == 2:
        clear_screen()
        tel_input = input(Fore.LIGHTYELLOW_EX + "Telefon numarası: " + Fore.LIGHTGREEN_EX).strip()
        tel_no = temizle_numara(tel_input)
        if not tel_no:
            print(Fore.LIGHTRED_EX + "Geçersiz numara.")
            sleep(2)
            continue

        clear_screen()
        mail = input(Fore.LIGHTYELLOW_EX + "Mail (enter boş): " + Fore.LIGHTGREEN_EX).strip()
        if mail and ("@" not in mail or "." not in mail):
            print(Fore.LIGHTRED_EX + "Mail hatalı.")
            sleep(2)
            continue

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
                    t.join(timeout=10)  # Deadlock önlemek için timeout

        print(Fore.LIGHTGREEN_EX + f"🚀 TURBO BAŞLADI → {tel_no}")
        print(Fore.LIGHTYELLOW_EX + "Durdurmak için Ctrl+C")

        try:
            turbo_mode()
        except KeyboardInterrupt:
            dur.set()
            clear_screen()
            print(Fore.LIGHTRED_EX + "Turbo durduruldu. Menüye dönülüyor...")
            sleep(1.5)

    else:
        print(Fore.LIGHTRED_EX + "Bilinmeyen menü seçeneği.")
        sleep(2)
