# Podcast Planner — ПР6

Система планирования выпусков подкастов на Python и Django.

В ПР6 веб-часть проекта переведена с формирования HTML-строк
в Python на стандартную систему Django Templates.

## Технологии

- Python 3;
- Django 5.2;
- Django Template Language;
- HTML5;
- CSS3;
- JavaScript;
- Bootstrap 5;
- JSON;
- pytest;
- flake8.

## Что изменилось в ПР6

В ПР5 HTML создавался непосредственно во view-функциях.
В ПР6 используется схема:

```text
URL → view → context → Django template → HTML → браузер
```

Функция `page()` больше не используется веб-представлениями.

Реализованы:

- `templates/base.html`;
- `{% extends %}`;
- `{% block %}`;
- `{% include %}`;
- передача данных через `context`;
- `{% for %}` и `{% empty %}`;
- `{% if %}`;
- именованные URL;
- пространства имён `app_name`;
- ссылки через `{% url %}`;
- фильтры `length` и `default`;
- Django static files;
- собственный CSS;
- изображение;
- JavaScript.

## Шаблоны

Общие шаблоны:

```text
templates/
├── base.html
├── includes/
│   └── navigation.html
└── errors/
    ├── 403.html
    └── 404.html
```

Шаблоны приложений:

```text
homepage/templates/homepage/
podcasts_web/templates/podcasts_web/
episodes_web/templates/episodes_web/
topics_web/templates/topics_web/
authors_web/templates/authors_web/
```

Повторяющиеся компоненты вынесены в include:

```text
podcasts_web/includes/podcast_card.html
episodes_web/includes/episode_status.html
```

## Static

```text
homepage/static/homepage/
├── css/
│   └── style.css
├── js/
│   └── main.js
└── img/
    └── logo.png
```

В `base.html` используется:

```django
{% load static %}
```

CSS:

```django
{% static 'homepage/css/style.css' %}
```

JavaScript:

```django
{% static 'homepage/js/main.js' %}
```

Изображение:

```django
{% static 'homepage/img/logo.png' %}
```

## Основные страницы

```text
/login/
/                       главная
/podcasts/              список подкастов
/podcasts/<id>/         отдельный подкаст
/episodes/              список выпусков
/episodes/<id>/         отдельный выпуск
/topics/                темы
/authors/               авторы
/statistics/            статистика
```

## Авторизация

Администратор:

```text
admin / admin123
```

Авторы:

```text
anna / anna123
ivan / ivan123
maria / maria123
alex / alex123
elena / elena123
```

Состояние входа хранится в Django Session до явного выхода.

## Хранение данных

Данные всё ещё хранятся в JSON:

```text
data/users.json
data/podcasts.json
data/topics.json
data/episodes.json
```

Используются существующие Python-классы из `models/`.
Django ORM в ПР6 не внедряется.

HTML-формы, существовавшие в ПР5, сохранены, но Django Forms
на этом этапе не используются.

## Проверка

```bash
python manage.py check
python manage.py runserver
pytest -v
flake8 . --extend-exclude=venv,.venv
```

Проверка статического изображения:

```bash
python manage.py findstatic homepage/img/logo.png
```

## Git

Коммит ПР6:

```bash
git add .
git commit -m "PR6: add Django templates and static files"
git push
```

Все коммиты этой работы должны начинаться с `PR6:`.
