import webcolors
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import SignUpForm
from .models import Image, Gender, SubCategory, ArticleType, BaseColour


def signup(request):
    form = SignUpForm(request.POST)
    errors = []

    if request.method == "POST":
        errors = form.errors

    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.customer.first_name = form.cleaned_data.get('first_name')
        user.customer.last_name = form.cleaned_data.get('last_name')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')

    return render(request, 'signup.html',
                  {'form': form, 'password_helper': form.fields["password1"].help_text, 'errors': errors})


@login_required
def login(request):
    user = request.user
    print(user)
    if user.is_authenticated:
        return render(request, 'items.html')
    return redirect('login')


def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie("sessionid")
    return response


def menu():
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


def item_list(request):
    title = "All item"
    keyword = ""
    gender = ""
    master = ""
    sub = ""
    colour = ""

    # Set value if query string exists
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        title = f"Keyword: {keyword}"
    if "gender" in request.GET:
        gender = request.GET["gender"]
        title = f"Gender: {gender}"
    if "master" in request.GET:
        master = request.GET["master"]
        title = f"Category: {master}"
    if "sub" in request.GET:
        sub = request.GET["sub"]
        title = f"Sub Category: {sub}"
    if "colour" in request.GET:
        colour = request.GET["colour"]
        # Covert hex colour code to colour name for display
        colour_name = webcolors.hex_to_name(f"#{request.GET['colour']}")
        title = f"Colour: {colour_name.capitalize()}"

    # Create WHERE clause from query strings
    where = []
    where_color = []
    if keyword != '':
        where.append(Q(item__display_name__contains=keyword))
    if gender != '':
        where.append(Q(item__gender=gender))
    if master != '':
        where.append(Q(item__master_category=master))
    if sub != '':
        where.append(Q(item__sub_category=sub))
    if colour != '':
        where_color.append(Q(item__base_colour__hex_code='#' + colour))

    items_with_image = Image.objects.all().select_related("item").filter(*where)
    # FIX ME
    items = items_with_image.select_related("item__base_colour").filter(*where_color)[:10]
    return render(request, 'item_list.html', {'title': title, 'menu': menu(), 'items': items, 'cnt': len(items)})


def item_detail(request, item_id):
    items_with_image = Image.objects.select_related("item").get(item_id=item_id)
    return render(request, 'item_detail.html', {'menu': menu(), 'items_with_image': items_with_image})
