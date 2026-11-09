"""Django ORM-модель темы выпуска."""

from django.db import models


class Topic(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название темы",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name", "pk"]
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
