from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomLoginForm
from . import views

urlpatterns = [
    path('login/',LoginView.as_view(template_name='login.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='home_generico'), name='logout'),
    path('registro/profesor/', views.registro_profesor, name='registro_profesor'),
    path('registro/estudiante/', views.registro_estudiante, name='registro_estudiante'),
    path('accounts/login/', views.redireccionar_despues_de_login, name='redireccionar_login'),
    path('home/estudiante/', views.home_estudiante, name='home_estudiante'),
    path('home/profesor/', views.home_profesor, name='home_profesor'),
    path('', views.home_generico, name='home_generico'),
    path('preguntas/agregar/', views.agregar_pregunta, name='agregar_pregunta'),
    path('preguntas/listar/', views.listar_preguntas, name='listar_preguntas'),
    path('respuestas/agregar/', views.agregar_respuesta, name='agregar_respuesta'),
    path('respuestas/listar/', views.listar_respuestas, name='listar_respuestas'),
    path('preguntas/<int:pregunta_id>/relacionar_respuestas/', views.relacionar_respuestas, name='relacionar_respuestas'),
    path('preguntas/<int:pregunta_id>/editar_completo/', views.editar_pregunta_completa, name='editar_pregunta_completa'),
    path('preguntas/<int:pregunta_id>/eliminar/', views.eliminar_pregunta, name='eliminar_pregunta'),
    path('evaluaciones/agregar/', views.agregar_evaluacion, name='agregar_evaluacion'),
    path('evaluaciones/listar/', views.listar_evaluaciones, name='listar_evaluacion'),
    path('evaluaciones/programar/', views.programar_evaluacion, name='programar_evaluacion'),
    path('evalua/obtener_datos_dinamicos/', views.obtener_datos_dinamicos, name='obtener_datos_dinamicos'),
    path('evaluaciones/programadas/', views.listar_evaluacion_programada, name='listar_evaluacion_programada'),
    path('evaluaciones/estudiante/', views.listar_evaluaciones_estudiante, name='listar_evaluaciones_estudiante'),
    path('evaluaciones/presentar/<str:asignatura>/<str:fecha>/<str:grupo>/',views.presentar_evaluacion,name='presentar_evaluacion'),
    path('evaluaciones/responder/<str:asignatura>/<str:fecha>/<str:grupo>/',views.responder_evaluacion,name='responder_evaluacion'),
]