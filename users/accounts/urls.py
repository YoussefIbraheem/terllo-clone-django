from django.urls import path, include
from .views import UserRegisterationView , UserLoginView , UserProfileView



urlpatterns = [
    path("register/", UserRegisterationView.as_view(), name="user-registration"),
    path("login/", UserLoginView.as_view(),name="user-login"),
    path("profile/",UserProfileView.as_view(),name="user-profile")
]
