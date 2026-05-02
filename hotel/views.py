from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from hotel.models import (
    Country, 
    Region, 
    City, 
    Address, 
    Hotel, 
    RoomCategory, 
    Room,
    RoomImage
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


class CountryListAPIView(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField() 
        iso_code = serializers.CharField()
        name = serializers.CharField()

    def get(self, request):
        countrys = Country.objects.all()
        serializer = self.OutputSerializer(countrys, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CountryCreateAPIView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Country
            fields = ['iso_code', 'name']
            extra_kwargs = {
                'iso_code': {'validators': []},
                'name': {'validators': []},
            }

    def post(self, request):
        payload = request.data
        if isinstance(payload, dict):
            payload = [payload]

        serializer = self.InputSerializer(data=payload, many=True)

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data

            existing_iso_codes = set(Country.objects.values_list('iso_code', flat=True))
            existing_names = set(Country.objects.values_list('name', flat=True))

            to_create = []
            seen_iso_codes = set()
            seen_names = set()

            for item in validated_data:
                iso = item['iso_code']
                name = item['name']

                if (iso not in existing_iso_codes and iso not in seen_iso_codes and
                        name not in existing_names and name not in seen_names):
                    to_create.append(Country(**item))
                    seen_iso_codes.add(iso)
                    seen_names.add(name)

            Country.objects.bulk_create(to_create)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CountryUpdateAPIView(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Country
            fields = ["iso_code", "name"]

    def patch(self, request, pk):
        country = get_object_or_404(Country, id=pk)

        serializer = self.InputSerializer(country, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Country attribute updated", status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CountryDeleteAPIView(APIView):
    def delete(self, request, pk):
        #breakpoint()
        country = get_object_or_404(Country, pk=pk)

        country.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)