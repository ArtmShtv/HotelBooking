from django.contrib import admin

from hotel.models import City, Address, Region, Country

admin.site.register(City)
admin.site.register(Address)
admin.site.register(Region)
admin.site.register(Country)
