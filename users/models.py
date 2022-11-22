import email
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
  
  ''' User Model Definition '''

  # not using first, last name
  first_name = models.CharField(max_length=30, editable=False)
  last_name = models.CharField(max_length=150, editable=False)
  
  # custom
  phone_regex = RegexValidator(regex=r'^\d{10,11}$', message="Phone number must be entered in the format: '01012345678'. Up to 11 digits allowed.")
  phone_number = models.CharField(validators=[phone_regex], max_length=11, unique=True)
  is_phone_number_authenticated = models.BooleanField(default=False)

  USERNAME_FIELD = 'phone_number'

  def __str__(self):
    return self.username


class Profile(models.Model):

  ''' Profile Model Definition '''

  class GenderChoices(models.TextChoices):
    MALE = ("male", "남자")
    FEMALE = ("female", "여자")
    ELSE = ("else", "기타")

  user = models.OneToOneField('User', unique=True, on_delete=models.CASCADE)
  is_leader = models.BooleanField(default=False)
  avatar = models.ImageField(blank=True)
  gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
  )
  date_of_birth = models.DateField()
  

  def __str__(self):
    return str(self.user)
