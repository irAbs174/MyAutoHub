from django.shortcuts import get_object_or_404, render

from .models import PriceReference


def list_prices(request):
    items = PriceReference.objects.filter(is_published=True).prefetch_related("photos")
    category = request.GET.get("category")
    if category:
        items = items.filter(category__iexact=category)
    return render(request, "pricing/list.html", {"items": items})


def detail(request, pk):
    item = get_object_or_404(
        PriceReference.objects.prefetch_related("photos"),
        pk=pk,
        is_published=True,
    )
    return render(request, "pricing/detail.html", {"item": item})