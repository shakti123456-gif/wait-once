
from django.db import models


class Baseclass(models.Model):
    AlternativeMobileNumber=models.CharField(max_length=100,null=True,blank=True)
    PermanentAddress1 = models.CharField(max_length=255,null=True,blank=True)
    PermanentAddress2 = models.CharField(max_length=255, blank=True, null=True)
    City = models.CharField(max_length=50,null=True,blank=True)
    State = models.CharField(max_length=50,null=True,blank=True)
    PIN = models.CharField(max_length=10,null=True,blank=True) 
    AdditionalInfo1 = models.TextField(blank=True, null=True)
    AdditionalInfo2 = models.TextField(blank=True, null=True)
    AdditionalInfo3 = models.TextField(blank=True, null=True)
    AdditionalInfo4 = models.TextField(blank=True, null=True)

