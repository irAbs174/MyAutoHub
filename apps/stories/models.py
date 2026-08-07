from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.core.i18n_content import localized


class Story(models.Model):
    title_fa = models.CharField(max_length=160, verbose_name=_("Title (فارسی)"))
    title_en = models.CharField(max_length=160, verbose_name=_("Title (English)"))
    title_ar = models.CharField(max_length=160, verbose_name=_("Title (العربية)"))
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    excerpt_fa = models.CharField(
        max_length=255, blank=True, verbose_name=_("Excerpt (فارسی)")
    )
    excerpt_en = models.CharField(
        max_length=255, blank=True, verbose_name=_("Excerpt (English)")
    )
    excerpt_ar = models.CharField(
        max_length=255, blank=True, verbose_name=_("Excerpt (العربية)")
    )
    body_fa = models.TextField(verbose_name=_("Body (فارسی)"))
    body_en = models.TextField(verbose_name=_("Body (English)"))
    body_ar = models.TextField(verbose_name=_("Body (العربية)"))
    cover_image = models.ImageField(upload_to="stories/covers/", blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stories",
    )
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name_plural = "stories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("stories:detail", kwargs={"slug": self.slug})

    @property
    def title(self):
        return localized(self, "title")

    @property
    def excerpt(self):
        return localized(self, "excerpt")

    @property
    def body(self):
        return localized(self, "body")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_source = self.title_en or self.title_fa or self.title_ar or "story"
            base = slugify(base_source)[:160] or "story"
            slug = base
            i = 2
            while Story.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)
