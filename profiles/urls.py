from django.urls import path
from . import views
from review.views import review_modal

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>',
         views.order_history, name='order_history'),
    path('edit_avatar/',
         views.edit_avatar, name='edit_avatar'),
    path('delete_avatar/', views.delete_avatar,
         name='delete_avatar'),
    path('review_modal/<int:review_id>/', review_modal,
         name='review_modal'),
]
