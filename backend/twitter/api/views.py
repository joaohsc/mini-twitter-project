from django.contrib.auth.models import User
from .models import Post
from rest_framework import generics
from .serializers import UserSerializer,PostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
import os

class CreateUserView(APIView):
    permission_classes = [AllowAny]
    def post(self,request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, format=None):
        users = User.objects.all() 
        serializer = UserSerializer(users, many=True) 
        return Response(serializer.data)

class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True) 
        return Response(serializer.data)

class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def delete_file(self, path):
        if os.path.isfile(path):
            os.remove(path)

    def check_Ownership(self,owner, user):
        if owner.id != user.id:
            raise ValidationError("You do not own this item to edit!")

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        owner = post.user
        self.check_Ownership(owner, request.user)

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        post = self.get_object(pk)
        owner = post.user
        self.check_Ownership(owner, request.user)
       
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        owner = post.user
        self.check_Ownership(owner, request.user)

        file = post.image
        post.delete()
        self.delete_file(file.path)
        return Response(status=status.HTTP_204_NO_CONTENT)