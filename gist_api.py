import requests
import json
import os

GIST_ID = os.getenv("GIST_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
FILENAME = "db.json"

def load_data():
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = requests.get(url, headers=headers)
    content = res.json()["files"][FILENAME]["content"]
    return json.loads(content)

def save_data(data):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "files": {
            FILENAME: {
                "content": json.dumps(data, indent=2)
            }
        }
    }
    res = requests.patch(url, headers=headers, json=payload)
    return res.status_code == 200
