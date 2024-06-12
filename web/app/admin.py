from django.contrib import admin
from app import models

models_list = [
    models.Truck,
    models.TruckModel,
    models.TruckContent,
    models.Storage
]

for model in models_list:
    admin.site.register(model)
