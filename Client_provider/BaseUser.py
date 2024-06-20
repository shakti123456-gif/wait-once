
from django.db import models

class Baseclass(models.Model):
    Permanent_Address_1 = models.CharField(max_length=255)
    Permanent_Address_2 = models.CharField(max_length=255, blank=True, null=True)
    City = models.CharField(max_length=50)
    State = models.CharField(max_length=50)
    PIN = models.CharField(max_length=10) 
    Additional_Info1 = models.TextField(blank=True, null=True)
    Additional_Info2 = models.TextField(blank=True, null=True)
    Additional_Info3 = models.TextField(blank=True, null=True)
    Additional_Info4 = models.TextField(blank=True, null=True)

