from django.db import models
from utils.image_optimizer import ImageOptimizer
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

optimizer = ImageOptimizer(quality=85)


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    order = models.PositiveIntegerField(default=0)
    emoji = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.emoji} {self.title}"


class Course(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    title = models.CharField(max_length=300, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, blank=True, null=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to="covers/", default='')
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Only process if an actual file was uploaded
        if self.picture and self.picture.name:
            self.picture = optimizer.process(self.picture, size=(900, 506))
        super().save(*args, **kwargs)


class CourseItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=200)

    # Polymorphic link
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.content_type})"
