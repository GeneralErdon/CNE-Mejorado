# Generated by Django 4.2.7 on 2023-12-04 16:47

import apps.candidatos.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCargo',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, help_text='Identificador del registro', verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=True, help_text='Activo✅ / Inactivo ❌ ', verbose_name='Estado')),
                ('created_date', models.DateTimeField(blank=True, db_index=True, editable=False, help_text='Fecha en la cuál se creó el registro', verbose_name='Fecha creación')),
                ('modified_date', models.DateTimeField(blank=True, editable=False, help_text='Fecha de última modificación del registro', verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateTimeField(blank=True, editable=False, help_text='Fecha de desactivación del registro.', verbose_name='Fecha de eliminación')),
                ('description', models.CharField(help_text='Cargo por el que se pueden postular los candidatos en unas elecciones', max_length=252, verbose_name='Cargo')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(blank=True, db_constraint=False, help_text='Último usuario en alterar el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical BaseModel',
                'verbose_name_plural': 'historical BaseModels',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCandidato',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, help_text='Identificador del registro', verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=True, help_text='Activo✅ / Inactivo ❌ ', verbose_name='Estado')),
                ('created_date', models.DateTimeField(blank=True, db_index=True, editable=False, help_text='Fecha en la cuál se creó el registro', verbose_name='Fecha creación')),
                ('modified_date', models.DateTimeField(blank=True, editable=False, help_text='Fecha de última modificación del registro', verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateTimeField(blank=True, editable=False, help_text='Fecha de desactivación del registro.', verbose_name='Fecha de eliminación')),
                ('identification', models.CharField(db_index=True, help_text='Número de documento de identificación', max_length=11, verbose_name='Cédula o Pasaporte')),
                ('name', models.CharField(help_text='Nombre y segundo nombre', max_length=252, verbose_name='Nombres')),
                ('last_name', models.CharField(help_text='Apellido y segundo apellido', max_length=252, verbose_name='Apellidos')),
                ('sex', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], db_index=True, default='M', help_text='Masculino o Femenino', max_length=1, verbose_name='Sexo')),
                ('photo', models.TextField(blank=True, help_text='Foto del candidato', max_length=100, null=True, verbose_name='Foto del candidato')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(blank=True, db_constraint=False, help_text='Último usuario en alterar el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Candidato',
                'verbose_name_plural': 'historical Candidatos',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, help_text='Identificador del registro', primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=True, help_text='Activo✅ / Inactivo ❌ ', verbose_name='Estado')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Fecha en la cuál se creó el registro', verbose_name='Fecha creación')),
                ('modified_date', models.DateTimeField(auto_now=True, help_text='Fecha de última modificación del registro', verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateTimeField(auto_now=True, help_text='Fecha de desactivación del registro.', verbose_name='Fecha de eliminación')),
                ('description', models.CharField(help_text='Cargo por el que se pueden postular los candidatos en unas elecciones', max_length=252, verbose_name='Cargo')),
                ('changed_by', models.ForeignKey(blank=True, help_text='Último usuario en alterar el registro', null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'BaseModel',
                'verbose_name_plural': 'BaseModels',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, help_text='Identificador del registro', primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=True, help_text='Activo✅ / Inactivo ❌ ', verbose_name='Estado')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Fecha en la cuál se creó el registro', verbose_name='Fecha creación')),
                ('modified_date', models.DateTimeField(auto_now=True, help_text='Fecha de última modificación del registro', verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateTimeField(auto_now=True, help_text='Fecha de desactivación del registro.', verbose_name='Fecha de eliminación')),
                ('identification', models.CharField(db_index=True, help_text='Número de documento de identificación', max_length=11, unique=True, verbose_name='Cédula o Pasaporte')),
                ('name', models.CharField(help_text='Nombre y segundo nombre', max_length=252, verbose_name='Nombres')),
                ('last_name', models.CharField(help_text='Apellido y segundo apellido', max_length=252, verbose_name='Apellidos')),
                ('sex', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], db_index=True, default='M', help_text='Masculino o Femenino', max_length=1, verbose_name='Sexo')),
                ('photo', models.ImageField(blank=True, help_text='Foto del candidato', null=True, upload_to=apps.candidatos.models.candidato_image_path, verbose_name='Foto del candidato')),
                ('changed_by', models.ForeignKey(blank=True, help_text='Último usuario en alterar el registro', null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Candidato',
                'verbose_name_plural': 'Candidatos',
            },
        ),
    ]
