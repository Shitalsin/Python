import requests             #to send HTTP request 
import os
from dotenv import load_dotenv
import json

load_dotenv()

GITHUB_TOKEN=os.getenv("GITHUB_TOKEN")
#This is a dictionary where we send extra info along with request
headers={
    "Authorization":f"token {GITHUB_TOKEN}",    # Identity to the github 
    "Accept":"application/vnd.github+json"     #Give me response in form of json
}

url="https://api.github.com/repos/fastapi/fastapi/commits"      # Exact location where we request 

"""
params={"per_page":30}  # Extra settings that convey pass 30 commits at a time 

response=requests.get(url,headers=headers,params=params)    #Send actual request through the internet to Github server 

print("Status code:",response.status_code)  #it tells success or not in form of number 200=success, 401=authentication fail

commits_data=response.json()

print("Number of commites fetched:",len(commits_data))
print("First commit message:",commits_data[0]["commit"]["message"])

with open("data/commits.json", "w", # file open=open/create | data/commits.json=file path | w=write mode 
    encoding="utf-8") as f: #to encode the text 
    json.dump(commits_data, f, indent=2) # Whatever data we have to write ,f=in which file | indent 2= make json readable maintain indentation 

print("Commits saved to data/commits.json")"""

#(Pagination)

all_commits = []    #Empty list 
max_pages = 20   #5 pages fetch 5x100=500 commits 

for page_number in range(1, max_pages + 1):
    params = {"per_page": 100, "page": page_number}
    response = requests.get(url, headers=headers, params=params) 

    if response.status_code != 200:  # if get error like rate limit end then loop will be break 
        print("Error on page", page_number, ":", response.status_code)
        break

    page_data = response.json()

    if len(page_data) == 0: # when commits end return empty list 
        print("No more commits found. Stopping at page", page_number)
        break

    all_commits.extend(page_data) #a list method that append other list items 
    print("Page", page_number, "fetched. Total commits so far:", len(all_commits))

print("Total commits collected:", len(all_commits))

with open("data/commits.json", "w", encoding="utf-8") as f:
    json.dump(all_commits, f, indent=2)

print("Saved to data/commits.json")
