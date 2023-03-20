from django.urls import path, include
from .views import CompetitorViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'all', CompetitorViewSet, basename='competitor')
urlpatterns = router.urls