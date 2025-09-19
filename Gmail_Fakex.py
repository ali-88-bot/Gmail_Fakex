import requests
import time
from bs4 import BeautifulSoup
from plyer import notification
from colorama import init, Fore
import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

init(autoreset=True)

def type_effect(text, delay=0.01, color=Fore.RED):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

domain_resp = requests.get("https://api.mail.tm/domains")
domain = domain_resp.json()["hydra:member"][0]["domain"]
username = "user" + str(int(time.time()))
email_address = f"{username}@{domain}"
password = "StrongPassword123!"

register_resp = requests.post("https://api.mail.tm/accounts", json={
    "address": email_address,
    "password": password
})
if register_resp.status_code != 201:
    print(Fore.RED + "❌ Failed to create account:", register_resp.text)
    exit()

token_resp = requests.post("https://api.mail.tm/token", json={
    "address": email_address,
    "password": password
})
token = token_resp.json()["token"]
headers = {"Authorization": f"Bearer {token}"}

ascii_banner = """
█▀▀▀ █▄ ▄█ █▀▀█ ▀█▀ █       █▀▀ █▀▀█ █ █ █▀▀ █ █ 
█ ▀█ █ █ █ █▄▄█  █  █       █▀▀ █▄▄█ █▀▄ █▀▀  █  
█▄▄█ █   █ █  █ ▄█▄ █▄▄     █   █  █ █ █ █▄▄ █ █
"""

type_effect(ascii_banner, delay=0.002, color=Fore.RED)
time.sleep(1.5)

print(f"✅ Temporary email created: {email_address}")
print("⏳ Waiting for incoming emails...")

seen_ids = set()
start_time = time.time()
max_runtime_minutes = 2
max_runtime_seconds = max_runtime_minutes * 60

try:
    while True:
        if time.time() - start_time > max_runtime_seconds:
            print("\n⏳ Runtime limit reached. Exiting.")
            break

        inbox_resp = requests.get("https://api.mail.tm/messages", headers=headers)
        messages = inbox_resp.json()["hydra:member"]
        for msg in messages:
            msg_id = msg["id"]
            if msg_id in seen_ids:
                continue

            seen_ids.add(msg_id)
            msg_detail = requests.get(f"https://api.mail.tm/messages/{msg_id}", headers=headers).json()
            print(f"\n📬 New email received!")
            print(f"Subject: {msg_detail.get('subject', 'No subject')}")
            print(f"Sender: {msg_detail.get('from', {}).get('address', 'Unknown')}")

            if msg_detail.get('text'):
                print(f"📝 Text:\n{msg_detail['text']}")
                try:
                    notification.notify(title="📬 New Email", message=msg_detail['subject'])
                except Exception as e:
                    print(f"⚠️ Notification error: {e}")
            elif msg_detail.get('html'):
                soup = BeautifulSoup(msg_detail['html'], 'html.parser')
                text = soup.get_text(separator='\n', strip=True)
                print(f"📄 HTML content:\n{text}")
                try:
                    notification.notify(title="📬 New Email", message=msg_detail['subject'])
                except Exception as e:
                    print(f"⚠️ Notification error: {e}")
            elif msg_detail.get('intro'):
                print(f"🔹 Preview:\n{msg_detail['intro']}")
            else:
                print(Fore.RED + "❌ No readable content found in the email.")

            if msg_detail.get('attachments'):
                print(f"📎 This email contains {len(msg_detail['attachments'])} attachment(s).")

        time.sleep(3)
except KeyboardInterrupt:
    print(Fore.RED + "\n🛑 Program interrupted by user.")
