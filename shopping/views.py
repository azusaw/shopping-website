from django.shortcuts import render

from .models import Item, Image


def item_list(request):
    items_with_image = Image.objects.select_related("item").all()[0:10]
    return render(request, 'all.html', {'items_with_image': items_with_image, 'cnt': len(items_with_image)})

