from django.contrib import admin

# Register your models here.

from .models import User_mobile,Error_handling,Client_details_view,Client_sub_view

class Client_Details(admin.ModelAdmin):
    list_display = ('Client_auth', 'Client_Number', 'Client_Sal','Type')
    # list_filter =  ('author', 'is_published', 'published_date')
    # search_fields = ('title', 'author_name')
    # ordering = ('-published_date',)
    fields = ['Client_auth', 'Client_Number', 'Client_Sal','Type','Add_Caretaker_Detail',
              'Alternative_mobile_number','Permanent_Address_1','Permanent_Address_2','City',
              'State','PIN','Additional_Info1','Additional_Info2','Additional_Info3','Additional_Info4']
    


admin.site.register(User_mobile)
admin.site.register(Error_handling)
admin.site.register(Client_details_view,Client_Details)
admin.site.register(Client_sub_view)
