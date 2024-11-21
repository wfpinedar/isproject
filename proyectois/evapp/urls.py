from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomLoginForm
from . import views

urlpatterns = [
    path('login/',LoginView.as_view(template_name='login.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/profesor/', views.registro_profesor, name='registro_profesor'),
    path('registro/estudiante/', views.registro_estudiante, name='registro_estudiante'),
    path('accounts/login/', views.redireccionar_despues_de_login, name='redireccionar_login'),
    path('home/estudiante/', views.home_estudiante, name='home_estudiante'),
    path('home/profesor/', views.home_profesor, name='home_profesor'),
    path('', views.home_generico, name='home_generico'),
]