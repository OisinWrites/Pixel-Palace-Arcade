from django.urls import path
from . import views

urlpatterns = [
    path('review/<int:product_id>/', views.view_reviews, name='view_reviews'),
    path('create/<int:product_id>/', views.create_review,
         name='create_review'),
    path('update/<int:review_id>/', views.update_review, name='update_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
