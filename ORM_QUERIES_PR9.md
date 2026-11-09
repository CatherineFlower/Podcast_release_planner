# ORM-запросы ПР9

В проекте реализовано более 15 различных ORM-выражений.

1. `User.objects.get(pk=user_id)` — получение одной записи.
2. `User.objects.filter(login=login).first()` — поиск пользователя.
3. `User.objects.filter(role=User.Role.AUTHOR).order_by("name")` — фильтрация + сортировка.
4. `Topic.objects.filter(name__iexact=name).exists()` — проверка существования.
5. `Topic.objects.create(...)` — создание.
6. `Podcast.objects.select_related("author")` — загрузка связи.
7. `.annotate(episode_count=Count("episodes"))` — аннотация количества выпусков.
8. `Podcast.objects.filter(author=user)` — фильтрация по FK.
9. `Podcast.objects.create(...)` — создание подкаста.
10. `podcast.episodes.select_related("topic", "author")` — обратная связь + связи.
11. `Episode.objects.filter(Q(...) | Q(...))` — поиск по нескольким полям.
12. `filter(status=status)` — фильтрация по одному условию.
13. `filter(release_date__gte=...)` и `__lte` — диапазон дат.
14. `order_by(order_field, "pk")` — сортировка из allow-list.
15. `annotate(...=F("podcast__title"))` — вычисляемые поля из связей.
16. `values(...)` — получение сокращённого набора полей.
17. `aggregate(Count(...))` — сводный показатель.
18. `values("status").annotate(count=Count("id"))` — группировка.
19. `exclude(status=Episode.Status.PUBLISHED)` — исключение записей.
20. `[:5]` — ограничение QuerySet срезом.
21. `Paginator(rows, 10)` — постраничный вывод.
22. `get_object_or_404(..., pk=...)` — получение объекта с обработкой 404.
23. `episode.save(update_fields=["status"])` — изменение записи.
24. `episode.delete()` — удаление записи.

Прямой SQL из ПР7 сохранён в `sql/` и `db/repository.py` только как предыдущая реализация. Django views ПР9 его не используют.
