from django.db import models

from utils.image_optimizer import ImageOptimizer

optimizer = ImageOptimizer(quality=85)

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="quiz/", default='')
    random = models.BooleanField(default=False)
    store_answers = models.BooleanField(default=False)
    single_attempt = models.BooleanField(default=False)
    pass_score = models.IntegerField(default=None, null=True, blank=True)  # like %80
    draft = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Only process if an actual file was uploaded
        if self.picture and self.picture.name:
            self.picture = optimizer.process(self.picture, size=(900, 506))
        super().save(*args, **kwargs)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True, null=True)
    picture = models.ImageField(upload_to="quiz/", default='', null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.picture and self.picture.name:
            self.picture = optimizer.process(self.picture, size=(900, 506))
        super().save(*args, **kwargs)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="quiz/", default='', null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.picture and self.picture.name:
            self.picture = optimizer.process(self.picture, size=(900, 506))
        super().save(*args, **kwargs)
