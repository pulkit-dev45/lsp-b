from django.contrib import admin

# Register your models here.
from .models import Course,Question,Quiz,Option,Lesson

admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Option)
admin.site.register(Lesson)