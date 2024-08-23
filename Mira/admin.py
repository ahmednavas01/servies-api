from django.contrib import admin,sites
from .models import UserLogin
# Register your models here.
class admin_category(admin.ModelAdmin):
    list=['user_email','user_status','user_request']
admin.site.register(UserLogin,admin_category)