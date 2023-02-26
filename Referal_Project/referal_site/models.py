from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser
import uuid

class userData(AbstractBaseUser):
    email = models.EmailField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    referral_code_used = models.CharField(max_length=12, unique=False, blank=True, null=True)
    referral_code_generated = models.CharField(max_length=12, unique=True, blank=False, null=False)
    number_of_referred = models.IntegerField(default=0)
    
    USERNAME_FIELD = 'email'
    
@receiver(pre_save, sender=userData)
def add_referral_code(sender, instance, **kwargs):
    if not instance.referral_code_generated:
        instance.referral_code_generated = generate_referral_code()
        
def generate_referral_code():
    code = str(uuid.uuid4().hex)[:12].upper()
    return code