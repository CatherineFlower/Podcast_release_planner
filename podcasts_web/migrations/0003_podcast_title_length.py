from django.db import migrations, models
from django.db.models.functions import Length


class Migration(migrations.Migration):
    dependencies = [
        ("podcasts_web", "0002_podcast_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="podcast",
            name="title_length",
            field=models.GeneratedField(
                db_persist=True,
                expression=Length("title"),
                output_field=models.IntegerField(),
                verbose_name="Длина названия",
            ),
        ),
    ]
