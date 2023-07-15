from django.contrib import admin
from .models import Avatar


class AvatarAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'image_url',
        'image',
        'avatar_name',
    )


admin.site.register(Avatar, AvatarAdmin)
