from typing import Dict, List, TypedDict

from django.contrib.gis.geos import Point, Polygon
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from app import forms, models


class OutputRow(TypedDict):
    """Словарь с данными для выходной таблицы
    """
    name: str
    weight_before: float
    weight_after: float
    sio2_percentage: float
    fe_percentage: float


class InputRow(TypedDict):
    """Словарь с данными о самосвале
    """
    board_number: str
    model: str
    max_weight: float
    current_weight: float
    overload: float
    sio2_proportion: float
    fe_proportion: float


InputTable = Dict[int, InputRow]
CoordTuplesDict = Dict[int, tuple]
CoordFormsDict = Dict[int, forms.CoordinateForm]


class RootView(View):
    """Главный view приложения"""

    def get(self, request, *args, **kwargs):
        # Получаем данные о самосвалах
        input_table = self.get_input_table()
        request.session["input_table"] = input_table
        truck_ids = list(input_table.keys())
        # Получаем формы координат для самосвалой
        coord_forms_dict = self.get_coord_forms_dict(request, truck_ids)
        # Получаем итоговую таблицу из сессии, если таковая имеется
        output_row = request.session.get("output_row", None)
        # Удаляем итоговую таблицу из сессии, чтобы при перезагрузке она пропала
        request.session['output_row'] = None
        # Создаем форму для выбора склада
        storage_form = forms.StorageChoiceForm(prefix="storage")
        context = {
            "input_table": input_table,
            "storage_form": storage_form,
            "coord_forms_dict": coord_forms_dict,
            "output_row": output_row,
        }
        return render(request, "root.html", context=context)

    def get_input_table(self) -> InputTable:
        """Создает и возвращает словарь словарей, в котором записаны все необходимые данные о самосвалах"""
        trucks_contents = models.TruckContent.objects.all()

        input_table: InputTable = {}
        for truck_content in trucks_contents:
            _id = truck_content.pk
            truck = truck_content.truck
            board_number = truck.board_number
            model = truck.model.name
            max_weight = truck.model.max_weight_t
            weight = truck_content.weight_t
            sio2_proportion = truck_content.sio2_proportion
            fe_proportion = truck_content.fe_proportion
            overload = round((weight / max_weight - 1) * 100, 2)
            overload = max(overload, 0)  # Чтобы не был меньше 0
            table_row = InputRow(
                board_number=board_number,
                model=model,
                max_weight=max_weight,
                current_weight=weight,
                overload=overload,
                sio2_proportion=sio2_proportion,
                fe_proportion=fe_proportion,
            )
            input_table[_id] = table_row

        return input_table

    def get_coord_forms_dict(
        self, request, truck_ids: List[int]
    ) -> CoordFormsDict:
        """Создает и возвращает словарь, где по id самосвала можно получить форму для координат этого самосвала

        Args:
            request: запрос пользователя
            truck_ids (List[int]): Список id самосвалов
        """
        coord_forms_dict = {}
        for _id in truck_ids:
            form = forms.CoordinateForm(request.POST or None, prefix=str(_id))
            coord_forms_dict[_id] = form
        return coord_forms_dict

    def post(self, request, *args, **kwargs):
        # Получаем таблицу из get-запроса
        input_table: InputTable = request.session["input_table"]
        truck_ids = list(input_table.keys())
        # Создаем формы
        coord_forms_dict = self.get_coord_forms_dict(request, truck_ids)
        storage_form = forms.StorageChoiceForm(request.POST, prefix="storage")
        # Валидируем формы
        forms_list = [form for form in coord_forms_dict.values()]
        forms_list.append(storage_form)
        is_valid = self.is_forms_valid(forms_list)

        if is_valid:
            # Преобразуем координаты из форм в словарь кортежей
            coord_tuples_dict = self.get_coord_tuples_dict(coord_forms_dict)
            # Получаем склад из формы
            storage: models.Storage = storage_form.cleaned_data["storage"]
            # Получаем и записываем в сессию итоговую таблицу
            output_row = self.get_output_row(
                input_table, coord_tuples_dict, storage
            )
            request.session["output_row"] = output_row
            return redirect(reverse("root"))

        context = {
            "input_table": input_table,
            "storage_form": storage_form,
            "coord_forms_dict": coord_forms_dict,
            "output_row": None,
        }
        return render(request, "root.html", context=context)

    @staticmethod
    def is_forms_valid(forms_list) -> bool:
        """Вызывает is_valid у всех форм в списке и возвращает "Все ли формы валидны"

        Args:
            forms_list (_type_): _description_

        Returns:
            bool: _description_
        """
        validation = True
        for form in forms_list:
            # Важно вызвать is_valid у всех форм, потому что иначе не будет выведено сообщение об ошибке
            validation = form.is_valid() and validation
        return validation

    @staticmethod
    def get_coord_tuples_dict(
        coord_forms_dict: CoordFormsDict,
    ) -> CoordTuplesDict:
        """Преобразует словарь форм в словарь кортежей с координатами"""
        coord_tuples_dict = {}
        for _id, coord_form in coord_forms_dict.items():
            coord_str = coord_form.cleaned_data["coordinates"]
            coord_tuple = forms.CoordinatesParser.get_two_floats(coord_str)
            coord_tuples_dict[_id] = coord_tuple
        return coord_tuples_dict

    @staticmethod
    def get_output_row(
        input_table: InputTable,
        coord_tuples_dict: CoordTuplesDict,
        storage: models.Storage,
    ) -> OutputRow:
        """Генерирует данные для выходной таблицы"""
        storage_polygon: Polygon = storage.coordinates
        sio2_proportion = Proportion(storage.weight_t, storage.sio2_proportion)
        fe_proportion = Proportion(storage.weight_t, storage.fe_proportion)

        weight_after = storage.weight_t
        for _id, input_row in input_table.items():
            x, y = coord_tuples_dict[_id]
            point = Point(x, y)
            if storage_polygon.intersects(point):  # Проверка на попадание
                sio2_proportion.add(
                    input_row["current_weight"], input_row["sio2_proportion"]
                )
                fe_proportion.add(
                    input_row["current_weight"], input_row["fe_proportion"]
                )
                weight_after += input_row["current_weight"]

        sio2_percentage = round(sio2_proportion.get_proportion() * 100, 2)
        fe_percentage = round(fe_proportion.get_proportion() * 100, 2)
        output_row = OutputRow(
            name=storage.name,
            weight_before=storage.weight_t,
            weight_after=weight_after,
            sio2_percentage=sio2_percentage,
            fe_percentage=fe_percentage,
        )
        return output_row


class Proportion:
    """Класс для рассчета пропорции"""

    def __init__(
        self, initial_weight_full: float, initial_proportion: float
    ) -> None:
        """
        Args:
            initial_weight_full (float): Полный вес
            initial_proportion (float): Пропорция вещества в весе

        Raises:
            ValueError: Пропорция находится не в интервале [0; 1]
        """
        if not (0 <= initial_proportion <= 1):
            raise ValueError("Proportion should be between 0 and 1")
        self.weight_full = initial_weight_full
        self.weight_proportion = initial_weight_full * initial_proportion

    def add(self, weight_full, proportion):
        self.weight_full += weight_full
        self.weight_proportion += weight_full * proportion

    def get_proportion(self):
        return self.weight_proportion / self.weight_full


# class TestView(View):
#     def get(self, request, *args, **kwargs):
#         input_table = self.get_input_table()
#         request.session["input_table"] = input_table
#         valid = request.session.get("valid", False)
#         # create form_dict
#         forms_dict = {}
#         for _id in input_table.keys():
#             form = forms.CoordinateForm(prefix=str(_id))
#             forms_dict[_id] = form

#         context = {
#             "input_table": input_table,
#             "valid": valid,
#             "forms_dict": forms_dict,
#         }
        
#         return render(request, "test.html", context)

#     def post(self, request, *args, **kwargs):
#         input_table = request.session["input_table"]
#         # create form dict
#         forms_dict = {}
#         for _id in input_table.keys():
#             form = forms.CoordinateForm(request.POST, prefix=str(_id))
#             forms_dict[_id] = form

#         valid = self.is_forms_valid(forms_dict.values())
#         request.session["valid"] = valid
#         if valid:
#             return redirect(reverse("test"))

#         context = {
#             "input_table": input_table,
#             "valid": valid,
#             "forms_dict": forms_dict,
#         }
#         return render(request, "test.html", context)

#     def is_forms_valid(self, forms_list):
#         validation = True
#         for form in forms_list:
#             # Важно вызвать is_valid у всех форм, потому что иначе не будет
#             # выведено сообщение об ошибке
#             validation = form.is_valid() and validation
#         return validation

#     def get_input_table(self):
#         ids = [1, 2]
#         names = ["first", "second"]
#         input_table = {}
#         for _id, name in zip(ids, names):
#             input_table[_id] = name
#         return input_table
