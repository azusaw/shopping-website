import urllib.request
from urllib.parse import urljoin

from behave import given, when, then

from shopping.models import Item, MasterCategory, SubCategory, ArticleType, BaseColour, Image, Gender


@given("the specific product which want to check")
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
    Image.objects.get_or_create(item=item,
                                link="http://assets.myntassets.com/v1/images/style/properties/b0d3dcd6aaa7274486236fa267ef8cb5_images.jpg"
                                )


@when('we access the item listing page')
def access_item_list_page(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url, '/')
    context.response = context.test.client.get("/")
    context.browser.get(open_url)


@when('we access the item detail page of "{item_id}"')
def access_item_detail_page(context, item_id):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url, f"/detail/{item_id}")
    context.browser.get(open_url)


@then('we will find "{keyword}"')
def check_keyword(context, keyword):
    assert keyword in context.browser.page_source
