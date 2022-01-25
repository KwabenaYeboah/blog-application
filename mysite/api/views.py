from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User

from blog.models import Post
from .serializers import AuthorSerializer, PostSerializer, UserSerializer
from .permissions import IsCurrentUserOrAdminOnly, IsAuthorOrReadOnly

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
class ProfileView(viewsets.ModelViewSet):
    queryset  = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get','retrieve','put','patch', 'delete']
    permission_classes = [IsAuthenticated, IsCurrentUserOrAdminOnly]

class AuthorView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    
    def get_queryset(self):
        author_ids = Post.objects.values_list('author', flat=True).distinct()
        return User.objects.filter(id__in=author_ids)
    
    
        
    
    