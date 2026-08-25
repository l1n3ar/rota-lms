from django.test import TestCase
from rest_framework.test import APIClient

from certificate.models import Certificate, IssuedCertificate
from core_auth.models import User


class CertificateViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="student@example.com")
        self.superuser = User.objects.create_user(
            email="admin@example.com",
            is_staff=True,
            is_superuser=True,
        )

        self.published = Certificate.objects.create(title="Published Certificate", draft=False)
        self.draft = Certificate.objects.create(title="Draft Certificate", draft=True)

    def test_anonymous_cannot_list_certificates(self):
        response = self.client.get("/api/v1/certificate/certificates/")
        self.assertEqual(response.status_code, 401)

    def test_regular_user_sees_only_published_certificates(self):
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/v1/certificate/certificates/")

        self.assertEqual(response.status_code, 200)
        titles = [c["title"] for c in response.data["results"]]
        self.assertIn("Published Certificate", titles)
        self.assertNotIn("Draft Certificate", titles)

    def test_public_serializer_hides_draft_flag(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f"/api/v1/certificate/certificates/{self.published.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("draft", response.data)

    def test_admin_sees_everything(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.get("/api/v1/certificate/certificates/")

        self.assertEqual(response.status_code, 200)
        titles = [c["title"] for c in response.data["results"]]
        self.assertIn("Published Certificate", titles)
        self.assertIn("Draft Certificate", titles)

        detail_response = self.client.get(f"/api/v1/certificate/certificates/{self.published.id}/")
        self.assertIn("draft", detail_response.data)

    def test_regular_user_cannot_create_certificate(self):
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/v1/certificate/certificates/", {"title": "Nope"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_create_certificate(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.post("/api/v1/certificate/certificates/", {"title": "New Certificate"}, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Certificate.objects.filter(title="New Certificate").exists())

    def test_superuser_can_delete_certificate(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.delete(f"/api/v1/certificate/certificates/{self.published.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Certificate.objects.filter(id=self.published.id).exists())


class IssuedCertificateViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="student@example.com", first_name="Ali", last_name="Rezaei"
        )
        self.other_user = User.objects.create_user(email="other@example.com")
        self.superuser = User.objects.create_user(
            email="admin@example.com",
            is_staff=True,
            is_superuser=True,
        )

        self.certificate = Certificate.objects.create(title="Python Basics", draft=False)
        self.issued = IssuedCertificate.objects.create(
            certificate=self.certificate, user=self.user, score=85
        )
        self.other_issued = IssuedCertificate.objects.create(
            certificate=self.certificate, user=self.other_user
        )

    def test_anonymous_cannot_list_issued_certificates(self):
        response = self.client.get("/api/v1/certificate/issued/")
        self.assertEqual(response.status_code, 401)

    def test_regular_user_sees_only_their_own_issued_certificates(self):
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/v1/certificate/issued/")

        self.assertEqual(response.status_code, 200)
        codes = [c["verification_code"] for c in response.data["results"]]
        self.assertIn(self.issued.verification_code, codes)
        self.assertNotIn(self.other_issued.verification_code, codes)

    def test_admin_sees_all_issued_certificates(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.get("/api/v1/certificate/issued/")

        self.assertEqual(response.status_code, 200)
        codes = [c["verification_code"] for c in response.data["results"]]
        self.assertIn(self.issued.verification_code, codes)
        self.assertIn(self.other_issued.verification_code, codes)

    def test_public_serializer_includes_user_name_and_pdf_url(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f"/api/v1/certificate/issued/{self.issued.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user_name"], "Ali Rezaei")
        self.assertEqual(response.data["certificate"]["title"], "Python Basics")
        self.assertTrue(
            response.data["pdf_url"].endswith(f"/api/v1/certificate/issued/{self.issued.id}/pdf/")
        )

    def test_my_endpoint_returns_own_certificates_even_for_superuser(self):
        # Even a superuser's "my" list only contains certificates issued to them
        IssuedCertificate.objects.create(certificate=self.certificate, user=self.superuser)

        self.client.force_authenticate(self.superuser)
        response = self.client.get("/api/v1/certificate/issued/my/")

        self.assertEqual(response.status_code, 200)
        codes = [c["verification_code"] for c in response.data["results"]]
        self.assertEqual(len(codes), 1)

    def test_regular_user_cannot_issue_certificate(self):
        self.client.force_authenticate(self.user)
        other_certificate = Certificate.objects.create(title="Django Advanced", draft=False)
        response = self.client.post(
            "/api/v1/certificate/issued/",
            {"certificate": other_certificate.id, "user": str(self.other_user.id)},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_issue_certificate(self):
        self.client.force_authenticate(self.superuser)
        other_certificate = Certificate.objects.create(title="Django Advanced", draft=False)
        response = self.client.post(
            "/api/v1/certificate/issued/",
            {"certificate": other_certificate.id, "user": str(self.other_user.id), "score": 90},
            format="json",
        )

        self.assertEqual(response.status_code, 201, response.data)
        issued = IssuedCertificate.objects.get(certificate=other_certificate, user=self.other_user)
        self.assertEqual(issued.score, 90)
        self.assertTrue(issued.verification_code)

    def test_superuser_can_revoke_certificate(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.delete(f"/api/v1/certificate/issued/{self.issued.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(IssuedCertificate.objects.filter(id=self.issued.id).exists())


class CertificatePdfTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="student@example.com", first_name="Ali", last_name="Rezaei")
        self.other_user = User.objects.create_user(email="other@example.com")
        self.superuser = User.objects.create_user(
            email="admin@example.com",
            is_staff=True,
            is_superuser=True,
        )

        self.certificate = Certificate.objects.create(title="Python Basics", draft=False)
        self.issued = IssuedCertificate.objects.create(
            certificate=self.certificate, user=self.user, score=85
        )

    def test_owner_can_download_pdf(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f"/api/v1/certificate/issued/{self.issued.id}/pdf/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn(
            f'attachment; filename="certificate-{self.issued.verification_code}.pdf"',
            response["Content-Disposition"],
        )

        content = b"".join(response.streaming_content)
        self.assertTrue(content.startswith(b"%PDF"))

    def test_superuser_can_download_any_pdf(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.get(f"/api/v1/certificate/issued/{self.issued.id}/pdf/")
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_download_pdf(self):
        self.client.force_authenticate(self.other_user)
        response = self.client.get(f"/api/v1/certificate/issued/{self.issued.id}/pdf/")
        self.assertEqual(response.status_code, 404)

    def test_anonymous_cannot_download_pdf(self):
        response = self.client.get(f"/api/v1/certificate/issued/{self.issued.id}/pdf/")
        self.assertEqual(response.status_code, 401)
