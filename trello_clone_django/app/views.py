from django.shortcuts import render
from rest_framework import views, permissions, response, status
from rest_framework_simplejwt import tokens
from .serializers import (
    UserRegisterationSerializer,
    UserSerializer,
    UserLoginSerializer,
    UserProfileSerializer
)
from .models import UserProfile
from .tasks import welcome_email_task
import logging


logger = logging.getLogger(__name__)


# Create your views here.


class UserRegisterationView(views.APIView):

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid():

            user = serializer.save()

            welcome_email_task.delay(user.email, user.username)

            refresh = tokens.RefreshToken.for_user(user=user)

            return response.Response(
                {
                    "message": "User registered successfully",
                    "user": UserSerializer(user).data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(views.APIView):

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            refresh = tokens.RefreshToken.for_user(user=user)

            logger.warning(
                f"REFRESH TOKEN FOR USER {user.username}: {str(refresh)}", exc_info=True
            )

            return response.Response(
                {
                    "message": "User logged in successfully",
                    "user": UserSerializer(user).data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(views.APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get(self,request):
        try:
        
            profile = request.user.profile
            serializer = UserProfileSerializer(profile).data
            return response.Response(serializer)
        
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            serializer = UserProfileSerializer(profile).data
            return response.Response(serializer)
            