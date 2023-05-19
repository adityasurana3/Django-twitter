from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile

# Register your models here.
admin.site.unregister(Group)

class ProfileInlene(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [ProfileInlene]

# Unregister User
admin.site.unregister(User)

# Re-register User

admin.site.register(User,UserAdmin)
# admin.site.register(Profile)