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
        
        self.post = Post.objects.create(
            author=self.user,
            title="Interesting times ahead",
            content="What will technology looks like in 2050?")
    
    def test_post_list_view(self):
        url = reverse('blog-home')
        response = self.client.get(url)
        print("\n", response.context)
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
        
