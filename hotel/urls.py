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
    path("country/", views.CountryListAPIView.as_view(), name="country_list"),
    path(
        "country/create/", views.CountryCreateAPIView.as_view(), name="country_create"
    ),
    path(
        "country/update/<int:pk>/",
        views.CountryUpdateAPIView.as_view(),
        name="country_update",
    ),
    path(
        "country/delete/",
        views.CountryDeleteAPIView.as_view(),
        name="country_delete",
    ),

    # Region enpoints
    path(
        "country/<int:country_id>/region/",
        views.RegionListAPIView.as_view(),
        name="region_list",
    ),
    path("country/<int:country_id>/region/create/", 
        views.RegionCreateAPIView.as_view(),
        name="region_create"
    ),
    path(
        "country/<int:country_id>/region/update/<int:region_id>/",
        views.RegionUpdateAPIView.as_view(),
        name="region_update",
    ),
    path(
        "country/<int:country_id>/region/delete/",
        views.RegionDeleteAPIView.as_view(),
        name="region_delete",
    ),

    # City enpoints
    path(
        "country/<int:country_id>/region/<int:region_id>/city/",
        views.CityListAPIView.as_view(),
        name="city_list",
    ),
    path(
        "country/<int:country_id>/region/<int:region_id>/city/create/", 
        views.CityCreateAPIView.as_view(), 
        name="city_create"
    ),
    path(
        "country/<int:country_id>/region/<int:region_id>/city/update/<int:city_id>/",
        views.CityUpdateAPIView.as_view(),
        name="city_update",
    ),
    path(
        "country/<int:country_id>/region/<int:region_id>/city/delete/",
        views.CityDeleteAPIView.as_view(),
        name="city_delete",
    ),
]
