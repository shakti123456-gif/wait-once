from typing import Iterable
from django.db import models
from mobile_api_user.models import User_mobile
from .BaseUser import Baseclass
from datetime import datetime ,timedelta



class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_num = models.CharField(max_length=100)
    location_name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=50)
    location_description = models.TextField(blank=True, null=True)
    street_number = models.CharField(max_length=10, blank=True, null=True)
    unit_number = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    pin = models.CharField(max_length=10) 
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.location_name



class Therapist(Baseclass):
    therapist_id = models.AutoField(primary_key=True)
    therapist_num = models.CharField(max_length=100)
    therapist_auth = models.OneToOneField(User_mobile,on_delete=models.CASCADE)
    therapist_type = models.CharField(max_length=50)
    abn = models.CharField(max_length=20, blank=True, null=True) 
    service_age_group = models.CharField(max_length=50, blank=True, null=True)
    dva = models.CharField(max_length=50,blank=True,null=True)  
    independent = models.BooleanField(default=False)
    multi_provider = models.BooleanField(default=False)
    multi_Location = models.ManyToManyField(Location)
    web = models.URLField(blank=True, null=True)
    date_field= models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"{self.therapist_auth.firstName}"
    

class Therapist_booked(models.Model):
    therapist_detail=models.ForeignKey(Therapist,on_delete=models.SET_NULL,null=True,blank=True)
    tharapist_Booked=models.BooleanField(default=False)
    therapy_completed=models.BooleanField(default=False)
    therapy_start_booked_time=models.DateTimeField(null=True,blank=True)
    therapy_end_booked_time=models.DateTimeField(null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.therapist_detail.therapist_id if self.therapist_detail else 'No Therapist'}"
    class Meta:
        managed = True
        verbose_name = 'Therapist Booked slot'
        verbose_name_plural = 'Therapist Booked slot'


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_num = models.IntegerField()
    service_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    service_description = models.CharField(max_length=128)
    session_duration = models.IntegerField()
    plan_duration = models.IntegerField()
    plan_type = models.CharField(max_length=8)
    category = models.CharField(max_length=8)
    age_group = models.CharField(max_length=8)
    prerequisites = models.CharField(max_length=128)
    information = models.CharField(max_length=256)

    def __str__(self):
        return self.service_name

class Provider_employee(models.Model):
    Users_name=models.CharField(max_length=100,null=True,blank=True)
    password=models.CharField(max_length=100,null=True,blank=True)
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('check', 'Check'),
        ('tech', 'Tech'),
    ]
    
    Usertype = models.CharField(max_length=5, choices=USER_TYPE_CHOICES)

    def __str__(self):        
        return f"{self.Users_name} ({self.Usertype})"
    

class therapist_service(models.Model):
    Therapist_Name=models.ForeignKey(Therapist,on_delete=models.CASCADE)
    service_Name=models.ForeignKey(Service,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('Therapist_Name', 'service_Name')
    
    def __str__(self):        
         return f"{self.Therapist_Name.therapist_auth.firstName} - {self.service_Name.service_name}"



class Provider(Baseclass):
    providerId = models.AutoField(primary_key=True)
    providerNum = models.PositiveIntegerField()
    mobileNumber = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    ndisNumber = models.CharField(max_length=15, null=True, blank=True)
    therapistServicemap=models.ManyToManyField(therapist_service)
    ProviderEmployers=models.ManyToManyField(Provider_employee)
    providerName = models.CharField(max_length=64)
    providerType = models.CharField(max_length=16)
    abn = models.CharField(max_length=16)
    ageGroup = models.CharField(max_length=16)
    DVA = models.CharField(max_length=16, blank=True, null=True)
    chain = models.CharField(max_length=16, blank=True, null=True)
    ProviderLocations = models.ManyToManyField(Location)
    phoneNo = models.CharField(max_length=16, blank=True, null=True)
    web = models.URLField(max_length=128, blank=True, null=True)

    
    def __str__(self):
        return self.providerName
    
    @property
    def therapist_and_service_details(self):
        provider_data_details = self.therapistServicemap.all()
        therapist_ids = [entry.Therapist_Name.therapist_id for entry in provider_data_details]
        service_ids = [entry.service_Name.service_id for entry in provider_data_details]
        therapist_details = Therapist.objects.filter(therapist_id__in=therapist_ids)
        service_details = Service.objects.filter(service_id__in=service_ids)

        return therapist_details,service_details

    
    def get_therapist_services(self, therapist_id=None):
        provider_data_details = self.therapistServicemap.all()
   
        service_details=[]
        if therapist_id:
            services = provider_data_details.filter(Therapist_Name__therapist_id=therapist_id)
            service_ids = [id.service_Name.service_id for id in services]
            service_details = Service.objects.filter(service_id__in=service_ids)
        return service_details 

   
    @property
    def Provider_locations_add(self):
        Provider_location=self.ProviderLocations.all()
        location_all_id=[provider.location_id for provider in Provider_location]
        location_details = Location.objects.filter(location_id__in=location_all_id)
        return location_details


        
class Appointment(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    therapy_start_time = models.DateTimeField(null=True,blank=True)
    therapy_end_time = models.DateTimeField(blank=True,null=True)
    Location_details=models.CharField(max_length=250,null=True,blank=True)
    Location_id=models.OneToOneField(Location,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"Appointment with {self.provider.providerName} at {self.therapy_start_time}"

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        self.full_clean()  
        super(Appointment, self).save(*args, **kwargs)

class Therapist_working_time(models.Model):
    therapist_id = models.ForeignKey(Therapist,on_delete=models.CASCADE)
    startime=models.TimeField()
    endtime=models.TimeField()
    createdAt = models.DateTimeField(null=True,blank=True)
    updateAt = models.DateTimeField(null=True,blank=True)


    def __str__(self) -> str:
        return f"{self.therapist_id.therapist_auth.firstName}   {self.startime}  - {self.endtime}"
    
    
    def save(self, *args, **kwargs):
        if not self.createdAt:
            self.createdAt = datetime.now() + timedelta(hours=5, minutes=30)
        self.updateAt = datetime.now() + timedelta(hours=5, minutes=30)
        super().save(*args, **kwargs)



class Therapist_unavailability(models.Model):
    therapist_id = models.ForeignKey(Therapist,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date=models.DateField()
    startime=models.TimeField()
    endtime=models.TimeField()
    createdAt = models.DateTimeField(null=True,blank=True)
    updateAt = models.DateTimeField(null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.start_date}  - {self.end_date}"
    
    def save(self, *args, **kwargs):
        if not self.createdAt:
            self.createdAt = datetime.now() + timedelta(hours=5, minutes=30)
        self.updateAt = datetime.now() + timedelta(hours=5, minutes=30)
        super().save(*args, **kwargs)



    
