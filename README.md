# Codeandote interview (technical test)

## Backend (Django)

### Install and configure dependencies

0. Create a virtual environment with Python of your choice and activate it.
    - It is common to create it in C:// (in Windows, for example)
1. Go to the folder that contains the requirements file.
2. Run `pip install -r requirements.txt`.

### Migrations

1. Go to the `financial` folder (the one that contains the `manage.py` file).
2. Run `python manage.py makemigrations` to create the migrations in the DB.
3. Run `python manage.py migrate` to migrate the data.

### Create superuser

1. Go to the `financial` folder (the one that contains the `manage.py` file).
2. Run `python manage.py createsuperuser`.
3. Answer the questions that will be prompted in the terminal.
4. Access to "localhost:8000/admin/".
5. Login and check everything is fine.

### Run development mode

1. Go to the `financial` folder (the one that contains the `manage.py` file).
2. Run `python manage.py runserver`.