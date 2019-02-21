from django.db import models
from django.contrib.auth.models import User #Default User model

# Create your models here.
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    is_seller = models.BooleanField(default = False)


        