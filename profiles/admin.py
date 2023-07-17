from django.contrib import admin
from .models import Avatar, UserProfile


class AvatarAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'image_url',
        'image',
        'avatar_name',
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'default_street_address1',
    )


admin.site.register(Avatar, AvatarAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
