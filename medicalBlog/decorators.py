from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import get_object_or_404
from .models import Blog

def is_author(user, blog_id):
    blog_post = get_object_or_404(Blog, pk=blog_id)
    return blog_post.author == user.profile

def author_access_only():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            blog_id = kwargs.get('pk')  # Adjust based on your URL configuration
            if not is_author(request.user, blog_id):
                return HttpResponseForbidden("Only the author is allowed to edit this post.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Decorator to ensure the user is a doctor
def doctor_test_function(user):
    if user.profile.account_user_type == 'doctor':
        return True
    return False

def doctor_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not doctor_test_function(request.user):
                return HttpResponse("Only Doctors are allowed to create blogs")
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator
