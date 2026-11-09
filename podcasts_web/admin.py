from django.contrib import admin

from episodes_web.models import Episode

from .models import Podcast


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 0
    fields = ("title", "topic", "author", "status", "release_date")
    show_change_link = True


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "title_length", "author", "episode_count", "slug"
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "description", "author__name")
    list_filter = ("author",)
    ordering = ("title",)
    list_per_page = 20
    prepopulated_fields = {"slug": ("title",)}
    inlines = (EpisodeInline,)
    view_on_site = True
    readonly_fields = ("title_length",)

    @admin.display(description="Выпусков")
    def episode_count(self, obj):
        return obj.episodes.count()
