import urllib.request
from urllib.parse import urljoin

from behave import given, when, then

from shopping.models import Item, Image, Gender, MasterCategory, ArticleType, SubCategory, BaseColour


@given("the specific product which want to check is exist")
def create_item(context):
    master_category = MasterCategory("Personal Care")
    sub_category = SubCategory(id="Fragrance", master_category=master_category)
    article_type = ArticleType(id="Perfume and Body Mist", sub_category=sub_category)
    item = Item.objects.create(id="99999",
                               gender=Gender("Women"),
                               master_category=master_category,
                               sub_category=sub_category,
                               article_type=article_type,
                               base_colour=BaseColour("Gold", "#ffd700"),
                               season="Spring",
                               year=2017,
                               usage="Casual",
                               display_name="Giorgio Armani Women Idole Perfume",
                               price=50.00
                               )
    Image.objects.create(item=item,
                         link="http://assets.myntassets.com/v1/images/style/properties/b0d3dcd6aaa7274486236fa267ef8cb5_images.jpg"
                         )


@when('we access the item listing page')
def access_item_list_page(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url, '/')
    context.browser.get(open_url)


@when('we access the item detail page')
def access_item_detail_page(context):
    item_id = '99999'
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url, f"/detail/{item_id}")
    context.browser.get(open_url)


@then('we will find (?P<keyword>)')
def check_keyword(context, keyword):
    assert keyword in context.browser.page_source
