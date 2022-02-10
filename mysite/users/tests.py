from django.test import TestCase
from django.urls import reverse

from .forms import UserCreationForm
class TestSignUpPage(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("register"))
    
    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "users/register.html")
        self.assertContains(self.response, "Join Today")
        self.assertNotContains(self.response, "This text is not there")
        
    def test_signup_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, UserCreationForm)
        self.assertContains(self.response, "csrfmiddlewaretoken")
    
    def test_register_and_login_user(self):
        data = {
            "username": "Kwabena",
            "email": "kwabena@gmail.com",
            "password1": "kobby.2020",
            "password2": "kobby.2020",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('sign_in'))
        
        login = self.client.login(username="Kwabena", password="kobby.2020")
        self.assertTrue(login)
        
        