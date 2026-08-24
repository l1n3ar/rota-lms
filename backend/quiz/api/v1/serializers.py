from rest_framework import serializers
from quiz.models import Quiz, Question, Answer

# ==========================================
# PUBLIC SERIALIZERS (Read-Only & Sanitized)
# ==========================================

class PublicAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        # SECURITY: 'is_correct' is intentionally missing here
        fields = ['id', 'title', 'picture']

class PublicQuestionSerializer(serializers.ModelSerializer):
    answers = PublicAnswerSerializer(source='answer_set', many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'picture', 'answers']

class PublicQuizSerializer(serializers.ModelSerializer):
    questions = PublicQuestionSerializer(source='question_set', many=True, read_only=True)

    class Meta:
        model = Quiz
        # 'draft' is omitted because the public only ever sees non-drafts anyway
        fields = [
            'id', 'title', 'picture', 'random', 'store_answers',
            'single_attempt', 'pass_score', 'questions'
        ]


# ==========================================
# ADMIN SERIALIZERS (Full CRUD, Flat Structure)
# ==========================================

class AdminAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class AdminQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class AdminQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'