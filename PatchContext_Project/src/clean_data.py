import json

with open("data/commits.json","r",encoding="utf-8") as f:
    raw_commits=json.load(f)    #opposite of dump JSON file convert into python list 

cleaned_commits=[]  #  After cleaning data will be save here 

for item in raw_commits:
    cleaned_commit={    # for neccessary keys
        "type":"commit",
        "id":item["sha"],
        "author":item["commit"]["author"]["name"],
        "date":item["commit"]["author"]["date"],
        "text":item["commit"]["message"],
        "url":item["html_url"]
    }
    cleaned_commits.append(cleaned_commit)  #each dict saved in list 

print("Cleaned Commits:",len(cleaned_commits))
print("Sample:",cleaned_commits[0])

with open("data/cleaned_commits.json","w",encoding="utf-8") as f:
    json.dump(cleaned_commits,f,indent=2,ensure_ascii=False)    #it makes the text more readable allow emojis/special symbol add

with open("data/pull_requests.json", "r", encoding="utf-8") as f:
    raw_prs = json.load(f)

cleaned_prs = []

for item in raw_prs:
    body_text=item["body"] if item["body"] else ""
    combined_text=item["title"]+"\n\n"+ body_text

    cleaned_pr = {
        "type": "pull_request",
        "id": str(item["number"]),
        "author": item["user"]["login"],
        "date": item["created_at"],
        "text": combined_text,
        "url": item["html_url"]
    }
    cleaned_prs.append(cleaned_pr)

print("Cleaned PRs:", len(cleaned_prs))
print("Sample:", cleaned_prs[0])

with open("data/cleaned_prs.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_prs, f, indent=2, ensure_ascii=False)

print("Saved to data/cleaned_commits.json")


with open("data/issues.json", "r", encoding="utf-8") as f:
    raw_issues = json.load(f)

cleaned_issues = []

for item in raw_issues:
    body_text = item["body"] if item["body"] else ""
    combined_text = item["title"] + "\n\n" + body_text

    cleaned_issue = {
        "type": "issue",
        "id": str(item["number"]),
        "author": item["user"]["login"],
        "date": item["created_at"],
        "text": combined_text,
        "url": item["html_url"]
    }
    cleaned_issues.append(cleaned_issue)

print("Cleaned issues:", len(cleaned_issues))
print("Sample:", cleaned_issues[0])

with open("data/cleaned_issues.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_issues, f, indent=2, ensure_ascii=False)


final_dataset = cleaned_commits + cleaned_prs + cleaned_issues

print("Total items in final dataset:", len(final_dataset))

with open("data/final_dataset.json", "w", encoding="utf-8") as f:
    json.dump(final_dataset, f, indent=2, ensure_ascii=False)

print("Saved to data/final_dataset.json")
print("Saved to data/cleaned_issues.json")