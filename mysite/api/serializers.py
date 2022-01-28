from rest_framework import serializers

from blog.models import Post
from django.contrib.auth.models import User
from users.models import Profile

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = Post
        fields = ['url','id','author','title','content','post_date']
        read_only_fields = ['post_date']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image'] 
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['url','profile','username','email'] 
    
    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     user = User.objects.create_user(**validated_data)
    #     Profile.objects.create(user=user, **profile_data)
    #     return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        
        profile.image = profile_data.get('image', profile.image)
        profile.save()
        return instance
        
class AuthorSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='post-detail')
    class Meta:
        model = User
        fields = ('username', 'email', 'posts')