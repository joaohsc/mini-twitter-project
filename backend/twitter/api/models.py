from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    text =  models.CharField(max_length=280)
    image = models.ImageField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
