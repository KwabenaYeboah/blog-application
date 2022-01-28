from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from blog.models import Post
from users.models import Profile

class TestPostView(APITestCase):
    def setUp(self):
        # create user 
        self.user = User.objects.create_user(
            username="Kobby",
            email="kobby4140@gmail.com",
            password="test2020")
        
        #self.token = Token.objects.create(user=self.user)
        
        # post data
        self.data = {
            "title": "Principles of Programming",
            "content": "My first algorithm course was principles of programming"
        }
        
        self.invalid_data = {
            "title": "",
            "content": "My first algorithm course was principles of programming"
        }
        
        # urls
        self.post_list_create_url = reverse("post-list")
        self.post_detail_url = "post-detail"    
        
    def test_get_post_list(self):
        response = self.client.get(self.post_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])
    
    def test_post_valid_data(self):
        # auhtenticate user via session authentication
        login = self.client.login(username="Kobby", password="test2020")
        self.assertTrue(login)
        # make POST request
        response = self.client.post(self.post_list_create_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], "Kobby")
        
    def test_post_invalid_data_results_400(self):
        login = self.client.login(username="Kobby", password="test2020")
        self.assertEqual(login, True)
        response = self.client.post(self.post_list_create_url, self.invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("\n", response.data)
        self.assertEqual(response.data["title"][0], "This field may not be blank.")
        
    def test_post_data_without_authentication_results_in_403(self):
        response = self.client.post(self.post_list_create_url, self.data, format="json")
        print("\n",response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")
        