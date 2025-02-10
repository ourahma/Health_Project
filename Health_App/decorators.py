from django.core.exceptions import PermissionDenied
from .models import *

def medcin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not isinstance(request.user, Medcin):
            raise PermissionDenied("Only Medcin can access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper
