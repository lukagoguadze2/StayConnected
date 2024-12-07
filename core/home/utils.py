from better_profanity import profanity

from post.models import Post

profanity.load_censor_words()


def contains_prohibited_words(text):
    return profanity.contains_profanity(text)


def django_filter_warning(get_queryset_func):
    """
    This decorator is used to fix a warning in django-filter.
    See: https://github.com/carltongibson/django-filter/issues/966
    """
    def get_queryset(self):
        # Return an empty queryset if this is a swagger_fake_view call.
        if getattr(self, "swagger_fake_view", False):
            return Post.objects.none()
        return get_queryset_func(self)

    return get_queryset
