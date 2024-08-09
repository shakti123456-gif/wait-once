from django.contrib import admin

# Register your models here.

from .models import User_mobile,Error_handling,Client_details_view,Client_sub_view

class Client_Details(admin.ModelAdmin):
    list_display = ('Client_auth','type',id)    
    # list_filter =  ('author', 'is_published', 'published_date')
    # search_fields = ('title', 'author_name')
    ordering = ('-id',)
    fields = ['Client_auth','type','addChildren',
              'alternativeMobileNumber','permanentAddress1','permanentAddress2','city',
              'state','pin','additionalInfo1','additionalInfo2','additionalInfo3','additionalInfo4']
    
class User_Details(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'mobileNumber','fireBaseKey')
    # list_filter =  ('author', 'is_published', 'published_date')
    # search_fields = ('title', 'author_name')
   
    # fields = ['Client_auth', 'Client_Number', 'Client_Sal','Type','Add_Caretaker_Detail',
    #           'Alternative_mobile_number','Permanent_Address_1','Permanent_Address_2','City',
    #           'State','PIN','Additional_Info1','Additional_Info2','Additional_Info3','Additional_Info4']



class Client_sub_view_add(admin.ModelAdmin):
    list_display = ('clientSubId', 'firstName', 'lastName')
    fields = ['firstName', 'lastName','dateofbirth','insuranceNumber']
    


admin.site.register(User_mobile,User_Details)
admin.site.register(Error_handling)
admin.site.register(Client_details_view,Client_Details)
admin.site.register(Client_sub_view,Client_sub_view_add)


