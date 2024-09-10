from django.core.cache import cache
from django.contrib import messages

class TaskCompletionMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for a task completion message in the cache
        task_message = cache.get('task_completion_message')
        
        # Ensure the message is only shown once to the user
        if task_message and not request.session.get('task_message_shown', False):
            messages.add_message(request, messages.SUCCESS, task_message)
            # Mark the message as shown in the session
            request.session['task_message_shown'] = True
            cache.delete('task_completion_message')  # Optionally, clear it if not needed

        response = self.get_response(request)
        return response
