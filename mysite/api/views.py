from rest_framework import viewsets

from blog.models import Post
from django.contrib.auth.models import User
from serializers import PostSerializer, UserSerializer
class PostView(viewsets.ModelViewsets):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UserView(viewsets.ModelViewsets):
    queryset  = User.objects.all()
    serializer_class = UserSerializer
    