from django.shortcuts import render
from rest_framework import views, permissions, response, status
from rest_framework_simplejwt import tokens
from .serializers import UserRegisterationSerializer, UserSerializer
from .tasks import welcome_email_task
# Create your views here.


class UserRegisterationView(views.APIView):

    permission_classes = [permissions.AllowAny]

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
