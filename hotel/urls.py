from django.urls import path

from hotel import views


urlpatterns = [
    # Address enpoints
    path("address/", views.AddressListAPIView.as_view(), name="address_list"),
    path(
        "address/<int:pk>/",
        views.AddressRetrieveAPIView.as_view(),
        name="retrieve_address",
    ),
    path(
        "address/create/", views.AddressCreateAPIView.as_view(), name="address_create"
    ),
    path(
        "address/update/<int:pk>/",
        views.AddressUpdateAPIView.as_view(),
        name="address_update",
    ),
    path(
        "address/delete/<int:pk>/",
        views.AddressDeleteAPIView.as_view(),
        name="address_delete",
    ),
    # Country enpoints
    path("country/", views.CountryAPIView.as_view(), name="hotel-country"),
    path(
        "country/<int:country_id>/",
        views.CountryDetailAPIView.as_view(),
        name="hotel-country-detail",
    ),
    # Region enpoints
    path(
        "country/<int:country_id>/regions/",
        views.RegionAPIView.as_view(),
        name="hotel-region",
    ),
    path("region/<int:region_id>/", views.RegionAPIView.as_view(), name="hotel-region-detail"),
    # City enpoints
    path(
        "region/<int:region_id>/city/", views.CityAPIView.as_view(), name="hotel-city"
    ),
    path(
        "city/<int:city_id>/",
        views.CityDetailAPIView.as_view(),
        name="hotel-city-detail",
    ),
]
