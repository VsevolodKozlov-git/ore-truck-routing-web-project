from django.contrib.gis.db import models
from django.core import validators

proportion_validators = [
    validators.MinValueValidator(0, message="Доля меньше 0"),
    validators.MaxValueValidator(1, message="Доля больше 1"),
]


weight_validators = [validators.MinValueValidator(0, message="Вес меньше 0")]


class Truck(models.Model):
    board_number = models.CharField(
        max_length=10, verbose_name="Бортовой номер"
    )
    model = models.ForeignKey(
        "TruckModel",
        related_name="trucks",
        on_delete=models.RESTRICT,
        verbose_name="Модель",
    )


class TruckModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    max_weight_t = models.FloatField(
        verbose_name="Грузоподъемность в тоннах", validators=weight_validators
    )


class TruckContent(models.Model):
    truck = models.ForeignKey(
        "Truck",
        related_name="contents",
        verbose_name="Самосвал",
        on_delete=models.RESTRICT,
    )

    weight_t = models.FloatField(
        verbose_name="Вес руды в тоннах", validators=weight_validators
    )
    sio2_proportion = models.FloatField(
        verbose_name="доля SiO2", validators=proportion_validators
    )
    fe_proportion = models.FloatField(
        verbose_name="доля Fe", validators=proportion_validators
    )


class Storage(models.Model):
    coordinates = models.PolygonField(verbose_name="Координаты хранилища")
    name = models.CharField(max_length=100, verbose_name="Склад 1")
    weight_t = models.FloatField(
        verbose_name="Текущий вес руды в тоннах", validators=weight_validators
    )

    sio2_proportion = models.FloatField(
        verbose_name="доля SiO2", validators=proportion_validators
    )
    fe_proportion = models.FloatField(
        verbose_name="доля Fe", validators=proportion_validators
    )

    def __str__(self):
        return str(self.name)
