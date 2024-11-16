# Generated by Django 5.0.6 on 2024-11-04 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_hardware_software_notificacion_hardware_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccionRegistro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_accion', models.CharField(choices=[('eliminar', 'Eliminar'), ('cambiar_prioridad', 'Cambiar Prioridad')], max_length=20)),
                ('notificacion_id', models.IntegerField()),
                ('prioridad_anterior', models.CharField(max_length=10)),
                ('fecha_accion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
