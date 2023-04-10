from decimal import Decimal

from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from shopping.forms import BasketAddItemForm
from shopping.models import Item, Image
from shopping.views.menu import get_menu_info


class Basket(object):
    """
    Basket for keeping selected items
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            # save an empty basket in the session
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def __iter__(self):
        """
        Iterate over the items in the basket and get the products
        from the database.
        """
        item_ids = self.basket.keys()
        # get the product objects and add them to the basket
        items = Item.objects.filter(id__in=item_ids)

        basket = self.basket.copy()
        for item in items:
            basket[str(item.id)]['item'] = Image.objects.get(item__id=item.id)
            basket[str(item.id)]['item_id'] = item.id
            basket[str(item.id)]['link'] = item.id

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the basket
        """
        return sum(item['quantity'] for item in self.basket.values())

    def add(self, item, quantity=1, override_quantity=False):
        """
        Add a product to the basket or update its quantity.
        """
        item_id = str(item.id)
        if item_id not in self.basket:
            self.basket[item_id] = {'quantity': 0,
                                    'price': str(item.price)}
        if override_quantity:
            self.basket[item_id]['quantity'] = int(quantity)
        else:
            self.basket[item_id]['quantity'] += int(quantity)
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, item):
        """
        Remove a product from the basket
        """
        item_id = str(item.id)
        if item_id in self.basket:
            del self.basket[item_id]
            self.save()

    def clear(self):
        # remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def get_total_price(self):
        """
        Calculate current total price
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())


@require_POST
def basket_add(request, item_id):
    """
    Add item into basket
    """
    basket = Basket(request)
    item = get_object_or_404(Item, id=item_id)
    form = BasketAddItemForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        basket.add(item=item, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('basket')


@require_POST
def basket_remove(request, item_id):
    """
    Remove item from basket
    """
    basket = Basket(request)
    product = get_object_or_404(Item, id=item_id)
    basket.remove(product)
    return redirect('basket')


def basket(request):
    """
    Render '/basket' page
    """
    basket = Basket(request)
    for item in basket:
        item['update_quantity_form'] = BasketAddItemForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'pages/basket.html', {'menu': get_menu_info(), 'basket': basket})
