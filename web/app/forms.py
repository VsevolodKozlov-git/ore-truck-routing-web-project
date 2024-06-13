from django import forms
from django.forms import widgets
from app import models
from django.core.exceptions import ValidationError
import re


class CoordinatesParser:
    default_error_messages = {"invalid": "Некорректный формат координат"}

    @staticmethod
    def two_floats_validator(input_str):
        try:
            CoordinatesParser.get_two_floats(input_str)
        except ValueError:
            raise ValidationError(
                CoordinatesParser.default_error_messages["invalid"]
            )

    @staticmethod
    def get_two_floats(input_str):
        pattern = r"^\s*([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s*$"
        match = re.match(pattern, input_str)
        if not match:
            raise ValueError("Невозможно конвертировать в 2 числа")
        float1, float2 = match.groups()
        return float(float1), float(float2)


class CoordinateForm(forms.Form):
    coordinates = forms.CharField(
        max_length=50,
        min_length=3,
        validators=[CoordinatesParser.two_floats_validator],
    )


class StorageChoiceForm(forms.Form):
    storage = forms.ModelChoiceField(
        queryset=models.Storage.objects.all(),
        label="Выберите склад",
        help_text="Выберите склад"
    )