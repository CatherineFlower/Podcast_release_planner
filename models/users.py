"""Пользователи системы и роли доступа."""

import hashlib

from .base import BaseEntity


def hash_password(password: str) -> str:
    """Вернуть SHA-256 хеш пароля."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class User(BaseEntity):
    """Базовый пользователь."""

    role = "user"

    def __init__(
        self,
        user_id: int,
        name: str,
        login: str,
        password_hash: str,
    ) -> None:
        super().__init__(user_id)
        self.name = name
        self.login = login
        self._password_hash = password_hash

    def verify_password(self, password: str) -> bool:
        """Проверить пароль пользователя."""
        return self._password_hash == hash_password(password)

    @property
    def password_hash(self) -> str:
        """Вернуть хеш пароля для сохранения."""
        return self._password_hash

    @property
    def can_edit(self) -> bool:
        """Есть ли право изменять данные."""
        return False

    def __str__(self) -> str:
        return f"#{self.id}: {self.name} ({self.role})"

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать объект нужного подкласса из JSON-данных."""
        role = data.get("role", "author")
        user_cls = Admin if role == "admin" else Author
        return user_cls(
            user_id=data["id"],
            name=data["name"],
            login=data["login"],
            password_hash=data["password_hash"],
        )


class Admin(User):
    """Администратор с полным доступом."""

    role = "admin"

    @property
    def can_edit(self) -> bool:
        return True


class Author(User):
    """Автор с доступом только к своим данным."""

    role = "author"
