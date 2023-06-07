from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>',
         views.order_history, name='order_history'),
    path('edit-avatar/',
         views.edit_avatar, name='edit_avatar'),
]
