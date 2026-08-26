from django.core.management.base import BaseCommand

from quiz.factories import QuestionFactory, QuizFactory


class Command(BaseCommand):
    help = "Seed the database with sample quiz data using factory_boy."

    def add_arguments(self, parser):
        parser.add_argument(
            "--quizzes", type=int, default=3, help="Number of quizzes to create."
        )
        parser.add_argument(
            "--questions", type=int, default=5, help="Questions per quiz."
        )
        parser.add_argument(
            "--answers", type=int, default=4, help="Answers per question."
        )
        parser.add_argument(
            "--delete-existing",
            action="store_true",
            help="Delete existing Quiz objects before seeding.",
        )

    def handle(self, *args, **options):
        from quiz.models import Quiz

        if options["delete_existing"]:
            deleted, _ = Quiz.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted existing data ({deleted} objects)."))

        quizzes = QuizFactory.create_batch(
            options["quizzes"],
            draft=False,
            pass_score=80,
        )

        for quiz in quizzes:
            QuestionFactory.create_batch(
                options["questions"],
                quiz=quiz,
                answers=options["answers"],
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(quizzes)} quizzes, each with "
                f"{options['questions']} questions and {options['answers']} answers per question."
            )
        )
