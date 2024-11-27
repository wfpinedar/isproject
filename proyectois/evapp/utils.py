from django.db import connection
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



def insertar_respuesta_manual(id_pro, id_asig, grupo, id_est, fecha, id_preg, id_resp):
    """
    Inserta manualmente una respuesta en la tabla Responde usando SQL crudo.
    """
    query = """
        INSERT INTO responde (id_pro, id_asig, grupo, id_est, fecha, id_preg, id_resp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        id_pro.pk if hasattr(id_pro, 'pk') else id_pro,  # ID del objeto o valor directo
        id_asig.pk if hasattr(id_asig, 'pk') else id_asig,  # ID del objeto o valor directo
        grupo,
        id_est.pk if hasattr(id_est, 'pk') else id_est,  # ID del objeto o valor directo
        fecha,
        id_preg.pk if hasattr(id_preg, 'pk') else id_preg,  # ID del objeto o valor directo
        id_resp.pk if hasattr(id_resp, 'pk') else id_resp   # ID del objeto o valor directo
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
        print("Respuesta insertada manualmente en la base de datos.")
        return True
    except Exception as e:
        print(f"Error al insertar manualmente: {e}")
        return False