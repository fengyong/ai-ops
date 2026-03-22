from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConfigVersionViewSet

router = DefaultRouter()
router.register(r'versions', ConfigVersionViewSet, basename='configversion')

urlpatterns = [
    path('', include(router.urls)),
]
