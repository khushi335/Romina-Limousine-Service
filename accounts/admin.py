from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Add your extra fields to the user edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone', 'address', 'is_user', 'is_head')}),
    )

    # Display these fields in the user list
    list_display = ('username', 'email', 'phone', 'address', 'is_user', 'is_head', 'is_staff', 'is_superuser')
    list_filter = ('is_user', 'is_head', 'is_staff', 'is_superuser', 'is_active')

    # Add your extra fields to the add user form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('phone', 'address', 'is_user', 'is_head')}),
    )
