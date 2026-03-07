import os
import requests
import time
from dotenv import load_dotenv

# 1. Load your GitHub Token from your existing .env file
load_dotenv()
# Make sure your .env file has: GITHUB_TOKEN=your_actual_token_here
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# 2. These are the "Gold Mine" targets from your screenshot
TARGETS = ["robinhood.com", "superbet.com", "syfe.com", "coinhako.com", "alsco.com", "23andmebugbounty.com", "earlywarning.com"]

def run_bounty_hunter():
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not found in .env file!")
        return

    print("--- System Boot: Ghost Hunter Active ---")
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}

    while True:
        for domain in TARGETS:
            # We are looking for .env files leaked on GitHub for these companies
            query = f'"{domain}" filename:.env'
            url = f"https://api.github.com/search/code?q={query}&sort=indexed"

            try:
                res = requests.get(url, headers=headers).json()
                if 'items' in res and len(res['items']) > 0:
                    print(f"!!! ALERT: potential leak found for {domain} !!!")
                    print(f"Link: {res['items'][0]['html_url']}")
                else:
                    print(f"Scanning {domain}... No leaks found yet.")
            except Exception as e:
                print(f"Scan Error: {e}")

            time.sleep(15) # Stay under GitHub's rate limit

        print("Cycle complete. Sleeping for 10 minutes...")
        time.sleep(600)

if __name__ == "__main__":
    run_bounty_hunter()