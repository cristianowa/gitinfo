# Git info

Have you ever wanted to know which developer, period is more productive (in terms of lines of code changed)? Well, this tools aims to provide some inside over it.

## Installing

For now, this is not published to pypi, so you have to use the source code.

## Structure
The gitinfo.py script provides a simple interface to discover the information via command line.

A django app is also provided to store permanently the information and allow out-of-the-app users (i.e. managers) to use it.

## Roadmap

- Do the same parsing in a sub-directory.
- Publish to pypi
- Save other content in the django app (e.g. test results)
- Compare errors among commits via Django
- Create method to update all repositories
- Create django command to update all repositories