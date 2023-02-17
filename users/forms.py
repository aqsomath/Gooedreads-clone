from django import forms
from django.core.mail import send_mail

from users.models import CustomUser


class UserCreationForm(forms.ModelForm):


    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "password", "profile_picture")

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()


        # send_mail(
        #     "Wecome to goodreads clone",
        #     f"Hi {user.username} , welcome to goodreads",
        #     "aqsomath@gmail.com",
        #     [user.email]
        # )

        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email","profile_picture")