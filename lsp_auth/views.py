from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer
from django.contrib.auth import authenticate

class SignupView(APIView):
    def post(self,request):
        serializer=SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User created successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.Error)
    
class LoginView(APIView):
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")
        user=authenticate(username=username,password=password)
        if user is not None:
            refresh=RefreshToken.for_user(user)
            return Response({"refresh":str(refresh),"access":str(refresh.access_token)})
        return Response({"error":"Invalid credenitals"},status=status.HTTP_401_UNAUTHORIZED)
