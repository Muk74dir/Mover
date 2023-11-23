from django.db import models
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE, PERSON_STATUS

class PersonModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='main_user')
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=15)
    dob = models.DateField()

    image = models.ImageField(upload_to='profile_image/')
    status = models.CharField(max_length=10, choices=PERSON_STATUS)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    rating = models.FloatField(blank=True, null=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    

class VehicleModel(models.Model):
    driver = models.ForeignKey(PersonModel, on_delete=models.CASCADE, related_name='vehicle_owner')
    image = models.ImageField(upload_to='vehicle_image/') 
    type = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    license_no = models.CharField(max_length=20)
    
    
class AddressModel(models.Model):
    person = models.ForeignKey(PersonModel, on_delete=models.CASCADE, related_name='address_owner')
    address_line = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=10)

class TripRequestModel(models.Model):
    passenger = models.ForeignKey(PersonModel, on_delete=models.CASCADE, related_name='requester')
    driver = models.ForeignKey(PersonModel, on_delete=models.CASCADE, related_name='responder')
    status = models.BooleanField(default=False)


class TripModel(models.Model):
    passenger = models.ForeignKey(PersonModel, on_delete=models.CASCADE, related_name='passenger')
    driver = models.ForeignKey(PersonModel, on_delete=models.CASCADE, related_name='driver')
    vehicle = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    
    start_from = models.CharField(max_length=100)
    end_to = models.CharField(max_length=100)
    distance = models.CharField(max_length=20)
    duration = models.CharField(max_length=20)
    fare = models.FloatField()
    
    status = models.BooleanField(default=False)
    rating = models.FloatField()
    comments = models.CharField(max_length=200)
    
    initiated = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(auto_now=True)
    

class CouponModel(models.Model):
    driver = models.ForeignKey(PersonModel, on_delete=models.CASCADE, related_name='coupon_owner')
    code = models.CharField(max_length=20)
    value = models.FloatField()