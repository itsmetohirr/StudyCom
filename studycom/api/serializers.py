from rest_framework.serializers import ModelSerializer
from studycom.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomDetailSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
