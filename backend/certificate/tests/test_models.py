import io
from unittest.mock import patch

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase

from certificate.models import Certificate, IssuedCertificate
from core_auth.models import User


def generate_dummy_image(name="test_image.jpg"):
    """
    Helper function to generate a valid dummy image file in memory.
    This prevents Django's ImageField from throwing validation errors.
    """
    file_obj = io.BytesIO()
    image = Image.new("RGB", (100, 100), color="white")
    image.save(file_obj, "JPEG")
    file_obj.seek(0)
    return SimpleUploadedFile(name, file_obj.read(), content_type="image/jpeg")


class CertificateModelTests(TestCase):

    def test_certificate_str(self):
        """Test the string representation of the Certificate model."""
        certificate = Certificate.objects.create(title="Python Basics")
        self.assertEqual(str(certificate), "Python Basics")

    def test_draft_defaults_to_true(self):
        """New certificates are drafts until an admin publishes them."""
        certificate = Certificate.objects.create(title="Drafty")
        self.assertTrue(certificate.draft)

    @patch("certificate.models.optimizer.process")
    def test_certificate_save_without_image(self, mock_process):
        """Test that the optimizer is NOT called if no image is uploaded."""
        Certificate.objects.create(title="No Image Certificate")
        mock_process.assert_not_called()

    @patch("certificate.models.optimizer.process")
    def test_certificate_save_with_image(self, mock_process):
        """Test that the optimizer IS called with A4-landscape dimensions when an image is provided."""
        dummy_image = generate_dummy_image()
        mock_process.return_value = dummy_image

        Certificate.objects.create(title="Image Certificate", picture=dummy_image)

        self.assertTrue(mock_process.called)
        args, kwargs = mock_process.call_args
        self.assertEqual(kwargs.get("size"), (1414, 1000))


class IssuedCertificateModelTests(TestCase):

    def setUp(self):
        self.certificate = Certificate.objects.create(title="Python Basics")
        self.user = User.objects.create_user(email="student@example.com")

    def test_issued_certificate_str(self):
        """Test the string representation of the IssuedCertificate model."""
        issued = IssuedCertificate.objects.create(certificate=self.certificate, user=self.user)
        self.assertIn("Python Basics", str(issued))
        self.assertIn("student@example.com", str(issued))

    def test_verification_code_is_generated(self):
        """A 32-char verification code is generated automatically on save."""
        issued = IssuedCertificate.objects.create(certificate=self.certificate, user=self.user)
        self.assertTrue(issued.verification_code)
        self.assertEqual(len(issued.verification_code), 32)

    def test_verification_codes_are_unique(self):
        certificate2 = Certificate.objects.create(title="Django Advanced")
        issued1 = IssuedCertificate.objects.create(certificate=self.certificate, user=self.user)
        issued2 = IssuedCertificate.objects.create(certificate=certificate2, user=self.user)
        self.assertNotEqual(issued1.verification_code, issued2.verification_code)

    def test_one_certificate_per_user(self):
        """A user cannot be issued the same certificate twice."""
        IssuedCertificate.objects.create(certificate=self.certificate, user=self.user)
        with self.assertRaises(IntegrityError):
            IssuedCertificate.objects.create(certificate=self.certificate, user=self.user)
