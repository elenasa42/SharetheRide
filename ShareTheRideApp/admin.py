from django.contrib import admin
from django.contrib.auth.models import User

from mapbox_location_field.admin import MapAdmin  
# Register your models here.

from .models import Customer,Route,Vehicle,History,Category


admin.site.register(Customer)
admin.site.register(Route,MapAdmin)
admin.site.register(Vehicle)
admin.site.register(History)
admin.site.register(Category)

