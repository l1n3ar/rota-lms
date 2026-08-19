from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. This endpoint generates the raw OpenAPI schema (JSON/YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # 2. Swagger UI endpoint
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # 3. ReDoc UI endpoint (Optional alternative to Swagger)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
