from django.shortcuts import render

from .models import Item


def item_list(request):
    items = Item.objects.all()
    return render(request, 'all.html', {'items': items, 'cnt': len(items)})

