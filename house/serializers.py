from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from house.models import DataHouse, Signer


class DataHouseSerializer(ModelSerializer):
    owner = serializers.StringRelatedField()  # Позволяет записывать имя не как int, а как строку

    class Meta:
        model = DataHouse
        fields = '__all__'


class OwnerSerializer(ModelSerializer):
    owner_name = serializers.StringRelatedField()

    class Meta:
        model = Signer
        fields = ('owner_name',)
