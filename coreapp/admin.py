from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from coreapp.models import User, Page, Post, Tag

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'image_s3_path',
                    'role',
                    'title',
                    'is_blocked',
                )
            }
        )
    
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'image_s3_path',
                    'role',
                    'title',
                    'is_blocked',   
                )
            }
        )
    
    )
    
admin.site.register(Page)
admin.site.register(Post)
admin.site.register(Tag)