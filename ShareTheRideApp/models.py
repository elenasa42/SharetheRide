from django.db import models
from django.contrib.auth.models import User
from mapbox_location_field.models import LocationField 
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank = True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=45)
    photo = models.ImageField(default="man.png", null = True, blank = True)
    
    def __str__(self):
        return self.lastname
    
    

class Vehicle(models.Model):
    
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=10)
    plate = models.CharField(max_length=10)
    seats = models.IntegerField()
    category = models.CharField(max_length=20)
    photo = models.CharField(max_length=150)
    owner_id = models.IntegerField()
    
    
    
class Route(models.Model):

    CREATE = 'create'
    FIND = 'find'
    
    ROUTE_CHOICES = (
        (CREATE, 'create'),
        (FIND, 'find'),
        
    )
    
    
    
    routFrom = LocationField(map_attrs={"id": "unique_id_1"})
    routTo = LocationField(map_attrs={"id": "unique_id_2"})
    maxPassenger = models.IntegerField()
    seatsReserved = models.IntegerField()
    user_id = models.ForeignKey(Customer, blank = True, on_delete=models.CASCADE,default = None)   
    vehicle_id = models.IntegerField()
    price = models.CharField(max_length=15)    
    rout_category = models.CharField(max_length=10, choices = ROUTE_CHOICES, default = CREATE)
    departure = models.DateTimeField()
    radius = models.FloatField()
    
    
    


class History(models.Model):
     # Constants in Model class
    COMLPETED = 'completed'
    PENDING = 'pending'
    
    STATUS_CHOICES = (
        (COMLPETED, 'completed'),
        (PENDING, 'pending'),
        
    )

    
    user_id = models.IntegerField()
    route_id = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
        
        
    
        
    
class Category(models.Model):
    
    category_name = models.CharField(max_length=20)
    
    


