
from django.db import models


class Baseclass(models.Model):
    alternativeMobileNumber=models.CharField(max_length=100,null=True,blank=True)
    permanentAddress1 = models.CharField(max_length=255,null=True,blank=True)
    permanentAddress2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    pin = models.CharField(max_length=10,null=True,blank=True) 
    additionalInfo1 = models.TextField(blank=True, null=True)
    additionalInfo2 = models.TextField(blank=True, null=True)
    additionalInfo3 = models.TextField(blank=True, null=True)
    additionalInfo4 = models.TextField(blank=True, null=True)

