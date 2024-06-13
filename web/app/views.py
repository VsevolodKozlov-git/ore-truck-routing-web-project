from dataclasses import dataclass

from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View

from app import forms, models


@dataclass(frozen=True)
class UpdatedStorage:
    name: str
    weight_before: float
    weight_after: float
    sio2_proportion: float
    fe_proportion: float


class TestView(View):
    def get(self, request, *args, **kwargs):
        input_table_data = self.get_input_table_data()
        request.session['input_table_data'] = input_table_data
        valid = request.session.get('valid', False)
        # create form_dict
        forms_dict = {}
        for _id in input_table_data.keys():
            form = forms.CoordinateForm(prefix=str(_id))
            forms_dict[_id] = form
        
        
        context = {
            'input_table_data': input_table_data,
            'valid': valid, 
            'forms_dict': forms_dict
        }
        return render(request, 'test.html', context)

    def post(self, request, *args, **kwargs):
        input_table_data = request.session["input_table_data"]
        # create form dict
        forms_dict = {}
        for _id in input_table_data.keys():
            form = forms.CoordinateForm(request.POST, prefix=str(_id))
            forms_dict[_id] = form
            
        valid = self.is_forms_valid(forms_dict.values())
        request.session['valid'] = valid
        if valid:
            return redirect(reverse('test'))

        context = {
            'input_table_data': input_table_data,
            'valid': valid,
            'forms_dict': forms_dict
        }
        return render(request, 'test.html', context)
            
        
    def is_forms_valid(self, forms_list):
        validation = True
        for form in forms_list:
            # Важно вызвать is_valid у всех форм, потому что иначе не будет
            # выведено сообщение об ошибке
            validation = form.is_valid() and validation
        return validation

    def get_input_table_data(self):
        ids = [1, 2]
        names = ['first', 'second']
        input_table_data = {}
        for _id, name in zip(ids, names):
            input_table_data[_id] = name
        return input_table_data


# class RootView(View):
#     def get(self, request, *args, **kwargs):
#         # Получить данные из сессии. Уже генерировалась таблица?

#         input_table_data = self.get_input_table_data()
#         context = {
#             "input_table_data": input_table_data,
#             "storage_form": forms.StorageChoiceForm(prefix="storage"),
#             # "form_dict": ,
#             "updated_storage": request.session.get("updated_storage", None),
        
#         }

#         render(request, "root.html", context=context)

#     def post(self, request, *args, **kwargs):
#         """
#         Такая работа с id сделана, чтобы предотвратить случай при котором
#         будет добавлен новый самосвал с грузом во время передачи post запроса

#         """
#         # Получаем таблицу с заполненными формами и данными самосвалов
#         input_table_data = self.get_input_table_data(
#             ids=request.session["ids"], session_post=request.POST
#         )

#         storage_choice_form = forms.StorageChoiceForm(
#             request.POST, prefix="storage"
#         )
#         # Валидируем формы
#         forms_list = [row["form"] for row in input_table_data.values()]
#         forms_list.append(storage_choice_form)
#         is_valid = self.is_forms_valid(forms_list)

#         if is_valid:
#             storage = storage_choice_form.cleaned_data["storage"]
#             updated_storage = self.get_updated_storage(
#                 input_table_data, storage
#             )
#             request.session["updated_storage"] = updated_storage

#     def is_forms_valid(forms_list):
#         validation = True
#         for form in forms_list:
#             # Важно вызвать is_valid у всех форм, потому что иначе не будет
#             # выведено сообщение об ошибке
#             validation = form.is_valid() and validation
#         return validation

#     def get_input_table_data_get(self, id_coordinates_dict):
#         self.get_input_table_data(id_coordinate_dict=id_coordinates_dict)

#     def get_input_table_data_post(self, request):
#         pass

#     def get_input_table_data(
#         self, ids=None, id_coordinate_dict=None, session_post=None
#     ):
#         if id_coordinate_dict is None and session_post is None:
#             raise ValueError(
#                 "Оба аргумента get_input_table_data не могут быть None"
#             )
#         if id_coordinate_dict is not None and session_post is not None:
#             raise ValueError(
#                 "Оба аргумента get_input_table_data не могут быть not None"
#             )

#         if ids is None:
#             trucks_contents = models.TruckContent.objects.all()
#         else:
#             trucks_contents = models.TruckContent.objects.filter(pk__in=ids)

#         input_table_data = {}
#         for truck_content in trucks_contents:
#             _id = truck_content.pk
#             if id_coordinate_dict:
#                 coordinates = id_coordinate_dict[_id]
#                 form = forms.CoordinateForm(
#                     initial={"coordinates": coordinates}, prefix=str(_id)
#                 )
#             else:
#                 form = forms.CoordinateForm(session_post, prefix=str(_id))

#             truck = truck_content.truck
#             board_number = truck.board_number
#             model = truck.model.name
#             max_weight = truck.model.max_weight_t
#             weight = truck_content.weight_t
#             overload = round((weight / max_weight - 1) * 100, 2)

#             table_dict = {
#                 "form": form,
#                 "board_number": board_number,
#                 "model": model,
#                 "max_weight": max_weight,
#                 "overload": overload,
#             }

#             input_table_data[_id] = table_dict
#         return input_table_data
