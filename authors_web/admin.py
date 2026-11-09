from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "login",
        "role",
        "podcast_count",
        "episode_count",
    )
    list_display_links = ("id", "name")
    search_fields = ("name", "login")
    list_filter = ("role",)
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("password_hash",)

    @admin.display(description="Подкастов")
    def podcast_count(self, obj):
        return obj.podcasts.count()

    @admin.display(description="Выпусков")
    def episode_count(self, obj):
        return obj.episodes.count()
