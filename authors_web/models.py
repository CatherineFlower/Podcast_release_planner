"""Django ORM-модель пользователя предметной области Podcast Planner."""

import hashlib

from django.db import models


def hash_password(password: str) -> str:
    """Вернуть SHA-256 хеш пароля для совместимости с данными ПР7."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class User(models.Model):
    """Пользователь компании: администратор или автор."""

    class Role(models.TextChoices):
        ADMIN = "admin", "Администратор"
        AUTHOR = "author", "Автор"

    name = models.CharField(
        max_length=200,
        verbose_name="Имя",
    )
    login = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Логин",
    )
    password_hash = models.CharField(
        max_length=64,
        verbose_name="Хеш пароля",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.AUTHOR,
        verbose_name="Роль",
    )

    def verify_password(self, password: str) -> bool:
        return self.password_hash == hash_password(password)

    @property
    def can_edit(self) -> bool:
        return self.role == self.Role.ADMIN

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name", "pk"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
