from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:10]}..."  # Display first 20 characters of content
    


class Like(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    user  = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tweet', 'user')

class Comment(models.Model):
    tweet      = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    content    = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)


