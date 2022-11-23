import base64
import hashlib
import hmac
import json
import time
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
import datetime
from django.utils import timezone

import requests
from common.models import CommonModel
from config import local_settings

class UserManager(BaseUserManager):    
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
        user.is_active = True
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

    username_regex = RegexValidator(regex=r'^[ㄱ-ㅎ|가-힣|a-z|A-Z|0-9|]+$', message="Username format invalid. Try eliminating spaces and symbols.")
    username = models.CharField(max_length=30, unique=True, validators=[username_regex])
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)


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
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.user)


class SMSAuth(CommonModel):
    phone_regex = RegexValidator(regex=r'^\d{10,11}$', message="Phone number must be entered in the format: '01012345678'. Up to 11 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=11, primary_key=True)
    auth_number = models.IntegerField(null=True, blank=True)
    is_phone_number_authenticated = models.BooleanField(default=False)

    def make_signature(self, string):
        secret_key = bytes(local_settings.NCP_SECRET_KEY, 'UTF-8')
        message = bytes(string, 'UTF-8')
        return base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    def send_sms(self):
        base_url = f'https://sens.apigw.ntruss.com'
        uri = f'/sms/v2/services/{local_settings.NCP_SERVICE_ID}/messages'

        timestamp = str(int(time.time() * 1000))
        message = "POST" + " " + uri + "\n" + timestamp + "\n" + local_settings.NCP_ACCESS_KEY_ID
        
        body = {
            "type": "SMS",
            "contentType": "COMM",
            "from": local_settings.SENDER_PHONE_NUMBER,
            "content": f"[be_major] 인증 번호 [{self.auth_number}]를 입력해주세요.",
            "messages" : [{"to": self.phone_number}]
        }

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": local_settings.NCP_ACCESS_KEY_ID,
            "x-ncp-apigw-signature-v2": self.make_signature(message),
        }
        requests.post(base_url + uri, data=json.dumps(body), headers=headers)

    @classmethod
    def check_auth_number(cls, phone_number, auth_number):
        time_limit = timezone.now() - datetime.timedelta(minutes=5)
        result = cls.objects.filter(
            phone_number=phone_number,
            auth_number=auth_number,
            updated_at__gte=time_limit
        )
        if result:
            return True
        return False