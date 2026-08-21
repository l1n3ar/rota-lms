from rest_framework import serializers


from course.models import *

from rest_framework.pagination import PageNumberPagination

class CoursePagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 50

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CourseHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["title", "slug", "picture", "featured", "price"]

