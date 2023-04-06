from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from shopping.forms import SignUpForm
from shopping.models import Gender, SubCategory, ArticleType, BaseColour


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
