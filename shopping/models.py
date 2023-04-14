from django.contrib.auth.models import User
from django.db import models


class Gender(models.Model):
    """
    Gender option
    """
    id = models.TextField(primary_key=True)

    def __str__(self):
        return str(self.id)


class MasterCategory(models.Model):
    """
    MasterCategory option
    """
    id = models.TextField(primary_key=True)

    def __str__(self):
        return str(self.id)


class SubCategory(models.Model):
    """
    SubCategory option under MasterCategory
    """
    id = models.TextField(primary_key=True)
    master_category = models.ForeignKey('MasterCategory', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class ArticleType(models.Model):
    """
    ArticleType option under SubCategory
    """
    id = models.TextField(primary_key=True)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class BaseColour(models.Model):
    """
    BaseColour option with hex colour code
    """
    id = models.TextField(primary_key=True)
    hex_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Item(models.Model):
    """
    Shopping item
    """
    id = models.TextField(primary_key=True, unique=True)
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE)
    master_category = models.ForeignKey('MasterCategory', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    article_type = models.ForeignKey('ArticleType', on_delete=models.CASCADE)
    base_colour = models.ForeignKey('BaseColour', on_delete=models.CASCADE)
    season = models.TextField()
    year = models.IntegerField()
    usage = models.TextField()
    display_name = models.TextField()
    price = models.FloatField()


class Image(models.Model):
    """
    Image link for shopping item
    """
    item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True)
    link = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.link)


class Customer(models.Model):
    """
    Customer additional information which User model does not have
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.TextField()
    address = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    """
    Basic order information
    """
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()


class OrderItem(models.Model):
    """
    Order items of each order
    """
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
