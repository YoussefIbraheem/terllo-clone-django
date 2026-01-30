from rest_framework import serializers
from .models import User, UserProfile
from django.contrib.auth import password_validation, hashers, authenticate


class UserRegisterationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        write_only=True, min_length=8, max_length=16
    )

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
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "password": {"required": True, "write_only": True},
            "password_confirm": {"required": True, "write_only": True},
        }

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create(**validated_data)
        UserProfile.objects.create(user=user)
        return user

    def validate_username(self, value):
        value_exists = User.objects.filter(username=value).exists()

        if value_exists:
            raise serializers.ValidationError(
                "A user with this username already exists!"
            )

        return value

    def validate_email(self, value):
        value_exists = User.objects.filter(email=value).exists()

        if value_exists:
            raise serializers.ValidationError("A user with this email already exists!")

        return value

    def validate(self, data):
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError("Passwords don't match!")
        password_validation.validate_password(data.get("password"))
        data["password"] = hashers.make_password(data.get("password"))
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


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get("email"), password=data.get("password"))

        if not user:
            raise serializers.ValidationError("Invalid Credentials.")
        if not user.is_verified:
            raise serializers.ValidationError(
                "Unverified user please contact us for verification."
            )
        if not user.is_active:
            raise serializers.ValidationError(
                "This account is inactive, refer to us for reverification."
            )

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["email", "username", "first_name", "last_name", "date_joined", "bio"]
