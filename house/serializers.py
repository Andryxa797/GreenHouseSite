from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from house.models import DataHouse


class DataHouseSerializer(ModelSerializer):
    owner = serializers.StringRelatedField()  # Позволяет записывать имя не как int, а как строку

    class Meta:
        model = DataHouse
        fields = '__all__'

