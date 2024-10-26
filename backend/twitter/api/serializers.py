from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = { "password": { "write_only": True } }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id","text", "image", "user"]
        extra_kwargs = { "user": { "read_only": True } }