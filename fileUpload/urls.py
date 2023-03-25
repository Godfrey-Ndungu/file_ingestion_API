from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include("user.urls")),
    path("v1/api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "v1/api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "v1/api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
     path('', RedirectView.as_view(url='v1/')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
