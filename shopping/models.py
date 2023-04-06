from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Gender(models.Model):
    id = models.TextField(primary_key=True)

    def __str__(self):
        return self.id


class MasterCategory(models.Model):
    id = models.TextField(primary_key=True)

    def __str__(self):
        return self.id


class SubCategory(models.Model):
    id = models.TextField(primary_key=True)
    master_category = models.ForeignKey('MasterCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class ArticleType(models.Model):
    id = models.TextField(primary_key=True)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class BaseColour(models.Model):
    id = models.TextField(primary_key=True)
    hex_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.id


class Item(models.Model):
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
    item = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, unique=True)
    link = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.link


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.TextField()
    address = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.customer.save()


class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
