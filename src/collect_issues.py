#To avoid Pull Request that mixed with issues and return PRs 
import requests
import os
from dotenv import load_dotenv
import json # # Python data <-> convert Into JSON File 


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

url = "https://api.github.com/repos/fastapi/fastapi/issues"

all_issues = []
max_pages = 20

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
        print("No more issues found. Stopping at page", page_number)
        break

    for item in page_data:
        if "pull_request" not in item:
            all_issues.append(item)

    print("Page", page_number, "fetched. Total real issues so far:", len(all_issues))

print("Total issues collected:", len(all_issues))

with open("data/issues.json", "w", encoding="utf-8") as f:
    json.dump(all_issues, f, indent=2)

print("Saved to data/issues.json")