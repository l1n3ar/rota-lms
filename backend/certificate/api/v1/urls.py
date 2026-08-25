from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CertificateViewSet, IssuedCertificateViewSet

router = DefaultRouter()
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'issued', IssuedCertificateViewSet, basename='issued-certificate')

urlpatterns = [
    path('', include(router.urls)),
]
