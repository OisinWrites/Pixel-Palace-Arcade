from django.urls import path
from . import views
from .views import create_review
urlpatterns = [
    path('blog/<int:product_id>/', create_review, name='create_review'),
]
