# Generated by Django 4.2.5 on 2024-11-21 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id_asig', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_asig', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'asignatura',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id_est', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_est', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'estudiante',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id_preg', models.AutoField(primary_key=True, serialize=False)),
                ('enunciado_preg', models.TextField()),
                ('tipo_preg', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'pregunta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id_pro', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_pro', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'profesor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id_resp', models.AutoField(primary_key=True, serialize=False)),
                ('enunciado_resp', models.TextField()),
            ],
            options={
                'db_table': 'respuesta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id_salon', models.AutoField(primary_key=True, serialize=False)),
                ('capacidad', models.IntegerField()),
            ],
            options={
                'db_table': 'salon',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Asocia',
            fields=[
                ('id_preg', models.OneToOneField(db_column='id_preg', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='evapp.pregunta')),
                ('fecha', models.DateField()),
            ],
            options={
                'db_table': 'asocia',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Corresponde',
            fields=[
                ('id_preg', models.OneToOneField(db_column='id_preg', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='evapp.pregunta')),
                ('es_correcta', models.BooleanField()),
            ],
            options={
                'db_table': 'corresponde',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Imparte',
            fields=[
                ('id_pro', models.OneToOneField(db_column='id_pro', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='evapp.profesor')),
                ('grupo', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'imparte',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cursa',
            fields=[
                ('id_pro', models.OneToOneField(db_column='id_pro', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='evapp.imparte')),
                ('id_asig', models.IntegerField()),
                ('grupo', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'cursa',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Evalua',
            fields=[
                ('id_pro', models.OneToOneField(db_column='id_pro', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='evapp.imparte')),
                ('id_asig', models.IntegerField()),
                ('grupo', models.CharField(max_length=50)),
                ('fecha', models.DateField()),
                ('nota', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
            ],
            options={
                'db_table': 'evalua',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Responde',
            fields=[
                ('id_pro', models.OneToOneField(db_column='id_pro', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='evapp.imparte')),
                ('id_asig', models.IntegerField()),
                ('grupo', models.CharField(max_length=50)),
                ('fecha', models.DateField()),
            ],
            options={
                'db_table': 'responde',
                'managed': False,
            },
        ),
    ]
