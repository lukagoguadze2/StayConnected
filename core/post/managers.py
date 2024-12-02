from django.apps import apps
from django.db import models
from django.db.models import Exists, OuterRef, Q, Count


class PostManager(models.Manager):
    def prefetch_posts(self):
        return (self
            .prefetch_related('tags')
            .prefetch_related('author')
            .prefetch_related('postreaction_set')
        ).order_by('-date_posted')

    def annotate_with_seen_by_user(self, user):
        post_reaction = apps.get_model(
            app_label='post',
            model_name='PostReaction'
        )
        return self.prefetch_posts().annotate(
                seen_by_user=Exists(
                    apps.get_model(
                        app_label='post',
                        model_name='PostSeen'
                    ).objects.filter(
                        post=OuterRef('pk'),
                        user=user
                    )
                ),
                like_count=Count(
                    'postreaction',
                    filter=Q(postreaction__reaction_type=post_reaction.LIKE),
                ),
                dislike_count=Count(
                    'postreaction',
                    filter=Q(postreaction__reaction_type=post_reaction.DISLIKE),
                ),
                comment_count=Count('comments', distinct=True),
                has_correct_answer=Exists(
                    apps.get_model(
                        app_label='comment',
                        model_name='Comment'
                    ).objects.filter(
                        post=OuterRef('pk'),
                        is_correct=True
                    )
                )
            )
