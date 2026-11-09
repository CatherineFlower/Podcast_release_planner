"""Django ORM-модель подкаста."""

from django.db import models

from authors_web.models import User


class Podcast(models.Model):
    title = models.CharField(
        max_length=250,
        verbose_name="Название",
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="podcasts",
        limit_choices_to={"role": User.Role.AUTHOR},
        verbose_name="Автор",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["title", "pk"]
        verbose_name = "Подкаст"
        verbose_name_plural = "Подкасты"
