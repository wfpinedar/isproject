from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .forms import ProfesorForm, EstudianteForm, PreguntaForm, RespuestaForm, EvaluacionForm, ProgramarEvaluacionForm
from .models import Pregunta, Respuesta, Corresponde, Asocia, Asignatura, Profesor, Estudiante, Evalua, Cursa, Imparte, Salon
from .utils import solo_profesores


def base_view(request):
    user = request.user
    is_profesor = False
    is_estudiante = False

    if user.is_authenticated:
        is_profesor = Profesor.objects.filter(user=user).exists()
        is_estudiante = Estudiante.objects.filter(user=user).exists()

    context = {
        'is_profesor': is_profesor,
        'is_estudiante': is_estudiante,
    }

    return render(request, 'base.html', context)


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

@solo_profesores
@login_required
def agregar_pregunta(request):
    if request.method == 'POST':
        form = PreguntaForm(request.POST)
        if form.is_valid():
            pregunta = form.save()
            return redirect(reverse('relacionar_respuestas', kwargs={'pregunta_id': pregunta.id_preg})) 
    else:
        form = PreguntaForm()
    return render(request, 'agregar_pregunta.html', {'form': form})

from django.core.paginator import Paginator

@login_required
@solo_profesores
def listar_preguntas(request):
    preguntas = Pregunta.objects.all().order_by('id_preg')  # Ordenar por ID
    paginator = Paginator(preguntas, 10)  # Paginación: 10 preguntas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listar_preguntas.html', {'page_obj': page_obj})

@login_required
@solo_profesores
def agregar_respuesta(request):
    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la respuesta directamente
            return redirect('listar_respuestas')  # Redirige a una página donde se listan las respuestas
    else:
        form = RespuestaForm()
    return render(request, 'agregar_respuesta.html', {'form': form})


@login_required
@solo_profesores
def listar_respuestas(request):
    respuestas = Respuesta.objects.all().order_by('id_resp')
    return render(request, 'listar_respuestas.html', {'respuestas': respuestas})



@login_required
@solo_profesores
def relacionar_respuestas(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id_preg=pregunta_id)
    respuestas = Respuesta.objects.all()  # Todas las respuestas disponibles
    relaciones_actuales = Corresponde.objects.filter(id_preg=pregunta)

    # Crear una lista de respuestas con su estado (relacionada/correcta)
    respuestas_con_estado = []
    for respuesta in respuestas:
        es_relacionada = relaciones_actuales.filter(id_resp=respuesta).exists()
        es_correcta = relaciones_actuales.filter(id_resp=respuesta, es_correcta=True).exists()
        respuestas_con_estado.append({
            'id': respuesta.id_resp,
            'enunciado': respuesta.enunciado_resp,
            'relacionada': es_relacionada,
            'correcta': es_correcta
        })

    if request.method == 'POST':
        respuestas_seleccionadas = request.POST.getlist('respuestas')  # IDs de respuestas seleccionadas
        respuestas_correctas = request.POST.getlist('es_correcta')  # IDs de respuestas marcadas como correctas

        # Eliminar relaciones existentes y actualizarlas
        Corresponde.objects.filter(id_preg=pregunta).delete()

        for respuesta_id in respuestas_seleccionadas:
            respuesta = Respuesta.objects.get(id_resp=respuesta_id)
            es_correcta = str(respuesta_id) in respuestas_correctas  # Comprobar si es correcta
            Corresponde.objects.create(id_preg=pregunta, id_resp=respuesta, es_correcta=es_correcta)

        return redirect('listar_preguntas')  # Redirige al listado de preguntas

    return render(request, 'relacionar_respuestas.html', {
        'pregunta': pregunta,
        'respuestas_con_estado': respuestas_con_estado,
    })

@login_required
@solo_profesores
def editar_pregunta_completa(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id_preg=pregunta_id)
    respuestas = Respuesta.objects.all()
    relaciones_actuales = Corresponde.objects.filter(id_preg=pregunta)

    # Crear una lista de respuestas con estado (relacionada/correcta)
    respuestas_con_estado = []
    for respuesta in respuestas:
        es_relacionada = relaciones_actuales.filter(id_resp=respuesta).exists()
        es_correcta = relaciones_actuales.filter(id_resp=respuesta, es_correcta=True).exists()
        respuestas_con_estado.append({
            'id': respuesta.id_resp,
            'enunciado': respuesta.enunciado_resp,
            'relacionada': es_relacionada,
            'correcta': es_correcta,
        })

    if request.method == 'POST':
        if 'editar_pregunta' in request.POST:  # Si se envió el formulario de edición
            form = PreguntaForm(request.POST, instance=pregunta)
            if form.is_valid():
                form.save()

        elif 'guardar_respuestas' in request.POST:  # Si se envió el formulario de respuestas
            respuestas_seleccionadas = request.POST.getlist('respuestas')
            respuestas_correctas = request.POST.getlist('es_correcta')

            # Eliminar relaciones existentes y actualizarlas
            Corresponde.objects.filter(id_preg=pregunta).delete()

            for respuesta_id in respuestas_seleccionadas:
                respuesta = Respuesta.objects.get(id_resp=respuesta_id)
                es_correcta = str(respuesta_id) in respuestas_correctas
                Corresponde.objects.create(id_preg=pregunta, id_resp=respuesta, es_correcta=es_correcta)

        return redirect('listar_preguntas')

    form = PreguntaForm(instance=pregunta)
    return render(request, 'editar_pregunta_completa.html', {
        'form': form,
        'pregunta': pregunta,
        'respuestas_con_estado': respuestas_con_estado,
    })
    
@login_required
@solo_profesores
def eliminar_pregunta(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id_preg=pregunta_id)

    if request.method == 'POST':
        pregunta.delete()
        return redirect('listar_preguntas')  # Redirigir al listado de preguntas

    return render(request, 'confirmar_eliminacion.html', {'pregunta': pregunta})


@solo_profesores
@login_required
def agregar_evaluacion(request):
    profesor = request.user.profesor
    if request.method == 'POST':
        form = EvaluacionForm(request.POST, profesor = profesor)
        if form.is_valid():
            preguntas = form.cleaned_data['preguntas']
            asignatura = form.cleaned_data['asignatura']
            fecha = form.cleaned_data['fecha']
            for pregunta in preguntas:
                Asocia.objects.create(id_preg = pregunta, id_asig = asignatura, fecha = fecha)
            return redirect(reverse('listar_evaluacion'))
                
    else:
        form = EvaluacionForm(profesor = profesor)
    return render(request, 'agregar_evaluacion.html', {'form': form})


@login_required
@solo_profesores
def listar_evaluaciones(request):
    evaluaciones = Asocia.objects.values(
        'id_asig', 'fecha'
    ).annotate(numero_preguntas=Count('id_preg'))

    evaluaciones_data = [
        {
            'asignatura': Asignatura.objects.get(id_asig=evaluacion['id_asig']).nombre_asig,
            'fecha': evaluacion['fecha'],
            'numero_preguntas': evaluacion['numero_preguntas'],
        }
        for evaluacion in evaluaciones
    ]

    return render(request, 'listar_evaluaciones.html', {'evaluaciones': evaluaciones_data})

@login_required
@solo_profesores
def programar_evaluacion(request):
    profesor = request.user.profesor  # Relación entre el usuario y el modelo Profesor
    if request.method == 'POST':
        form = ProgramarEvaluacionForm(request.POST, profesor=profesor)

        # Obtener la asignatura seleccionada
        asignatura_id = request.POST.get('asignatura')
        if asignatura_id:
            # Actualizar las opciones de grupo
            grupos = (
                Cursa.objects.filter(id_asig=asignatura_id)
                .values_list('grupo', 'grupo')
                .distinct()
            )
            form.fields['grupo'].choices = grupos

            # Actualizar las opciones de evaluación
            evaluaciones = (
                Asocia.objects.filter(id_asig=asignatura_id)
                .values('id_asig_id', 'fecha')
                .distinct()
            )
            form.fields['evaluacion'].choices = [
                (f"{evaluacion['id_asig_id']}|{evaluacion['fecha']}", f"Evaluación - {evaluacion['fecha'].strftime('%Y-%m-%d')}")
                for evaluacion in evaluaciones
            ]

        # Validar el formulario
        if form.is_valid():
            asignatura = form.cleaned_data['asignatura']
            grupo = form.cleaned_data['grupo']
            evaluacion = form.cleaned_data['evaluacion']
            salon = form.cleaned_data['salon']

            # Descomponer la clave compuesta (id_asig|fecha)
            id_asig, fecha = evaluacion.split('|')

            # Obtener la instancia de Imparte
            imparte = Imparte.objects.filter(id_pro=profesor, id_asig=id_asig, grupo=grupo).first()
            if not imparte:
                return JsonResponse({'error': 'No se encontró relación entre profesor, asignatura y grupo.'}, status=400)

            # Obtener estudiantes del grupo seleccionado
            estudiantes = Estudiante.objects.filter(cursa__id_asig=id_asig, cursa__grupo=grupo)

            # Obtener las preguntas de la evaluación seleccionada
            preguntas = Pregunta.objects.filter(id_preg__in=Asocia.objects.filter(id_asig=id_asig, fecha=fecha).values_list('id_preg', flat=True))


            # Crear relaciones en Evalua
            for estudiante in estudiantes:
                for pregunta in preguntas:
                    # Verificar si ya existe
                    if not Evalua.objects.filter(
                        id_pro=imparte,
                        id_asig=id_asig,
                        grupo=grupo,
                        id_est=estudiante,
                        id_preg=pregunta,
                        fecha=fecha,
                        id_salon=salon
                    ).exists():
                        # Crear solo si no existe
                        # try:
                        Evalua.objects.create(
                            id_pro=imparte,
                            id_asig=id_asig,
                            grupo=grupo,
                            id_est=estudiante,
                            id_preg=pregunta,
                            fecha=fecha,
                            id_salon=salon
                        )
                        # except IntegrityError:
                        #     print("Ha ocurrido un error de integridad en los datos")
                        #     pass

            return redirect('listar_evaluacion')

    else:
        form = ProgramarEvaluacionForm()
        # Filtrar asignaturas que el profesor dicta
        form.fields['asignatura'].queryset = Asignatura.objects.filter(imparte__id_pro=profesor)

    return render(request, 'programar_evaluacion.html', {'form': form})

@login_required
def obtener_datos_dinamicos(request):
    asignatura_id = request.GET.get('asignatura_id')  # Obtenemos el ID de la asignatura seleccionada

    if not asignatura_id:
        return JsonResponse({'error': 'No se proporcionó asignatura_id'}, status=400)

    # Obtener grupos asociados a la asignatura
    grupos = (
        Cursa.objects.filter(id_asig=asignatura_id)
        .values_list('grupo', flat=True)
        .distinct()
    )
    print(grupos)
    # Obtener evaluaciones asociadas a la asignatura
    evaluaciones = (
        Asocia.objects.filter(id_asig=asignatura_id)
        .values('id_asig_id', 'fecha')
        .distinct()
    )

    # Crear una representación única para cada evaluación
    evaluaciones_formateadas = [
        {
            'id': f"{evaluacion['id_asig_id']}|{evaluacion['fecha']}",
            'texto': f"Evaluación - {evaluacion['fecha'].strftime('%Y-%m-%d')}"
        }
        for evaluacion in evaluaciones
    ]
    print(evaluaciones_formateadas)
    return JsonResponse({
        'grupos': list(grupos),
        'evaluaciones': list(evaluaciones_formateadas),
    })
    
@login_required
@solo_profesores
def listar_evaluacion_programada(request):
    profesor = request.user.profesor  # Relación entre usuario y profesor

    evaluaciones = (
        Evalua.objects.filter(id_pro__id_pro=profesor.id_pro)  # Filtrar evaluaciones del profesor logueado
        .values('id_asig__nombre_asig', 'grupo', 'fecha', 'id_salon__id_salon', 'id_salon__capacidad')
        .annotate(num_estudiantes=Count('id_est', distinct=True))
        .order_by('fecha')  # Ordenar por fecha
    )

    return render(request, 'listar_evaluacion_programada.html', {'evaluaciones': evaluaciones})