from django.urls import path, include
from .views import UserRegisterationView


urlpatterns = [
    path("register/", UserRegisterationView.as_view(), name="user-registration"),
    path("test/", lambda request: print("test successful")),
    
]
