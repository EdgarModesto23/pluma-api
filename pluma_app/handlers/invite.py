from typing import List
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, parser_classes
from rest_framework.mixins import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from pluma_users.models import User
from django.conf import settings
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders


def logo_data(path, cid):
    with open(finders.find(path), "rb") as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header("Content-ID", f"<{cid}>")
    return logo


@api_view(["POST"])
@parser_classes([JSONParser])
def invite_user(request):
    validator = EmailValidator(message="You must provide a valid email")
    data = dict(request.data)
    user = User.objects.get(email=request.user)
    data["sender"] = user.username
    if "receivers" in data.keys():
        for receiver in data["receivers"]:
            try:
                validator(receiver)
            except ValidationError as validation_err:
                return Response(
                    {"error": validation_err},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if sendInvite(sender=user.username, recipients=data["receivers"]):
            return Response({"message": "Email sent"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Something went wrong while sending the invite"},
                status=status.HTTP_409_CONFLICT,
            )

    else:
        return Response(
            {"error": "You must provide a valid sequence of emails to invite"},
            status=status.HTTP_400_BAD_REQUEST,
        )


def sendInvite(sender: str, recipients: List) -> bool:
    subject = f"Join {sender} in taking notes on Pluma!"
    message = f"{sender} invited you to join his board on pluma!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients_list = [email for email in recipients]
    html_message = render_to_string(
        "../templates/invite.html", context={"sender": sender}
    )
    message = EmailMultiAlternatives(
        subject=subject, body=message, from_email=from_email, to=recipients_list
    )
    message.attach_alternative(html_message, "text/html")
    message.attach(logo_data(path="Pluma.png", cid="Pluma"))
    message.attach(logo_data(path="github.png", cid="github"))
    message.send(fail_silently=False)
    return True
