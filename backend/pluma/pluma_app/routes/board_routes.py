from pluma.pluma_app.handlers.board import boardViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"", boardViewSet)


urlpatterns = router.urls
