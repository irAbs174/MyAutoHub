from django.shortcuts import get_object_or_404, render

from .models import YoutubeVideo


def list_videos(request):
    videos = YoutubeVideo.objects.filter(is_published=True)
    return render(request, "youtube/list.html", {"videos": videos})


def detail(request, pk):
    video = get_object_or_404(YoutubeVideo, pk=pk, is_published=True)
    return render(request, "youtube/detail.html", {"video": video})
