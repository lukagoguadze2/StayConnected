from django.db import models
from authentication.models import User
from post.models import Post


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )

    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    is_correct = models.BooleanField(default=False)
    date_answered = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.author:
            self.author, created = User.objects.get_or_create(username='DeletedUser')

        super().save(*args, **kwargs)

    def __str__(self):
        return 'Correct' if self.is_correct else 'Incorrect' + f' answer by {self.author} - post: {self.post.id}'


class CommentReaction(models.Model):
    LIKE = 1
    DISLIKE = 0
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reaction_type = models.BooleanField(choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'comment')

    def __str__(self):
        return 'dis' if not self.reaction_type else '' + f'liked by {self.author} - comment: {self.comment.id}'

