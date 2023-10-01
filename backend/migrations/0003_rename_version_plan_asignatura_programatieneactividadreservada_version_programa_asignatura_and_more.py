# Generated by Django 4.2.4 on 2023-10-01 21:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_alter_estandar_descriptores_alter_notificacion_leida_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programatieneactividadreservada',
            old_name='version_plan_asignatura',
            new_name='version_programa_asignatura',
        ),
        migrations.RenameField(
            model_name='programatienedescriptor',
            old_name='version_plan_asignatura',
            new_name='version_programa_asignatura',
        ),
        migrations.RemoveField(
            model_name='versionprogramaasignatura',
            name='metodologia',
        ),
        migrations.AddField(
            model_name='versionprogramaasignatura',
            name='creado_en',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
