from rest_framework import serializers
from .models import Course,Lesson,Quiz,Question,Option

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Option
        fields=["id","option_value","is_correct"]
class QuestionSerializer(serializers.ModelSerializer):
    options=OptionSerializer(many=True)
    class Meta:
        model=Question
        fields=[
            "id",
            "question",
            "options",
        ] 
class QuizSerializer(serializers.ModelSerializer):
    questions=QuestionSerializer(many=True)
    class Meta:
        model=Quiz
        fields=[
            "id",
            "title",
            "questions",
        ]

class LessonSerializer(serializers.ModelSerializer):
    quizzes=QuizSerializer(many=True)
    class Meta:
        model=Lesson
        fields=["id","title","quizzes"]
 
class CourseDetailsSerializer(serializers.ModelSerializer):
    lessons=LessonSerializer(many=True,read_only=True)
    class Meta:
        model=Course
        fields = [
            "id",
            "title",
            "description",
            "thumbnail",
            "lessons"
        ]
    
