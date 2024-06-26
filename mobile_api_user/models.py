
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import datetime,timedelta
from Client_provider.BaseUser import Baseclass
from django.db.models.signals import pre_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self,mobileNumber,password, firstName=None, lastName=None, dateofBirth=None, email=None, ndisNumber=None,communicationPreference=None,refferalCode=None,signingAs="Self"):
        if not mobileNumber:
            raise ValueError('Users must have a mobile number')
        
        user = self.model(
            signingAs=signingAs,
            mobileNumber=mobileNumber,
            firstName=firstName,
            lastName=lastName,
            dateofBirth=dateofBirth,
            email=email,
            ndisNumber=ndisNumber,
            communicationPreference=communicationPreference,
            refferalCode=refferalCode,
            password=password
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobileNumber,password):
        user = self.create_user(
            mobileNumber=mobileNumber,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


def default_created_at():
    return datetime.now() + timedelta(hours=5, minutes=30)

class User_mobile(AbstractBaseUser):
    SIGNING_AS_CHOICES = [
        ('Self', 'Self'),
        ('Parent', 'Parent'),
    ]
    signingAs = models.CharField(
        max_length=6,
        choices=SIGNING_AS_CHOICES,
        default='Self',
    )
    userId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100,null=True,blank=True)
    lastName = models.CharField(max_length=100,null=True,blank=True)
    dateofBirth = models.DateField(null=True, blank=True)
    mobileNumber = models.CharField(max_length=15, unique=True)
    email = models.CharField(max_length=100, null=True, blank=True,unique=True)
    ndisNumber = models.CharField(max_length=15, null=True, blank=True,unique=True)
    communicationPreference=models.CharField(max_length=100,null=True,blank=True)
    refferalCode=models.CharField(max_length=50,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    lastUpdate = models.DateTimeField(auto_now=True,null=True,blank=True)
    password=models.CharField(max_length=15,verbose_name="Password")

    objects = UserManager()

    USERNAME_FIELD = 'mobileNumber'
    # REQUIRED_FIELDS = ['first_name', 'last_name', 'Dateofbirth']

    class Meta:
        db_table = 'mobile_api_user_user_mobile'
        managed = True
        verbose_name = "Mobile user"
        verbose_name_plural = "Mobile user"


    def __str__(self):
        return str(self.mobileNumber)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def check_password(self, raw_password):
        return self.password==raw_password

    def save(self, *args, **kwargs):
        if not self.createdAt:
            self.Created_At = default_created_at()
        super().save(*args, **kwargs)
 
def Fix_time(time):
    formatted_timestamp = time.strftime("%B %d, %Y, at %I:%M %p and %S.%f seconds")
    return formatted_timestamp



class Error_handling(models.Model):
    errorId = models.AutoField(primary_key=True)
    status=models.CharField(max_length=30)
    status_Code=models.IntegerField()
    message=models.CharField(max_length=100)
    details=models.TextField()
    default_message=models.BooleanField(default=False)

    def __str__(self):
        return  str(self.status_Code)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Error handling'
        verbose_name_plural = 'Error handling'



class Client_sub_view(models.Model):
    clientSubId=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    dateofbirth=models.DateField(null=True,blank=True) 
    Ndisnumber=models.CharField(max_length=20,unique=True,null=True,blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Client sub'
        verbose_name_plural = 'Client sub'


class Client_details_view(Baseclass):
    Type_CHOICES = (
        ('M', 'M'),
        ('F', 'F'),
    )
    Client_ID = models.AutoField(primary_key=True)
    Client_auth = models.OneToOneField(User_mobile, on_delete=models.CASCADE)
    Client_Number = models.PositiveIntegerField(null=True,blank=True)
    Client_Sal = models.CharField(max_length=5,null=True,blank=True)
    Type = models.CharField(max_length=1, choices=Type_CHOICES,null=True,blank=True)
    Add_Caretaker_Detail=models.ManyToManyField(Client_sub_view)
    
    def __str__(self):
        return f"{self.Client_Number}"
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Client details'
        verbose_name_plural = 'Client details'


@receiver(pre_save, sender=User_mobile)
def create_profile(sender, instance, **kwargs):
    print("value")