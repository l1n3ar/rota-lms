from core_auth.permissions import IsSuperUserOrReadOnly
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view, extend_schema
from quiz.models import Quiz, Question, Answer
from . import serializers

@extend_schema_view(
    list=extend_schema(tags=["Quiz"], summary="List all quizzes"),
    retrieve=extend_schema(tags=["Quiz"], summary="Retrieve a specific quiz"),
    create=extend_schema(tags=["Quiz"], summary="Create a new quiz (Admin only)"),
    update=extend_schema(tags=["Quiz"], summary="Update a quiz (Admin only)"),
    partial_update=extend_schema(tags=["Quiz"], summary="Partially update a quiz (Admin only)"),
    destroy=extend_schema(tags=["Quiz"], summary="Delete a quiz (Admin only)"),
)
class QuizViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Quiz.objects.all()
        return Quiz.objects.filter(draft=False)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return serializers.AdminQuizSerializer
        return serializers.PublicQuizSerializer


@extend_schema_view(
    list=extend_schema(tags=["Questions"], summary="List all questions"),
    retrieve=extend_schema(tags=["Questions"], summary="Retrieve a specific question"),
    create=extend_schema(tags=["Questions"], summary="Create a question (Admin only)"),
    update=extend_schema(tags=["Questions"], summary="Update a question (Admin only)"),
    partial_update=extend_schema(tags=["Questions"], summary="Partially update a question (Admin only)"),
    destroy=extend_schema(tags=["Questions"], summary="Delete a question (Admin only)"),
)
class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Question.objects.all()
        return Question.objects.filter(quiz__draft=False)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return serializers.AdminQuestionSerializer
        return serializers.PublicQuestionSerializer


@extend_schema_view(
    list=extend_schema(tags=["Answers"], summary="List all answers"),
    retrieve=extend_schema(tags=["Answers"], summary="Retrieve a specific answer"),
    create=extend_schema(tags=["Answers"], summary="Create an answer (Admin only)"),
    update=extend_schema(tags=["Answers"], summary="Update an answer (Admin only)"),
    partial_update=extend_schema(tags=["Answers"], summary="Partially update an answer (Admin only)"),
    destroy=extend_schema(tags=["Answers"], summary="Delete an answer (Admin only)"),
)
class AnswerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Answer.objects.all()
        return Answer.objects.filter(question__quiz__draft=False)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return serializers.AdminAnswerSerializer
        return serializers.PublicAnswerSerializer