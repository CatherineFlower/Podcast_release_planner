from django.db import migrations, models
from django.utils.text import slugify


def fill_slugs(apps, schema_editor):
    Podcast = apps.get_model("podcasts_web", "Podcast")
    used = set()
    for podcast in Podcast.objects.order_by("pk"):
        base = slugify(podcast.title, allow_unicode=True) or "podcast"
        slug = base
        suffix = 2
        while slug in used:
            slug = f"{base}-{suffix}"
            suffix += 1
        podcast.slug = slug
        podcast.save(update_fields=["slug"])
        used.add(slug)


class Migration(migrations.Migration):
    dependencies = [("podcasts_web", "0001_initial")]
    operations = [
        migrations.AddField(
            model_name="podcast",
            name="slug",
            field=models.SlugField(blank=True, max_length=280, null=True),
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="podcast",
            name="slug",
            field=models.SlugField(blank=True, max_length=280, unique=True, verbose_name="Slug"),
        ),
    ]
