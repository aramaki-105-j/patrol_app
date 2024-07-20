web: gunicorn --workers=1 myproject.wsgi --timeout 300 --log-file -
release: python manage.py collectstatic --noinput