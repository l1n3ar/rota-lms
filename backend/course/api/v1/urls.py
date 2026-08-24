from django.urls import path
from .views import CourseListView, CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path("list/", CourseListView.as_view(), name="course-list"),
    path("list/<int:category_id>/", CourseListView.as_view(), name="course-list-by-category"),

    path("cat/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("cat/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
]