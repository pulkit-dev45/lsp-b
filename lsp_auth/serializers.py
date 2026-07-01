from django.contrib.auth.models import User
from rest_framework import serializers

class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields="__all__"

    def validate_username(self,value):
        if len(value) <= 3:
            raise serializers.ValidationError("Username Must be greater than there 3 character")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exits")
        return value
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email was already registered")
        return value
            
    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        return user
