neo-sociality
=============

Для запуска идем в Django консоль и набираем:
```python
from neo_facebook.views import *
```
… добавляем группу в базу
```python
create_new_newsmaker('alanismorissette')
create_new_newsmaker('LeagueOfLegendsOceania')
```
… запускаем асинхронное обновление всех новостей за 10 дней (не забываем запустить redis_server и celery worker)
```python
run_news_update(10)
```
… обновляем новости группы по имени
```python
load_newsmaker_posts_into_db_by_username('alanismorissette')
```