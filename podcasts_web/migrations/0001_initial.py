import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [("authors_web", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="Podcast",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=250, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                ("author", models.ForeignKey(limit_choices_to={"role": "author"}, on_delete=django.db.models.deletion.PROTECT, related_name="podcasts", to="authors_web.user", verbose_name="Автор")),
            ],
            options={"verbose_name": "Подкаст", "verbose_name_plural": "Подкасты", "ordering": ["title", "pk"]},
        ),
    ]
