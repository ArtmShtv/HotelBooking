from django.contrib import admin
from django.urls import include
from django.urls import path

from hotel import urls as hotel_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v0/hotel/", include(hotel_urls)),
]
