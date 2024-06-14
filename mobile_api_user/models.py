from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models



class UserManager(BaseUserManager):
    def create_user(self,signing_as,mobile_number, first_name, last_name, Dateofbirth, email_address=None, ndis_number=None, password=None,Language_perfered=None,Refferal_code=None):
        if not mobile_number:
            raise ValueError('Users must have a mobile number')
        user = self.model(
            signing_as=signing_as,
            mobile_number=mobile_number,
            first_name=first_name,
            last_name=last_name,
            Dateofbirth=Dateofbirth,
            email_address=email_address,
            ndis_number=ndis_number,
            Language_perfered=Language_perfered,
            Refferal_code=Refferal_code
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

class User_mobile(AbstractBaseUser):
    SIGNING_AS_CHOICES = [
        ('Self', 'Self'),
        ('Parent', 'Parent'),
    ]
    signing_as = models.CharField(
        max_length=6,
        choices=SIGNING_AS_CHOICES,
        default='Self',
    )
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    Dateofbirth = models.DateField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    email_address = models.CharField(max_length=100, null=True, blank=True,unique=True)
    ndis_number = models.CharField(max_length=15, null=True, blank=True,unique=True)
    Language_perfered=models.CharField(max_length=100,null=True,blank=True)
    Refferal_code=models.CharField(max_length=50,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    password=models.CharField(max_length=15)

    objects = UserManager()

    USERNAME_FIELD = 'mobile_number'
    # REQUIRED_FIELDS = ['first_name', 'last_name', 'Dateofbirth']

    class Meta:
        db_table = 'mobile_api_user_user_mobile'
        managed = True

    def __str__(self):
        return self.mobile_number

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def check_password(self, raw_password):
        return self.password==raw_password

    def delete(self, *args, **kwargs):
        print(f"Deleting instance: {self}")
        super().delete(*args, **kwargs)  # Call the superclass delete method







