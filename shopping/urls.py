from django.urls import path

from . import views

urlpatterns = [
    path('', views.item_list, name='items'),
    path('detail/<slug:item_id>', views.item_detail, name='detail'),
]
