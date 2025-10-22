.PHONY: install migrate collectstatic start render-start build test setup start-server

install:
	uv sync

migrate:
	uv run python manage.py migrate --noinput

collectstatic:
	uv run python manage.py collectstatic --noinput

start:
	uv run python manage.py runserver 0.0.0.0:8000

start-server:
	uv run python manage.py runserver 0.0.0.0:3000

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh

test:
	uv run python manage.py test

setup: install migrate
