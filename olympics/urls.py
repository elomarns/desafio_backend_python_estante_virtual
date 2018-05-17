from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import CompetitionViewSet, ResultDetail, CreateResult

router = DefaultRouter()
router.register(r'competitions', CompetitionViewSet)

urlpatterns = [
  re_path(r'^', include(router.urls)),
  path("results/", CreateResult.as_view()),
  path("results/<int:pk>/", ResultDetail.as_view())
]
