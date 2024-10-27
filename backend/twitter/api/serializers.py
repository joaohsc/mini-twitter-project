from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Post, PostLike, Follower, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = { "password": { "write_only": True } }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    user_id = serializers.IntegerField(source='user.id')
    class Meta:
        model = Profile
        fields = ["id", "user_id","username","email","created_at", "followers_count", "following_count"]
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id","text", "image", "user", "like_count", "created_at"]
        extra_kwargs = { "user": { "read_only": True } }