import os
import requests
import time
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# 1. Load secrets from .env
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# 2. Configuration
TARGETS = ["superbet.com", "robinhood.com", "syfe.com", "23andmebugbounty.com", "earlywarning.com", "alsco.com", "coinhako.com"]
SENDER_EMAIL = os.getenv("EMAIL_SENDER")
SENDER_PASS = os.getenv("EMAIL_PASSWORD") # Your 16-character App Password

def send_email_alert(domain, leak_url):
    msg = EmailMessage()
    msg.set_content(f"🚨 BOUNTY ALERT!\n\nPotential leak found for {domain}.\nView here: {leak_url}")
    msg['Subject'] = f"!!! LEAK DETECTED: {domain} !!!"
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL # Sends to yourself

    try:
        # PythonAnywhere Free Tier allows Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASS)
            smtp.send_message(msg)
        print(f"Email Alert Sent for {domain}!")
    except Exception as e:
        print(f"Email failed: {e}")

def run_hunter():
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN missing in .env")
        return

    print("--- Hunter Online: Monitoring Superbet & Robinhood ---")
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}

    while True:
        for domain in TARGETS:
            query = f'"{domain}" filename:.env'
            url = f"https://api.github.com/search/code?q={query}&sort=indexed"
            try:
                res = requests.get(url, headers=headers).json()
                if 'items' in res and len(res['items']) > 0:
                    leak_link = res['items'][0]['html_url']
                    print(f"MATCH FOUND: {domain}!")
                    send_email_alert(domain, leak_link)
                else:
                    print(f"Scanning {domain}... No leaks.")
            except:
                pass
            time.sleep(20) # Stay safe with API limits

        print("Cycle finished. Sleeping 10 mins...")
        time.sleep(600)

if __name__ == "__main__":
    run_hunter()