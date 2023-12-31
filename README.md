# Scribble
## Какво представлява проекта:
Scribble е онлайн мултиплейър игра за рисуване на картинки, направена по подобието на известния сайт skribbl.io.

Всеки играч има избора да създаде нова стая или да влезе във вече същестуваща.
Играта е разделена на рундове, в които всеки играч трябва да се опита да нарисува дадена дума, а останалите да я познаят.
Целта на играта е да се съберат най-много точки, като за всяка позната дума се дават по 100 точки, а ако играчът рисува -
по 100 за всеки, който е познал думата по рисунката. 

## Ползвано:
* Python
* Django
* Redis
## Стартиране на проекта:
В директорията на проекта
```
cd mysite
```
```
python manage.py runserver
```
## Requirements
### Django Channels and Djaphne ASGI
```
python -m pip install -U channels["daphne"]
```
### Redis
Django Channels използва Redis като backend. В този случай е използван Docker за инсталация и стартиране на Redis.
За стартиране на Redis в Docker на порт 6379 (портът може да се промени в `setting.py`) може да се ползва следната команда:
```
docker run -p 6379:6379 -d redis:5
```
Ако не е инсталирано `channels_redis`, което е необходимо за интеграция на Redis с Django Channels,
може да се ползва следната команда:
```
python3 -m pip install channels_redis
```

## Документация:
### Модули:
Архитектурата на сайта следва типичната архитектура на един Django проект.
Разделено е на 4 модула, като на всеки съответства една страница в сайта.

В `mysite` модула се съдържат основно Django настройките и началната страница.

Модулът `chat`, или по-добре трябваше да бъде кръстен `game`, отговаря за всички ресурси необходими за играта - 
аутентикация, база данни, изгледи, game manager (контролер), web sockets и др.

`create_room` и `join_room` са събмодулуте в `chat`, които отговарят за различни страници,
но изискват достъп до ресурси в `chat`.

```
mysite (project)
    |
    |___chat
    |       |
    |       |___create_room
    |       |
    |       |___join_room
    |
    |___mysite    
```

### База данни
В `models.py` има 3 класа, всеки от които отговаря на една таблица в базата данни: Room - съдържа информация за всяка 'стая' или игра, Player - играч се създава при всяко влизане в някоя стая,
ако играч със същото ID/име в тази стая все още не съществува,
Message - всяко изпратено съобщение в чат на някоя стая се пази в базата данни.

### Аутентикация на играчите
За разлика от повечето Django проекти, посетителите на сайта/играчите нямат уникално име, а само уникално ID - автоматично генерирано.
Това премахва нуждата от регистрация и се осъществява в `authentication.py` от класа `PlayerBackend`.
Играч се създава само ако клиент влезе в някоя стая и там не съществува вече играч със същото име/ID.

### Websockets
За комуникация между онлайн играчите се използва Django channels в `consumers.py`. Там са имплементирани 3 класа, отговарящи за различни websockets - chat, leaderboard, drawing board.
Всяко се визуализира в `room.html` страницата и динамично се променя по време на игра (frontend логиката е имплементирана в `chat/static/chat/sockets.js`). Websocket url адресите се намират в `routing.py`.

### Изгледи
В `view.py` функциите могат да бъдат разделени на 2 вида - тези, които препращат към друга страница (ще се обърнат към събмодулите), и тези, които обработват POST или GET изпратен от клиент към сървъра.
Django изисква вторите да имат атрибут `@csrf_exempt`.

Обмяната на информация между клиента и сървъра става по посока `Клиент -> Сървър -> Клиент`,
т.е. след получаване на съобщение от клиент сървърът ще обработи информацията и ще върне съобщение.
В повечето случаи отговорът ще бъде върнат в JSON формат и ще бъде визуализиран от frontend-а.

### Game Controller
`GameController` класа в `game.py` отговаря за обработването на информация от и към базата данни след почване на игра до приключването ѝ.
Една игра е разделена на определен брой рундове, като всеки включва избирането на дума и всеки играч да бъде 'рисуващ' точно веднъж (офлайн играчите се пропускат).

Времето за познаване на избраната дума и броят рундове се определя при създаване на стаята. Думите се избират от списъка, намиращ се в `chat/words.py`,
както и от списъка с допълнителни думи (ако не е празен) - задава се при създаване на стаята.

TBА: таймер 

### Познати бъгове
Ако приложението бъде затворено неправилно по време на игра,
при следващо отваряне таймерът най-вероятно ще бъде спрян.
За да се оправи бъгa трябва да се сетне `room.in_progress = False`
в shell.

Ако приложението не е спряно коректно, може някои играчи да останат *онлайн* в
списъка с играчи, въпреки че не са.

Таймерите между различните клиенти не са синхронизирани със сървъра.
Поради тази причина таймерите на клиентите са с няколко секунди по-бавни
от таймера на сървъра.

### Тестове: TBA

### Полезни команди при работа с базата данни
```python manage.py shell```

```python manage.py makemigrations```

```python manage.py migrate```

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
