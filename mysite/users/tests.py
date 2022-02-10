from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestSignUpPage(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("register"))
    
    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "users/register.html")
        self.assertContains(self.response, "Join Today")
        self.assertNotContains(self.response, "This text is not there")
        
