from django.contrib import admin
from django.urls import path, include
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

    # Other endpoints
    path('api/v1/auth/', include("core_auth.api.v1.urls")),
    path('api/v1/ticket/', include("ticket.api.v1.urls")),
    path('api/v1/course/', include("course.api.v1.urls")),
    path('api/v1/quiz/', include("quiz.api.v1.urls")),
    path('api/v1/certificate/', include("certificate.api.v1.urls")),
]
