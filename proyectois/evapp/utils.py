from django.http import HttpResponseForbidden
from .models import Profesor

def solo_profesores(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            # Verifica si el usuario está registrado como profesor
            request.user.profesor
        except Profesor.DoesNotExist:
            return HttpResponseForbidden("Solo los profesores pueden realizar esta acción.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
