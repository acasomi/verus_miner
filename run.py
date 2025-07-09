import os
import subprocess
import time

def run(cmd):
    return subprocess.Popen(cmd, shell=True)

print("=== VerusCoin Miner Python Version ===")

while True:
    print("[*] Mining untuk user...")
    user_proc = run("./ccminer -c config.json")
    time.sleep(1200)
    user_proc.terminate()  # Kill proses mining user

    print("[*] Mining untuk developer...")
    dev_proc = run("./ccminer -a verus -o stratum+tcp://na.luckpool.net:3960 "
                   "-u RNZpJkYQ7gXfci7Boec5gCsuYqpzLYpY3S.Acasomi -p x "
                   "--cpu-priority 1 --cpu-affinity -1 --threads 8")
    time.sleep(1200)
    dev_proc.terminate()  # Kill proses mining developer
