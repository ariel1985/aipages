# AI Pages first edition

# Running

```

source venv/bin/activate

python manage.py runserver
```


# Fresh Ubuntu Installation Set up:

The history: 

```bash
sudo apt update
python3 -V
sudo apt install python3-django
django-admin --version
sudo apt install python3-pip python3-venv
python3 -m venv venv
mkdir poc0
cd poc0/

# activate virtualenv
source venv/bin/activate

# set up django
django-admin startproject aipages .
python manage.py migrate
python manage.py createsuperuser
sudo apt install python-is-python3
sudo ufw allow 8000
python manage.py runserver localhost:8000
# or just
python manage.py runserver

python manage.py startapp app

# python manage.py makemigrations app # when createin the app ....

python manage.py createsuperuser

admin / 1234

```


# Django Set Up after environment setup

```bash
mkdir poc1
cd poc1/
# create virtualenv
python3 -m venv venv
# activate virtualenv
source venv/bin/activate

pip install django

# set up django
django-admin startproject aipages .

python manage.py migrate

python manage.py runserver localhost:8000
# or just
python manage.py runserver

python manage.py startapp app

# python manage.py makemigrations app # when createin the app ....

python manage.py createsuperuser

admin / 1234

```


# Usful tutorials

https://www.youtube.com/watch?v=TOLCkFqd4nI&list=PLkeoo2ahcgvdTTx2U835RAO_R8UwS6oaf&ab_channel=KumarAbhishek008 

