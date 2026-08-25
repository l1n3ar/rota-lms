from django.contrib import admin

from certificate.models import Certificate, IssuedCertificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "draft", "created_at", "updated_at")
    list_filter = ("draft",)


@admin.register(IssuedCertificate)
class IssuedCertificateAdmin(admin.ModelAdmin):
    list_display = ("certificate", "user", "score", "verification_code", "issued_at")
    list_filter = ("certificate",)
    search_fields = ("user__email", "user__first_name", "user__last_name", "verification_code")
    readonly_fields = ("verification_code", "issued_at")
