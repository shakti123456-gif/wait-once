from django.contrib import admin
from .models import *




class Therapist_Details(admin.ModelAdmin):
  
    list_display = ('therapist_auth', 'therapist_num','Alternative_mobile_number')
   
    fields = [ 'therapist_auth','therapist_num','service_age_group','therapist_type',
              'dva','independent','multi_provider','multi_Location','web',
              'Alternative_mobile_number','Permanent_Address_1','Permanent_Address_2','City',
              'State','PIN','Additional_Info1','Additional_Info2','Additional_Info3','Additional_Info4']
    
class Provider_Details(admin.ModelAdmin):
  
    list_display = ('provider_name','provider_num')
  
    fields = [ 'provider_name','provider_num','provider_type','therapist_service_map','email','ndisNumber',
              'abn', 'Provider_employers','Provider_locations','age_group','web','chain','phoneNo', 
              'Alternative_mobile_number','Permanent_Address_1','Permanent_Address_2','City',
              'State','PIN','Additional_Info1','Additional_Info2','Additional_Info3','Additional_Info4']
    

admin.site.register(Therapist,Therapist_Details)
admin.site.register(Provider,Provider_Details)
admin.site.register(Location)
admin.site.register(Service)
admin.site.register(Appointment)
admin.site.register(Therapist_booked)
admin.site.register(therapist_service)
admin.site.register(Provider_employee)