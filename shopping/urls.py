from django.urls import path

from . import views

urlpatterns = [
    path('', views.item_list, name=''),
    path('all/', views.item_list, name='all'),
]
