from django.urls import path

from . import views

urlpatterns = [
    path('', views.item_list, name='home'),
    path('all/', views.item_list, name='all'),
    path('detail/<slug:item_id>', views.item_detail, name='detail'),
]
