from os.path import basename
from django.urls import path
import pluma_users.handlers.user_handlers as handlers
from rest_framework import routers

router = routers.SimpleRouter()
router.register("", handlers.UpdateUser, basename="update-user")


urlpatterns = [
    path(r"register/", handlers.RegisterUser.as_view()),
    path(r"list", handlers.ListUsers.as_view({"get": "list"})),
    path(r"get", handlers.RetrieveUser.as_view()),
] + router.urls
