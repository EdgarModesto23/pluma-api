from rest_framework import viewsets
from pluma.pluma_app.serializers.board_serializers import boardSerializer
from pluma_app.models import Board


class boardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = boardSerializer
