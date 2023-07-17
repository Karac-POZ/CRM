from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class RootPageTest(TestCase):
    def test_status_code(self):
        response = self.client.get(reverse("root-page"))
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        response = self.client.get(reverse("root-page"))
        self.assertTemplateUsed(response, "root.html")


class DashPageTest(TestCase):
    def test_status_code(self):
        response = self.client.get(reverse("dash"))
        self.assertEqual(response.status_code, 302)


class LoginPageTest(TestCase):
    def test_status_code(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "registration/login.html")


class SignUpPageTest(TestCase):
    def test_status_code(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_template_name(self):
        response = self.client.get(reverse("signup"))
        self.assertTemplateUsed(response, "registration/signup.html")


class LogoutPageTest(TestCase):
    def test_status_code(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
