from typing import Iterable
from django.db import models
from mobile_api_user.models import User_mobile
from .BaseUser import Baseclass



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
        return f"{self.therapist_id}"

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
    Therapist_Name=models.ForeignKey(Therapist,on_delete=models.SET_NULL,null=True,blank=True)
    service_Name=models.ForeignKey(Service,on_delete=models.SET_NULL,null=True,blank=True) 

    class Meta:
        unique_together = ('Therapist_Name', 'service_Name')


class Provider(Baseclass):
    provider_id = models.AutoField(primary_key=True)
    provider_num = models.PositiveIntegerField()
    mobileNumber = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    ndisNumber = models.CharField(max_length=15, null=True, blank=True)
    therapist_service_map=models.ManyToManyField(therapist_service)
    Provider_employers=models.ManyToManyField(Provider_employee)
    provider_name = models.CharField(max_length=64)
    provider_type = models.CharField(max_length=16)
    abn = models.CharField(max_length=16)
    age_group = models.CharField(max_length=16)
    DVA = models.CharField(max_length=16, blank=True, null=True)
    chain = models.CharField(max_length=16, blank=True, null=True)
    Provider_locations = models.ManyToManyField(Location)
    phoneNo = models.CharField(max_length=16, blank=True, null=True)
    web = models.URLField(max_length=128, blank=True, null=True)
    
    def __str__(self):
        return self.provider_name


class Appointment(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    therapy_start_time = models.DateTimeField(null=True,blank=True)
    therapy_end_time = models.DateTimeField(blank=True,null=True)
    Location_details=models.CharField(max_length=250,null=True,blank=True)
    Location_id=models.OneToOneField(Location,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"Appointment with {self.provider.provider_name} at {self.therapy_start_time}"

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method
        super(Appointment, self).save(*args, **kwargs)
