import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

url = "https://api.github.com/repos/fastapi/fastapi/pulls"

all_prs = []
max_pages = 5

for page_number in range(1, max_pages + 1):
    params = {
        "state": "closed",
        "per_page": 100,
        "page": page_number,
        "sort": "updated",
        "direction": "desc"
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Error on page", page_number, ":", response.status_code)
        break

    page_data = response.json()

    if len(page_data) == 0:
        print("No more PRs found. Stopping at page", page_number)
        break

    all_prs.extend(page_data)
    print("Page", page_number, "fetched. Total PRs so far:", len(all_prs))

print("Total PRs collected:", len(all_prs))

with open("data/pull_requests.json", "w", encoding="utf-8") as f:
    json.dump(all_prs, f, indent=2)

print("Saved to data/pull_requests.json")