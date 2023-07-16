from django.contrib import admin
from .models import Review, Rating


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'user',
        'title',
        'created_at',
        'updated_at',
    )


class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'rating',
    )


# Register your models here.
admin.site.register(Review, ReviewAdmin)
admin.site.register(Rating, RatingAdmin)
