import requests
url="git@github.com:cristianowa/gitinfo.git"
ans = requests.get("http://127.0.0.1:8000/git/repository/?url={}".format(url))
ans.raise_for_status()
print(ans.json())
if not ans.json():
    ans = requests.post("http://127.0.0.1:8000/git/repository/", json=dict(url=url))
    ans.raise_for_status()
ans = requests.get("http://127.0.0.1:8000/git/repository/?url={}".format(url))
ans.raise_for_status()
repo_id = ans.json()[0]["id"]

ans = requests.post("http://127.0.0.1:8000/git/repository/{}/update/".format(repo_id))
ans.raise_for_status()

ans = requests.post("http://127.0.0.1:8000/git/commiterrortype/", json=dict(name="Test Failure"))
ans.raise_for_status()
