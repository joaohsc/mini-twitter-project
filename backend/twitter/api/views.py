from django.contrib.auth.models import User
from .models import Post, PostLike, Follower
from rest_framework import generics
from .serializers import UserSerializer,PostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
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

class UserFollowerListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk, format=None):
        followers = Follower.objects.filter(user=pk)
        users = [ f.follower for f in followers ]

        serializer = UserSerializer(users, many=True) 
        return Response(serializer.data)

class UserFollowingListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk, format=None):
        following = Follower.objects.filter(follower=pk)
        users = [ f.user for f in following ]

        serializer = UserSerializer(users, many=True) 
        return Response(serializer.data)

class UserFollowView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    # follow
    def post(self, request, pk, format=None):
        followed_user = self.get_object(pk)
        if request.user == followed_user:
            return Response({"message": "You cannot follow your profile"}, status=status.HTTP_400_BAD_REQUEST)
        
        obj, created = Follower.objects.get_or_create(user=followed_user,follower = request.user )

        if created:
            return Response({"message": "User followed successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You already follow this user"}, status=status.HTTP_200_OK)
        
    # unfollow
    def delete(self, request, pk, format=None):
        followed_user = self.get_object(pk)
        
        try:
            follower = Follower.objects.get(user=followed_user,follower = request.user)
            follower.delete()
            return Response({"message": "Unfollow successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Follower.DoesNotExist:
            return Response({"error": "You do not follow this user"}, status=status.HTTP_404_NOT_FOUND)
        
class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        following = Follower.objects.filter(follower=user)
        users = [f.user for f in following]
        posts = Post.objects.filter(user__in= users).order_by('-created_at')
        return posts

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
        
    def post(self, request, pk, format=None):
        post = self.get_object(pk)
        
        obj, created = PostLike.objects.get_or_create(user=request.user,post=post)

        if created:
            return Response({"message": "Post liked successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You already liked this post"}, status=status.HTTP_200_OK)
        
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        
        try:
            post_like = PostLike.objects.get(user=request.user, post=post)
            return Response({"message": "Unliked successfully"}, status=status.HTTP_204_NO_CONTENT)
        except PostLike.DoesNotExist:
            return Response({"error": "You didn't liked this post."}, status=status.HTTP_404_NOT_FOUND)

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