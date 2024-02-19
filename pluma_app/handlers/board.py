from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import status
from rest_framework.response import Response
from pluma_users.models import User
import pluma_app.serializers.board_serializers as serializers
from pluma_app.models import Board
from rest_framework import permissions


class boardViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.boardSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related("note_board", "allowed_users").filter(
            allowed_users__email=self.request.user
        )

    def create(self, request, *args, **kwargs):
        user = User.objects.get(email=self.request.user)
        data = request.data
        data["creator"] = user.id
        data["allowed_users"] = [user.id]
        print(data)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.retrieveBoardSerializer(instance)
        return Response(serializer.data)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        url_path="users",
        url_name="users",
    )
    def add_allowed_user(self, request, pk):
        serializer = serializers.AllowedUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.data)
        print(data)
        try:
            board = Board.objects.prefetch_related("allowed_users").get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "board does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            user = User.objects.get(email=data["email"])
        except ObjectDoesNotExist:
            return Response(
                {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        if data["action"] == "add":
            board.allowed_users.add(user)
            return Response(
                {"data": "User added to board succesfully"}, status=status.HTTP_200_OK
            )
        elif data["action"] == "del":
            if board.allowed_users.filter(pk=user.id).exists():
                board.allowed_users.remove(user)
                return Response(
                    {"data": "User removed from board succesfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "User is not in the board"},
                    status=status.HTTP_404_NOT_FOUND,
                )
