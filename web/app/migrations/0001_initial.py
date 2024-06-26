# Generated by Django 5.0.6 on 2024-06-12 19:49

import django.contrib.gis.db.models.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinates', django.contrib.gis.db.models.fields.PolygonField(srid=4326, verbose_name='Координаты хранилища')),
                ('name', models.CharField(max_length=100, verbose_name='Склад 1')),
                ('weight_t', models.FloatField(validators=[django.core.validators.MinValueValidator(0, message='Вес меньше 0')], verbose_name='Текущий вес руды в тоннах')),
                ('sio2_proportion', models.FloatField(validators=[django.core.validators.MinValueValidator(0, message='Доля меньше 0'), django.core.validators.MaxValueValidator(1, message='Доля больше 1')], verbose_name='доля SiO2')),
                ('fe_proportion', models.FloatField(validators=[django.core.validators.MinValueValidator(0, message='Доля меньше 0'), django.core.validators.MaxValueValidator(1, message='Доля больше 1')], verbose_name='доля Fe')),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_number', models.CharField(max_length=10, verbose_name='Бортовой номер')),
            ],
        ),
        migrations.CreateModel(
            name='TruckModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('max_weight_t', models.FloatField(validators=[django.core.validators.MinValueValidator(0, message='Вес меньше 0')], verbose_name='Грузоподъемность в тоннах')),
            ],
        ),
        migrations.CreateModel(
            name='TruckContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight_t', models.FloatField(validators=[django.core.validators.MinValueValidator(0, message='Вес меньше 0')], verbose_name='Вес руды в тоннах')),
                ('sio2_proportion', models.FloatField(validators=[django.core.validators.MinValueValidator(0, message='Доля меньше 0'), django.core.validators.MaxValueValidator(1, message='Доля больше 1')], verbose_name='доля SiO2')),
                ('fe_proportion', models.FloatField(validators=[django.core.validators.MinValueValidator(0, message='Доля меньше 0'), django.core.validators.MaxValueValidator(1, message='Доля больше 1')], verbose_name='доля Fe')),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='contents', to='app.truck', verbose_name='Самосвал')),
            ],
        ),
        migrations.AddField(
            model_name='truck',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='trucks', to='app.truckmodel', verbose_name='Модель'),
        ),
    ]
