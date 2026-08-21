import os
import random
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PIL import Image, ImageDraw, ImageFont

from course.models import Category, Course


class Command(BaseCommand):
    help = "Populate database with sample categories and courses"

    def generate_image(self, text):
        """Generate a 900x506 placeholder image with text."""
        width, height = 900, 506
        img = Image.new("RGB", (width, height), color=(random.randint(0, 255), 150, 150))
        draw = ImageDraw.Draw(img)

        # Simple text placement
        draw.text((50, 50), text, fill="white")

        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        return ContentFile(buffer.getvalue(), f"{slugify(text)}.jpg")

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding database..."))

        # Clear existing data
        Course.objects.all().delete()
        Category.objects.all().delete()

        categories = []
        category_names = [
            ("Programming", "💻"),
            ("Design", "🎨"),
            ("Marketing", "📣"),
            ("Business", "📊"),
            ("Photography", "📷"),
        ]

        # Create categories
        for idx, (title, emoji) in enumerate(category_names):
            cat = Category.objects.create(
                title=title,
                emoji=emoji,
                order=idx
            )
            categories.append(cat)

        # Create courses
        for cat in categories:
            for i in range(5):
                title = f"{cat.title} Course {i+1}"
                slug = slugify(title)

                course = Course(
                    title=title,
                    slug=slug,
                    category=cat,
                    summary=f"This is a sample summary for {title}.",
                    price=random.randint(10, 200),
                    featured=random.choice([True, False]),
                )

                # Generate image
                img_file = self.generate_image(title)
                course.picture.save(img_file.name, img_file, save=False)

                course.save()

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))