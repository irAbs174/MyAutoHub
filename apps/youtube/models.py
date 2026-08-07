from django.db import models
from django.urls import reverse


class YoutubeVideo(models.Model):
    title = models.CharField(max_length=160)
    youtube_id = models.CharField(max_length=32, unique=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="youtube/covers/", blank=True)
    published_at = models.DateField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("youtube:detail", kwargs={"pk": self.pk})

    @property
    def embed_url(self):
        return f"https://www.youtube.com/embed/{self.youtube_id}"

    @property
    def thumbnail_url(self):
        if self.cover_image:
            return self.cover_image.url
        return f"https://i.ytimg.com/vi/{self.youtube_id}/hqdefault.jpg"
