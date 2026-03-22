from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConfigTypeViewSet

router = DefaultRouter()
router.register(r'types', ConfigTypeViewSet, basename='configtype')

urlpatterns = [
    path('', include(router.urls)),
]
