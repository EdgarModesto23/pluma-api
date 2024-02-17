import uuid
from django.db import models
from django.conf import settings


class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    public = models.BooleanField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="board_creator"
    )
    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="board_users"
    )


class Note(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    color = models.CharField(max_length=7, default="#FFFFFF")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="note_creator"
    )
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="note_board"
    )
