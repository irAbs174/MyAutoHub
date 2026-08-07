from django.contrib import admin

from .models import YoutubeVideo


@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "youtube_id", "published_at", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "youtube_id", "description")
