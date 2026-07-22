from django.contrib import admin
from .models import Course, Question, Quiz, Option, Lesson, Enrollment, LessonProgress, Module, QuizAttempt, QuizResponse, Certificate

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Option)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(QuizAttempt)
admin.site.register(QuizResponse)
admin.site.register(Certificate)
