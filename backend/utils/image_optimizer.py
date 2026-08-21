import hashlib
import os
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile

class ImageOptimizer:
    def __init__(self, quality=85):
        self.quality = quality

    def process(self, uploaded_file, size):
        """
        Process the image to the given `size` and compress to WebP.
        If the image is already WebP, return it untouched.
        """
        # Robust WebP check: by extension and Pillow's format
        ext = os.path.splitext(getattr(uploaded_file, 'name', ''))[1].lower()
        try:
            # Read once to allow format detection without consuming stream
            uploaded_file.seek(0)
            img = Image.open(uploaded_file)
            img_format = (img.format or '').upper()
        except Exception:
            # If it's not an image or Pillow can't open, return as-is
            return uploaded_file

        if ext == ".webp" or img_format == "WEBP":
            # Do nothing: leave WebP files untouched
            uploaded_file.seek(0)
            return uploaded_file

        # Normalize orientation from EXIF (common for mobile uploads)
        img = ImageOps.exif_transpose(img)

        # Convert palette/LA to RGBA or RGB for consistent WebP output
        if img.mode in ("P", "LA"):
            img = img.convert("RGBA")
        elif img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        # Resize while preserving aspect ratio
        # `size` is a tuple (max_width, max_height)
        img.thumbnail(size)

        # Save to buffer as WebP with requested quality
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=self.quality, method=6)
        buffer.seek(0)

        # Hash filename from content bytes
        digest = hashlib.sha256(buffer.getvalue()).hexdigest()[:20]
        hash_name = f"{digest}.webp"

        return ContentFile(buffer.getvalue(), name=hash_name)