
from django.db import models
from mobile_api_user.models import User_mobile


class Client_sub(models.Model):
    first_name=models.CharField(max_length=100) 
    last_name=models.CharField(max_length=100)
    dateofbirth=models.DateTimeField()
    Ndisnumber=models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Client sub'
        verbose_name_plural = 'Client sub'


class Client_details(models.Model):
    Type_CHOICES = (
        ('M', 'M'),
        ('K', 'k'),
    )
    Client_ID = models.AutoField(primary_key=True)
    Client_auth = models.OneToOneField(User_mobile, on_delete=models.CASCADE,blank=True,null=True)
    Client_Number = models.IntegerField()
    Client_Sal = models.CharField(max_length=100)
    Type = models.CharField(max_length=1, choices=Type_CHOICES)
    date_of_birth = models.DateTimeField()
    Ndis_Registered = models.BooleanField(default=False)
    Ndis_number = models.CharField(max_length=20)
    Care_taker_details=models.ManyToManyField(Client_sub)
    Permanent_Address_1 = models.CharField(max_length=255)
    Permanent_Address_2 = models.CharField(max_length=255, blank=True, null=True)
    City = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    PIN = models.CharField(max_length=10) 
    Additional_Info1 = models.TextField(blank=True, null=True)
    Additional_Info2 = models.TextField(blank=True, null=True)
    Additional_Info3 = models.TextField(blank=True, null=True)
    Additional_Info4 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.Client_Number}"
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Client details'
        verbose_name_plural = 'Client details'



class Therapist(models.Model):
    therapist_id = models.AutoField(primary_key=True)
    therapist_num = models.CharField(max_length=100)
    therapist_sal = models.CharField(max_length=10)
    Therapist_auth=models.OneToOneField(User_mobile,on_delete=models.CASCADE)
    therapist_type = models.CharField(max_length=50)
    dob = models.DateField()
    abn = models.CharField(max_length=20, blank=True, null=True) 
    ndis_registered = models.BooleanField(default=False)
    ndis_number = models.CharField(max_length=20, blank=True, null=True)
    service_age_group = models.CharField(max_length=50, blank=True, null=True)
    dva = models.BooleanField(default=False)  
    independent = models.BooleanField(default=False)
    multi_provider = models.BooleanField(default=False)
    state = models.CharField(max_length=50)
    alternative_phone_2 = models.CharField(max_length=15, blank=True, null=True)
    web = models.URLField(blank=True, null=True)
    additional_info1 = models.TextField(blank=True, null=True)
    additional_info2 = models.TextField(blank=True, null=True)
    additional_info3 = models.TextField(blank=True, null=True)
    additional_info4 = models.TextField(blank=True, null=True)
    additional_info5 = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.therapist_id}"


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_num = models.IntegerField()
    service_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    service_description = models.CharField(max_length=128)
    session_type = models.CharField(max_length=16)
    session_duration = models.IntegerField()
    plan_duration = models.IntegerField()
    plan_type = models.CharField(max_length=8)
    category = models.CharField(max_length=8)
    age_group = models.CharField(max_length=8)
    prerequisites = models.CharField(max_length=128)
    information = models.CharField(max_length=256)

    def __str__(self):
        return self.service_name



class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_num = models.CharField(max_length=100)
    location_name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=50)
    location_description = models.TextField(blank=True, null=True)
    street_number = models.CharField(max_length=10, blank=True, null=True)
    unit_number = models.CharField(max_length=10, blank=True, null=True)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    pin = models.CharField(max_length=10) 
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.location_name
    


class Provider(models.Model):
    provider_id = models.AutoField(primary_key=True)
    provider_num = models.IntegerField()
    provider_auth=models.OneToOneField(User_mobile,on_delete=models.CASCADE,blank=True,null=True)
    provider_name = models.CharField(max_length=64)
    provider_type = models.CharField(max_length=16)
    abn = models.CharField(max_length=16)
    ndis_registered = models.BooleanField()
    ndis_number = models.CharField(max_length=16, blank=True, null=True)  
    age_group = models.CharField(max_length=16)
    dva = models.CharField(max_length=16, blank=True, null=True)
    chain = models.CharField(max_length=16, blank=True, null=True)
    multi_location = models.CharField(max_length=16, blank=True, null=True)
    state = models.CharField(max_length=16)
    phone_1 = models.CharField(max_length=16)
    phone_2 = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(max_length=128)
    web = models.URLField(max_length=128, blank=True, null=True)
    contact_1 = models.CharField(max_length=32)
    contact_2 = models.CharField(max_length=32, blank=True, null=True)
    additional_info1 = models.CharField(max_length=64)
    additional_info2 = models.CharField(max_length=64, blank=True, null=True)
    additional_info3 = models.CharField(max_length=64, blank=True, null=True)
    additional_info4 = models.CharField(max_length=64, blank=True, null=True)
    additional_info5 = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.provider_name
