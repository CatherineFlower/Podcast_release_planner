from django.contrib import admin

from .models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "episode_count")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20

    @admin.display(description="Выпусков")
    def episode_count(self, obj):
        return obj.episodes.count()
