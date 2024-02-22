from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from pluma_users.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({"username": self.user.username})
        data.update({"id": self.user.id})
        data.update({"name": self.user.first_name})
        data.update({"email": self.user.email})
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "username", "email", "password", "id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
