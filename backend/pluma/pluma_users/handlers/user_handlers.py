from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet, mixins
from pluma_users.models import User
from pluma_users.serializers.user_serializers import UserSerializer


class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ListUsers(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
