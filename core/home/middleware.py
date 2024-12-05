import logging
from time import sleep

from django.db import connection
from django.utils.timezone import now
from rest_framework.response import Response

from home import ratings

logger = logging.getLogger(__name__)


class DatabaseRetryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        retries = 5
        while retries > 0:
            try:
                connection.ensure_connection()
                break
            except Exception as e:
                retries -= 1
                logger.error(
                    f"Database connection failed (retries left: {retries})." 
                    f"Error: {e}",
                    exc_info=True
                )
                if retries == 0:
                    logger.critical(
                        "Database connection failed after multiple retries."
                    )
                    return Response(
                        {
                            "detail": (
                                "Service temporarily unavailable due to database failure."
                            )
                        },
                        status=503
                    )
                sleep(1)
        return self.get_response(request)


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            current_time = now()
            last_activity = request.user.last_activity or now()
            inactive_days = (current_time - last_activity).days
            if inactive_days > 1:
                request.user.update_rating(
                    ratings.INACTIVITY_PENALTY * inactive_days
                )

            request.user.last_activity = now()
            request.user.save()

        return response
