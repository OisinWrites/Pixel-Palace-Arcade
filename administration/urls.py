from django.urls import path
from . import views

urlpatterns = [
     path('pending_orders/', views.pending_orders,
          name='pending_orders'),
     path('completed_orders/', views.completed_orders,
          name='completed_orders'),
     path('menu/', views.admin_menu, name='admin_menu'),
]
