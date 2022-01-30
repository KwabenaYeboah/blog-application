from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from blog.models import Post
from users.models import Profile

class TestPostView(APITestCase):
    def setUp(self):
        #create a superuser
        self.user = User.objects.create_superuser(
            username="Boss",
            email="boss@gmail.com",
            password="boss.2020")
        
        # create user 
        self.user = User.objects.create_user(
            username="Kobby",
            email="kobby4140@gmail.com",
            password="test2020")
        
        # create a second user
        self.user2 = User.objects.create_user(
            username="Kwabena",
            email="kwabena@gmail.com",
            password="post2020")
        
        self.token = Token.objects.create(user=self.user)
        
        # post data
        self.data = {
            "title": "Principles of Programming",
            "content": "My first algorithm course was principles of programming"
        }
        
        # invalid Data
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
        self.assertEqual(response.data["title"][0], "This field may not be blank.")
        
    def test_post_data_without_authentication_results_in_403(self):
        response = self.client.post(self.post_list_create_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")
    
    def test_post_and_retrieve_by_id(self):
        # login via token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        post_response = self.client.post(self.post_list_create_url, self.data, format="json")
        response = self.client.get(reverse(self.post_detail_url, args=[post_response.data["id"]]))
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["author"], "Kobby")
        
    def test_post_wrong_id_returns_404(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        post_response = self.client.post(self.post_list_create_url, self.data, format="json")
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse(self.post_detail_url, args=[404]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_post_and_update_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        update_data = {
            "title": "Principles of Programming = COMP 109",
            "content": "My first algorithm course was principles of programming in level 100"
        }
        post_response = self.client.post(self.post_list_create_url, self.data, format="json")
        update_response = self.client.put(
            reverse(self.post_detail_url, args=[post_response.data["id"]]),
            update_data, 
            format="json")
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["title"], "Principles of Programming = COMP 109")
    
    def test_delete_exitsting_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        post_response = self.client.post(self.post_list_create_url, self.data, format="json")
        response = self.client.delete(reverse(self.post_detail_url, args=[post_response.data["id"]]))
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_if_another_author_has_post_object_permission(self):
        # authenticate author and create a post
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        post_response = self.client.post(self.post_list_create_url, self.data, format="json")
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        
        # log author out
        self.client.credentials()
        # Authenticate different User/Author and make delete request to the post object
        self.client.login(username="Kwabena", password="post2020")
        response = self.client.delete(reverse(self.post_detail_url, args=[post_response.data["id"]]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You do not have permission to perform this action.")
    
    def test_if_superuser_has_no_post_object_permission(self):
         # authenticate author and create a post
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        post_response = self.client.post(self.post_list_create_url, self.data, format="json")
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        
        # log author out
        self.client.credentials()
        # Authenticate superuser and make delete request to the post object
        self.client.login(username="Boss", password="boss.2020")
        response = self.client.delete(reverse(self.post_detail_url, args=[post_response.data["id"]]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You do not have permission to perform this action.")
        
        