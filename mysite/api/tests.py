from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from blog.models import Post

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
    
    # A function to authenticate user via session authentication 
    def session_auth(self, username, password):
        self.client.login(username=username, password=password)
    
    # A function to authenticate user via token authentication
    def token_auth(self, user):
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')  
        
    def test_get_post_list(self):
        response = self.client.get(self.post_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])
    
    def test_post_valid_data(self):
        # auhtenticate user via session authentication
        self.session_auth("Kobby", "test2020")
        # make POST request
        response = self.client.post(self.post_list_create_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], "Kobby")
        
    def test_post_invalid_data_results_400(self):
        self.session_auth("Kobby", "test2020")
        response = self.client.post(self.post_list_create_url, self.invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["title"][0], "This field may not be blank.")
        
    def test_post_data_without_authentication_results_in_403(self):
        response = self.client.post(self.post_list_create_url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")
    
    def test_post_and_retrieve_by_id(self):
        # login via token
        self.token_auth(self.user)
        post_response = self.client.post(self.post_list_create_url, self.data, format="json")
        response = self.client.get(reverse(self.post_detail_url, args=[post_response.data["id"]]))
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["author"], "Kobby")
        
    def test_post_wrong_id_returns_404(self):
        self.token_auth(self.user)
        post_response = self.client.post(self.post_list_create_url, self.data, format="json")
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse(self.post_detail_url, args=[404]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_post_and_update_data(self):
        self.token_auth(self.user)
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
        self.token_auth(self.user)
        post_response = self.client.post(self.post_list_create_url, self.data, format="json")
        response = self.client.delete(reverse(self.post_detail_url, args=[post_response.data["id"]]))
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_if_another_author_has_post_object_permission(self):
        # authenticate author and create a post
        self.token_auth(self.user)
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
        self.token_auth(self.user)
        post_response = self.client.post(self.post_list_create_url, self.data, format="json")
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        
        # log author out
        self.client.credentials()
        # Authenticate superuser and make delete request to the post object
        self.session_auth("Boss", "boss.2020")
        response = self.client.delete(reverse(self.post_detail_url, args=[post_response.data["id"]]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "You do not have permission to perform this action.")
        
    def test_pagination(self):
        #create test data
        for post in range(20):
            Post.objects.create(
                author=self.user,
                title=f'Post {post + 1}',
                content="My first algorithm course was principles of programming"
            )
        
        response = self.client.get(self.post_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 20)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['previous'], None)
        self.assertNotEqual(response.data['next'], None)
        
        # Test pagination max limit works by increasing the upper bound(limit)
        limit_offset = {'limit':15, 'offset':5}
        url = f"{self.post_list_create_url}?{urlencode(limit_offset)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Upper bound can't exceed 10
        self.assertNotEqual(response.data['previous'], None)
        self.assertNotEqual(response.data['next'], None)
        

class TestAuthorView(APITestCase):
    '''Test for AuthorView which lists all blog authors and their posts'''
    def setUp(self):
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
    
        
        # urls
        self.authors_list_url = reverse("author-list")
        
        # Create 5 posts for first user
        for post in range(5):
            Post.objects.create(
                author=self.user,
                title=f'Post {post + 1}',
                content="My first algorithm course was principles of programming"
            )
        
        for post in range(5):
            Post.objects.create(
                author=self.user2,
                title=f'Post {post + 1}',
                content="My first algorithm course was principles of programming"
            )

    def test_get_author_lists(self):
        response = self.client.get(self.authors_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2) # Only two authors so far (pagination)
        self.assertEqual(len(response.data["results"][0]["posts"]), 5)  # First author has 5 posts
        self.assertEqual(response.data["results"][0]["username"], "Kobby") 
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(response.data['next'], None)
        
class TestProfileView(APITestCase):
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
        
        # Urls 
        self.profile_list_url = reverse("user-list")
        self.profile_detail_url = "user-detail"
        
    # A function to authenticate user via session authentication 
    def session_auth(self, username, password):
        self.client.login(username=username, password=password)
    
    def test_get_profile_list(self):
        self.session_auth(username="Kobby", password="test2020")
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3) # Only three users so far
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(response.data['next'], None)
        #print("\n", response.data)
   
    def test_get_profile_list_without_authentication_results_in_403(self):
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")
        
    def test_get_profile_by_id(self):
        self.session_auth(username="Kwabena", password="post2020")
        response = self.client.get(reverse(self.profile_detail_url, args=[self.user2.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["url"], None) # user profile url exists
        self.assertEqual(response.data["username"], "Kwabena")
        self.assertEqual(response.data["email"], "kwabena@gmail.com")
        self.assertEqual(response.data["profile"]["image"].split("/")[-1], "default.jpg") # Default image for user profile
    
    def test_get_profile_with_incorrect_id(self):
        self.session_auth(username="Kwabena", password="post2020")
        response = self.client.get(reverse(self.profile_detail_url, args=[404]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # def test_update_existing_user_profile(self):
    #     self.session_auth(username="Kobby", password="test2020")
    #     update_data = {
    #         "profile": {"image":self.user.profile.image},
    #         "username":"Kobby",
    #         "email": "kobby@gmail.com"
    #     }
    #     response = self.client.put(reverse(self.profile_detail_url, args=[self.user.id]),
    #                                update_data,
    #                                format="json")
    #     print("\n", response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["email"], "kobby@gmail.com")
        
    def test_delete_existing_user_profile(self):
        self.session_auth(username="Kobby", password="test2020")
        response = self.client.delete(reverse(self.profile_detail_url, args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_if_normal_user_can_delete_another_existing_user_profile(self):
        self.session_auth(username="Kobby", password="test2020")
        response = self.client.delete(reverse(self.profile_detail_url, args=[self.user2.id])) # user 2
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_if_superuser_has_permission_to_delete_exiting_user_profile(self):
        self.session_auth(username="Boss", password="boss.2020")
        response = self.client.delete(reverse(self.profile_detail_url, args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)