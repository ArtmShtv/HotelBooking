from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from decimal import Decimal

User = get_user_model()


class Country(models.Model):
    iso_code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="country_regions")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="region_cities")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Address(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="country_addresses")
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="region_addresses")
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="city_addresses")

    street = models.CharField(max_length=255)
    house = models.CharField(max_length=50)
    building = models.CharField(max_length=50, null=True, blank=True)
    apartment = models.CharField(max_length=50, null=True, blank=True)

    postal_code = models.CharField(max_length=20)

    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    @property
    def coordinates(self) -> tuple[Decimal, Decimal]:
        return (self.longitude, self.latitude)
    
    def __str__(self):
        parts = [
            str(self.country),
            str(self.region),
            str(self.city),
            f"{self.street} {self.house}",
        ]

        if self.building:
            parts.append(self.building)
        if self.apartment:
            parts.append(self.apartment)

        parts.append(self.postal_code)

        return ", ".join(parts)


class Hotel(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    address = models.ForeignKey(to=Address, on_delete=models.PROTECT)

    description = models.TextField(
        blank=True,
        default="No description"
    )
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.address.city})"


class RoomCategory(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="room_categories"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    capacity = models.IntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("hotel", "name")

    def __str__(self):
        return f"{self.hotel.name} — category: {self.name}"


class Room(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.PROTECT,
        related_name="rooms"
    )

    room_number = models.CharField(max_length=20)
    category = models.ForeignKey(
        RoomCategory,
        on_delete=models.PROTECT,
        related_name="rooms"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ("hotel", "room_number")

    def clean(self):
        if self.category.hotel_id != self.hotel_id:
            raise ValidationError("Category must belong to the same hotel")

    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_number}"


class RoomImage(models.Model):
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE, related_name="images")

    image = models.ImageField(upload_to='rooms/')

    order = models.IntegerField(default=0)
    is_main = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
