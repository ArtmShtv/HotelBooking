from django.urls import path

from hotel import views


urlpatterns = [
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
        "country/delete/<int:pk>/",
        views.CountryDeleteAPIView.as_view(),
        name="country_delete",
    ),
    path(
        "country/<int:country_id>/region/",
        views.RegionListAPIView.as_view(),
        name="region_list",
    ),
    path("region/create/", views.RegionCreateAPIView.as_view(), name="region_create"),
    path(
        "region/update/<int:region_id>/",
        views.RegionUpdateAPIView.as_view(),
        name="region_update",
    ),
    path(
        "region/delete/<int:region_id>/",
        views.RegionDeleteAPIView.as_view(),
        name="region_delete",
    ),
]
