HOST			?=		127.0.0.1
PORT			?=		8000
ALLOWED_HOST	?=		*
LANGUAGE_CODE	?=		en-us
TIME_ZONE		?=		Europe/Paris
SECRET_KEY		?=		django-secret-key-wow-so-random0123456789
PACKAGE			?=

runserver-dev:
	source ./.venv/bin/activate && 				\
		ALLOWED_HOST=${ALLOWED_HOST} 			\
		DEBUG=True								\
		LANGUAGE_CODE=${LANGUAGE_CODE} 			\
		TIME_ZONE=${TIME_ZONE} 					\
		SECRET_KEY=${SECRET_KEY} 				\
		./manage.py runserver ${HOST}:${PORT}

runserver-prod:
	source ./.venv/bin/activate &&				\
		ALLOWED_HOST=${ALLOWED_HOST} 			\
		DEBUG=False								\
		LANGUAGE_CODE=${LANGUAGE_CODE} 			\
		TIME_ZONE=${TIME_ZONE} 					\
		SECRET_KEY=${SECRET_KEY} 				\
		daphne ParadoxiBox.asgi:application -p ${PORT} -b ${HOST}

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

install: pip-install migrate
