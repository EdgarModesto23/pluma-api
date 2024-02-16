from pluma_app.handlers.board import boardViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r"", boardViewSet, basename="board")


urlpatterns = router.urls
