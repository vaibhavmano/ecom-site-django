from django.db import models
from django.contrib.auth.models import User #Default User model
from django.core.validators import RegexValidator

# Create your models here.
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    is_seller = models.BooleanField(default = False)

class ContactInfo(models.Model):
    fullname = models.CharField(max_length = 60)
    email_address = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    message = models.TextField(max_length = 250)
    
    def __str__(self):
        return self.fullname