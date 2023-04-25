import urllib
from urllib.parse import urljoin

from behave import given, when, then

from shopping.models import Gender, MasterCategory, SubCategory, ArticleType, BaseColour, Item, Image


@given("the specific product which want to add into basket")
def create_item(context):
    # Convert table into dictionary
    args = dict(context.table)

    gender, _ = Gender.objects.get_or_create(id=args["gender"])
    master_category, _ = MasterCategory.objects.get_or_create(id=args["master_category"])
    sub_category, _ = SubCategory.objects.get_or_create(id=args["sub_category"], master_category=master_category)
    article_type, _ = ArticleType.objects.get_or_create(id=args["article_type"], sub_category=sub_category)
    base_colour, _ = BaseColour.objects.get_or_create(id=args["base_colour"], hex_code=args["hex_code"])
    item, _ = Item.objects.get_or_create(id=args["item_id"],
                                         gender=gender,
                                         master_category=master_category,
                                         sub_category=sub_category,
                                         article_type=article_type,
                                         base_colour=base_colour,
                                         season=args["season"],
                                         year=args["year"],
                                         usage=args["usage"],
                                         display_name=args["display_name"],
                                         price=args["price"]
                                         )
    Image.objects.get_or_create(item=item, link=args["link"])


@when('we add the item with id "{item_id}" into basket')
def add_item_into_basket(context, item_id):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url, f"/detail/{item_id}")
    context.browser.get(open_url)

    quantity_textfield = context.browser.find_element('name', 'quantity')
    quantity_textfield.send_keys(1)
    context.browser.find_element('name', 'add-basket').click()


@when('we update the item quantity to "{quantity}"')
def update_quantity(context, quantity):
    quantity_textfield = context.browser.find_element('name', 'quantity')
    quantity_textfield.send_keys(quantity)
    context.browser.find_element('name', 'update-quantity').click()
    assert 'Your Basket' in context.browser.page_source


@when('we process a purchase')
def process_purchase(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url, "/purchase/")
    context.browser.get(open_url)


@then('we will be redirected to the basket page')
def check_basket(context):
    assert 'Your Basket' in context.browser.page_source


@then('item quantity will be updated to "{quantity}"')
def check_quantity(context, quantity):
    quantity_textfield = context.browser.find_element('name', 'quantity')
    assert quantity_textfield.get_attribute("value") == quantity


@then('we will be redirected to login page')
def check_redirect_to_login_page(context):
    assert 'Login' in context.browser.page_source
