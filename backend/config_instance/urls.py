from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConfigInstanceViewSet

router = DefaultRouter()
router.register(r'instances', ConfigInstanceViewSet, basename='configinstance')

urlpatterns = [
    path('', include(router.urls)),
]
