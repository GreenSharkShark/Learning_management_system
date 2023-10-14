pip install poetry
poetry shell
poetry install
python3.11 manage.py migrate
python3.11 manage.py collectstatic
deactivate