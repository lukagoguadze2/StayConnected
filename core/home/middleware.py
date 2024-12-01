from django.db import connection
from time import sleep


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
                if retries == 0:
                    raise e
                sleep(1)
        return self.get_response(request)
