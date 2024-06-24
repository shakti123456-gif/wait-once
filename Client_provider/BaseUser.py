
from django.db import models


class Baseclass(models.Model):
    Alternative_mobile_number=models.CharField(max_length=100,null=True,blank=True)
    Permanent_Address_1 = models.CharField(max_length=255,null=True,blank=True)
    Permanent_Address_2 = models.CharField(max_length=255, blank=True, null=True)
    City = models.CharField(max_length=50,null=True,blank=True)
    State = models.CharField(max_length=50,null=True,blank=True)
    PIN = models.CharField(max_length=10,null=True,blank=True) 
    Additional_Info1 = models.TextField(blank=True, null=True)
    Additional_Info2 = models.TextField(blank=True, null=True)
    Additional_Info3 = models.TextField(blank=True, null=True)
    Additional_Info4 = models.TextField(blank=True, null=True)

