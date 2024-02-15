from django.db import models
from django.conf import settings


class Board(models.Model):
    title = models.CharField(max_length=150)
    public = models.BooleanField()
    creator = models.IntegerField()


class Note(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    color = models.CharField(max_length=7)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="note_creator"
    )
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="note_board"
    )


class Allowed_Users(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="allowed_user"
    )
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="allowed_board"
    )
