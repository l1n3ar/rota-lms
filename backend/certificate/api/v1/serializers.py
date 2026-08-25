from django.urls import reverse
from rest_framework import serializers

from certificate.models import Certificate, IssuedCertificate

# ==========================================
# PUBLIC SERIALIZERS (Read-Only & Sanitized)
# ==========================================

class PublicCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        # 'draft' is omitted because the public only ever sees non-drafts anyway
        fields = ['id', 'title', 'description', 'picture']


class IssuedCertificateSerializer(serializers.ModelSerializer):
    certificate = PublicCertificateSerializer(read_only=True)
    user_name = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = IssuedCertificate
        fields = [
            'id', 'certificate', 'user_name', 'score',
            'verification_code', 'issued_at', 'pdf_url',
        ]

    def get_user_name(self, obj):
        name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return name or obj.user.email

    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return request.build_absolute_uri(
            reverse('issued-certificate-pdf', kwargs={'pk': obj.pk})
        )


# ==========================================
# ADMIN SERIALIZERS (Full CRUD, Flat Structure)
# ==========================================

class AdminCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class AdminIssuedCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuedCertificate
        fields = '__all__'
