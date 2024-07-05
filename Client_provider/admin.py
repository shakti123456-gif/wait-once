from django.contrib import admin
from .models import *


class Therapist_Details(admin.ModelAdmin):
  
    list_display = ('therapist_auth', 'therapist_num','AlternativeMobileNumber','therapist_id')
   
    fields = [ 'therapist_auth','therapist_num','service_age_group','therapist_type',
              'dva','independent','multi_provider','multi_Location','web',
              'AlternativeMobileNumber','PermanentAddress1','PermanentAddress2','City',
              'State','PIN','AdditionalInfo1','AdditionalInfo2','AdditionalInfo3','AdditionalInfo4']


class Provider_Details(admin.ModelAdmin):
  
    list_display = ('providerName','providerType')
  
    fields = [ 'providerName','providerNum','providerType','therapistServicemap','email','ndisNumber',
              'abn', 'ProviderEmployers','ProviderLocations','ageGroup','web','chain','phoneNo', 
              'AlternativeMobileNumber','PermanentAddress1','PermanentAddress2','City',
              'State','PIN','AdditionalInfo1','AdditionalInfo2','AdditionalInfo3','AdditionalInfo4']
    

class service_details(admin.ModelAdmin):
  
    list_display = ('service_name','service_id')
    

admin.site.register(Therapist,Therapist_Details)
admin.site.register(Provider,Provider_Details)
admin.site.register(Location)
admin.site.register(Service,service_details)
admin.site.register(Appointment)
admin.site.register(Therapist_booked)
admin.site.register(therapist_service)
admin.site.register(Provider_employee)
admin.site.register(Therapist_working_time)
admin.site.register(Therapist_unavailability)
admin.site.register(therapistAvailability)