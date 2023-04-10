from django.urls import path, include

from shopping.views import basket, general, item, order
from . import views

urlpatterns = [
    path('', views.item.item_list, name='item_list'),
    path('detail/<slug:item_id>', views.item.item_detail, name='item_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.general.signup, name='signup'),
    path('basket_add/<int:item_id>/', views.basket.basket_add, name='basket_add'),
    path('basket_remove/<int:item_id>/', views.basket.basket_remove, name='basket_remove'),
    path('basket/', views.basket.basket, name='basket'),
    path('purchase/', views.general.purchase, name='purchase'),
    path('payment/', views.general.payment, name='payment'),
    path('order_list/', views.order.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order.order_detail, name='order_detail'),
    path('thanks/<int:order_id>', views.order.thanks, name='thanks'),
    path('profile/', views.general.profile, name='profile'),
    path('dashboard/', views.general.dashboard, name='dashboard'),
]
