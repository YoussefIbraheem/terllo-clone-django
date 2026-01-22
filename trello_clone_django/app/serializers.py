from rest_framework import serializers
from .models import User, UserProfile
from django.contrib.auth.password_validation import validate_password


class UserRegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=16)
    password_confirm = serializers.CharField(write_only=True, min_length=8, max_length=16)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {"email": {"required": True}, "username": {"required": True}}
        
    def create(self, validated_data):
        validated_data.pop("password_confirm")
        print(validated_data)
        user = User.objects.create(**validated_data)
        UserProfile.objects.create(user=user)
        return user
    
    def validate_username(self,value):
        value_exists = User.objects.filter(username=value).exists()
        
        if value_exists:
            raise serializers.ValidationError("A user with this username already exists!")
        
        return value
        
    def validate_email(self,value):
        value_exists = User.objects.filter(email=value).exists()
        
        if value_exists:
            raise serializers.ValidationError("A user with this email already exists!")
        
        return value
        
    
    def validate(self, data):
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError("Passwords don't match!")
        validate_password(data.get("password"))
        return data
        
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_verified",
            "date_joined",
            "last_login",
            "profile_picture",
        ]
        read_only_fields = ["id", "date_joined", "last_login"]