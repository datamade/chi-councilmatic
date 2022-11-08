from django.contrib import admin
from django.contrib.auth.models import User

from .models import ChicagoBill


class CustomUserAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("email", "date_joined", "last_login", "is_superuser")
    list_filter = ("is_superuser",)


# Register your models here.
admin.site.register(ChicagoBill)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
