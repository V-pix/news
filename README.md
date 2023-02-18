# REST API News

## Оглавление
- [Описание](#description)
- [Используемые технологии](#technologies)
- [Запуск проекта с докером](#launch)
- [Примеры работы с API для всех пользователей](#unauth)

<a id=description></a>
## Описание
API включает в себя посты, каналы, комментарии, ответы, возможность подписаться и узнать подписчиков, реакции. Авторизация реализованна через JWT-токен.
### Реализован функционал дающий возможность:
* Просматривать, создавать новые, удалять и изменять посты.
* Просматривать, создавать новые, удалять, изменять каналы.
* Подписываться на каналы и отписываться от них
* Комментировать, смотреть, удалять и обновлять комментарии.
* Просматривать, создавать новые, удалять и изменять ответы на комментарии.
* Просматривать, создавать новые, удалять и изменять реакции.

### К API есть документация по адресу `http://localhost/swagger/
---
<a id=technologies></a>
## Используемые технологии:
- Python 3.7
- Django 2.2.19
- Django REST Framework
- PostgreSQL
- Nginx
- Gunicorn
- Docker
- Simple JWT+ Djoser
- Django Filter 

<a id=launch></a>
## Запуск проекта с докером
Выполните установку git, docker и docker-compose
```sh
sudo apt install git docker docker-compose -y
```
Клонируйте репозиторий:
```sh
git clone git@github.com:V-pix/news.git
```
### Перейти в репозиторий в командной строке:
```bash
cd news
```
## Cоберите контейнер и запустите:
```bash
docker build -t news .
```
```bash
docker-compose up -d
```
### Выполните миграции:
```bash
docker-compose exec web python manage.py migrate
```
### Заполните тестовые данные:
```bash
docker-compose exec web python manage.py loaddata dump.json
```
### Теперь проект доступен по адресам: 
http://localhost/admin/
http://localhost/swagger/
http://localhost/api/v1/chanels/
http://localhost/api/v1/posts/
http://localhost/api/v1/posts/5/comments/
http://localhost/api/v1/posts/5/comments/1/replies/
http://localhost/api/v1/posts/5/reactions/
http://localhost/api/v1/users/subscription/


Учетная запись администратора
```sh
login: v
password: 123
```

<a id=unauth></a>
## Примеры работы с API.
```bash
GET api/v1/posts/ - получить список всех публикаций.
При указании параметров limit и offset выдача должна работать с пагинацией
GET api/v1/posts/{id}/ - получение публикации по id
GET api/v1/chanels/ - получение списка доступных каналов
GET api/v1/chanels/{id}/ - получение информации о канале по id
GET api/v1/{post_id}/comments/ - получение всех комментариев к публикации
GET api/v1/{post_id}/comments/{id}/ - Получение комментария к публикации по id
```
Получение доступа к эндпоинту api/v1/users/subscription/
(подписки) доступен только для авторизованных пользователей.

Зарегистрировать пользователя можно по адрессу http://localhost/api/v1/users/

Доступ авторизованным пользователем доступен по JWT-токену (Joser),
который можно получить выполнив POST запрос по адресу:
```bash
POST /api/v1/jwt/create/
```
Передав в body данные пользователя (например в postman):
```bash
{
"username": "string",
"password": "string"
}
```
Полученный токен добавляем в headers (postman), после чего буду доступны все функции проекта:
```bash
Authorization: Bearer {your_token}
```
Обновить JWT-токен:
```bash
POST /api/v1/jwt/refresh/ - обновление JWT-токена
```
Проверить JWT-токен:
```bash
POST /api/v1/jwt/verify/ - проверка JWT-токена
```
Так же в проекте API реализована пагинация (LimitOffsetPagination):
```bash
GET /api/v1/posts/?limit=5&offset=0 - пагинация на 5 постов, начиная с первого
```

К проекту есть схема базы данных:
https://drive.google.com/file/d/1p9Rwt55bsyibUgeIj-EFLx_0d_ChEUrU/view?usp=sharing
