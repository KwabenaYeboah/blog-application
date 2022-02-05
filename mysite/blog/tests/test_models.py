from django.test import TestCase
from django.contrib.auth.models import User

from blog.models import Post

class TestPost(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Kobby", 
            email="kobby@gmail.com",
            password="post.2020"
        )
    
        self.post = Post.objects.create(
            author=self.user,
            title="Interesting times ahead",
            content="What will technology looks like in 2050?"
        )
    
    def test_post_object(self):
        self.assertEqual(self.post.author.username, "Kobby")
        self.assertEqual(self.post.title, "Interesting times ahead")
        self.assertEqual(self.post.content,"What will technology looks like in 2050?")
        self.assertEqual(Post.objects.count(), 1)