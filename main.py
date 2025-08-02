import requests
import random
import time
import threading

# Config
NAMES = 10
THREADS = 150
FILE = 'valid.txt'
BIRTHDAY = '1999-04-20'

# Phonetic components
starts = ['lu', 'zo', 'ka', 'le', 'su', 'mi', 'no', 'ze', 'fi', 'vi', 'to', 'ra', 'sa', 'po']
ends = ['ra', 'no', 'li', 'ka', 'ro', 'to', 'na', 'ko', 'za', 'qi', 'mo', 'vu', 'xi', 'lu', 'en']

# Color formatting
class bcolors:
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# Shared variables
found = 0
lock = threading.Lock()

def make_username():
    # Build a pseudo-syllabic 5-letter name
    start = random.choice(starts)
    end = random.choice(ends)
    name = (start + end)[:5]
    return name

def check_username(username):
    url = f'https://auth.roblox.com/v1/usernames/validate?request.username={username}&request.birthday={BIRTHDAY}'
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 429:
            return None, 429
        r.raise_for_status()
        return r.json().get('code'), r.status_code
    except:
        return None, None

def success(username, thread_id):
    global found
    with lock:
        found += 1
        print(f"{bcolors.OKBLUE}[{found}/{NAMES}] [+] Found Username: {username} [T{thread_id}]{bcolors.ENDC}")
        with open(FILE, 'a+') as f:
            f.write(f"{username}\n")

def taken(username, thread_id):
    print(f'{bcolors.FAIL}[-] {username} is taken [T{thread_id}]{bcolors.ENDC}')

def worker(thread_id):
    global found
    while True:
        with lock:
            if found >= NAMES:
                break

        username = make_username()
        result, status = check_username(username)

        if status == 429:
            time.sleep(5)
            continue
        if result is None:
            time.sleep(0.1)
            continue

        if result == 0:
            success(username, thread_id)
        else:
            taken(username, thread_id)

# Start threads
print(f"[*] Starting {THREADS} threads. Looking for {NAMES} aesthetic usernames.\n")
threads = []
for i in range(THREADS):
    t = threading.Thread(target=worker, args=(i+1,), daemon=True)
    t.start()
    threads.append(t)

try:
    while found < NAMES:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[!] Interrupted by user.")

print(f"\n{bcolors.OKBLUE}[!] Finished. {found} usernames saved to {FILE}.{bcolors.ENDC}")

