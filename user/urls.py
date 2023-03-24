from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserDataViewSet, FileUploadViewSet

router = DefaultRouter()
router.register("users", UserDataViewSet, basename="user")
router.register("file-upload", FileUploadViewSet, basename="file-upload")

urlpatterns = [
    path("", include(router.urls)),
]
