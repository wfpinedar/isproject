import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from .models import Profesor, Estudiante, Pregunta, Respuesta, Asocia, Asignatura

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign In', css_class='btn btn-success w-100'))

class ProfesorForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profesor
        fields = ['nombre_pro']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar'))

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        profesor = super().save(commit=False)
        profesor.user = user
        if commit:
            profesor.save()
        return profesor

class EstudianteForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Estudiante
        fields = ['nombre_est']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar'))

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        estudiante = super().save(commit=False)
        estudiante.user = user
        if commit:
            estudiante.save()
        return estudiante

class PreguntaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar'))
    class Meta:
        model = Pregunta
        fields = ['enunciado_preg', 'tipo_preg']
        widgets = {
            'enunciado_preg': forms.Textarea(attrs={'placeholder': 'Escribe el enunciado aquí', 'class': 'form-control'}),
            'tipo_preg': forms.Select(choices=[('unique', 'Respuesta Única'), ('multiple', 'Selección Múltiple'), ('true_false', 'Verdadero/Falso')], attrs={'class': 'form-control'}),
        }

class EvaluacionForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        profesor = kwargs.pop('profesor', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar'))
        if profesor:
            # Filtrar asignaturas que el profesor dicta
            self.fields['asignatura'].queryset = Asignatura.objects.filter(
                imparte__id_pro=profesor
        )
    
    asignatura = forms.ModelChoiceField(queryset = Asignatura.objects.none(), 
                                        widget = forms.Select(attrs = {"class" : "form-control"}), 
                                        label = "Asignatura")
    
    preguntas = forms.ModelMultipleChoiceField(queryset = Pregunta.objects.all(), 
                                    widget = forms.CheckboxSelectMultiple(), 
                                    label = "Preguntas")
    
    fecha = forms.DateField(
        widget = forms.DateInput(attrs = {"class" : "form-control", "type" : "date",}) , label = "Fecha Evaluación" 
    )
        
class RespuestaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Registrar'))
    class Meta:
        model = Respuesta
        fields = ['enunciado_resp']
        widgets = {
            'enunciado_resp': forms.Textarea(attrs={'placeholder': 'Escribe el enunciado aquí', 'class': 'form-control'}),
        }