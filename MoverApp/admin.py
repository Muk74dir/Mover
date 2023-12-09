from django.contrib import admin
from .models import PersonModel, AddressModel, VehicleModel, TripModel, PaymentGatewaySettingsModel

@admin.register(PersonModel)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'dob', 'status', 'account_type', 'image', 'dob', 'rating', 'date_created', 'date_modified')
    list_filter = ('status', 'account_type', 'date_created', 'date_modified')
    
    def __str__(self):
        return self.username

@admin.register(AddressModel)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('person', 'address_line', 'city', 'state', 'zipcode', 'country')
    list_filter = ('person', 'city', 'state', 'zipcode', 'country')
    
    def __str__(self):
        return self.person.username
    
@admin.register(VehicleModel)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('driver', 'type', 'model', 'license_no', 'color')
    list_filter = ('driver', 'type', 'model', 'license_no', 'color')
    
    def __str__(self):
        return self.driver.username
    
@admin.register(TripModel)
class TripAdmin(admin.ModelAdmin):
    def __str__(self):
        return f"{self.passenger.username} --> {self.driver.username}"
    
    
@admin.register(PaymentGatewaySettingsModel)
class PaymentGatewaySettingsAdmin(admin.ModelAdmin):
    
    def __str__(self):
        return self.person.username