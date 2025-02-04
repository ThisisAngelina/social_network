from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.TextField(max_length=250)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")
    comments = models.ManyToManyField(User, blank=True, related_name="commented_posts")

    def __str__(self):
        return f"{self.user} posted: {self.content[:50]}..."

    class Meta:
        ordering = ['-timestamp']
        