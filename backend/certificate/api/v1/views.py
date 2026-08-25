from django.http import FileResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from certificate.models import Certificate, IssuedCertificate
from certificate.pdf import generate_certificate_pdf
from core_auth.permissions import IsSuperUserOrReadOnly
from . import serializers

@extend_schema_view(
    list=extend_schema(tags=["Certificates"], summary="List all certificates"),
    retrieve=extend_schema(tags=["Certificates"], summary="Retrieve a specific certificate"),
    create=extend_schema(tags=["Certificates"], summary="Create a certificate (Admin only)"),
    update=extend_schema(tags=["Certificates"], summary="Update a certificate (Admin only)"),
    partial_update=extend_schema(tags=["Certificates"], summary="Partially update a certificate (Admin only)"),
    destroy=extend_schema(tags=["Certificates"], summary="Delete a certificate (Admin only)"),
)
class CertificateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Certificate.objects.all()
        return Certificate.objects.filter(draft=False)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return serializers.AdminCertificateSerializer
        return serializers.PublicCertificateSerializer


@extend_schema_view(
    list=extend_schema(tags=["Certificates"], summary="List issued certificates"),
    retrieve=extend_schema(tags=["Certificates"], summary="Retrieve an issued certificate"),
    create=extend_schema(tags=["Certificates"], summary="Issue a certificate to a user (Admin only)"),
    update=extend_schema(tags=["Certificates"], summary="Update an issued certificate (Admin only)"),
    partial_update=extend_schema(tags=["Certificates"], summary="Partially update an issued certificate (Admin only)"),
    destroy=extend_schema(tags=["Certificates"], summary="Revoke an issued certificate (Admin only)"),
)
class IssuedCertificateViewSet(viewsets.ModelViewSet):
    """
    Issued certificates management.

    Superusers can issue, update, revoke and view every issued certificate.
    Regular users can only list/retrieve certificates issued to themselves.
    """
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return IssuedCertificate.objects.select_related('certificate', 'user').all().order_by('-issued_at')
        return IssuedCertificate.objects.filter(user=self.request.user).select_related('certificate', 'user').order_by('-issued_at')

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return serializers.AdminIssuedCertificateSerializer
        return serializers.IssuedCertificateSerializer

    @extend_schema(tags=["Certificates"], summary="List my issued certificates")
    @action(detail=False, methods=['get'], url_path='my')
    def my(self, request):
        """Certificates issued to the logged-in user (applies to superusers too)."""
        queryset = IssuedCertificate.objects.filter(user=request.user).select_related('certificate', 'user').order_by('-issued_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["Certificates"],
        summary="Download an issued certificate as PDF",
        responses={(200, "application/pdf"): OpenApiTypes.BINARY},
    )
    @action(detail=True, methods=['get'], url_path='pdf')
    def pdf(self, request, pk=None):
        """Stream the generated PDF for an issued certificate (owner or admin)."""
        issued = self.get_object()
        buffer = generate_certificate_pdf(issued)
        filename = f"certificate-{issued.verification_code}.pdf"
        return FileResponse(buffer, as_attachment=True, filename=filename, content_type="application/pdf")
