from django.db.models import Q
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
    gender = ""
    master = ""
    sub = ""
    colour = ""

    # Set value if query string exists
    if "gender" in request.GET:
        gender = request.GET["gender"]
    if "master" in request.GET:
        master = request.GET["master"]
    if "sub" in request.GET:
        sub = request.GET["sub"]
    if "colour" in request.GET:
        colour = request.GET["colour"]

    # Create WHERE clause from query strings
    where = []
    where_color = []
    if gender != '':
        where.append(Q(item__gender=gender))
    if master != '':
        where.append(Q(item__master_category=master))
    if sub != '':
        where.append(Q(item__sub_category=sub))
    if colour != '':
        where_color.append(Q(item__base_colour__hex_code='#' + colour))

    items_with_image = Image.objects.all().select_related("item").filter(*where)
    # FIX ME
    items = items_with_image.select_related("item__base_colour").filter(*where_color)
    return render(request, 'all.html', {'menu': menu(), 'items': items, 'cnt': len(items)})


def item_detail(request, item_id):
    items_with_image = Image.objects.select_related("item").get(item_id=item_id)
    return render(request, 'item_detail.html', {'menu': menu(), 'items_with_image': items_with_image})
