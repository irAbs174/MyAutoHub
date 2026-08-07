# Generated manually for trilingual content fields

from django.db import migrations, models


def copy_story_langs(apps, schema_editor):
    Story = apps.get_model("stories", "Story")
    for story in Story.objects.all():
        title = story.title or ""
        excerpt = story.excerpt or ""
        body = story.body or ""
        story.title_fa = title
        story.title_en = title
        story.title_ar = title
        story.excerpt_fa = excerpt
        story.excerpt_en = excerpt
        story.excerpt_ar = excerpt
        story.body_fa = body
        story.body_en = body
        story.body_ar = body
        story.save(
            update_fields=[
                "title_fa",
                "title_en",
                "title_ar",
                "excerpt_fa",
                "excerpt_en",
                "excerpt_ar",
                "body_fa",
                "body_en",
                "body_ar",
            ]
        )


class Migration(migrations.Migration):
    dependencies = [
        ("stories", "0002_add_cover_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="story",
            name="title_fa",
            field=models.CharField(max_length=160, null=True, verbose_name="Title (فارسی)"),
        ),
        migrations.AddField(
            model_name="story",
            name="title_en",
            field=models.CharField(max_length=160, null=True, verbose_name="Title (English)"),
        ),
        migrations.AddField(
            model_name="story",
            name="title_ar",
            field=models.CharField(max_length=160, null=True, verbose_name="Title (العربية)"),
        ),
        migrations.AddField(
            model_name="story",
            name="excerpt_fa",
            field=models.CharField(blank=True, max_length=255, verbose_name="Excerpt (فارسی)"),
        ),
        migrations.AddField(
            model_name="story",
            name="excerpt_en",
            field=models.CharField(blank=True, max_length=255, verbose_name="Excerpt (English)"),
        ),
        migrations.AddField(
            model_name="story",
            name="excerpt_ar",
            field=models.CharField(blank=True, max_length=255, verbose_name="Excerpt (العربية)"),
        ),
        migrations.AddField(
            model_name="story",
            name="body_fa",
            field=models.TextField(null=True, verbose_name="Body (فارسی)"),
        ),
        migrations.AddField(
            model_name="story",
            name="body_en",
            field=models.TextField(null=True, verbose_name="Body (English)"),
        ),
        migrations.AddField(
            model_name="story",
            name="body_ar",
            field=models.TextField(null=True, verbose_name="Body (العربية)"),
        ),
        migrations.RunPython(copy_story_langs, migrations.RunPython.noop),
        migrations.RemoveField(model_name="story", name="title"),
        migrations.RemoveField(model_name="story", name="excerpt"),
        migrations.RemoveField(model_name="story", name="body"),
        migrations.AlterField(
            model_name="story",
            name="title_fa",
            field=models.CharField(max_length=160, verbose_name="Title (فارسی)"),
        ),
        migrations.AlterField(
            model_name="story",
            name="title_en",
            field=models.CharField(max_length=160, verbose_name="Title (English)"),
        ),
        migrations.AlterField(
            model_name="story",
            name="title_ar",
            field=models.CharField(max_length=160, verbose_name="Title (العربية)"),
        ),
        migrations.AlterField(
            model_name="story",
            name="body_fa",
            field=models.TextField(verbose_name="Body (فارسی)"),
        ),
        migrations.AlterField(
            model_name="story",
            name="body_en",
            field=models.TextField(verbose_name="Body (English)"),
        ),
        migrations.AlterField(
            model_name="story",
            name="body_ar",
            field=models.TextField(verbose_name="Body (العربية)"),
        ),
    ]
