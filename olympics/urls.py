from rest_framework.routers import DefaultRouter
from .views import CompetitionViewSet

router = DefaultRouter()
router.register(r'competitions', CompetitionViewSet)
urlpatterns = router.urls
