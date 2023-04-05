from django.shortcuts import render

from .models import Image, Gender, SubCategory, ArticleType, BaseColour


def menu():
    gender = Gender.objects.all()
    sub_category = SubCategory.objects.all()
    article_type = ArticleType.objects.all()
    base_colour = BaseColour.objects.all().values('hex_code').distinct().order_by('-hex_code')

    master_sub_category = {}
    for item in sub_category:
        if item.master_category.id not in master_sub_category.keys():
            master_sub_category[item.master_category.id] = [item.id]
        else:
            master_sub_category[item.master_category.id].append(item.id)

    return {'gender': gender, 'master_sub_category': master_sub_category,
            'article_type': article_type, 'base_colour': base_colour}


def item_list(request):
    items_with_image = Image.objects.select_related("item").all()[0:10]
    return render(request, 'all.html',
                  {'menu': menu(), 'items_with_image': items_with_image, 'cnt': len(items_with_image)})


def item_detail(request, item_id):
    items_with_image = Image.objects.select_related("item").get(item_id=item_id)
    return render(request, 'item_detail.html', {'menu': menu(), 'items_with_image': items_with_image})
