import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("authors_web", "0001_initial"),
        ("podcasts_web", "0001_initial"),
        ("topics_web", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="Episode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=250, verbose_name="Название выпуска")),
                ("status", models.CharField(choices=[("idea", "Идея"), ("planned", "Запланирован"), ("recording", "Идет запись"), ("ready", "Готов к публикации"), ("published", "Опубликован")], default="idea", max_length=20, verbose_name="Статус")),
                ("release_date", models.DateField(verbose_name="Дата выпуска")),
                ("author", models.ForeignKey(limit_choices_to={"role": "author"}, on_delete=django.db.models.deletion.PROTECT, related_name="episodes", to="authors_web.user", verbose_name="Автор")),
                ("podcast", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="episodes", to="podcasts_web.podcast", verbose_name="Подкаст")),
                ("topic", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="episodes", to="topics_web.topic", verbose_name="Тема")),
            ],
            options={"verbose_name": "Выпуск", "verbose_name_plural": "Выпуски", "ordering": ["release_date", "pk"]},
        ),
    ]
