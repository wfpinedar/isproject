from django.db.models.signals import post_migrate
from django.db import connection
from django.dispatch import receiver

@receiver(post_migrate)
def ajustar_secuencias(sender, **kwargs):
    with connection.cursor() as cursor:
        # Ajustar la secuencia para la tabla "respuestas"
        cursor.execute("""
            SELECT setval(pg_get_serial_sequence('"respuesta"', 'id_resp'), 
            COALESCE(MAX(id_resp), 1)) FROM respuesta
        """)
        # Ajustar la secuencia para la tabla "preguntas"
        cursor.execute("""
            SELECT setval(pg_get_serial_sequence('"pregunta"', 'id_preg'), 
            COALESCE(MAX(id_preg), 1)) FROM pregunta
        """)
