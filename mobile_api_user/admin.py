from django.contrib import admin

# Register your models here.

from .models import User_mobile,Error_handling

admin.site.register(User_mobile)
admin.site.register(Error_handling)
