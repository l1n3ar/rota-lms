from django.contrib import admin
from django.contrib.admin import TabularInline, StackedInline

from quiz.models import Quiz, Question, Answer


class AnswerInline(TabularInline):
    model = Answer
    extra = 4  # start with 4 empty answer rows
    fields = ("title", "picture", "is_correct")

    # When a row is saved with is_correct=True, unset it on the question's other answers
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_correct:
            Answer.objects.filter(question=obj.question).exclude(pk=obj.pk).update(is_correct=False)


class QuestionInline(StackedInline):
    model = Question
    extra = 1
    fields = ("title", "description", "picture")
    show_change_link = True
    inlines = [AnswerInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "draft", "random", "single_attempt", "store_answers", "pass_score", "question_count")
    list_filter = ("draft", "random", "single_attempt", "store_answers")
    list_editable = ("draft", "random", "single_attempt", "store_answers")  # toggle right from the list
    search_fields = ("title",)
    inlines = [QuestionInline]

    @admin.display(description="Questions")
    def question_count(self, obj):
        return obj.question_set.count()


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "quiz", "answer_count")
    list_filter = ("quiz",)
    search_fields = ("title", "description")
    list_select_related = ("quiz",)
    inlines = [AnswerInline]

    @admin.display(description="Answers")
    def answer_count(self, obj):
        return obj.answer_set.count()


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("title", "question", "is_correct")
    list_filter = ("is_correct", "question__quiz")
    list_editable = ("is_correct",)
    search_fields = ("title",)
    list_select_related = ("question", "question__quiz")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_correct:
            Answer.objects.filter(question=obj.question).exclude(pk=obj.pk).update(is_correct=False)
