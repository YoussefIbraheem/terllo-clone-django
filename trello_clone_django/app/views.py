from django.shortcuts import render
from rest_framework import views, permissions, response, status
from rest_framework_simplejwt import tokens
from .serializers import UserRegisterationSerializer, UserSerializer

# Create your views here.


class UserRegisterationView(views.APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
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
