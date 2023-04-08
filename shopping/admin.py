from django.contrib import admin

from shopping.models import Item, Customer, Image, MasterCategory, SubCategory, ArticleType, BaseColour, Order, \
    OrderItem

# Register your models here.
admin.site.register(Item)
admin.site.register(Image)
admin.site.register(MasterCategory)
admin.site.register(SubCategory)
admin.site.register(ArticleType)
admin.site.register(BaseColour)

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
