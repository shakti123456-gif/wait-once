
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import datetime,timedelta

class UserManager(BaseUserManager):
    def create_user(self,Signing_as,MobileNumber, FirstName, LastName, DateofBirth, EmailAddress=None, NdisNumber=None, password=None,Language=None,RefferalCode=None):
        if not MobileNumber:
            raise ValueError('Users must have a mobile number')
        
        user = self.model(
            Signing_as=Signing_as,
            MobileNumber=MobileNumber,
            FirstName=FirstName,
            LastName=LastName,
            DateofBirth=DateofBirth,
            EmailAddress=EmailAddress,
            NdisNumber=NdisNumber,
            Language=Language,
            RefferalCode=RefferalCode,
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
    Signing_as = models.CharField(
        max_length=6,
        choices=SIGNING_AS_CHOICES,
        default='Self',
    )
    UserId = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=100,null=True,blank=True)
    LastName = models.CharField(max_length=100,null=True,blank=True)
    DateofBirth = models.DateField(null=True, blank=True)
    MobileNumber = models.CharField(max_length=15, unique=True)
    EmailAddress = models.CharField(max_length=100, null=True, blank=True,unique=True)
    NdisNumber = models.CharField(max_length=15, null=True, blank=True,unique=True)
    Language=models.CharField(max_length=100,null=True,blank=True)
    RefferalCode=models.CharField(max_length=50,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    Created_At=models.DateTimeField(null=True,blank=True)
    password=models.CharField(max_length=15,verbose_name="Password")

    objects = UserManager()

    USERNAME_FIELD = 'MobileNumber'
    # REQUIRED_FIELDS = ['first_name', 'last_name', 'Dateofbirth']

    class Meta:
        db_table = 'mobile_api_user_user_mobile'
        managed = True

    def __str__(self):
        return self.MobileNumber

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def check_password(self, raw_password):
        return self.password==raw_password

    def save(self, *args, **kwargs):
        # timestamp = datetime.fromisoformat(str(self.Created_At))
        # new_timestamp = timestamp + timedelta(hours=5,minutes=30)
        if not self.Created_At:
            self.Created_At = default_created_at()
        super().save(*args, **kwargs)
 
def Fix_time(time):
    formatted_timestamp = time.strftime("%B %d, %Y, at %I:%M %p and %S.%f seconds")
    return formatted_timestamp





