"""Django ORM-модель подкаста с slug и get_absolute_url()."""

from django.db import models
from django.db.models.functions import Length
from django.urls import reverse
from django.utils.text import slugify

from authors_web.models import User


class Podcast(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название")
    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True,
        verbose_name="Slug",
    )
    description = models.TextField(verbose_name="Описание")
    title_length = models.GeneratedField(
        expression=Length("title"),
        output_field=models.IntegerField(),
        db_persist=True,
        verbose_name="Длина названия",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="podcasts",
        limit_choices_to={"role": User.Role.AUTHOR},
        verbose_name="Автор",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title, allow_unicode=True) or "podcast"
            candidate = base
            number = 2
            while (
                Podcast.objects.exclude(pk=self.pk)
                .filter(slug=candidate)
                .exists()
            ):
                candidate = f"{base}-{number}"
                number += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("podcasts_web:detail_slug", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["title", "pk"]
        verbose_name = "Подкаст"
        verbose_name_plural = "Подкасты"
