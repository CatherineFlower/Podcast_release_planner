from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, verbose_name="Имя")),
                ("login", models.CharField(max_length=100, unique=True, verbose_name="Логин")),
                ("password_hash", models.CharField(max_length=64, verbose_name="Хеш пароля")),
                ("role", models.CharField(choices=[("admin", "Администратор"), ("author", "Автор")], default="author", max_length=20, verbose_name="Роль")),
            ],
            options={"verbose_name": "Пользователь", "verbose_name_plural": "Пользователи", "ordering": ["name", "pk"]},
        ),
    ]
