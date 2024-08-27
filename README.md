# cURL запросы

Первый вариант cURL запроса рассчитан на ввод в cmd, нет переноса строк. Логин и пароль для авторизации передаются с помощью --user, не зашифрованы.

Второй вариант запроса создан Swagger, логин и пароль передаются с помощью Authorization: Basic и шифруются средствами HTTPBasic.

<h2>Создание заметки для текущего пользователя - /notes/post/current</h2>

**1) Без авторизации**

IN:
```
curl -X "POST" "http://127.0.0.1:8000/notes/post/current?note_content=text" -H "accept: application/json"
```
or
```
curl -X 'POST' \
  'http://127.0.0.1:8000/notes/post/current?note_content=text' \
  -H 'accept: application/json' \
  -d ''
```

OUT:
```
{
"detail":"Not authenticated"
}
```

**2) Введенные логин и пароль не существуют в БД или в них допущена ошибка**

IN: 
```
curl -X "POST" "http://127.0.0.1:8000/notes/post/current?note_content=text" -H "accept: application/json" --user "NotExists:password"
```
or
```
curl -X 'POST' \
  'http://127.0.0.1:8000/notes/post/current?note_content=text' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic MTox'
```

OUT:
```
{
  "detail": "Incorrect username or password"
}
```


**3) Успешная авторизация, введен существующий логин и пароль**

IN:
```
curl -X "POST" "http://127.0.0.1:8000/notes/post/current" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"content\": \"textt\",\"owner_id\": 1}" --user "first:111"
```
or
```
curl -X 'POST' \
  'http://127.0.0.1:8000/notes/post/current' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic Zmlyc3Q6MTEx' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "textt",
  "owner_id": 1
}'
```

OUT:
```
{
  "content": "text",
  "owner_id": 1,
  "id": 4
}
```

<h2>Создание заметки по айди пользователя - /notes/post/{owner_id}</h2>

**1) Без авторизации**

IN:
```
curl -X "POST" "http://127.0.0.1:8000/notes/post/{owner_id}" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"content\": \"текст заметки\", \"owner_id\": 1}" --user "NotExists:password"
```
or
```
curl -X 'POST' \
  'http://127.0.0.1:8000/notes/post/{owner_id}' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "текст заметки",
  "owner_id": 1
}'
```

OUT:
```
{
  "detail":"Not authenticated"
}
```

**2) Введенные логин и пароль не существуют в БД или в них допущена ошибка**

IN: 
```
curl -X "POST" "http://127.0.0.1:8000/notes/post/{owner_id}" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"content\": \"текст заметки\", \"owner_id\": 1}" --user "NotExists:password"
```
or
```
curl -X 'POST' \
  'http://127.0.0.1:8000/notes/post/{owner_id}' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic MTox' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "текст заметки",
  "owner_id": 1
}'
```

OUT:
```
{
  "detail": "Incorrect username or password"
}
```


**3) Успешная авторизация, введен существующий логин и пароль**

IN:
```
curl -X "POST" "http://127.0.0.1:8000/notes/post/{owner_id}" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"content\": \"Создание новой заметки с апечатками\", \"owner_id\": 1}" --user "first:111" 
```
or
```
curl -X 'POST' \
  'http://127.0.0.1:8000/notes/post/{owner_id}' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic Zmlyc3Q6MTEx' \
  -H 'Content-Type: application/json' \
  -d '{
  "content": "Создание новой заметки с апечатками",
  "owner_id": 1
}'
```

OUT:
```
{
  "content": "Создание новой заметки с опечатками",
  "owner_id": 1,
  "id": 4
}
```

<h2>Получение заметок текущего пользователя - /users/current/notes</h2>

**1) Без авторизации**

IN:
```
curl -X "GET" "http://127.0.0.1:8000/users/current/notes" -H "accept: application/json"
```
or
```
curl -X 'GET' \
  'http://127.0.0.1:8000/users/current/notes' \
  -H 'accept: application/json'
```

OUT:
```
{
"detail":"Not authenticated"
}
```

**2) Введенные логин и пароль не существуют в БД или в них допущена ошибка**

IN: 
```
curl -X "GET" "http://127.0.0.1:8000/users/current/notes" -H "accept: application/json" --user "NotExists:password"
```
or
```
curl -X 'GET' \
  'http://127.0.0.1:8000/users/current/notes' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic MTox'
```

OUT:
```
{
  "detail": "Incorrect username or password"
}
```


**3) Успешная авторизация, введен существующий логин и пароль**

IN:
```
curl -X "GET" "http://127.0.0.1:8000/users/current/notes" -H "accept: application/json" --user "third:333"
```
or
```
curl -X 'GET' \
  'http://127.0.0.1:8000/users/current/notes' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic dGhpcmQ6MzMz'
```

OUT:
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

<h2>Получение данных текущего пользователя - /users/current</h2>

**1) Без авторизации**

IN:
```
curl -X "GET" "http://127.0.0.1:8000/users/current" -H "accept: application/json"
```
or
```
curl -X 'GET' \
  'http://127.0.0.1:8000/users/current' \
  -H 'accept: application/json'
```

OUT:
```
{
"detail":"Not authenticated"
}
```

**2) Введенные логин и пароль не существуют в БД или в них допущена ошибка**

IN: 
```
curl -X "GET" "http://127.0.0.1:8000/users/current" -H "accept: application/json" --user "NotExists:password"
```
or
```
curl -X 'GET' \
  'http://127.0.0.1:8000/users/current' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic MTox'
```

OUT:
```
{
  "detail": "Incorrect username or password"
}
```


**3) Успешная авторизация, введен существующий логин и пароль**

IN:
```
curl -X "GET" "http://127.0.0.1:8000/users/current" -H "accept: application/json" --user "third:333"
```
or
```
curl -X 'GET' \
  'http://127.0.0.1:8000/users/current' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic dGhpcmQ6MzMz'
```

OUT:
```
{
  "username": "third",
  "password": "333"
}
```
