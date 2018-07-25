from rest_framework import serializers

from restapi.models import Creator, Prezi


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = '__all__'


class PreziSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer(read_only=True)

    class Meta:
        model = Prezi
        fields = '__all__'
