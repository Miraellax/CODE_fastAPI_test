# Технологии
- Python 3.10
- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Docker
  
- REST API
- Авторизация: HTTPBasic

# Описание
Web-сервис на fastAPI с методами добавления заметок текущему пользователю и их просмотра. Модели данных User и Note реализованы Pydantic схемами.

Реализована проверка аутентификации(******) - пользователь имеет доступ только к своим заметкам, без корректного логина и пароля (они должны присутствовать в БД) нет возможности просматривать и добавлять заметки.

Авторизация реализована с помощью fastapi.HTTPBasic.

# Методы запросов
Реализовано два метода: получение заметок текущего пользователя (GET) и создание новой заметки для текущего пользователя (POST). Данные передаются и возвращаются в формате Pydantic схем и SQLAlchemy ORM моделей (json).
![изображение](https://github.com/user-attachments/assets/af2dc2ab-8491-4734-82e1-b11189860c9e)

При сохранении заметки, ее текст корректируется с помощью сервиса **Яндекс.Спеллер** методом correct_text(******). Для получения исправлений используется GET запрос к json-версии [сервиса](https://speller.yandex.net/services/spellservice.json/checkText).

# База данных
Для хранения данных о пользователях и заметках используется PostgreSQL. БД инициализируется с помощью SQLAlchemy ORM, созданы модели таблиц User, Notes в файле models(******). Для создания и получения пользователей и заметок в запросах используются SQLAlchemy модели и Pydantic схемы User, Notes.

Между таблицами пользователей и заметок реализована односторонняя связь, владелец заметки записан как owner_id (FK). Схема базы данных:
(****картинка)

При инициализации(******) БД создаются три пользователя с несколькими заметками:
![изображение](https://github.com/user-attachments/assets/7424c012-9df9-434b-a0ad-36955c4d9a1b)

# Docker
FastAPI сервер собирается с помощью Dockerfile(******).

Сервер и база данных объединяются и запускаются с помощью docker-compose файла(*****).
![изображение](https://github.com/user-attachments/assets/c29fc9c7-98e0-437a-8dbd-0d2157cd29b4)


# cURL запросы

Первый вариант cURL запроса рассчитан на ввод в cmd, нет переноса строк. Логин и пароль для авторизации передаются с помощью --user, не зашифрованы. (Заметка: логин и пароль передаются таким способом для демонстрации, они могут передаваться и с помощью заголовка Authorization: Basic.)

Второй вариант запроса создан Swagger, логин и пароль передаются с помощью Authorization: Basic и шифруются средствами HTTPBasic.

<h2>Создание заметки для текущего пользователя - [POST] /users/current/notes</h2>

**1) Без авторизации**

IN:
```
curl -X "POST" "http://localhost/users/current/notes?note_content=textt" -H "accept: application/json"
```
or
```
curl -X 'POST' \
  'http://localhost/users/current/notes?note_content=textt' \
  -H 'accept: application/json' \
  -d ''
```

OUT: 

HTTP Status: 401 (Error: Unauthorized)
```
{
"detail":"Not authenticated"
}
```

**2) Введенные логин и пароль не существуют в БД или в них допущена ошибка**

IN: 
```
curl -X "POST" "http://localhost/users/current/notes?note_content=textt" -H "accept: application/json" --user "NotExists:password"
```
or
```
curl -X 'POST' \
  'http://localhost/users/current/notes?note_content=textt' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic MTox' \
  -d ''
```

OUT:

HTTP Status: 401 (Error: Unauthorized)
```
{
  "detail": "Incorrect username or password"
}
```


**3) Успешная авторизация, введен существующий логин и пароль**

IN:
```
curl -X "POST" "http://localhost/users/current/notes?note_content=textt" -H "accept: application/json" -H "Content-Type: application/json" --user "third:333"
```
or
```
curl -X 'POST' \
  'http://localhost/users/current/notes?note_content=textt' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic dGhpcmQ6MzMz' \
  -d ''
```

OUT:

HTTP Status: 200 (OK)
```
{
  "content": "text",
  "owner_id": 3,
  "id": 5
}
```
Опечатка исправлена с помощью сервиса Яндекс Спеллер tex*tt* -> tex*t*.

<h2>Получение заметок текущего пользователя - [GET] /users/current/notes</h2>

**1) Без авторизации**

IN:
```
curl -X "GET" "http://localhost/users/current/notes" -H "accept: application/json"
```
or
```
curl -X 'GET' \
  'http://localhost/users/current/notes' \
  -H 'accept: application/json'
```

OUT:

HTTP Status: 401 (Error: Unauthorized)
```
{
"detail":"Not authenticated"
}
```

**2) Введенные логин и пароль не существуют в БД или в них допущена ошибка**

IN: 
```
curl -X "GET" "http://localhost/users/current/notes" -H "accept: application/json" --user "NotExists:password"
```
or
```
curl -X 'GET' \
  'http://localhost/users/current/notes' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic MTox'
```

OUT:

HTTP Status: 401 (Error: Unauthorized)
```
{
  "detail": "Incorrect username or password"
}
```


**3) Успешная авторизация, введен существующий логин и пароль**

IN:
```
curl -X "GET" "http://localhost/users/current/notes" -H "accept: application/json" --user "third:333"
```
or
```
curl -X 'GET' \
  'http://localhost/users/current/notes' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic dGhpcmQ6MzMz'
```

OUT:

HTTP Status: 200 (OK)
```
[
  {
    "content": "one more",
    "owner_id": 3,
    "id": 2
  },
  {
    "content": "another good note",
    "owner_id": 3,
    "id": 3
  }
]
```
