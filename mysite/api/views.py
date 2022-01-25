from rest_framework import viewsets

from blog.models import Post
from django.contrib.auth.models import User
from .serializers import AuthorSerializer, PostSerializer, UserSerializer
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class ProfileView(viewsets.ModelViewSet):
    queryset  = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get','retrieve','put','patch']

class AuthorView(viewsets.ReadOnlyModelViewSet):
    
    serializer_class = AuthorSerializer
    
    def get_queryset(self):
        author_ids = Post.objects.values_list('author', flat=True).distinct()
        return User.objects.filter(id__in=author_ids)
    
    
        
    
    