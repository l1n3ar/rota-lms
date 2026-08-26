import factory
from factory.django import DjangoModelFactory

from quiz.models import Answer, Question, Quiz


class QuizFactory(DjangoModelFactory):
    class Meta:
        model = Quiz

    title = factory.Faker("sentence", nb_words=4)
    random = factory.Faker("boolean", chance_of_getting_true=30)
    store_answers = factory.Faker("boolean", chance_of_getting_true=50)
    single_attempt = factory.Faker("boolean", chance_of_getting_true=30)
    pass_score = factory.Faker("random_int", min=50, max=100)
    draft = True


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer

    question = factory.SubFactory("quiz.factories.QuestionFactory")
    title = factory.Faker("sentence", nb_words=3)
    is_correct = False


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    quiz = factory.SubFactory(QuizFactory)
    title = factory.Faker("sentence", nb_words=6)
    description = factory.Faker("paragraph", nb_sentences=2)

    @factory.post_generation
    def answers(self, create, extracted, **kwargs):
        """
        Populate answers for the question.

        ``extracted`` may be:
        - an int: create that many answers, exactly one of them correct
        - an iterable of dicts: create one answer per dict (overrides
          fields, e.g. ``{"title": "...", "is_correct": True}``)
        - None: create no answers
        """
        if not create or extracted is None:
            return

        if isinstance(extracted, int):
            # one correct answer, the rest wrong
            AnswerFactory.create_batch(max(extracted - 1, 0), question=self)
            AnswerFactory(question=self, is_correct=True)
        else:
            for data in extracted:
                AnswerFactory(question=self, **data)
