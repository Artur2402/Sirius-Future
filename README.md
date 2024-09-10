# Sirius-Future
# Инструкция по запуску и тестированию проекта:
## 1. Установка зависимостей: 

Склонируйте проект и перейдите в директорию проекта:
```
git clone <ссылка на репозиторий>
cd <название директории проекта>
```
Установите виртуальное окружение и активируйте его:
```
python -m venv env
source env/bin/activate  # Linux/MacOS
.\env\Scripts\activate  # Windows
```
Установите зависимости проекта:
```
pip install -r requirements.txt
```
## 2. Настройка окружения: 
Создайте файл .env в корневой директории и добавьте следующие переменные:
```
DEBUG=True
SECRET_KEY=<ваш секретный ключ>
SENTRY_DSN=<dsn, полученный с Sentry>
```
Сгенерированный ключ Ключ для Django можно сгенерировать по пути https://djecrety.ir/

Как получить DSN из Sentry?
1. Зарегистрируйся в Sentry на https://sentry.io/sentry.io.

2. Создай проект:

После регистрации и входа в аккаунт, выбери или создай организацию.
Перейди на вкладку "Projects" и создай новый проект, выбрав платформу (в твоём случае — Django).

3. Получи DSN:

После создания проекта Sentry покажет тебе инструкцию, как подключить SDK, и предоставит уникальный DSN.
Этот DSN будет выглядеть примерно так:
```
https://your_unique_key@o123456.ingest.sentry.io/123456
```
## 3. Подготовка базы данных: 
Примените миграции для создания нужных таблиц в базе данных:
```
python manage.py makemigrations
python manage.py migrate
```
## 4. Запуск Redis-сервера: 
Redis используется для кэширования, и его нужно запустить перед запуском приложения. 

Для этого:
Установите Redis (если еще не установлен) с сайта [redis.io](https://redis.io/)

Запустите сервер Redis:
redis-server

## 5. Запуск приложения:
```
python manage.py runserver
```
## 6. Тестирование: 
Для запуска тестов используйте команду:
```
python manage.py test
```
**Sentry интеграция: Убедитесь, что переменная SENTRY_DSN добавлена в файл .env, чтобы активировать мониторинг ошибок.**

# Документация по API:
## 1. Регистрация пользователя:

**Endpoint:**  ```/api/register/```

**Метод**: ```POST```

**Тело запроса:**
```
{
  "username": "johndoe123",
  "email": "johndoe@example.com",
  "password": "your_password"
}
```

**Ответ:**
```
{
  "message": "User registered successfully",
  "token": "<jwt_token>"
}
```

## 2. Аутентификация (JWT):

**Endpoint:** ```/api/auth/login/```

**Метод:** ```POST```

**Тело запроса:**
```
{
  "email": "johndoe@example.com",
  "password": "your_password"
}
```

**Ответ:**
```
{
  "token": "<jwt_token>"
}
```

## 3. Получение реферальной ссылки:

**Endpoint:** ```/api/user/<username>/referral/```

**Метод:** ```GET```

**Описание:** Получить реферальную ссылку пользователя.

**Ответ:**
```
{
  "referral_link": "http://127.0.0.1:8000/register/<unique_id>"
}
```

## 4. Создание платежа:

**Endpoint:** ```/api/payment/```

**Метод:** ```POST```

**Тело запроса:**
```
{
  "amount": 100
}
```

**Ответ:**
```
{
  "message": "Payment successful",
  "payment_id": "<payment_id>"
}
```

Документация должна быть также доступна в формате Swagger/OpenAPI по пути /swagger/ (если настроено).
