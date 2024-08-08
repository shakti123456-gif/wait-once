from django.contrib import admin
from .models import *


class TherapistDetails(admin.ModelAdmin):  
    list_display = ('therapist_auth', 'therapist_num','alternativeMobileNumber','therapist_id')
    fields = [ 'therapist_auth','therapist_num','service_age_group','therapist_type',
              'dva','independent','multi_provider','multi_Location','web','experience',
              'alternativeMobileNumber','permanentAddress1','permanentAddress2','city',
              'state','pin','additionalInfo1','additionalInfo2','additionalInfo3','additionalInfo4']


class Provider_Details(admin.ModelAdmin):
  
    list_display = ('providerName','providerType','providerId')  
    fields = ['providerName','providerNum','providerType','therapistServicemap','email','ndisNumber',
              'abn', 'ProviderEmployers','ProviderLocations','ageGroup','web','chain','dva', 
               'alternativeMobileNumber','permanentAddress1','permanentAddress2','city',
              'state','pin','additionalInfo1','additionalInfo2','additionalInfo3','additionalInfo4']
    

class service_details(admin.ModelAdmin):
    list_display = ('service_name','service_id')
    


class TherapistAvailAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_therapist_first_name', 'date')
    ordering = ('date',)

    def get_therapist_first_name(self, obj):
        return obj.therapist_id.therapist_auth.firstName
    get_therapist_first_name.short_description = 'Therapist First Name'



admin.site.register(Therapist,TherapistDetails)
admin.site.register(Provider,Provider_Details)
admin.site.register(Location)
admin.site.register(Service,service_details)
admin.site.register(Appointment)
admin.site.register(Therapist_booked)
admin.site.register(therapist_service)
admin.site.register(Provider_employee)
admin.site.register(Therapist_working_time)
admin.site.register(Therapist_unavailability)
admin.site.register(therapistAvailability,TherapistAvailAdmin)
admin.site.register(Appointment1)
admin.site.register(clientPrebookAppointments)
admin.site.register(ReoccureAppointments)