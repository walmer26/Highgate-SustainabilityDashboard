from django.core.cache import cache
from django.contrib import messages

class PopulateDataMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        message = cache.get('populate_data_message')
        if message:
            messages.add_message(request, messages.SUCCESS, message)
            cache.delete('populate_data_message')
        return response
