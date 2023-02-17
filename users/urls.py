from django.urls import path
from .views import RegisterView,LoginView,ProfilePageView,LogoutView,ProfileUpdateView



app_name = "users"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfilePageView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile-edit")
]