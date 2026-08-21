from django.contrib import admin

from .models import *

# Register your models here.
from django.contrib import admin
from .models import Course, Category
from django.utils.html import format_html


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("picture_preview", "title", "category", "price", "featured" )
    list_filter = ("category", "featured")
    search_fields = ("title", "slug")
    ordering = ("category", "title")

    def picture_preview(self, obj):
        if obj.picture:
            return format_html(
                '<img src="{}" width="120" style="border-radius:4px;" />',
                obj.picture.url
            )
        return "No Image"

    picture_preview.short_description = "Cover"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "emoji", "order")
    ordering = ("order",)

admin.site.register(CourseItem)