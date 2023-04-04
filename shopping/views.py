from django.shortcuts import render

from .models import Item, Image


def item_list(request):
    items_with_image = Image.objects.select_related("item").all()[0:10]
    return render(request, 'all.html', {'items_with_image': items_with_image, 'cnt': len(items_with_image)})


def item_detail(request, item_id):
    items_with_image = Image.objects.select_related("item").get(item_id=item_id)
    return render(request, 'item_detail.html', {'items_with_image': items_with_image})

