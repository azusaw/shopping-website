import webcolors
from django.db.models import Q
from django.shortcuts import render

from shopping.forms import BasketAddItemForm
from shopping.models import Item
from shopping.views.menu import get_menu_info


def item_list(request):
    """
    Render '/' page with items filtered by search condition
    """
    title = "All Items"
    keyword = ""
    gender = ""
    master = ""
    sub = ""
    colour = ""

    # Set value if query string exists
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        title = f"Keyword: {keyword}"
    if "gender" in request.GET:
        gender = request.GET["gender"]
        title = f"Gender: {gender}"
    if "master" in request.GET:
        master = request.GET["master"]
        title = f"Category: {master}"
    if "sub" in request.GET:
        sub = request.GET["sub"]
        title = f"Sub Category: {sub}"
    if "colour" in request.GET:
        colour = request.GET["colour"]
        # Covert hex colour code to colour name for display
        colour_name = webcolors.hex_to_name(f"#{request.GET['colour']}")
        title = f"Colour: {colour_name.capitalize()}"

    # Create WHERE clause from query strings
    where = []

    if keyword != '':
        where.append(Q(display_name__contains=keyword))
    if gender != '':
        where.append(Q(gender=gender))
    if master != '':
        where.append(Q(master_category=master))
    if sub != '':
        where.append(Q(sub_category=sub))
    if colour != '':
        where.append(Q(base_colour__hex_code='#' + colour))

    items = Item.objects.select_related("base_colour").filter(*where)

    return render(request, 'pages/item_list.html',
                  {'title': title, 'menu': get_menu_info(), 'items': items, 'cnt': len(items)})


def item_detail(request, item_id):
    """
    Render '/detail/<item_id>' page with item data
    """
    item = Item.objects.get(id=item_id)
    basket_item_form = BasketAddItemForm()
    return render(request, 'pages/item_detail.html',
                  {'menu': get_menu_info(), 'item': item, 'basket_item_form': basket_item_form})
