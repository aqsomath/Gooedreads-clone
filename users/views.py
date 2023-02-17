from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from users.forms import UserCreationForm, ProfileUpdateForm


class RegisterView(View):
    def get(self, request):
        user_form = UserCreationForm()
        return render(request, "users/register.html", {"form": user_form})

    def post(self, request):

        user_form = UserCreationForm(data=request.POST)

        if user_form.is_valid():
            user_form.save()

            return redirect("users:login")
        else:
            return render(request, "users/register.html", {"form": user_form})


class LoginView(View):
    def get(self, request):

        login_form = AuthenticationForm()

        return render(request, "users/login.html", {"form": login_form})

    def post(self, request):

        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():

            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in !!")
            return redirect("landing")
        else:
            return render(request, "users/login.html", {"form": login_form})


class ProfilePageView(LoginRequiredMixin,View):
    def get(self, request):
     if request.user.is_authenticated:
        return render(request, "users/profile.html",{"user":request.user})
     return redirect("users:login")


class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request, "You have successfully logout in!!")
        return redirect("landing")


class ProfileUpdateView(LoginRequiredMixin,View):
    def get(self, request):
        profile_update = ProfileUpdateForm(instance=request.user)
        return render(request, "users/profile_edit.html",{"form":profile_update})

    def post(self,request):
        profile_update = ProfileUpdateForm(
            instance=request.user,
            files=request.FILES,
            data=request.POST)
        if profile_update.is_valid():
            profile_update.save()
            return redirect("users:profile")
        return render(request,"users/profile_edit.html",{"form":profile_update})









