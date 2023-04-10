from datetime import datetime, timezone

from django.test import TestCase

from shopping.models import Gender, MasterCategory, SubCategory, ArticleType, BaseColour, Item, Image, Customer, Order, \
    OrderItem


class ShoppingModelTest(TestCase):
    fixtures = ['test_data.json']

    def test_model_gender(self):
        """ Model Test: 1 """
        item = Gender.objects.get(pk="Men")
        self.assertEqual(item.id, "Men")
        items = Gender.objects.all()
        self.assertEqual(items.count(), 2)

    def test_model_master_category(self):
        """ Model Test: 2 """
        item = MasterCategory.objects.get(pk="Personal Care")
        self.assertEqual(item.id, "Personal Care")
        items = MasterCategory.objects.all()
        self.assertEqual(items.count(), 2)

    def test_model_sub_category(self):
        """ Model Test: 3 """
        item = SubCategory.objects.get(pk="Fragrance")
        self.assertEqual(item.id, "Fragrance")
        self.assertEqual(item.master_category.id, "Personal Care")
        items = SubCategory.objects.all()
        self.assertEqual(items.count(), 2)

    def test_model_article_type(self):
        """ Model Test: 4 """
        item = ArticleType.objects.get(pk="Shirts")
        self.assertEqual(item.id, "Shirts")
        self.assertEqual(item.sub_category.id, "Topwear")
        items = ArticleType.objects.all()
        self.assertEqual(items.count(), 2)

    def test_model_base_colour(self):
        """ Model Test: 5 """
        item = BaseColour.objects.get(pk="Navy Blue")
        self.assertEqual(item.id, "Navy Blue")
        self.assertEqual(item.hex_code, "#0000ff")
        items = BaseColour.objects.all()
        self.assertEqual(items.count(), 2)

    def test_model_item(self):
        """ Model Test: 6 """
        item = Item.objects.get(pk="15970")
        self.assertEqual(item.id, "15970")
        self.assertEqual(item.gender.id, "Men")
        self.assertEqual(item.master_category.id, "Apparel")
        self.assertEqual(item.sub_category.id, "Topwear")
        self.assertEqual(item.article_type.id, "Shirts")
        self.assertEqual(item.base_colour.id, "Navy Blue")
        self.assertEqual(item.season, "Fall")
        self.assertEqual(item.year, 2011)
        self.assertEqual(item.usage, "Casual")
        self.assertEqual(item.display_name, "Turtle Check Men Navy Blue Shirt")
        self.assertEqual(item.price, 18.37)
        items = Item.objects.all()
        self.assertEqual(items.count(), 2)

    def test_model_image(self):
        """ Model Test: 7 """
        item = Image.objects.get(pk="15970")
        self.assertEqual(item.item.id, "15970")
        self.assertEqual(item.link,
                         "http://assets.myntassets.com/v1/images/style/properties/7a5b82d1372a7a5c6de67ae7a314fd91_images.jpg")
        items = Image.objects.all()
        self.assertEqual(items.count(), 2)

    def test_model_customer(self):
        """ Model Test: 8 """
        item = Customer.objects.get(pk=1)
        self.assertEqual(item.user.id, 1)
        self.assertEqual(item.phone, "012345678")
        self.assertEqual(item.address, "123 Aberdeen")
        self.assertEqual(item.created_date,
                         datetime(2023, 4, 5, 19, 38, 50, 667189, tzinfo=timezone.utc))
        items = Customer.objects.all()
        self.assertEqual(items.count(), 1)

    def test_model_order(self):
        """ Model Test: 9 """
        item = Order.objects.get(pk=33)
        self.assertEqual(item.id, 33)
        self.assertEqual(item.customer.user.id, 1)
        self.assertEqual(item.total_price, 86.78)
        self.assertEqual(item.created_date,
                         datetime(2023, 4, 6, 17, 0, 1, 993077, tzinfo=timezone.utc))
        items = Order.objects.all()
        self.assertEqual(items.count(), 1)

    def test_model_order_item(self):
        """ Model Test: 10 """
        item = OrderItem.objects.get(pk=19)
        self.assertEqual(item.id, 19)
        self.assertEqual(item.order.id, 33)
        self.assertEqual(item.item.id, "15970")
        self.assertEqual(item.price, 18.37)
        self.assertEqual(item.quantity, 2)
        items = OrderItem.objects.all()
        self.assertEqual(items.count(), 2)
