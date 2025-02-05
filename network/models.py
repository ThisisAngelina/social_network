from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")
    active = models.BooleanField(default=True) # the admin can block users
    
    def __str__(self):
        return f"{self.user} posted: {self.content[:50]}..."

    def like_count(self):
        return self.likes.count()
    
    class Meta:
        ordering = ['-timestamp']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)


class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_accounts')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')  # Prevent duplicate follows\
    
    def clean(self):
        """Prevent users from following themselves."""
        if self.follower == self.followed:
            raise ValidationError("A user cannot follow themselves.")

    def save(self, *args, **kwargs):
        """Run clean() before saving to enforce validation."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower} follows {self.followed}"
        