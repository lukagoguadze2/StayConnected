from django.db import models
from authentication.models import User

from home.models import Tag
from .managers import PostManager


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(to=Tag, blank=True)

    objects = PostManager()

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title


class PostReaction(models.Model):
    LIKE = 1
    DISLIKE = 0
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reaction_type = models.BooleanField(choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'post')

    def __str__(self):
        return f'{self.author} - {self.post}'


class PostSeen(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name="seen_relationships"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="seen_relationships"
    )
    seen_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the user saw the post

    class Meta:
        unique_together = ('post', 'user')
