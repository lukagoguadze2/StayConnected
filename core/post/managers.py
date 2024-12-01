from django.apps import apps
from django.db import models
from django.db.models import Exists, OuterRef


class PostManager(models.Manager):
    def prefetch_posts(self):
        return (self
            .prefetch_related('tags')
            .prefetch_related('author')
        )

    def annotate_with_seen_by_user(self, user):
        return self.prefetch_posts().annotate(
                seen_by_user=Exists(
                    apps.get_model(
                        app_label='post',
                        model_name='PostSeen'
                    ).objects.filter(
                        post=OuterRef('pk'),
                        user=user
                    )
                )
            )
