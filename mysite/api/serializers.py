from rest_framework import serializers

from blog.models import Post
from django.contrib.auth.models import User
from users.models import Profile

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','author','title','content','post_date']

class ProfileSerializer(serializers.Modelserializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image'] 
class UserSerializer(serializers.ModleSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['id', 'profile']
        
