from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserDataViewSet

router = DefaultRouter()
router.register("users", UserDataViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
