from app import models
from pathlib import Path
from django.contrib.gis.geos import GEOSGeometry

root = Path(__file__).parent


def create_instances(model, instances_dicts):
    return [model(**instance_dict) for instance_dict in instances_dicts]


def create_db_entries(instances):
    for instance in instances:
        instance.save()


def run():
    # Добавляем модели самосвалов
    print("Началось добавление данныех:")
    model_instances_dicts = [
        {"name": "БЕЛАЗ", "max_weight_t": 120},
        {"name": "Komatsu", "max_weight_t": 110},
    ]
    model_instances = create_instances(models.TruckModel, model_instances_dicts)
    create_db_entries(model_instances)
    print("Добавлены модели самосвалов")
    # Добавляем самосвалы
    truck_instances_dicts = [
        {"board_number": "101", "model": model_instances[0]},
        {"board_number": "102", "model": model_instances[0]},
        {"board_number": "K103", "model": model_instances[1]},
    ]
    truck_instances = create_instances(models.Truck, truck_instances_dicts)
    create_db_entries(truck_instances)
    print("Добавлены самосвалы")
    # Добавляем содержимое самосвалов
    content_instances_dicts = [
        {
            "truck": truck_instances[0],
            "weight_t": 100,
            "sio2_proportion": 0.32,
            "fe_proportion": 0.67,
        },
        {
            "truck": truck_instances[1],
            "weight_t": 125,
            "sio2_proportion": 0.30,
            "fe_proportion": 0.65,
        },
        {
            "truck": truck_instances[2],
            "weight_t": 120,
            "sio2_proportion": 0.35,
            "fe_proportion": 0.62,
        },
    ]
    content_instances = create_instances(
        models.TruckContent, content_instances_dicts
    )
    create_db_entries(content_instances)
    print("Добавлено содержимое самосвалов")
    # Добавляем склад
    with open(root / "wkt_data.txt", "r") as file:
        wkt = file.read().strip()
    polygon = GEOSGeometry(wkt)
    storage = models.Storage(
        coordinates=polygon,
        name="Склад 1",
        weight_t=900,
        sio2_proportion=0.34,
        fe_proportion=0.66,
    )
    storage.save()
    print("Добавлено хранилище для руды")
