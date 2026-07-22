from django.urls import path
from . import views

urlpatterns = [
    path('courselist/', views.CourseList.as_view(), name="courselist"),
    path('coursedetails/<int:pk>', views.CourseDetails.as_view(), name="coursedetails"),
    path('', views.course_list_view, name='course-list'),
    path('search/', views.course_search_view, name='course-search'),
    path('<int:pk>/', views.course_detail_view, name='course-detail'),
    path('lessons/<int:pk>/', views.lesson_detail_view, name='lesson-detail'),
    path('<int:pk>/enroll/', views.enroll_course, name='enroll-course'),
    path('lessons/<int:pk>/complete/', views.mark_lesson_complete, name='mark-complete'),
    path('lessons/<int:pk>/progress/', views.update_lesson_progress, name='lesson-progress'),
    path('modules/<int:pk>/quiz/', views.quiz_view, name='module-quiz'),
    path('modules/<int:pk>/quiz/submit/', views.submit_quiz, name='submit-quiz'),
    path('modules/<int:pk>/quiz/result/<int:attempt_id>/', views.quiz_result_view, name='quiz-result'),
    path('certificate/<int:pk>/', views.certificate_view, name='certificate'),
]
