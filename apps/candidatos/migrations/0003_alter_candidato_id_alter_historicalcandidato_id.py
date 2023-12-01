# Generated by Django 4.2.7 on 2023-12-01 14:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('candidatos', '0002_alter_candidato_id_alter_historicalcandidato_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidato',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, help_text='Identificador del registro', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='historicalcandidato',
            name='id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, help_text='Identificador del registro', verbose_name='ID'),
        ),
    ]
