from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from course.models import Category, Course
from .serializers import CategorySerializer, CourseHomeSerializer, CoursePagination


@extend_schema(
    tags=["Course"],
    description=(
            "List all courses with pagination (9 per page). "
            "Featured courses appear first. "
            "Optionally filter by category using /list/<category_id>/."
    )
)
class CourseListView(generics.ListAPIView):
    serializer_class = CourseHomeSerializer
    pagination_class = CoursePagination

    def get_queryset(self):
        queryset = Course.objects.all()

        category_id = self.kwargs.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset.order_by("-featured", "id")


@extend_schema_view(
    get=extend_schema(
        tags=["Course"],
        description="Retrieve all categories (public)."
    ),
    post=extend_schema(
        tags=["Course"],
        description="Create a new category (staff only)."
    ),
)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by("order")
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]


@extend_schema_view(
    get=extend_schema(
        tags=["Course"],
        description="Retrieve all courses inside this category (public)."
    ),
    put=extend_schema(
        tags=["Course"],
        description="Fully update this category (superuser only)."
    ),
    patch=extend_schema(
        tags=["Course"],
        description="Partially update this category (superuser only)."
    ),
    delete=extend_schema(
        tags=["Course"],
        description="Delete this category (superuser only)."
    ),
)
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer  # used for PUT/PATCH/DELETE

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def retrieve(self, request, *args, **kwargs):
        """Override GET to return courses in this category."""
        category = self.get_object()

        courses = Course.objects.filter(category=category).order_by("-featured", "id")

        paginator = CoursePagination()
        page = paginator.paginate_queryset(courses, request)

        serializer = CourseHomeSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
