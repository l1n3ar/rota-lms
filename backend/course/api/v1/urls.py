from django.urls import path
from course.api.v1.views import *


# courses/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("list/", CourseListView.as_view(), name="course-list"),
    path("list/<int:category_id>/", CourseListView.as_view(), name="course-list-by-category"),

    path("cat/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("cat/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
]