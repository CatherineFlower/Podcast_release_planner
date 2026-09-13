from datetime import date


def get_status_description(status):
    if status == "idea":
        return "Идея выпуска"
    elif status == "planned":
        return "Выпуск запланирован"
    elif status == "recording":
        return "Идет запись"
    elif status == "ready":
        return "Выпуск готов к публикации"
    else:
        return "Неизвестный статус"


def check_release_readiness(title, topic, status):
    if title == "" or topic == "":
        return "Не заполнены название или тема выпуска"

    if status == "ready" or status == "published":
        return "Выпуск готов к публикации"

    return "Выпуск еще находится в работе"


def get_days_until_release(release_date):
    today = date.today()
    days = (release_date - today).days

    if days > 0:
        return f"До публикации осталось дней: {days}"
    elif days == 0:
        return "Публикация запланирована на сегодня"
    else:
        return f"Дата публикации прошла дней назад: {-days}"


podcast_name = "Технологии без сложностей"
episode_title = "Как выбрать тему для первого подкаста"
episode_topic = "Подготовка и планирование подкаста"
episode_status = "ready"
episode_number_text = "1"
episode_number = int(episode_number_text)
release_date = date(2026, 9, 20)

print("Подкаст:", podcast_name)
print("Выпуск №", episode_number)
print("Название:", episode_title)
print("Тема:", episode_topic)
print("Статус:", get_status_description(episode_status))
print("Готовность:", check_release_readiness(
    episode_title,
    episode_topic,
    episode_status
))
print(get_days_until_release(release_date))