This is a simple Django app for managing Assetto Corsa Servers, without entry_list.cfg.

*Installation*
- put this code into your django folder
- add "'ac'," to you INSTALL_APPS in settings.py
- make migrations for ac
  - python manage.py makemigrations ac
- migrate migrations for ac
  - python manage.py migrate ac
- load default/sample data (default tracks, cars and sample car classes)
  - python manage.py loaddata ac.json

*Tested with:*
- python 3.5
- Django 1.11
