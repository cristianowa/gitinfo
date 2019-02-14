# Git info

Have you ever wanted to know which developer, period is more productive (in terms of lines of code changed)? Well, this tools aims to provide some inside over it.

## Requirements

You need to install git-extra `sudo apt-get install git-extra` so all comands are avaialble.

## Installing

For now, this is not published to pypi or dockerhub, so you have to use the source code or build the docker yourself.

## Structure
The gitinfo.py script provides a simple interface to discover the information via command line.

A django app and site is also provided to store permanently the information and allow out-of-the-app users (i.e. managers) to use it.

## Features

 - Commit timeline with metrics (lines/characters add/sub/churned) and files involved
 - Dependencies (to and from) of each repository (require dependencies to be listed for complete check)
 - Developers metrics in the last 30, 60, 90, 180 and 360
 - Database update with single command (update\_repos, update\_devs and recreate)

## Running

You can run the production server *gunicorn* using this command:

```bash
gunicorn gitinfodjango.wsgi:application --bind 0.0.0.0:8000 --workers 3
```
 
## Docker 

If you want to run this service inside a docker, run:
```bash
sudo docker-compose up --build
```

## Roadmap

- Do the same parsing in a sub-directory.
- Publish to pypi
- Save other content in the django app (e.g. test results)
- Compare errors among commits via Django
- Plugin info: create plugins for calculating metrics for each language (based on extension)
- File count(add, removed, modified) (# partially done, counting files involved in each commit)

## Related projects
### FOSS
- https://github.com/asharov/git-hammer
### Proprietary
- https://www.gitprime.com/
