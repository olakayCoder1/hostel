from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin ,BaseUserManager
# Create your models here.



def upload_to(instance, filename):
    return 'profiles/{filename}'.format(filename=filename)


class UserManager(BaseUserManager):

    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model( email=email , **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self,email,password, **extra_fields):

        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must be given is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be given is_superuser=True')
        return self.create_user(email,password,**extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    GENDER_STATUS = (
        ('male','Male'),
        ('female','Female'),
    )
    uuid = models.CharField(max_length=100 , null=True , blank=True , unique=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100 , default='') 
    gender = models.CharField(max_length=20 , choices=GENDER_STATUS, null=True , blank=True)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False, help_text=_('Flag to determine if email has been verified'))
    image = models.ImageField( 
        upload_to=upload_to , null=True , blank=True ,
        help_text=_(
            ""
        ),
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects= UserManager()

    USERNAME_FIELD ="email" 



    def __str__(self) -> str:
        return self.email


    @classmethod
    def check_email(cls, email:str):
        return cls.objects.filter(email=email).exists()


    @classmethod
    def disabled_user(cls):
        return cls.objects.filter(is_active=False , is_staff=False).count()


    @classmethod
    def active_user(cls):
        return cls.objects.filter(is_active=True , is_staff=False).count()



class Profile(models.Model):
    
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20 , null=True , blank=True)
    address = models.CharField(max_length=200 , null=True , blank=True)
    role = models.ManyToManyField('account.UserRole')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Permission(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()



class UserRole(models.Model):
    name = models.CharField(max_length=50)
    permission = models.ManyToManyField(Permission)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    