from django.urls import path
import pluma_users.handlers.user_handlers as handlers


urlpatterns = [
    path(r"register/", handlers.RegisterUser.as_view()),
    path(r"list", handlers.ListUsers.as_view({"get": "list"})),
]
