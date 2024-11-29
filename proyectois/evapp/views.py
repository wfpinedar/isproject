from django.db import IntegrityError
from django.http import JsonResponse
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg
from django.db.models.functions import TruncDate
from django.utils.timezone import now
from collections import defaultdict
from .forms import ProfesorForm, EstudianteForm, PreguntaForm, RespuestaForm, EvaluacionForm, ProgramarEvaluacionForm, ResponderEvaluacionForm
from .models import (Pregunta, Respuesta, Corresponde, Asocia, Asignatura, Profesor, Estudiante, Evalua, Cursa, Imparte, Salon, 
    Responde, Evaluacreate, Asociacreate, RespondeInsert)
from .utils import solo_profesores, insertar_respuesta_manual


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
    if hasattr(request.user, 'profesor'):
        return redirect('home_profesor')
    elif hasattr(request.user, 'estudiante'):
        return redirect('home_estudiante')
    return redirect('login')
    
@login_required
def home_estudiante(request):
    return render(request, 'home_estudiante.html')

@login_required
def home_profesor(request):
    is_profesor = Profesor.objects.filter(user=request.user).exists()
    context = {
        'is_profesor': is_profesor,
    }
    return render(request, 'home_profesor.html', context)

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
                Asociacreate.objects.create(id_preg = pregunta, id_asig = asignatura, fecha = fecha)
            return redirect(reverse('listar_evaluacion'))
                
    else:
        form = EvaluacionForm(profesor = profesor)
    return render(request, 'agregar_evaluacion.html', {'form': form})


@login_required
@solo_profesores
def listar_evaluaciones(request):
    profesor = request.user.profesor
    evaluaciones = Asocia.objects.values(
        'id_asig', 'fecha'
    ).annotate(numero_preguntas=Count('id_preg'))
    
    evaluaciones_data = [
        {
            'asignatura': Asignatura.objects.get(id_asig=evaluacion['id_asig']).nombre_asig,
            'fecha': evaluacion['fecha'],
            'numero_preguntas': evaluacion['numero_preguntas'],
            'grupo': (
                        Imparte.objects.filter(
                            id_pro=profesor.id_pro,
                            id_asig=evaluacion['id_asig']
                        )
                        .values_list('grupo', flat=True)
                        .first()
                    )
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
                (f"{evaluacion['id_asig_id']}|{evaluacion['fecha']}", f"Evaluación - {evaluacion['fecha'].strftime('%Y-%m-%d')} - {evaluacion['id_asig_id']}")
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
                        Evaluacreate.objects.create(
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


@login_required
def listar_evaluaciones_estudiante(request):
    estudiante = request.user.estudiante
    evaluaciones = (
        Evalua.objects.filter(id_est=estudiante)
        .values('id_asig__nombre_asig', 'grupo', 'fecha', 'id_salon__id_salon', 'id_salon__capacidad')
        .distinct()
        .order_by('fecha')
    )

    return render(request, 'listar_evaluaciones_estudiante.html', {'evaluaciones': evaluaciones})

from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
@login_required
def presentar_evaluacion(request, asignatura, fecha, grupo):
    # Obtener la asignatura
    asignatura_obj = get_object_or_404(Asignatura, nombre_asig=asignatura)

    # Obtener al estudiante actual
    estudiante = request.user.estudiante

    # Convertir la fecha a un objeto datetime
    # try:
    #     fecha_obj = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    # except ValueError:
    #     messages.error(request, "Fecha inválida.")
    #     return redirect('evaluaciones')  # Redirigir a una página de evaluaciones, si existe.
    
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')

    # Verificar si el estudiante ya respondió alguna pregunta de esta evaluación
    evaluacion_respondida = Responde.objects.filter(
        id_asig=asignatura_obj,
        grupo=grupo,
        id_est=estudiante,
        fecha=fecha_obj
    ).exists()

    if evaluacion_respondida:
        evaluacion = Evalua.objects.filter(
            id_est__id_est=estudiante.id_est,
            id_asig__id_asig=asignatura_obj.id_asig,
            grupo=grupo,
            fecha=fecha_obj) \
        .values('nota') \
        .annotate(num_estudiantes=Count('nota', distinct=True)) \
        .order_by('nota').first()
        nota = evaluacion['nota']
        messages.info(request, "Ya has presentado esta evaluación.")
        return render(request, 'presentar_evaluacion.html', {
            'asignatura': asignatura,
            'fecha': fecha,
            'grupo': grupo,
            'nota': nota
        })
    # Validar rango de tiempo para presentación (fecha + 2 horas)
    inicio = fecha_obj
    fin = fecha_obj + timedelta(hours=2)
    tiempo_actual = now().replace(tzinfo=None) - timedelta(hours=5)
    
    print(inicio, tiempo_actual, fin, "******************************************")
    if not inicio <= tiempo_actual <= fin:
        messages.error(request, "Esta evaluación solo puede presentarse en el horario permitido.")
        return redirect('listar_evaluaciones_estudiante')

    # Calcular tiempo restante en segundos para el temporizador
    tiempo_restante = int((fin - tiempo_actual).total_seconds())
    
    # Si no ha sido respondida, redirigir a la URL de responder_evaluacion
    return redirect('responder_evaluacion', asignatura=asignatura, fecha=fecha, grupo=grupo, tiempo_restante=tiempo_restante)
    # return render(request, 'responder_evaluacion.html', {
    #     'asignatura': asignatura,
    #     'fecha': fecha,
    #     'grupo': grupo,
    #     'tiempo_restante': tiempo_restante
    # })
    


@login_required
def responder_evaluacion(request, asignatura, grupo, fecha, tiempo_restante):
    asignatura_id = Asignatura.objects.get(nombre_asig=asignatura).id_asig
    estudiante = request.user.estudiante

    # Convertir fecha de la URL a un objeto datetime
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')

    # Verificar que el estudiante está inscrito en el grupo y asignatura
    imparte = Imparte.objects.filter(id_asig=asignatura_id, grupo=grupo).first()
    if not imparte:
        return render(request, 'error.html', {'mensaje': 'No estás inscrito en esta asignatura y grupo.'})

    # preguntas = Pregunta.objects.filter(
    #     evalua__id_asig=asignatura_id, 
    #     evalua__grupo=grupo, 
    #     evalua__fecha=fecha_obj, 
    #     evalua__id_est=estudiante)
    preguntas = Pregunta.objects.annotate(fecha_truncada=TruncDate('evalua__fecha')).filter(
                evalua__id_asig=asignatura_id,
                evalua__grupo=grupo,
                fecha_truncada=fecha_obj,
                evalua__id_est=estudiante
            ).distinct()
    # print(preguntas, "<------------------------------- 2!")
    
    if request.method == 'POST':
        form = ResponderEvaluacionForm(request.POST, preguntas=preguntas)
        if form.is_valid():
            for pregunta in preguntas:
                field_name = f'pregunta_{pregunta.id_preg}'
                try:
                    if pregunta.tipo_preg == 'unique':
                        respuesta = form.cleaned_data[field_name]
                        RespondeInsert.objects.create(
                            id_pro=imparte.id_pro_id,
                            id_asig=asignatura_id,
                            grupo=grupo,
                            id_est=estudiante.id_est,
                            fecha=fecha_obj,
                            id_preg=pregunta.id_preg,
                            id_resp=respuesta.id_resp
                        )
                    elif pregunta.tipo_preg == 'multiple':
                        respuestas = form.cleaned_data[field_name]
                        for respuesta in respuestas:
                            if not Responde.objects.filter(
                                id_pro=imparte,
                                id_asig=asignatura_id,
                                grupo=grupo,
                                id_est=estudiante,
                                fecha=fecha_obj,
                                id_preg=pregunta,
                                id_resp=respuesta
                            ).exists():
                                RespondeInsert.objects.create(
                                    id_pro=imparte.id_pro_id,
                                    id_asig=asignatura_id,
                                    grupo=grupo,
                                    id_est=estudiante.id_est,
                                    fecha=fecha_obj,
                                    id_preg=pregunta.id_preg,
                                    id_resp=respuesta.id_resp
                                )
                    elif pregunta.tipo_preg == 'true_false':
                        respuesta_vf = form.cleaned_data[field_name]
                        RespondeInsert.objects.create(
                            id_pro=imparte.id_pro_id,
                            id_asig=asignatura_id,
                            grupo=grupo,
                            id_est=estudiante.id_est,
                            fecha=fecha_obj,
                            id_preg=pregunta.id_preg,
                            id_resp=respuesta_vf.id_resp
                        )
                except Exception as e:
                    # Llamar a la función de inserción manual en caso de error
                    print(f"Error al insertar en Responde: {e}")
                    if pregunta.tipo_preg == 'unique':
                        respuesta = form.cleaned_data[field_name]
                        insertar_respuesta_manual(
                        id_pro=imparte.id_pro,
                        id_asig=asignatura_id,
                        grupo=grupo,
                        id_est=estudiante.id_est,
                        fecha=fecha_obj,
                        id_preg=pregunta.id_preg,
                        id_resp=respuesta.id_resp
                    )
                    elif pregunta.tipo_preg == 'multiple':
                        respuestas = form.cleaned_data[field_name]
                        for respuesta in respuestas:
                            insertar_respuesta_manual(
                            id_pro=imparte.id_pro,
                            id_asig=asignatura_id,
                            grupo=grupo,
                            id_est=estudiante.id_est,
                            fecha=fecha_obj,
                            id_preg=pregunta.id_preg,
                            id_resp=respuesta.id_resp
                        )
                    elif pregunta.tipo_preg == 'true_false':
                        respuesta_vf = form.cleaned_data[field_name]
                        insertar_respuesta_manual(
                        id_pro=imparte.id_pro,
                        id_asig=asignatura_id,
                        grupo=grupo,
                        id_est=estudiante.id_est,
                        fecha=fecha_obj,
                        id_preg=pregunta.id_preg,
                        id_resp=respuesta_vf.id_resp
                    )
                    
                    # Calcular nota
            respuestas_correctas = 0
            total_preguntas = 0

            # Obtener todas las preguntas respondidas en esta evaluación
            preguntas = Pregunta.objects.annotate(fecha_truncada=TruncDate('evalua__fecha')).filter(
                evalua__id_asig=asignatura_id,
                evalua__grupo=grupo,
                fecha_truncada=fecha_obj,
                evalua__id_est=estudiante
            ).distinct()

            for pregunta in preguntas:
                # Incrementar el contador de preguntas
                total_preguntas += 1

                # Verificar si la respuesta es correcta
                respuestas_estudiante = Responde.objects.annotate(fecha_truncada=TruncDate('fecha')).filter(
                    id_pro__id_asig=asignatura_id,
                    id_est=estudiante,
                    fecha_truncada=fecha_obj,
                    id_preg=pregunta
                ).values_list('id_resp', flat=True)

                respuestas_correctas_db = Corresponde.objects.filter(
                    id_preg=pregunta,
                    es_correcta=True
                ).values_list('id_resp', flat=True)

                # Comprobar si todas las respuestas del estudiante coinciden con las correctas
                if set(respuestas_estudiante) == set(respuestas_correctas_db):
                    respuestas_correctas += 1
                
            # Calcular nota como porcentaje
            if total_preguntas > 0:
                nota = (respuestas_correctas / total_preguntas) * 5
            else:
                nota = 0
            # **Actualizar el campo nota en Evalua**
            # Evalua.objects.annotate(fecha_truncada=TruncDate('fecha')).filter(
            #     id_asig=asignatura_id,
            #     grupo=grupo,
            #     id_est=estudiante,
            #     fecha_truncada=fecha_obj
            # ).update(nota=nota)
            
            if Evalua.objects.annotate(fecha_truncada=TruncDate('fecha')).filter(
                id_asig=asignatura_id,
                grupo=grupo,
                id_est=estudiante,
                fecha_truncada=fecha_obj
            ).exists():
                # Validar el valor de la nota antes de actualizar
                if nota < 0 or nota > 5.0:
                    raise ValueError(f"El valor de la nota ({nota}) está fuera del rango permitido (0-5).")

                try:
                    # Actualizar solo si la nota está dentro del rango permitido
                    Evalua.objects.annotate(fecha_truncada=TruncDate('fecha')).filter(
                        id_asig=asignatura_id,
                        grupo=grupo,
                        id_est=estudiante,
                        fecha_truncada=fecha_obj
                    ).update(nota=nota)
                except IntegrityError as e:
                    print(f"Error de integridad al actualizar la nota: {e}")
            return render(request, 'confirmacion.html', {'mensaje': 'Respuestas enviadas con éxito.', 'nota': nota})
    else:
        form = ResponderEvaluacionForm(preguntas=preguntas)

    return render(request, 'responder_evaluacion.html', {'form': form, 'tiempo_restante':tiempo_restante})


@login_required
@solo_profesores
def consultar_resultados(request, asignatura, grupo, fecha):
    # Obtener el profesor actual
    profesor = request.user.profesor

    # Validar que el profesor dicta esta asignatura en el grupo especificado
    imparte = get_object_or_404(Imparte, id_pro=profesor, id_asig__nombre_asig=asignatura, grupo=grupo)
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    # Obtener los resultados promedio de los estudiantes para la asignatura y grupo
    resultados = Evalua.objects.filter(
        id_pro=imparte,
        id_asig=imparte.id_asig,
        grupo=grupo,
        fecha=fecha_obj
    ).values('id_est__nombre_est', 'id_est__id_est', 'fecha').annotate(promedio_nota=Avg('nota'))
    
    return render(request, 'consultar_resultados.html', {
        'asignatura': asignatura,
        'grupo': grupo,
        'resultados': resultados,
        'previous_url': request.META['HTTP_REFERER']
    })
    
@login_required
def detalle_evaluacion(request, estudiante_id, asignatura, fecha, grupo):
    # Obtener la asignatura
    asignatura_obj = get_object_or_404(Asignatura, nombre_asig=asignatura)

    # Convertir la fecha a un objeto datetime
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return render(request, 'error.html', {'mensaje': 'Fecha inválida.'})

    # Obtener las preguntas relacionadas a la evaluación
    # preguntas = Pregunta.objects.filter(
    #     evalua__id_asig=asignatura_obj,
    #     evalua__id_est=estudiante_id,
    #     evalua__grupo=grupo,
    #     evalua__fecha=fecha_obj.date()
    # ).distinct()
    
    preguntas = Pregunta.objects.annotate(fecha_truncada=TruncDate('evalua__fecha')).filter(
                evalua__id_asig=asignatura_obj,
                evalua__grupo=grupo,
                fecha_truncada=fecha_obj,
                evalua__id_est=estudiante_id
            ).distinct()

    # Obtener las respuestas del estudiante
    # respuestas = Responde.objects.filter(
    #     id_asig=asignatura_obj,
    #     id_est=estudiante_id,
    #     grupo=grupo,
    #     fecha=fecha_obj.date()
        
    # )
    respuestas = Responde.objects.annotate(fecha_truncada=TruncDate('fecha')).filter(
                    id_pro__id_asig=asignatura_obj,
                    id_est=estudiante_id,
                    fecha_truncada=fecha_obj
                ).values('id_pro', 'id_asig', 'grupo', 'id_est', 'fecha', 'id_preg', 'id_resp', )#.values_list('id_resp', 'id_preg')

    # Relacionar las preguntas con sus respuestas y si fueron correctas
    consolidado = []
    for pregunta in preguntas:
        respuesta = respuestas.filter(id_preg=pregunta).order_by('id_asig').first()
       
        if respuesta:
            correcta = Corresponde.objects.filter(
                id_preg=pregunta,
                id_resp__id_resp=respuesta['id_resp'],
                es_correcta=True
            ).exists()
        else:
            correcta = False

        consolidado.append({
            'pregunta': pregunta.enunciado_preg,
            'respuesta': Respuesta.objects.get(id_resp=respuesta['id_resp']).enunciado_resp if respuesta else 'Sin responder',
            'correcta': 'Sí' if correcta else 'No'
        })

    # Obtener la nota final
    # nota = Evalua.objects.filter(
    #     id_asig=asignatura_obj,
    #     id_est=estudiante_id,
    #     grupo=grupo,
    #     fecha=fecha_obj.date()
    # ).values_list('nota', flat=True).first()
    evaluacion = Evalua.objects.filter(
            id_est__id_est=estudiante_id,
            id_asig__id_asig=asignatura_obj.id_asig,
            grupo=grupo,
            fecha=fecha_obj) \
        .values('nota') \
        .annotate(num_estudiantes=Count('nota', distinct=True)) \
        .order_by('nota').first()
    nota = evaluacion['nota']

    return render(request, 'detalle_evaluacion.html', {
        'asignatura': asignatura,
        'fecha': fecha,
        'grupo': grupo,
        'consolidado': consolidado,
        'nota': nota,
        'previous_url': request.META['HTTP_REFERER']
    })
