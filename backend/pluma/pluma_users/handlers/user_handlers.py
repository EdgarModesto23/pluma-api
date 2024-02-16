from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from pluma_users.serializers.user_serializers import CreateUser


class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CreateUser(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
