from django.contrib import admin
from .models import Review
from .forms import ReviewForm


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product'
        'title'
        'body'
        'rating'
        'created_at'
        'updated_at'
    )


class ReviewFormAdmin(admin.ModelAdmin):
    list_display = (
        'model',
        'fields',
    )


admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewForm, ReviewFormAdmin)
