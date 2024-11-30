from django.db import models
from authentication.models import User

class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,  
    )

    liked_by = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True,
    )

    unliked_by = models.ManyToManyField(
        User,
        related_name='unliked_posts',
        blank=True,
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        if not self.author:
            self.author, created = User.objects.get_or_create(username='DeletedUser')
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,  
    )

    liked_by = models.ManyToManyField(
        User,
        related_name='liked_comments',
        blank=True,
    )

    unliked_by = models.ManyToManyField(
        User,
        related_name='unliked_comments',
        blank=True,
    )

    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments',
    )
    
    is_correct = models.BooleanField(default=False)
    date_answered = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.author:
            self.author, created = User.objects.get_or_create(username='DeletedUser')
        super(Post, self).save(*args, **kwargs)

