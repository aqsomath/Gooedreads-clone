from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegisterTest(TestCase):
    def test_created_new_account(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username":"jamshid1",
                "first_name":"jamshid",
                "last_name":"omonov",
                "email":"aqsomath@gmail.com",
                "password":"somepassword"
            }
        )

        user = CustomUser.objects.get(username="jamshid1")

        self.assertEqual(user.last_name, "omonov")
        self.assertEqual(user.first_name, "jamshid")
        self.assertEqual(user.email, "aqsomath@gmail.com")
        self.assertNotEqual(user.password, "somepassword")
        self.assertTrue(user.check_password, "somepassword")

    def test_required_fields(self):
        response =self.client.post(
            reverse("users:register"),
            data={

                "first_name": "jamshid",
                "last_name": "omonov",
                "email": "aqsomath@gmail.com",
            }
        )


        user_count = CustomUser.objects.count()


        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username":"jamshid",
                "first_name": "jamshid",
                "last_name": "omonov",
                "email": "invalid-email",
                "password":"somepassword",
            }
        )
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "jamshid",
                "first_name": "jamshid",
                "last_name": "omonov",
                "email": "aqsomath@gmail.com",
                "password": "somepassword",
            }
        )
        response1 = self.client.post(
            reverse("users:register"),
            data={
                "username": "jamshid",
                "first_name": "jamshid",
                "last_name": "omonov",
                "email": "aqsomath@gmail.com",
                "password": "somepassword",
            }
        )
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 1)
        self.assertFormError(response1, "form", "username", "A user with that username already exists.")



class LoginTest(TestCase):

    def test_successful_login(self):
        user = CustomUser.objects.create(username="jamshid", first_name="omonov")
        user.set_password("somepass")
        user.save()

        self.client.post(
            reverse("users:login"),
            data={
                "username":"jamshid",
                "password":"somepass"
            }
        )


        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_failed_login(self):
        user = CustomUser.objects.create(username="jamshid", first_name="omonov")
        user.set_password("somepass")
        user.save()

        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong",
                "password": "somepass"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)



        self.client.post(
            reverse("users:login"),
            data={
                "username": "jamshid",
                "password": "wrong"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        user = CustomUser.objects.create(username="jamshid", first_name="omonov", last_name="jamshidbek",
                                   email="aqsomath@gmail.com")
        user.set_password("somepass")
        user.save()

        self.client.login(username="jamshid", password="somepass")
        self.client.get(reverse("users:logout"))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestcase(TestCase):
    def test_profile_login(self):
        response=self.client.get(
            reverse("users:profile"),
        )

        self.assertEqual(response.url, reverse("users:login")+"?next=/users/profile/")


    def test_profile_page(self):
        user = CustomUser.objects.create(username="jamshid", first_name="omonov", last_name="jamshidbek", email="aqsomath@gmail.com")
        user.set_password("somepass")
        user.save()

        self.client.login(username="jamshid", password="somepass")
        response = self.client.get(
            reverse("users:profile"),
        )
        self.assertContains(response, user.username)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.email)

class ProfileUpdateTest(TestCase):
    def test_profile_update(self):
        user = CustomUser.objects.create(username="jamshid", first_name="omonov", last_name="jamshidbek",
                                   email="aqsomath@gmail.com")
        user.set_password("somepass")
        user.save()

        self.client.login(username="jamshid", password="somepass")

        self.client.post(
            reverse("users:profile-edit"),
            data={
                "username":"jamshidbek",
                "first_name":"omon",
                "last_name":"jamshid",
                "email":"aqsomath@gmail.com"
            }
        )

        user = CustomUser.objects.get(pk=user.pk)

        self.assertEqual(user.username, "jamshidbek")
        self.assertEqual(user.first_name, "omon")
        self.assertEqual(user.last_name, "jamshid")
        self.assertEqual(user.email, "aqsomath@gmail.com")



