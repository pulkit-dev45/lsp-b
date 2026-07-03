from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('courselist/',views.CourseList.as_view(),name="courselist"),
    path('coursedetails/<int:pk>',views.CourseDetails.as_view(),name="coursedetails"),
]
