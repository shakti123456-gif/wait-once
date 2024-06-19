
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import datetime,timedelta

class UserManager(BaseUserManager):
    def create_user(self,signingAs,mobileNumber, firstName, lastName, dateofBirth, email=None, ndisNumber=None, password=None,communicationPreference=None,refferalCode=None):
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

    def create_superuser(self, mobile_number,password=None):
        user = self.create_user(
            mobile_number,
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
    createdAt=models.DateTimeField(null=True,blank=True)
    password=models.CharField(max_length=15,verbose_name="Password")

    objects = UserManager()

    USERNAME_FIELD = 'mobileNumber'
    # REQUIRED_FIELDS = ['first_name', 'last_name', 'Dateofbirth']

    class Meta:
        db_table = 'mobile_api_user_user_mobile'
        managed = True

    def __str__(self):
        return self.mobileNumber

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





