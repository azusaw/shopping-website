from shopping.models import SubCategory, Gender, BaseColour, ArticleType


def get_menu_info():
    gender = Gender.objects.all().order_by("id")
    sub_category = SubCategory.objects.all()
    article_type = ArticleType.objects.all()
    base_colour = BaseColour.objects.all().values('hex_code').distinct().order_by('-hex_code')

    master_sub_category = {}
    for item in sub_category:
        if item.master_category.id not in master_sub_category.keys():
            master_sub_category[item.master_category.id] = [item.id]
        else:
            master_sub_category[item.master_category.id].append(item.id)

    return {'gender': gender, 'master_sub_category': master_sub_category,
            'article_type': article_type, 'base_colour': base_colour}
