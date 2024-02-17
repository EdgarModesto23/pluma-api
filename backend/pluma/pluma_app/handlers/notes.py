from rest_framework import viewsets
from pluma_users.models import User
from pluma_app.models import Note, Board

from pluma_app.serializers.note_serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer

    def get_queryset(self):
        data = self.request.data
        return Note.objects.select_related("board", "creator").filter(
            board=data["board"]
        )

    def get_serializer_context(self):
        return {"creator": self.request.user}

    def create(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user)
        request.data["creator"] = user.id
        print(request.data)

        return super().create(request, *args, **kwargs)
