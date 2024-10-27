from django.db import models
from django.contrib.auth.models import User
from datetime import datetime as dt

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    @property
    def followers_count(self):
        return Follower.objects.filter(user=self.user).count()
    @property
    def following_count(self):
        return Follower.objects.filter(follower=self.user).count()

class Post(models.Model):
    text =  models.CharField(max_length=250)
    image = models.ImageField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField( auto_now_add = True )
    
    @property
    def like_count(self):
        return PostLike.objects.filter(post=self).count()

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')



