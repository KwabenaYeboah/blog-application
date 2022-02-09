from ast import arg
import email
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from blog.models import Post

class TestBlogViews(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="Kobby",
            email="kobby@gmail.com",
            password="post.2020")
        
        self.user2 = User.objects.create_user(
            username="Kwabena",
            email="kwabena@gmail.com",
            password="test.2020")
        
        self.post = Post.objects.create(
            author=self.user,
            title="Interesting times ahead",
            content="What will technology looks like in 2050?")
    
    def test_post_list_view(self):
        url = reverse('blog-home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "technology")
        self.assertTemplateUsed(response, 'blog/home.html')
        
    def test_post_detail_view(self):
        url = reverse('post_detail', args=[self.post.pk])
        response = self.client.get(url)
        no_response = self.client.get(reverse('post_detail', args=[4]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Interesting times ahead")
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        
    def test_post_create_view(self):
        login = self.client.login(username="Kobby", password="post.2020")
        self.assertTrue(login)
        
        data = {
            "title": "Principles of Programming",
            "content": "My first algorithm course was principles of programming"
        }
        response = self.client.post(reverse("post-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "Principles of Programming")
    
    def test_if_post_create_requires_authentication(self):
        data = {
            "title": "Principles of Programming",
            "content": "My first algorithm course was principles of programming"
        }
        
        redirect_url = f"{reverse('sign_in')}?next={reverse('post-create')}"
        response = self.client.post(reverse("post-create"), data)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_url) 
          
    def test_post_update_view(self):
        post_id = Post.objects.last().id
        login = self.client.login(username="Kobby", password="post.2020")
        self.assertTrue(login)
        
        update_data = {
            "title": "Designing and Analysis of Algorithm",
            "content": "My first algorithm course was principles of programming"
        }
        response = self.client.post(reverse("post-update", args=[post_id]), update_data) 
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "Designing and Analysis of Algorithm")
        
    def test_post_delete_view(self):
        post_id = Post.objects.last().id
        login = self.client.login(username="Kobby", password="post.2020")
        self.assertTrue(login)
        
        response = self.client.post(reverse("post-delete", args=[post_id]))
        self.assertEqual(response.status_code, 302)
        
    def test_if_another_author_has_permission_to_delete_other_posts(self):
        post_id = Post.objects.last().id
        login = self.client.login(username="Kwabena", password="test.2020")
        self.assertTrue(login)
        
        response = self.client.post(reverse("post-delete", args=[post_id]))
        self.assertEqual(response.status_code, 403)
        
    def test_user_post_list_view(self):
        # Create a series of posts
        for post in range(1, 11):
            Post.objects.create(
            author=self.user2,
            title=f"Post {post}",
            content=f"Principles of programming{post}")
        
        response = self.client.get(reverse("user-posts", args=[self.user2.username]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Principles of programming")
        self.assertEqual(Post.objects.filter(author=self.user2).count(), 10)
        
class TestPagination(TestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create_user(
            username="Kwabena",
            email="kwabena@gmail.com",
            password="test.2020")
        
         # Create a series of posts
        for post in range(1, 11):
            Post.objects.create(
            author=self.user,
            title=f"Pagination {post}",
            content=f"Testing for Pagination {post}")

    def test_pagination(self):
        response = self.client.get(reverse("blog-home"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(str(response.context["page_obj"]), "<Page 1 of 2>")
        self.assertTrue(response.context["paginator"])
        self.assertEqual(len(response.context["object_list"]), 5)

        
            
      