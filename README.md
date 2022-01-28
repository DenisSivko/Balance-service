# Микросервис для работы с балансом пользователей
## Описание
Список технологий: Python, Django Rest Framework, Docker, Gunicorn, Nginx, PostgreSQL.

Данные по текущему курсу валют взяты с [сайта](https://freecurrencyapi.net/).

#### Задача:
Необходимо реализовать микросервис для работы с балансом пользователей (зачисление средств, списание средств, перевод средств от пользователя к пользователю, а также метод получения баланса пользователя и получения списка транзакций с комментариями откуда и зачем были начислены/списаны средства с баланса). Сервис должен предоставлять HTTP API и принимать/отдавать запросы/ответы в формате JSON.

## Установка
#### Шаг 1. Проверьте установлен ли у вас Docker
Прежде, чем приступать к работе, необходимо знать, что Docker установлен. Для этого достаточно ввести:
```bash
docker -v
```
Или скачайте [Docker Desktop](https://www.docker.com/products/docker-desktop) для Mac или Windows. [Docker Compose](https://docs.docker.com/compose) будет установлен автоматически. В Linux убедитесь, что у вас установлена последняя версия [Compose](https://docs.docker.com/compose/install/). Также вы можете воспользоваться официальной [инструкцией](https://docs.docker.com/engine/install/).

#### Шаг 2. Клонируйте репозиторий себе на компьютер
Введите команду:
```bash
git clone https://github.com/DenisSivko/Balance-service.git
```

#### Шаг 3. Создайте в клонированной директории файл .env
Пример:
```bash
SECRET_KEY=django-insecure-i&ij02ry7@5m67xbt3@t$_s+n9um0c2kh0il0!kj&m8g0!5#(&

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

API_KEY={API_KEY_freecurrencyapi}
```

#### Шаг 4. Запуск docker-compose
Для запуска необходимо выполнить из директории с проектом команду:
```bash
docker-compose up -d
```

#### Документация
Документация к API доступна по адресу:
```json
http://127.0.0.1/redoc/
```

##### Другие команды
Создание суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

Для пересборки и запуска контейнеров воспользуйтесь командой:
```bash
docker-compose up -d --build 
```

Останавливаем и удаляем контейнеры, сети, тома и образы:
```bash
docker-compose down -v
```

## Примеры
Для формирования запросов и ответов использована программа [Postman](https://www.postman.com/).

### Создание счета
```json
POST http://127.0.0.1/api/v1/account/
```
### Информация о счете
```json
GET http://127.0.0.1/api/v1/balance/

# Body(json)
{
    "id": 1
}
```
### Получить баланс пользователя в валюте, отличной от рубля (пример - USD)
```json
GET http://127.0.0.1/api/v1/balance/?currency=USD

# Body(json)
{
    "id": 1
}
```
### Зачислить деньги на счет
```json
POST http://127.0.0.1/api/v1/accrual/

# Body(json)
{
    "id": 1,
    "amount": 1000
}
```
### Списать деньги со счета
```json
POST http://127.0.0.1/api/v1/debiting/

# Body(json)
{
    "id": 1,
    "amount": 1000
}
```
### Перевести деньги с одного счета на другой
```json
POST http://127.0.0.1/api/v1/transfer/

# Body(json)
{
    "from_account": 1,
    "to_account": 2,
    "amount": 500
}
```
### Просмотреть транзакции связанные с заданным счетом (с сортировкой по убыванию даты и пагинацией)
```json
GET http://127.0.0.1/api/v1/transactions/?ordering=-date

# Body(json)
{
    "id": 1
}
```
### Просмотреть транзакции связанные с заданным счетом (с сортировкой по возрастанию суммы и пагинацией)
```json
GET http://127.0.0.1/api/v1/transactions/?ordering=amount

# Body(json)
{
    "id": 1
}
```
