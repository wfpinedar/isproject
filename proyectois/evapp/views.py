from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfesorForm, EstudianteForm



def registro_profesor(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = ProfesorForm()
    return render(request, 'registro_profesor.html', {'form': form})


def registro_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = EstudianteForm()
    return render(request, 'registro_estudiante.html', {'form': form})

@login_required
def redireccionar_despues_de_login(request):
    if hasattr(request.user, 'estudiante'):
        return redirect('home_estudiante')
    elif hasattr(request.user, 'profesor'):
        return redirect('home_profesor')
    else:
        return redirect('home_generico')
    
@login_required
def home_estudiante(request):
    return render(request, 'home_estudiante.html')

@login_required
def home_profesor(request):
    return render(request, 'home_profesor.html')

def home_generico(request):
    return render(request, 'home_generico.html')
