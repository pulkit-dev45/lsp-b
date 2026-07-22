from django.db import models
from django.contrib.auth.models import User
import uuid

class Course(models.Model):
    title=models.CharField(max_length=50)
    thumbnail=models.ImageField(upload_to="thumbnails/")
    description=models.TextField()
    is_active=models.BooleanField(default=True)
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="lessons")
    module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name="lessons",null=True,blank=True)
    title=models.CharField(max_length=50)
    description=models.TextField()
    youtube_url=models.URLField()
    order=models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=10)

    class Meta:
        ordering=['order']

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at=models.DateTimeField(auto_now_add=True)
    progress_percentage=models.IntegerField(default=0)

    class Meta:
        unique_together=['user', 'course']

    def __str__(self):
        return f"{self.user.username} -> {self.course.title}"


class LessonProgress(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson=models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress")
    is_completed=models.BooleanField(default=False)
    completed_at=models.DateTimeField(null=True, blank=True)
    watched_seconds = models.IntegerField(default=0)
    last_position = models.IntegerField(default=0)

    class Meta:
        unique_together=['user', 'lesson']

    def __str__(self):
        return f"{self.user.username} -> {self.lesson.title}: {'✓' if self.is_completed else '○'}"


class Quiz(models.Model):
    module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name="quizzes")
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


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-attempted_at']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}/{self.total})"


class QuizResponse(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.question[:50]} - {'✓' if self.is_correct else '✗'}"


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificates")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="certificates")
    issued_at = models.DateTimeField(auto_now_add=True)
    verification_id = models.CharField(max_length=64, unique=True, default=uuid.uuid4)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
