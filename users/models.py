from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator

from common.models import CommonModel

class UserManager(BaseUserManager):    
  use_in_migrations = True
  
  def create_user(self, phone_number, username, password):
      
      if not phone_number:
          raise ValueError('must have user phone_number.')
      if not username:
          raise ValueError('must have username.')
      if not password:
          raise ValueError('must have user password.')

      user = self.model(            
          phone_number=phone_number,
          username=username,
      )        
      user.set_password(password)        
      user.save(using=self._db)
      return user

  def create_superuser(self, phone_number, username, password):
  
      user = self.create_user(            
          phone_number=phone_number,
          username=username,
          password=password
      )
      user.is_admin = True
      user.is_staff = True
      user.is_superuser = True
      user.is_active = True
      user.save(using=self._db)

      return user

class User(AbstractBaseUser, PermissionsMixin):    
  
  ''' User Model Definition '''
  
  objects = UserManager()
  
  phone_regex = RegexValidator(regex=r'^\d{10,11}$', message="Phone number must be entered in the format: '01012345678'. Up to 11 digits allowed.")
  phone_number = models.CharField(validators=[phone_regex], max_length=11, unique=True)
  is_phone_number_authenticated = models.BooleanField(default=False)

  username = models.CharField(max_length=30, unique=True)
  is_staff = models.BooleanField(default=False)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)


  USERNAME_FIELD = 'phone_number'
  REQUIRED_FIELDS = ['username']

  def __str__(self):
    return self.username


class Profile(CommonModel):

  ''' Profile Model Definition '''

  class GenderChoices(models.TextChoices):
    MALE = ("male", "남자")
    FEMALE = ("female", "여자")
    ELSE = ("else", "기타")

  user = models.OneToOneField('User', unique=True, on_delete=models.CASCADE)
  is_leader = models.BooleanField(default=False)
  avatar = models.URLField(blank=True)
  gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
  )
  date_of_birth = models.DateField()
  email = models.EmailField(        
      max_length=255,        
      unique=True,    
  )

  def __str__(self):
    return str(self.user)
