from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile

# Register your models here.


class UserAdmin(BaseUserAdmin):
    search_fields = ["username", "email", "first_name", "last_name"]
    list_filter = ["date_joined", "is_verified"]
    readonly_fields = ['date_joined','last_login']
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "date_joined",
        "is_verified",
    ]
    fieldsets = [
        (None,{"fields":[ "username","email",]}),
        ("Personal Data",{"fields":["first_name","last_name"]}),
        ("Advanced Options",{"fields":["is_verified"]}),
        ("General Data",{"fields":["date_joined"]}),
        ("Danger Zone",{"classes":["collapsable"],"fields":["password"]})
    ]


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ["user__username", "user__email"]
    list_filter = ["created_at"]
    list_display = ["user__username", "user__first_name", "user__last_name", "bio"]


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
