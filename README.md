## Установка и запуск проекта


```commandline
    git clone https://github.com/molodcovnik/test_ref_system.git
```
```commandline
    cd test_ref_system/
```

```commandline
    docker-compose up --build
```

#### После сборки докер образов переходим по урл http://0.0.0.0:8080/api/v1


## Реферальная система

#### Стек технологий:
- Python
- Django, DRF
- PostgreSQL
- Nginx

****


### Описание АПИ

- Аутентицикация пользователя
- Метод проверяет наличие пользователя, если нет, то создаст нового и вернет смс-код(имитация) в своем ответе

**GET**  http://0.0.0.0:8080/api/v1/users/auth

*payload*

```json
{
  "phone_number": "string"
}
```

*response*

```json
{
  "code": "string"
}
```

****

- Логин
- Логиним пользователя через номер телефона и смс-код, в ответ получаем токен аутентификации

**POST**  http://0.0.0.0:8080/api/v1/users/auth/login

*payload*

```json
{
  "phone_number": "string",
  "code": "string"
}
```

*response*

```json
{
  "token": "string"
}
```

****

- Выход из системы

**GET**  http://0.0.0.0:8080/api/v1/users/logout

*response*

200


****

- Профиль пользователя

**GET** http://0.0.0.0:8080/api/v1/referrals/profile

*response*

```json
{
  "id": 0,
  "phone_number": "string",
  "full_name": "string",
  "invite_code": "string",
  "active_invite_code": "string",
  "invited_users": [
    {
      "id": "string",
      "invite_code": "string",
      "invited": "string"
    }
  ]
}
```

****

- Активировать чужой инвайт код в своем профиле

**POST** http://0.0.0.0:8080/api/v1/referrals/profile/active-invite

*payload*

```json
{
  "invite_code": "string"
}
```

*response*

```json
{
"detail": "Инвайт-код успешно активирован."
}
```

****


### Задание:

#### Реализовать простую реферальную систему. Минимальный интерфейс для тестирования. ####
Реализовать логику и API для следующего функционала :

- Авторизация по номеру телефона. Первый запрос на ввод номера
телефона. Имитировать отправку 4хзначного кода авторизации(задержку
на сервере 1-2 сек). Второй запрос на ввод кода

- Если пользователь ранее не авторизовывался, то записать его в бд

- Запрос на профиль пользователя

- Пользователю нужно при первой авторизации нужно присвоить
рандомно сгенерированный 6-значный инвайт-код(цифры и символы)

- В профиле у пользователя должна быть возможность ввести чужой
инвайт-код(при вводе проверять на существование). В своем профиле
можно активировать только 1 инвайт код, если пользователь уже когда-
то активировал инвайт код, то нужно выводить его в соответсвующем
поле в запросе на профиль пользователя

- В API профиля должен выводиться список пользователей(номеров
телефона), которые ввели инвайт код текущего пользователя.


