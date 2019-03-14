from django.db import models
from django.contrib.auth.models import User #Default User model
from django.core.validators import RegexValidator

# Create your models here.
# Uses email instead of username for validation!
User.USERNAME_FIELD = 'email'
User._meta.get_field('email')._unique = True
User.REQUIRED_FIELDS = ['username']

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 30, default = 'User')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return self.first_name

class CustomSeller(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    company_name = models.CharField(max_length = 30)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    company_address = models.CharField(max_length = 150)

    def __str__(self):
        return self.company_name

class ContactInfo(models.Model):
    fullname = models.CharField(max_length = 60)
    email_address = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    message = models.TextField(max_length = 250)
    
    def __str__(self):
        return '%s - %s' % (self.fullname, self.message)

class ProductsInfo(models.Model):
    nameofprod = models.CharField(max_length = 50)
    description = models.CharField(max_length = 150)
    size = models.CharField(max_length = 3)
    gender = models.CharField(max_length = 6)
    colors = models.CharField(max_length = 18, default = "All")
    category = models.CharField(max_length = 10, default = "None")
    price = models.PositiveIntegerField(default = 20)
    seller = models.ForeignKey(CustomSeller, on_delete = models.CASCADE)

class CartInfo(models.Model):
    nameofprod = models.CharField(max_length = 50)
    price = models.PositiveIntegerField(default = 20)
    seller = models.ForeignKey(CustomSeller, on_delete = models.CASCADE) #New

class OrderInfo(models.Model):
    totalprice = models.PositiveIntegerField(default = 20)
    products = models.CharField(max_length = 200)
    customer = models.ForeignKey(CustomUser, on_delete = models.CASCADE)

class WishlistInfo(models.Model):
    # totalprice = models.PositiveIntegerField(default = 20)
    products = models.CharField(max_length = 200)
    customer = models.ForeignKey(CustomUser, on_delete = models.CASCADE)

class SellerOrderInfo(models.Model):
    # totalprice = models.PositiveIntegerField(default = 20)
    products = models.CharField(max_length = 200)
    seller = models.ForeignKey(CustomSeller, on_delete = models.CASCADE)
    customer = models.CharField(max_length = 75, default = "Anonymous")

