# Rest API Rental PPM
"Repository for rental project" 

### How to use
#### Preparation 

- Python 3.8 above

- pip

- virtualenv

- postgresql 

#### Install Library

- `virtualenv ven`
- `activate`

Go to app directory

- `pip install -r requirements.txt`

After all library installed, migrate database

- `python manage.py makemigrations`

- `python manage.py migrate`

create super user

- `python manage.py createsuperuser`

Running aplication

- `python manage.py runserver`  