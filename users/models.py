from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class UserContactModel(models.Model):
    name  = models.CharField(max_length=100,blank=False,null=False)
    email = models.EmailField()
    description = models.TextField(max_length=500,blank=True)
    phonenumber = models.IntegerField()
    
class PasswordResetOtp(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    otp = models.ImageField()
    created_at = models.DateField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + datetime.timedelta(minutes=10)