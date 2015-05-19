# Atable

Atable is a recipe manager, written in Django.

## Requirements

Atable is written in Python3, and does not plan to support Python2 for now
(althrough it could come later). Its only real requirement is Django-1.8 (but
some optional Django dependencies are also required, like Pillow or PyYAML).

## Setup

1. Install Virtualenv, if you don’t have it yet

    pip install --user virtualenv

2. Create a virtualenv with Python3

    virtualenv -p /usr/bin/python3 atable_env

3. Activate this virtualenv

    source ./atable_env/bin/activate

4. Clone repository, and get in the project dir

    git clone https://github.com/gordon-/atable
    cd atable

5. Install project dependencies

    pip install -r requirements.txt


## Run in debug mode

The provided `settings.py` is sufficient for debug purposes. In development
environment, you can work with a SQLite database. Get in the *atable* dir in the
project repository, and type:

    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver

## Run in production

In production, you are adviced to use a Postgresql database. From the Django
root (`/atable` from the repository root), copy
`atable/localsettings.py.example` to `atable/localsettings.py`, and edit the
contents of the new file. Then, type:

    ./manage.py collectstatic
    ./manage.py migrate
    ./manage.py createsuperuser

The Django app is ready to serve. You now have to make it run with the supplied
Gunicorn, one way or another. We suggest `supervisor`, and [this nice guide (in
french)](http://www.miximum.fr/deployer-django-en-production-nginx-gunicorn-supervisor.html) 
that clearly explains how to install all of this.

Don’t forget to statically serve the `staticfiles` dir under the `/static/` URL,
in your virtualhost!

## Licence

Copyright © 2015, FFDN

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

The Software is provided “as is”, without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability, fitness
for a particular purpose and noninfringement. In no event shall the authors or
copyright holders X be liable for any claim, damages or other liability, whether
in an action of contract, tort or otherwise, arising from, out of or in
connection with the software or the use or other dealings in the Software.

Except as contained in this notice, the name of the FFDN shall not be used in
advertising or otherwise to promote the sale, use or other dealings in this
Software without prior written authorization from the FFDN.
