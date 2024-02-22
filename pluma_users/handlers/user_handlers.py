from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.viewsets import GenericViewSet, mixins
from pluma_users.models import User
from pluma_users.serializers.user_serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class LoginUser(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


class RetrieveUser(APIView):
    def get(self, request):
        user_data = User.objects.values("name", "username", "email", "id").get(
            email=request.user
        )
        return Response(
            {
                "id": user_data["id"],
                "name": user_data["name"],
                "username": user_data["username"],
                "email": user_data["email"],
            }
        )


class UpdateUser(mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        print(self.kwargs)
        user = User.objects.values("id").get(email=request.user)
        if str(user["id"]) == self.kwargs["pk"]:
            return super().update(request, *args, **kwargs)
        else:
            return Response(
                {"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def get_queryset(self):
        return User.objects.all()


class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(email=request.data["email"])
        token = get_tokens_for_user(user)
        user_values = {
            "username": user.username,
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }
        token.update(user_values)
        return Response(token)


class ListUsers(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
