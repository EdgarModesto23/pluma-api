from rest_framework import serializers
from pluma_app.models import Board


class boardSerializer(serializers.ModelField):
    class Meta:
        model = Board
        fields = "__all__"
