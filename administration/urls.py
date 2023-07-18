from django.urls import path
from . import views

urlpatterns = [
     path('admin/orders/', views.admin_order_list,
          name='admin_order_list'),
]
