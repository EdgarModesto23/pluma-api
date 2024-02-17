from rest_framework import serializers
from pluma_users.models import User
from pluma_app.models import Board
from .note_serializers import NoteSerializer


class EmailUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class boardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"

    creator = EmailUser(many=False)
    allowed_users = EmailUser(many=True, read_only=True)


class retrieveBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "title", "public", "creator", "allowed_users", "note_board"]

    allowed_users = EmailUser(many=True, read_only=True)
    note_board = NoteSerializer(many=True, read_only=True)


class AllowedUserSerializer(serializers.Serializer):
    ADD = "add"
    DELETE = "del"
    actions = [
        (ADD, "Add an allowed user to board"),
        (DELETE, "Remove an allowed user from board"),
    ]
    email = serializers.EmailField()
    action = serializers.ChoiceField(choices=actions)
