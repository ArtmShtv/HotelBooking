from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from hotel.models import (
    Country,
    Region,
    City,
    Address,
)


class HotelAPIView(APIView):
    class HotelSerializer(serializers.Serializer):
        pass

    def get(self, request):
        return Response("hi")


class AddressListAPIView(APIView):
    class AddressSerializer(serializers.Serializer):
        country = serializers.CharField()
        region = serializers.CharField()
        city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
        street = serializers.CharField()
        house = serializers.CharField()
        building = serializers.CharField(required=False)
        apartment = serializers.CharField(required=False)
        postal_code = serializers.CharField()
        coordinates = serializers.CharField(required=False)

    def get(self, request):
        addresses = Address.objects.all()
        serializer = self.AddressSerializer(addresses, many=True)

        return Response(serializer.data)


class AddressRetrieveAPIView(APIView):
    class AddressSerializer(serializers.Serializer):
        country = serializers.CharField()
        region = serializers.CharField()
        city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
        street = serializers.CharField()
        house = serializers.CharField()
        building = serializers.CharField(required=False)
        apartment = serializers.CharField(required=False)
        postal_code = serializers.CharField()
        coordinates = serializers.CharField(required=False)

    def get(self, request, pk):
        pass


class AddressCreateAPIView(APIView):
    class AddressSerializer(serializers.Serializer):
        country = serializers.CharField()
        region = serializers.CharField()
        city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
        street = serializers.CharField()
        house = serializers.CharField()
        building = serializers.CharField()
        apartment = serializers.CharField()
        postal_code = serializers.CharField()
        longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
        latitude = serializers.DecimalField(max_digits=9, decimal_places=6)

    def post(self, request):
        pass


class AddressUpdateAPIView(APIView):
    class AddressSerializer(serializers.Serializer):
        country = serializers.CharField()
        region = serializers.CharField()
        city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
        street = serializers.CharField()
        house = serializers.CharField()
        building = serializers.CharField()
        apartment = serializers.CharField()
        postal_code = serializers.CharField()
        longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
        latitude = serializers.DecimalField(max_digits=9, decimal_places=6)

    def put(self, request):
        pass


class AddressDeleteAPIView(APIView):
    def delete(self, request, pk):
        pass


class CountryAPIView(APIView):
    class OutputListSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        iso_code = serializers.CharField()
        name = serializers.CharField()

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=OutputListSerializer(many=True),
                description="List of countries",
            ),
        },
        examples=[
            OpenApiExample(
                name="Countries",
                value=[
                    {"id": 1, "iso_code": "DE", "name": "Germany"},
                    {"id": 2, "iso_code": "FR", "name": "France"},
                ],
                response_only=True,
                status_codes=["200"],
            )
        ],
        description="Get list of countries",
        tags=["1. Countries"],
    )
    def get(self, request):
        countries = Country.objects.all()
        serializer = self.OutputSerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    class InputCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Country
            fields = ["iso_code", "name"]
            extra_kwargs = {
                "iso_code": {"validators": []},
                "name": {"validators": []},
            }

    @extend_schema(
        request=InputCreateSerializer(many=True),
        responses={
            201: OpenApiResponse(description="Countries created successfully"),
            400: OpenApiResponse(description="Invalid input"),
        },
        examples=[
            OpenApiExample(
                name="Create single country",
                value=[{"iso_code": "DE", "name": "Germany"}],
                request_only=True,
            ),
            OpenApiExample(
                name="Create multiple countries",
                value=[
                    {"iso_code": "DE", "name": "Germany"},
                    {"iso_code": "FR", "name": "France"},
                ],
                request_only=True,
            ),
        ],
        description="Create one or several countrys",
        tags=["1. Countries"],
    )
    def post(self, request):
        payload = request.data
        if isinstance(payload, dict):
            payload = [payload]

        serializer = self.InputSerializer(data=payload, many=True)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data

            existing_iso_codes = set(Country.objects.values_list("iso_code", flat=True))
            existing_names = set(Country.objects.values_list("name", flat=True))

            to_create = []
            seen_iso_codes = set()
            seen_names = set()

            for item in validated_data:
                iso = item["iso_code"]
                name = item["name"]

                if (
                    iso not in existing_iso_codes
                    and iso not in seen_iso_codes
                    and name not in existing_names
                    and name not in seen_names
                ):
                    to_create.append(Country(**item))
                    seen_iso_codes.add(iso)
                    seen_names.add(name)

            with transaction.atomic():
                Country.objects.bulk_create(to_create)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CountryDetailAPIView(APIView):
    class InputUpdateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Country
            fields = ["iso_code", "name"]

    @extend_schema(
        request=InputUpdateSerializer(),
        responses={
            200: OpenApiResponse(description="Country updated"),
            400: OpenApiResponse(description="Invalid input"),
            404: OpenApiResponse(description="Country not found"),
        },
        examples=[
            OpenApiExample(
                name="Update country",
                value={"iso_code": "DE", "name": "Deutschland"},
                request_only=True,
            )
        ],
        description="Update (Patch) country by its pk",
        tags=["1. Countries"],
    )
    def patch(self, request, pk):
        country = get_object_or_404(Country, id=pk)

        serializer = self.InputSerializer(country, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Country updated", status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={
            204: OpenApiResponse(description="Country deleted"),
            404: OpenApiResponse(description="Country not found"),
        },
        description="Delete country by its pk",
        tags=["1. Countries"],
    )
    def delete(self, request, country_id: int):
        country = get_object_or_404(Country, pk=country_id)

        country.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RegionAPIView(APIView):
    class InputDeleteSerializer(serializers.Serializer):
        regions_id = serializers.ListField()

    @extend_schema(
        responses={
            204: OpenApiResponse(description="Regions deleted"),
            400: OpenApiResponse(description="Invalid input"),
        },
        examples=[
            OpenApiExample(
                name="Delete regions",
                value={"region_ids": [1, 2, 3]},
                request_only=True,
            )
        ],
        description="Delete several regions by its pk",
        tags=["2. Regions"],
    )
    def delete(self, request):
        serializer = self.InputDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Region.objects.filter(id__in=serializer.validated_data["regions_id"]).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegionDetailAPIView(APIView):
    class OutputListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Region
            fields = ["id", "name"]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=OutputListSerializer(many=True),
                description="Regions for a country",
            ),
            404: OpenApiResponse(description="Country not found"),
        },
        examples=[
            OpenApiExample(
                name="Get list of regions",
                value=[
                    {"id": 1, "name": "Bavaria"},
                    {"id": 2, "name": "Berlin"},
                ],
                response_only=True,
                status_codes=["200"],
            )
        ],
        tags=["2. Regions"],
    )
    def get(self, request, country_id: int):
        country = get_object_or_404(Country, id=country_id)
        regions = Region.objects.filter(country=country)

        serializer = self.OutputSerializer(regions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    class InputCreateSerializer(serializers.Serializer):
        regions = serializers.ListField(
            child=serializers.CharField(),
            allow_empty=False,
        )

    @extend_schema(
        request=InputCreateSerializer(),
        responses={
            201: OpenApiResponse(description="Regions created"),
            404: OpenApiResponse(description="Country not found"),
        },
        examples=[
            OpenApiExample(
                name="Create regions for a country",
                value={"regions": ["Some regions", "to", "Create"]},
                request_only=True,
                status_codes=["201"],
            )
        ],
        tags=["2. Regions"],
    )
    def post(self, request, country_id: int):
        country = get_object_or_404(Country, id=country_id)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        region_names = serializer.validated_data["regions"]

        country_regions = set(
            Region.objects.filter(country_id=country_id).values_list("name", flat=True)
        )
        seen_names = set()
        to_create = []

        for name in region_names:
            if name not in country_regions and name not in seen_names:
                to_create.append(Region(name=name, country=country))
                seen_names.add(name)

        with transaction.atomic():
            Region.objects.bulk_create(to_create)

        return Response(status=status.HTTP_201_CREATED)


    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Region
            fields = ["country", "name"]

    @extend_schema(
        request=InputSerializer(),
        responses={
            200: OpenApiResponse(description="Region updated"),
            400: OpenApiResponse(description="Invalid input"),
            404: OpenApiResponse(description="Region not found"),
        },
        examples=[
            OpenApiExample(
                name="Update country",
                value={"country": 1, "name": "Some name"},
                request_only=True,
            )
        ],
        description="Update (Patch) region by its pk",
        tags=["2. Regions"],
    )
    def patch(self, request, region_id: int):
        region = get_object_or_404(Region, id=region_id)

        serializer = self.InputSerializer(region, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class CityDetailAPIView(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = City
            fields = ["id", "name"]

    @extend_schema(
        responses={200: OpenApiResponse(description="Get list of cities for region")},
        examples=[
            OpenApiExample(
                name="Get list of cities for region",
                value={
                    "id": 1,
                    "name": "Some city",
                },
            )
        ],
    )
    def get(self, request, region_id: int):
        region = get_object_or_404(Region, id=region_id)
        cities = City.objects.filter(region=region)
        serializer = self.OutputSerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    class InputCreateSerializer(serializers.ModelSerializer):
        cities_names = serializers.ListField()

        class Meta:
            model = City
            fields = ["cities_names"]

    @extend_schema(request=InputCreateSerializer())
    def post(self, request, region_id: int):
        payload = request.data
        if isinstance(payload, dict):
            payload = [payload]

        serializer = self.InputSerializer(data=payload, many=True)
        serializer.is_valid(raise_exception=True)
        to_create = []

        for item in payload:
            region = get_object_or_404(Region, id=item["region"])
            cities_names = item["cities_names"]
            existing_region_cities = set(
                City.objects.filter(region=region).values_list("name", flat=True)
            )

            seen_names = set()

            for city_name in cities_names:
                if (
                    city_name not in seen_names
                    and city_name not in existing_region_cities
                ):
                    to_create.append(City(region=region, name=city_name))
                    seen_names.add(city_name)

        with transaction.atomic():
            City.objects.bulk_create(to_create)
        return Response(status=status.HTTP_201_CREATED)

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = City
            fields = ["region", "name"]

    def patch(self, request, city_id: int):
        city = get_object_or_404(City, id=city_id)

        serializer = self.InputSerializer(city, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class CityAPIView(APIView):
    class InputSerializer(serializers.Serializer):
        cities_id = serializers.ListField()

    def delete(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid()
        City.objects.filter(id__in=serializer.validated_data["cities_id"]).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
