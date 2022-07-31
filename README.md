# api_final

В этом учебном проекте **"API для Yatube"** создан *REST API - сервис* для проекта Yatube на основе классов предоставляемых библиотекой **Django REST Framework**.
Аутентификация выпоняется по **JWT-токену**.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/Vladislav-76/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейти в корневую папку проекта:

```
cd yatube_api
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
После запуска проекта, по адресу http://127.0.0.1:8000/redoc/ будет доступна документация для API **Yatube**. В документации описано, работает API. Документация представлена в формате **Redoc**.
Ссылки для **Browsable API**:
http://127.0.0.1:8000/api/v1/posts/
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
http://127.0.0.1:8000/api/v1/groups/

### Некоторые примеры запросов к API:

**POST** /api/v1/posts/

*Request samples*
```
{
    "text": "Тестовый пост",
    "image": "string",
    "group": 0
}
```
*Response samples*
```
{
    "id": 4,
    "author": "User_1",
    "text": "Тестовый пост",
    "pub_date": "2022-07-11T10:06:45.533294Z",
    "image": "string",
    "group": null
}
```

**GET** /api/v1/posts/{post_id}/comments/

*Response samples*
```
{
    "id": 6,
    "author": "User_1",
    "text": "Тестовый комментарий",
    "created": "2022-07-07T14:41:24.270378Z",
    "post": 1
}
```

**POST** /api/v1/follow/

*Request samples*
```
{
    "following": "string"
}
```
*Response samples*
```
{
    "user": "string",
    "following": "string"
}
```