# AI Pages first edition

## Python Running
```bash
source venv/bin/activate

python manage.py runserver
```


## Fresh Ubuntu Installation Set up:

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
```


## Django Installation Set up:

```bash
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

### Usful tutorials

https://www.youtube.com/watch?v=TOLCkFqd4nI&list=PLkeoo2ahcgvdTTx2U835RAO_R8UwS6oaf&ab_channel=KumarAbhishek008 

Free Components for blocks : https://tailwindcomponents.com/



# Chatbots are next: 

## To install 
```bash
pip install rasa
python -m rasa --version

pip install 'sqlalchemy<2.0'
```

## To run

```bash
cd poc3/rasabot # folder rasa was installed

python -m rasa run --enable-api --cors "*"

python -m rasa shell --debug

```

### To test
```bash
curl localhost:5005/model/parse -d '{"text":"hello"}'
```

chatGPT can be implemented in rasa 
https://medium.com/@maliahrajan/unleashing-the-power-of-ai-create-a-next-generation-chatbot-with-rasa-and-chatgpt-aba87f30cb94


# WhatsApp API is next...
https://medium.com/@alfredpfrancis/integrate-rasa-with-whatsapp-1b1477b51090



# R&D

## Then comes payment methods

### Paypal :

https://github.com/jazzband/django-payments

https://django-payments.readthedocs.io/en/latest/index.html  - has a lot of providers backend 

https://djangopackages.org/grids/g/payment-processing/ - comparisons

Best practice file structure:

my_website/
│
├── templates/
│   └── base.html
│
├── home/
│   ├── templates/
│   │   ├── home/
│   │   │   └── index.html
│   │
│   ├── static/
│   │   ├── home/
│   │   │   ├── css/
│   │   │   └── js/
│
├── builder/
│   ├── templates/
│   │   ├── builder/
│   │   │   └── index.html
│   │
│   ├── static/
│   │   ├── builder/
│   │   │   ├── css/
│   │   │   └── js/



# Troubleshooting:

```
sudo lsof -i:8000
kill -9 PI
```


