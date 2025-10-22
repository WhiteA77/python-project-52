# Task_manager

<https://python-project-52-peuw.onrender.com>

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=WhiteA77_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=WhiteA77_python-project-52)

## Hexlet tests and linter status

[![Actions Status](https://github.com/WhiteA77/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/WhiteA77/python-project-52/actions)

## Описание

Task Manager — учебное Django-приложение из трека Хекслета. Сервис позволяет:

- регистрировать пользователей и управлять личными данными;
- создавать, редактировать и фильтровать задачи по статусу, исполнителю, меткам или только собственные;
- поддерживать списки статусов и меток с защитой от удаления при наличии связанных задач.

Интерфейс строится на Bootstrap, весь фронтенд рендерится сервером через Django Templates. Секреты и доступы подаются через переменные окружения, приложение одинаково работает с SQLite и PostgreSQL.

## Используемые технологии

- Django 5: серверная логика и class-based views
- Django Templates + Bootstrap 5: интерфейс и верстка
- django-filter: фильтрация задач
- uv: управление зависимостями и запуск команд
- Gunicorn + Whitenoise: продакшен-сервер и отдача статики
- Rollbar: мониторинг ошибок
- SonarCloud: контроль качества и покрытия тестами

## Команды Makefile

- `make install` — установить зависимости через uv
- `make migrate` — применить миграции (`uv run python manage.py migrate --noinput`)
- `make collectstatic` — собрать статику (`uv run python manage.py collectstatic --noinput`)
- `make start` — запустить сервер разработки (`uv run python manage.py runserver 0.0.0.0:8000`)
- `make build` — выполнить скрипт деплоя `build.sh`
- `make render-start` — старт приложения на Render (`gunicorn task_manager.wsgi`)
- `make test` — прогнать тесты (`uv run python manage.py test`)

## Мониторинг

- [Rollbar: мониторинг ошибок](https://rollbar.com/vden032/TaskManager/)
