# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class Asignatura(models.Model):
    id_asig = models.AutoField(primary_key=True)
    nombre_asig = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'asignatura'

    def __str__(self):
        return self.nombre_asig

class Asocia(models.Model):
    id_preg = models.ForeignKey('Pregunta', models.CASCADE, db_column='id_preg')  # The composite primary key (id_preg, id_asig, fecha) found, that is not supported. The first column is selected.
    id_asig = models.ForeignKey(Asignatura, models.CASCADE, db_column='id_asig')
    fecha = models.DateTimeField()
    
    def __str__(self):
        return f"Evaluación de la Asignatura {self.id_asig} en la fecha {self.fecha}"

    class Meta:
        managed = False
        db_table = 'asocia'
        unique_together = (('id_preg', 'id_asig', 'fecha'),)

class Asociacreate(models.Model):
    id_preg = models.ForeignKey('Pregunta', models.DO_NOTHING, db_column='id_preg', primary_key=True)  # The composite primary key (id_preg, id_asig, fecha) found, that is not supported. The first column is selected.
    id_asig = models.ForeignKey(Asignatura, models.DO_NOTHING, db_column='id_asig')
    fecha = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'asocia'
        unique_together = (('id_preg', 'id_asig', 'fecha'),)

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Corresponde(models.Model):
    id_preg = models.OneToOneField('Pregunta', models.DO_NOTHING, db_column='id_preg', primary_key=True)  # The composite primary key (id_preg, id_resp) found, that is not supported. The first column is selected.
    id_resp = models.ForeignKey('Respuesta', models.DO_NOTHING, db_column='id_resp')
    es_correcta = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'corresponde'
        unique_together = (('id_preg', 'id_resp'),)


class Cursa(models.Model):
    id_pro = models.OneToOneField('Imparte', models.DO_NOTHING, db_column='id_pro', primary_key=True)  # The composite primary key (id_pro, id_asig, grupo, id_est) found, that is not supported. The first column is selected.
    id_asig = models.IntegerField()
    grupo = models.CharField(max_length=50)
    id_est = models.ForeignKey('Estudiante', models.DO_NOTHING, db_column='id_est')

    class Meta:
        managed = False
        db_table = 'cursa'
        unique_together = (('id_pro', 'id_asig', 'grupo', 'id_est'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id_est = models.AutoField(primary_key=True)
    nombre_est = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'estudiante'

class Imparte(models.Model):
    id_pro = models.OneToOneField('Profesor', models.DO_NOTHING, db_column='id_pro', primary_key=True)
    id_asig = models.ForeignKey(Asignatura, models.DO_NOTHING, db_column='id_asig')
    grupo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'imparte'
        unique_together = (('id_pro', 'id_asig', 'grupo'),)


class Pregunta(models.Model):
    id_preg = models.AutoField(primary_key=True)
    enunciado_preg = models.TextField()
    tipo_preg = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'pregunta'
        
    def __str__(self):
        return self.enunciado_preg
    
class Salon(models.Model):
    id_salon = models.AutoField(primary_key=True)
    capacidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'salon'
        
    def __str__(self):
        return str(self.id_salon)

class Evalua(models.Model):
    id_pro = models.ForeignKey(Imparte, on_delete=models.CASCADE, db_column='id_pro', primary_key=True)
    id_asig = models.ForeignKey(Asignatura, on_delete=models.CASCADE, db_column='id_asig')
    grupo = models.CharField(max_length=50)
    id_est = models.ForeignKey(Estudiante, models.CASCADE, db_column='id_est')
    id_preg = models.ForeignKey(Pregunta, models.CASCADE, db_column='id_preg')
    fecha = models.DateTimeField()
    id_salon = models.ForeignKey(Salon, models.CASCADE, db_column='id_salon', blank=True, null=True)
    nota = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evalua'
        unique_together = (('id_pro', 'id_asig', 'grupo', 'id_est', 'id_preg', 'fecha'),)

class Evaluacreate(models.Model):
    id_pro = models.ForeignKey(Imparte, on_delete=models.CASCADE, db_column='id_pro', primary_key=True)
    id_asig = models.IntegerField()
    grupo = models.CharField(max_length=50)
    id_est = models.ForeignKey(Estudiante, models.CASCADE, db_column='id_est')
    id_preg = models.ForeignKey(Pregunta, models.CASCADE, db_column='id_preg')
    fecha = models.DateTimeField()
    id_salon = models.ForeignKey(Salon, models.CASCADE, db_column='id_salon', blank=True, null=True)
    nota = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evalua'
        unique_together = (('id_pro', 'id_asig', 'grupo', 'id_est', 'id_preg', 'fecha'),)


class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id_pro = models.AutoField(primary_key=True)
    nombre_pro = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'profesor'

class Respuesta(models.Model):
    id_resp = models.AutoField(primary_key=True)
    enunciado_resp = models.TextField()

    class Meta:
        managed = False
        db_table = 'respuesta'
        
    def __str__(self):
        return self.enunciado_resp


class Responde(models.Model):
    id_pro = models.ForeignKey(Imparte, on_delete=models.CASCADE, db_column='id_pro')
    id_asig = models.ForeignKey(Asignatura, on_delete=models.CASCADE, db_column='id_asig')
    grupo = models.CharField(max_length=50)
    id_est = models.ForeignKey(Estudiante, on_delete=models.CASCADE, db_column='id_est')
    fecha = models.DateTimeField()
    id_preg = models.ForeignKey(Pregunta, on_delete=models.CASCADE, db_column='id_preg')
    id_resp = models.ForeignKey(Respuesta, on_delete=models.CASCADE, db_column='id_resp')
    

    class Meta:
        managed = False
        db_table = 'responde'
        unique_together = (('id_pro', 'id_asig', 'grupo', 'id_est', 'fecha', 'id_preg', 'id_resp'),)
