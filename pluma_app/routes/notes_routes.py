from pluma_app.handlers.notes import NoteViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r"", NoteViewSet, basename="note")


urlpatterns = router.urls
