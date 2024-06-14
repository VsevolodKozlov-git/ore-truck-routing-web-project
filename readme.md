# Веб-приложение на django для контроля разгрузки самосвалов с рудой

## Формулировка задачи

Есть самосвалы с рудой, они разгружаются на складах с координатами заданными полигонами в формате WKT. 
Оператор должен вводить координаты разгрузки грузовика и если они попали в координаты склада, то учитывать их при расчете характеристик руды в складе.
У руды есть следующие характеристики:

* Масса
* Процентное содержание SiO2
* Процентное содержание Fe

## Где посмотреть результат?

Я захостил результат на Jino VPS: [ссылка](https://d159f7489c6a.vps.myjino.ru/)

## Реализация

Стек технологий:

* Django с библиотеками для GeoDjango
* PostgreSQL с расширением PostGis
* Docker 
* gunicorn
* nginx

Результат:

|![input](https://github.com/VsevolodKozlov-git/ore-truck-routing-web-project/blob/gh-static/gh-static/input.png?raw=true)|
|:--:|
|Таблица для ввода|

|![output](https://github.com/VsevolodKozlov-git/ore-truck-routing-web-project/blob/gh-static/gh-static/output.png?raw=true)|
|:--:|
|Вывод|

## Запуск

### В режиме разработки

1. Создайте `dev.env` файл в корне проекта со следующими переменными(через пробел введите ваши значения):

```dosini
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_PASSWORD=

DJANGO_SECRET_KEY=
DJANGO_DEBUG=
DJANGO_ALLOWED_HOSTS=


POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
```

2. Запустить docker compose командой:
``` bash
docker compose -f docker-compose.yaml up --build
```
3. Как инициализация всех контейнеров завершится. Можете подключаться к сервису `web` командой: 
```bash
docker compose exec web "sh"
```
4. Можете запустить сервер командой 
```bash
python manage.py runserver 0.0.0.0:8100
```
5. Теперь по адресу `127.0.0.1:8100` у вас будет доступно приложение, 
при этом любые изменения в коде будут автоматически применять из-за того, что файлы приложения примаунчены через bind mount
6. Как завершите работу не забудьте отключить docker compose командой:
```bash
docker compose -f docker-compose.yaml down
```

### В продакшене

1. Создайте `prod.env` файл в корне проекта со следующими переменными(через пробел введите ваши значения):

```dosini
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_PASSWORD=

DJANGO_SECRET_KEY=
DJANGO_DEBUG=
DJANGO_ALLOWED_HOSTS=


POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
```
2. Запустить docker compose командой:
``` bash
docker compose -f docker-compose.prod.yaml up --build
```
3. Теперь приложени доступно на порту 80
4. Как завершите работу не забудьте отключить docker compose командой:
```bash
docker compose -f docker-compose.yaml down
```