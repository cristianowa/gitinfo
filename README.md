# Git info

Have you ever wanted to know which developer, period is more productive (in terms of lines of code changed)? Well, this tools aims to provide some inside over it.

## Installing

For now, this is not published to pypi, so you have to use the source code.

## Structure
The gitinfo.py script provides a simple interface to discover the information via command line.

A django app is also provided to store permanently the information and allow out-of-the-app users (i.e. managers) to use it.

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
- Create method to update all repositories
- Create django command to update all repositories
- Parse submodules and create a dependency graph among all registred repositories 
