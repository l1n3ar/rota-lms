from django.core.exceptions import ValidationError
import os

def validate_attachment(file):
    # Allowed extensions
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in allowed_extensions:
        raise ValidationError("Only JPG, JPEG, PNG, and PDF files are allowed.")

    # Max size: 5MB
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError("File size must be 5MB or less.")