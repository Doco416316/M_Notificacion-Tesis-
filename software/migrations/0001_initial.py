# Generated by Django 5.0.6 on 2024-07-16 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('version', models.CharField(max_length=50)),
                ('licencia', models.CharField(max_length=100)),
                ('fecha_instalacion', models.DateField()),
            ],
        ),
    ]
