from django.core.management.utils import get_random_secret_key

key = get_random_secret_key()

file = 'kaboom/db_secrets.example.py'

with open(file, 'r+') as f:
    file_src = f.read()
    new_src = file_src.replace('<secret_key>', key)
    f.seek(0)
    f.write(new_src)
    f.truncate()