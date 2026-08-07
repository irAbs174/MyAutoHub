from django.shortcuts import get_object_or_404, render

from .models import Story


def list_stories(request):
    stories = Story.objects.filter(is_published=True)
    return render(request, "stories/list.html", {"stories": stories})


def detail(request, slug):
    story = get_object_or_404(Story, slug=slug, is_published=True)
    return render(request, "stories/detail.html", {"story": story})
