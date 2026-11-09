from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Topic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True, verbose_name="Название темы")),
            ],
            options={"verbose_name": "Тема", "verbose_name_plural": "Темы", "ordering": ["name", "pk"]},
        ),
    ]
