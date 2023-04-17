from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'user',
        'title',
        'rating',
        'created_at',
        'updated_at',
    )


# Register your models here.
admin.site.register(Review, ReviewAdmin)
