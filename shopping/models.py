from django.db import models


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

    def __str__(self):
        return self.id


class ArticleType(models.Model):
    id = models.TextField(primary_key=True)

    def __str__(self):
        return self.id


class BaseColour(models.Model):
    id = models.TextField(primary_key=True)
    hex_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.id


class Item(models.Model):
    id = models.TextField(primary_key=True, unique=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    master_category = models.ForeignKey('MasterCategory', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    article_type = models.ForeignKey('ArticleType', on_delete=models.CASCADE)
    base_colour = models.ForeignKey('BaseColour', on_delete=models.CASCADE)
    season = models.TextField()
    year = models.IntegerField()
    usage = models.TextField()
    display_name = models.TextField()


class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, primary_key=True, unique=True)
    link = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.link
