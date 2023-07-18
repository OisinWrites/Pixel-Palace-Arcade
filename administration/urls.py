from django.urls import path
from . import views

urlpatterns = [
     path('pending_orders/', views.admin_order_list,
          name='admin_order_list'),
     path('menu/', views.admin_menu, name='admin_menu'),
]
