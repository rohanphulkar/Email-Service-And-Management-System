from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import UserManager
import uuid

GENDER_CHOICES = (('male','Male'),('female','Female'))

class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255,editable=False,unique=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15,blank=True,null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    pwd_reset_code = models.CharField(max_length=255,null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = UserManager() # custom user manager for creating and managing users

    def __str__(self):
        return self.username
    
    def save(self,*args,**kwargs):
        # Append "@metabyte.one" to the username if it doesn't contain an email domain
        if len(self.username.split("@"))==1:
            self.username = f"{self.username}@metabyte.one"
        super().save(*args, **kwargs)
    
    # For checking permissions to keep it simple all admin have all permissions
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return self.is_admin

