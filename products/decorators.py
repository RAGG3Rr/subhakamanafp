from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authroized to view this page.')
    
    return wrapper_func
   