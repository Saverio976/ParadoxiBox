# HOST=0.0.0.0
HOST=127.0.0.1
PORT=8000
PACKAGE?=

runserver:
	source ./.venv/bin/activate && ./manage.py runserver ${HOST}:${PORT}

migrate:
	source ./.venv/bin/activate && ./manage.py migrate

makemigrations:
	source ./.venv/bin/activate && ./manage.py makemigrations

shell:
	source ./.venv/bin/activate && ./manage.py shell

createsuperuser:
	source ./.venv/bin/activate && ./manage.py createsuperuser

pip-install:
	if [ -n "${PACKAGE}" ]; then \
		echo "${PACKAGE}" >> requirements.txt; \
	fi
	if [ ! -d "./.venv" ]; then \
		python -m venv ./.venv; \
	fi
	source ./.venv/bin/activate && pip install -r requirements.txt

clean:
	find . -name "*.pyc" -type f -delete

re: fclean makemigrations migrate createsuperuser runserver

install: pip-install migrate
