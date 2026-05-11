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
    country_1, country_2, country_3 = country_data
    url = reverse("hotel-country")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[0] == {
        "id": country_1.id,
        "iso_code": "AA",
        "name": "Country 1",
    }


@pytest.mark.django_db
def test_create_single_country(authenticated_admin_client):
    url = reverse("hotel-country")
    payload = [{"iso_code": "DE", "name": "Germany"}]
    response = authenticated_admin_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert Country.objects.filter(iso_code="DE").exists()


@pytest.mark.django_db
def test_create_multiple_countries(authenticated_admin_client):
    url = reverse("hotel-country")
    payload = [
        {"iso_code": "DE", "name": "Germany"},
        {"iso_code": "FR", "name": "France"},
    ]
    response = authenticated_admin_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert Country.objects.count() == 2


@pytest.mark.django_db
def test_create_country_accepts_single_dict(authenticated_admin_client):
    """Test that a single dict (not list) is also accepted"""
    url = reverse("hotel-country")
    payload = {"iso_code": "DE", "name": "Germany"}
    response = authenticated_admin_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert Country.objects.filter(iso_code="DE").exists()


@pytest.mark.django_db
def test_create_country_skips_duplicate_iso_code(authenticated_admin_client):
    """Duplicate iso_code in DB should be silently skipped"""
    Country.objects.create(iso_code="DE", name="Germany")
    url = reverse("hotel-country")
    payload = [{"iso_code": "DE", "name": "Germany New"}]
    response = authenticated_admin_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert Country.objects.count() == 1


@pytest.mark.django_db
def test_create_country_skips_duplicate_within_payload(authenticated_admin_client):
    """Duplicates within the same payload should be deduplicated"""
    url = reverse("hotel-country")
    payload = [
        {"iso_code": "DE", "name": "Germany"},
        {"iso_code": "DE", "name": "Germany"},
    ]
    response = authenticated_admin_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert Country.objects.count() == 1


@pytest.mark.django_db
def test_create_country_invalid_payload(authenticated_admin_client):
    """Missing required fields should return 400"""
    url = reverse("hotel-country")
    payload = [{"iso_code": "DE"}]
    response = authenticated_admin_client.post(url, payload, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_as_regular_user(authenticated_client):
    """Regular user should get 403"""
    url = reverse("hotel-country")
    payload = [{"iso_code": "DE", "name": "Germany"}]
    response = authenticated_client.post(url, payload, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_as_unauthorized_user(api_client):
    """Unauthenticated request should get 403"""
    url = reverse("hotel-country")
    payload = [{"iso_code": "DE", "name": "Germany"}]
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_patch_country(authenticated_admin_client, country_data):
    country_1, _, _ = country_data
    url = reverse("hotel-country-detail", kwargs={"country_id": country_1.id})
    payload = {"iso_code": "XX", "name": "Updated"}
    response = authenticated_admin_client.patch(url, payload, format="json")
    assert response.status_code == 200
    country_1.refresh_from_db()
    assert country_1.iso_code == "XX"
    assert country_1.name == "Updated"


@pytest.mark.django_db
def test_patch_country_partial(authenticated_admin_client, country_data):
    country_1, _, _ = country_data
    url = reverse("hotel-country-detail", kwargs={"country_id": country_1.id})
    response = authenticated_admin_client.patch(
        url, {"name": "Only Name"}, format="json"
    )
    assert response.status_code == 200
    country_1.refresh_from_db()
    assert country_1.name == "Only Name"
    assert country_1.iso_code == "AA"


@pytest.mark.django_db
def test_patch_country_not_found(authenticated_admin_client):
    url = reverse("hotel-country-detail", kwargs={"country_id": 99999})
    response = authenticated_admin_client.patch(url, {"name": "X"}, format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_patch_country_as_regular_user(authenticated_client, country_data):
    country_1, _, _ = country_data
    url = reverse("hotel-country-detail", kwargs={"country_id": country_1.id})
    response = authenticated_client.patch(url, {"name": "Hacked"}, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_patch_country_as_unauthenticated(api_client, country_data):
    country_1, _, _ = country_data
    url = reverse("hotel-country-detail", kwargs={"country_id": country_1.id})
    response = api_client.patch(url, {"name": "Hacked"}, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_country(authenticated_admin_client, country_data):
    country_1, _, _ = country_data
    url = reverse("hotel-country-detail", kwargs={"country_id": country_1.id})
    response = authenticated_admin_client.delete(url)
    assert response.status_code == 204
    assert not Country.objects.filter(id=country_1.id).exists()


@pytest.mark.django_db
def test_delete_country_not_found(authenticated_admin_client):
    url = reverse("hotel-country-detail", kwargs={"country_id": 99999})
    response = authenticated_admin_client.delete(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_country_as_regular_user(authenticated_client, country_data):
    country_1, _, _ = country_data
    url = reverse("hotel-country-detail", kwargs={"country_id": country_1.id})
    response = authenticated_client.delete(url)
    assert response.status_code == 403
    assert Country.objects.filter(id=country_1.id).exists()


@pytest.mark.django_db
def test_delete_country_as_unauthenticated(api_client, country_data):
    country_1, _, _ = country_data
    url = reverse("hotel-country-detail", kwargs={"country_id": country_1.id})
    response = api_client.delete(url)
    assert response.status_code == 403
    assert Country.objects.filter(id=country_1.id).exists()
