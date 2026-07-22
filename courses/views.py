from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CourseSerializer, CourseDetailsSerializer
from .models import Course, Lesson, Enrollment, LessonProgress, Module, Quiz, Question, Option, QuizAttempt, QuizResponse, Certificate
import uuid
import json


class CourseList(APIView):
    def get(self, request):
        course = Course.objects.all()
        serializer = CourseSerializer(course, many=True)
        return Response(serializer.data)


class CourseDetails(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(id=pk)
            serializer = CourseDetailsSerializer(course)
            return Response(serializer.data)
        except:
            return Response({"error": "Course Not found"})


def landing_view(request):
    featured = Course.objects.filter(is_active=True)[:3]
    return render(request, 'landing.html', {'featured': featured})


def course_list_view(request):
    courses = Course.objects.filter(is_active=True)
    enrolled_ids = set()
    if request.user.is_authenticated:
        enrolled_ids = set(Enrollment.objects.filter(
            user=request.user, course__in=courses
        ).values_list('course_id', flat=True))
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'enrolled_ids': enrolled_ids,
    })


def course_detail_view(request, pk):
    course = get_object_or_404(Course, id=pk)
    modules = course.modules.prefetch_related('lessons').all()
    is_enrolled = False
    completed_lesson_ids = set()
    first_lesson_url = None
    locked_module_ids = set()

    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        is_enrolled = enrollment is not None
        completed_lesson_ids = set(LessonProgress.objects.filter(
            user=request.user, lesson__course=course, is_completed=True
        ).values_list('lesson_id', flat=True))
        if is_enrolled:
            for m in modules:
                if _is_module_locked(request.user, m):
                    locked_module_ids.add(m.id)

    first_lesson = Lesson.objects.filter(course=course).first()
    if first_lesson:
        first_lesson_url = f'/courses/lessons/{first_lesson.id}/'

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'is_enrolled': is_enrolled,
        'completed_lesson_ids': completed_lesson_ids,
        'first_lesson_url': first_lesson_url,
        'locked_module_ids': locked_module_ids,
    })


def course_search_view(request):
    q = request.GET.get('q', '')
    courses = Course.objects.filter(is_active=True)
    if q:
        courses = courses.filter(title__icontains=q)
    enrolled_ids = set()
    if request.user.is_authenticated:
        enrolled_ids = set(Enrollment.objects.filter(
            user=request.user, course__in=courses
        ).values_list('course_id', flat=True))
    return render(request, 'courses/partials/course_cards.html', {
        'courses': courses,
        'enrolled_ids': enrolled_ids,
    })


@login_required
def dashboard_view(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    in_progress = enrollments.exclude(progress_percentage=100).count()
    completed_courses = enrollments.filter(progress_percentage=100).count()
    certificates = Certificate.objects.filter(user=request.user).select_related('course')
    return render(request, 'dashboard/index.html', {
        'enrollments': enrollments,
        'in_progress': in_progress,
        'completed': completed_courses,
        'certificates': certificates,
        'cert_count': completed_courses,
    })


@login_required
def lesson_detail_view(request, pk):
    lesson = get_object_or_404(Lesson, id=pk)
    course = lesson.course
    modules = course.modules.prefetch_related('lessons').all()
    lessons = list(course.lessons.all())
    idx = lessons.index(lesson)
    prev_lesson = lessons[idx - 1] if idx > 0 else None
    next_lesson = lessons[idx + 1] if idx < len(lessons) - 1 else None

    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    if not is_enrolled:
        messages.error(request, 'You must enroll first.')
        return redirect('course-detail', pk=course.id)

    if lesson.module and _is_module_locked(request.user, lesson.module):
        messages.error(request, f'Complete the previous module\'s quiz to unlock "{lesson.module.title}".')
        return redirect('course-detail', pk=course.id)

    progress, _ = LessonProgress.objects.get_or_create(
        user=request.user, lesson=lesson,
        defaults={'is_completed': False}
    )

    completed_ids = set(LessonProgress.objects.filter(
        user=request.user, lesson__course=course, is_completed=True
    ).values_list('lesson_id', flat=True))

    locked_module_ids = set()
    for m in modules:
        if _is_module_locked(request.user, m):
            locked_module_ids.add(m.id)

    for m in modules:
        for l in m.lessons.all():
            l.progress_completed = l.id in completed_ids

    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'modules': modules,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'is_completed': progress.is_completed,
        'watched_seconds': progress.watched_seconds,
        'is_enrolled': is_enrolled,
        'locked_module_ids': locked_module_ids,
    })


@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, id=pk)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    messages.success(request, f'Enrolled in {course.title}!')
    first_lesson = Lesson.objects.filter(course=course).order_by('order').first()
    if first_lesson:
        url = redirect('lesson-detail', pk=first_lesson.id)
        url['HX-Redirect'] = url.url
        return url
    return redirect('course-detail', pk=course.id)


@login_required
def mark_lesson_complete(request, pk):
    lesson = get_object_or_404(Lesson, id=pk)
    progress, _ = LessonProgress.objects.get_or_create(
        user=request.user, lesson=lesson
    )
    progress.is_completed = not progress.is_completed
    if progress.is_completed:
        progress.completed_at = timezone.now()
    else:
        progress.completed_at = None
    progress.save()

    _recalc_course_progress(lesson.course, request.user)
    if progress.is_completed:
        _check_and_issue_certificate(lesson.course, request.user)

    return render(request, 'courses/partials/lesson_progress.html', {
        'lesson': lesson,
        'is_completed': progress.is_completed,
    })


@login_required
@require_POST
def update_lesson_progress(request, pk):
    lesson = get_object_or_404(Lesson, id=pk)
    data = json.loads(request.body)
    watched_seconds = data.get('watched_seconds', 0)
    last_position = data.get('last_position', 0)
    duration = data.get('duration', 0)
    video_ended = data.get('ended', False)

    progress, _ = LessonProgress.objects.get_or_create(
        user=request.user, lesson=lesson
    )

    progress.watched_seconds = max(progress.watched_seconds, watched_seconds)
    progress.last_position = last_position

    if video_ended and not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = timezone.now()
    elif duration > 0 and (watched_seconds / duration) >= 0.9 and not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = timezone.now()

    progress.save()

    if progress.is_completed:
        _recalc_course_progress(lesson.course, request.user)
        _check_and_issue_certificate(lesson.course, request.user)

    return JsonResponse({
        'is_completed': progress.is_completed,
        'watched_seconds': progress.watched_seconds,
    })


def _is_module_locked(user, module):
    modules = list(module.course.modules.all())
    idx = modules.index(module)
    if idx == 0:
        return False
    prev_module = modules[idx - 1]
    quiz = Quiz.objects.filter(module=prev_module).first()
    if not quiz:
        return False
    return not QuizAttempt.objects.filter(user=user, quiz=quiz, passed=True).exists()


def _recalc_course_progress(course, user):
    enrollment = Enrollment.objects.filter(user=user, course=course).first()
    if not enrollment:
        return
    total_lessons = course.lessons.count()
    completed_count = LessonProgress.objects.filter(
        user=user, lesson__course=course, is_completed=True
    ).count()
    if total_lessons > 0:
        pct = int(completed_count / total_lessons * 100)
        enrollment.progress_percentage = pct
        enrollment.save()


@login_required
def quiz_view(request, pk):
    module = get_object_or_404(Module, id=pk)
    course = module.course

    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if not enrollment:
        messages.error(request, 'You must enroll first.')
        return redirect('course-detail', pk=course.id)

    if _is_module_locked(request.user, module):
        messages.error(request, f'Complete the previous module\'s quiz to unlock "{module.title}".')
        return redirect('course-detail', pk=course.id)

    quiz = Quiz.objects.filter(module=module).first()
    if not quiz:
        messages.error(request, 'No quiz for this module.')
        return redirect('course-detail', pk=course.id)

    questions = quiz.questions.prefetch_related('options').all()
    if not questions:
        messages.error(request, 'No questions in this quiz.')
        return redirect('course-detail', pk=course.id)

    previous_attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz)
    best_attempt = previous_attempts.order_by('-score').first()

    modules = list(course.modules.all())
    next_module = None
    mod_idx = modules.index(module)
    if mod_idx < len(modules) - 1:
        next_module = modules[mod_idx + 1]

    return render(request, 'courses/quiz.html', {
        'module': module,
        'course': course,
        'quiz': quiz,
        'questions': questions,
        'previous_attempts': previous_attempts,
        'best_attempt': best_attempt,
        'next_module': next_module,
    })


@login_required
@require_POST
def submit_quiz(request, pk):
    module = get_object_or_404(Module, id=pk)
    course = module.course

    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if not enrollment:
        messages.error(request, 'You must enroll first.')
        return redirect('course-detail', pk=course.id)

    if _is_module_locked(request.user, module):
        messages.error(request, f'Complete the previous module\'s quiz to unlock "{module.title}".')
        return redirect('course-detail', pk=course.id)

    quiz = get_object_or_404(Quiz, module=module)
    questions = list(quiz.questions.all())

    total = len(questions)
    score = 0

    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=0,
        total=total,
        passed=False,
    )

    for question in questions:
        selected_option_id = request.POST.get(f'question_{question.id}')
        if not selected_option_id:
            continue
        try:
            selected_option = Option.objects.get(id=selected_option_id)
        except Option.DoesNotExist:
            continue

        is_correct = selected_option.is_correct
        if is_correct:
            score += 1

        QuizResponse.objects.create(
            attempt=attempt,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
        )

    passed = (score / total) >= 0.6
    attempt.score = score
    attempt.passed = passed
    attempt.save()

    _check_and_issue_certificate(course, request.user)

    return redirect('quiz-result', pk=module.id, attempt_id=attempt.id)


def _check_and_issue_certificate(course, user):
    total_lessons = course.lessons.count()
    completed_lessons = LessonProgress.objects.filter(
        user=user, lesson__course=course, is_completed=True
    ).count()
    if completed_lessons < total_lessons:
        return

    modules = course.modules.all()
    if not modules:
        return

    total_questions = 0
    correct_answers = 0

    for module in modules:
        quiz = Quiz.objects.filter(module=module).first()
        if not quiz:
            return
        attempts = QuizAttempt.objects.filter(user=user, quiz=quiz)
        best = attempts.order_by('-score').first()
        if not best or not best.passed:
            return
        correct_answers += best.score
        total_questions += best.total

    if total_questions == 0:
        return

    overall_pct = correct_answers / total_questions
    if overall_pct < 0.6:
        return

    enrollment = Enrollment.objects.filter(user=user, course=course).first()
    if enrollment:
        enrollment.progress_percentage = 100
        enrollment.save()

    Certificate.objects.get_or_create(
        user=user,
        course=course,
        defaults={'verification_id': uuid.uuid4().hex[:16].upper()}
    )


@login_required
def quiz_result_view(request, pk, attempt_id):
    module = get_object_or_404(Module, id=pk)
    course = module.course
    quiz = get_object_or_404(Quiz, module=module)
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    responses = attempt.responses.select_related('question', 'selected_option').all()

    modules = list(course.modules.all())
    next_module = None
    mod_idx = modules.index(module)
    if mod_idx < len(modules) - 1:
        next_module = modules[mod_idx + 1]
    first_lesson = Lesson.objects.filter(module=next_module).order_by('order').first() if next_module else None

    return render(request, 'courses/quiz_result.html', {
        'module': module,
        'course': course,
        'quiz': quiz,
        'attempt': attempt,
        'responses': responses,
        'next_module': next_module,
        'next_lesson': first_lesson,
    })


@login_required
def certificate_view(request, pk):
    certificate = get_object_or_404(Certificate, id=pk, user=request.user)
    return render(request, 'certificates/detail.html', {
        'certificate': certificate,
    })
