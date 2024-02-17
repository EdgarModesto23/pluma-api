from rest_framework import serializers
from pluma_users.models import User
from pluma_app.models import Note


class EmailUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        extra_kwargs = {"board": {"write_only": True}}
