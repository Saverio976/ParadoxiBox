HOST					?=		127.0.0.1
PORT					?=		8000
ALLOWED_HOST			?=		*
LANGUAGE_CODE			?=		en-us
TIME_ZONE				?=		Europe/Paris
SECRET_KEY				?=		django-secret-key-wow-so-random0123456789
PACKAGE					?=
PYTHON					?=		python
COMMAND					?=

TARGET_SERVICE_PATH		=		/etc/systemd/user/paradoxibox.service

runserver-dev:
	. ./.venv/bin/activate && 				\
		ALLOWED_HOST=${ALLOWED_HOST} 			\
		DEBUG=True								\
		LANGUAGE_CODE=${LANGUAGE_CODE} 			\
		TIME_ZONE=${TIME_ZONE} 					\
		SECRET_KEY=${SECRET_KEY} 				\
		./manage.py runserver ${HOST}:${PORT}

runserver-prod:
	. ./.venv/bin/activate &&				\
		ALLOWED_HOST=${ALLOWED_HOST} 			\
		DEBUG=False								\
		LANGUAGE_CODE=${LANGUAGE_CODE} 			\
		TIME_ZONE=${TIME_ZONE} 					\
		SECRET_KEY=${SECRET_KEY} 				\
		daphne ParadoxiBox.asgi:application -p ${PORT} -b ${HOST}

migrate:
	. ./.venv/bin/activate && ./manage.py migrate --noinput

makemigrations:
	. ./.venv/bin/activate && ./manage.py makemigrations

collectstatic:
	. ./.venv/bin/activate && ./manage.py collectstatic --noinput

shell:
	. ./.venv/bin/activate && ./manage.py shell

managepy:
	. ./.venv/bin/activate && ./manage.py ${COMMAND}

createsuperuser:
	. ./.venv/bin/activate && ./manage.py createsuperuser

pip-install:
	if [ -n "${PACKAGE}" ]; then \
		echo "${PACKAGE}" >> requirements.txt; \
	fi
	if [ ! -d "./.venv" ]; then \
		${PYTHON} -m venv --system-site-packages ./.venv; \
	fi
	. ./.venv/bin/activate && pip install -U pip
	. ./.venv/bin/activate && pip install -U wheel
	. ./.venv/bin/activate && pip install -r requirements.txt

pip-install-dev: pip-install
	. ./.venv/bin/activate && pip install -r requirements-dev.txt

install: pip-install migrate collectstatic

service-setup:
	PARADOXIBOX_FOLDER="$$PWD"				\
	ALLOWED_HOST="${ALLOWED_HOST}"			\
	LANGUAGE_CODE="${LANGUAGE_CODE}"		\
	TIME_ZONE="${TIME_ZONE}"				\
	SECRET_KEY="${SECRET_KEY}"				\
	HOST="${HOST}"							\
	PORT="${PORT}"							\
	PYTHON="${PYTHON}"						\
		envsubst < ./paradoxibox.service > "${TARGET_SERVICE_PATH}"

service-enable:
	systemctl --user enable --now paradoxibox.service

service-disable:
	systemctl --user disable --now paradoxibox.service

service-fclean:
	rm -f "${TARGET_SERVICE_PATH}"

service-restart:
	systemctl --user restart paradoxibox.service
