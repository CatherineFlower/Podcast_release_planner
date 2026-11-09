from django.contrib import admin

from .models import Episode


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "podcast", "topic", "author", "status", "release_date"
    )
    list_display_links = ("id", "title")
    search_fields = (
        "title", "podcast__title", "topic__name", "author__name"
    )
    list_filter = ("status", "release_date", "topic", "author")
    ordering = ("-release_date", "title")
    list_per_page = 25
    autocomplete_fields = ("podcast", "topic", "author")
    list_select_related = ("podcast", "topic", "author")
    actions = ("mark_ready", "mark_published")

    @admin.action(description="Отметить выбранные как готовые")
    def mark_ready(self, request, queryset):
        queryset.update(status=Episode.Status.READY)

    @admin.action(description="Опубликовать выбранные выпуски")
    def mark_published(self, request, queryset):
        queryset.update(status=Episode.Status.PUBLISHED)
