from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from .serializers import CourseSerializer,CourseDetailsSerializer
from .models import Course ,Lesson


class CourseList(APIView):
    def get(self,request):
        course=Course.objects.all()
        serializer=CourseSerializer(course,many=True)
        return Response(serializer.data)


class CourseDetails(APIView):
    def get(self,request,pk):
        try:
            course=Course.objects.get(id=pk)
            serializer=CourseDetailsSerializer(course)
            return Response(serializer.data)
        except:
            return Response({"error":"Course Not found"})
        

        
