import pytest
from django.urls import reverse

from hotel.models import Country


@pytest.fixture
def country_data(db):
    country_1 = Country.objects.create(iso_code="AA", name="Country 1")
    country_2 = Country.objects.create(iso_code="BB", name="Country 2")
    country_3 = Country.objects.create(iso_code="CC", name="Country 3")

    return country_1, country_2, country_3


@pytest.mark.django_db
def test_list_country(api_client, country_data):
    url = reverse("hotel-country")
    response = api_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, list)