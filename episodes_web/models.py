"""Django ORM-модель выпуска подкаста."""

from django.db import models

from authors_web.models import User
from podcasts_web.models import Podcast
from topics_web.models import Topic


class Episode(models.Model):
    class Status(models.TextChoices):
        IDEA = "idea", "Идея"
        PLANNED = "planned", "Запланирован"
        RECORDING = "recording", "Идет запись"
        READY = "ready", "Готов к публикации"
        PUBLISHED = "published", "Опубликован"

    podcast = models.ForeignKey(
        Podcast,
        on_delete=models.PROTECT,
        related_name="episodes",
        verbose_name="Подкаст",
    )
    title = models.CharField(
        max_length=250,
        verbose_name="Название выпуска",
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.PROTECT,
        related_name="episodes",
        verbose_name="Тема",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="episodes",
        limit_choices_to={"role": User.Role.AUTHOR},
        verbose_name="Автор",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IDEA,
        verbose_name="Статус",
    )
    release_date = models.DateField(
        verbose_name="Дата выпуска",
    )

    @property
    def status_title(self) -> str:
        return self.get_status_display()

    def change_status(self, status: str) -> None:
        if status not in self.Status.values:
            raise ValueError("Недопустимый статус")
        self.status = status
        self.save(update_fields=["status"])

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["release_date", "pk"]
        verbose_name = "Выпуск"
        verbose_name_plural = "Выпуски"
