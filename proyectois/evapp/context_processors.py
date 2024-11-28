from .models import Profesor, Estudiante

def es_profesor(request):

    if request.user.is_authenticated:
        return {'is_profesor': Profesor.objects.filter(user=request.user).exists()}
    return {'is_profesor': False}


def es_estudiante(request):

    if request.user.is_authenticated:
        return {'is_estudiante': Estudiante.objects.filter(user=request.user).exists()}
    return {'is_estudiante': False}
