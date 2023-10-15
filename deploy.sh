pip install poetry
source $(poetry env info --path)/bin/activate
poetry install
python3.11 manage.py migrate
python3.11 manage.py collectstatic
deactivate