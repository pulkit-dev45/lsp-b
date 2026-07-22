from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer
from courses.models import Enrollment


class SignupView(APIView):
    def post(self,request):
        serializer=SignupSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            refresh=RefreshToken.for_user(user)
            return Response({"message":"User created successfully","refresh":str(refresh),"access":str(refresh.access_token)},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")
        user=authenticate(username=username,password=password)
        if user is not None:
            refresh=RefreshToken.for_user(user)
            return Response({"refresh":str(refresh),"access":str(refresh.access_token)},status=status.HTTP_200_OK)
        return Response({"error":"Invalid credenitals"},status=status.HTTP_401_UNAUTHORIZED)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('course-list')
        return render(request, 'lsp_auth/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'lsp_auth/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'lsp_auth/signup.html', {'error': 'Username already taken.'})
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, f'Account created! Welcome, {username}!')
        return redirect('course-list')
    return render(request, 'lsp_auth/signup.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            request.user.email = email
            request.user.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    return render(request, 'accounts/profile.html', {'enrollments': enrollments})


@login_required
def password_change_view(request):
    if request.method == 'POST':
        old = request.POST.get('old_password')
        new1 = request.POST.get('new_password1')
        new2 = request.POST.get('new_password2')
        if not request.user.check_password(old):
            messages.error(request, 'Current password is incorrect.')
        elif new1 != new2:
            messages.error(request, 'New passwords do not match.')
        elif len(new1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        else:
            request.user.set_password(new1)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password changed successfully.')
        return redirect('profile')
    return redirect('profile')
