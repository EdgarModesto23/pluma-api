from django.contrib.auth.hashers import receiver
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import status
from rest_framework.response import Response
from pluma_users.models import User
import pluma_app.serializers.board_serializers as serializers
from pluma_app.models import Board
from rest_framework import permissions
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from pluma_users.models import User
from django.conf import settings
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string


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
        try:
            board = Board.objects.prefetch_related("allowed_users").get(id=pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "board does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            user = User.objects.get(email=data["email"])
        except ObjectDoesNotExist:
            self.sendInvite(sender=self.request.user, recipients=data["email"])
            return Response({"message": "Email sent"}, status=status.HTTP_200_OK)

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

    def logo_data(self, path, cid):
        print("hey")
        with open(finders.find(path), "rb") as f:
            logo_data = f.read()
        logo = MIMEImage(logo_data)
        logo.add_header("Content-ID", f"<{cid}>")
        return logo

    def sendInvite(self, sender, recipients) -> bool:
        print("chavalos")
        subject = f"Join {sender} in taking notes on Pluma!"
        message = f"{sender} invited you to join his board on pluma!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipients_list = [recipients]
        html_message = render_to_string(
            "../templates/invite.html", context={"sender": sender}
        )
        message = EmailMultiAlternatives(
            subject=subject, body=message, from_email=from_email, to=recipients_list
        )
        message.attach_alternative(html_message, "text/html")
        message.attach(self.logo_data(path="Pluma.png", cid="Pluma"))
        message.attach(self.logo_data(path="github.png", cid="github"))
        message.send(fail_silently=False)
        print("hey")
        return True
