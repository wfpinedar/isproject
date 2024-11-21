from django.contrib import admin
from .models import Profesor, Asignatura, Estudiante

# Register your models here.
@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('id_pro', 'nombre_pro') 

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('id_asig', 'nombre_asig')

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('id_est', 'nombre_est')