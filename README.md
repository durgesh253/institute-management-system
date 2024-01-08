# institute-management-panel
institute-management-panel


# create virtual environment
>>> python -m venv [venv-name]

# Activate venv
>>> [venv-name]\Scripts\activate

# Deactivate venv
>>> [venv-name]\Scripts\deactivate

# install python libraries
>>> pip install [lib-name]

# check installed libraries
>>> pip list/ pip freeze

# add libraries and package with version in requiremnts.txt
>>> pip freeze > requirements.txt

# install libraries and package from requiremts.txt
>>> pip install -r requirements.txt

# install django [make sure you are in activated env]
>>> pip install django

# create django project
>>> django-admin startproject [project-name] .

# create app 
>>> python manage.py startapp [app-name]

# run server
>>> python manage.py runserver [port]

# migrate your table
>>> python manage.py migrate

# makemigrations
>>> python manage.py makemigrations

# create superuser[Admin]
>>> python manage.py createsuperuser
Username (leave blank to use 'admin'): admin
Email address: admin@gmail.com
Password:
Password (again):
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.