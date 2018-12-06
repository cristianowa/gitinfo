import requests

ans = requests.post("http://127.0.0.1:8000/git/repository/", json=dict(url="git@github.com:cristianowa/gitinfo.git"))
ans.raise_for_status()
ans = requests.post("http://127.0.0.1:8000/git/repository/1/update/")
ans.raise_for_status()