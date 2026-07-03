from django.db import models

# Create your models here.
class Course(models.Model):
    title=models.CharField(max_length=50)
    thumbnail=models.ImageField(upload_to="thumbnails/")
    description=models.TextField()
    is_active=models.BooleanField(default=True)
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="lessons")
    title=models.CharField(max_length=50)
    description=models.TextField()
    youtube_url=models.URLField()

    def __str__(self):
        return self.title

class Quiz(models.Model):
    lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name="quizzes")
    title=models.CharField(max_length=200)

    def __str__(self):
        return str(self.title)

class Question(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="questions")
    question=models.TextField()
    def __str__(self):
        return self.question

class Option(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name="options")
    option_value=models.CharField(max_length=120)
    is_correct=models.BooleanField(default=False)

    def __str__(self):
        return self.option_value
