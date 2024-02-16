from typing import Type
from rest_framework import viewsets
from rest_framework.response import Response
from pluma_users.models import User
from pluma_app.serializers.board_serializers import boardSerializer
from pluma_app.models import Board
from django.conf import settings


class boardViewSet(viewsets.ModelViewSet):
    serializer_class = boardSerializer

    def get_queryset(self):
        print(self.request.user)
        return Board.objects.prefetch_related("allowed_users").filter(
            allowed_users__email=self.request.user
        )

    def create(self, request, *args, **kwargs):
        user = User.objects.get(email=self.request.user)
        data = request.data
        data["creator"] = user.id
        if "allowed_users" not in data.keys():
            data["allowed_users"] = [user.id]
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
