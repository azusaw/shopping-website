from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.item_list, name='items'),
    path('detail/<slug:item_id>', views.item_detail, name='detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
]
