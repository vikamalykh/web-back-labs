from flask import Blueprint, url_for, request, redirect, abort
import datetime
from werkzeug.exceptions import HTTPException

lab1 = Blueprint('lab1', __name__)


@lab1.route("/test/402")
def test_402():
    return '''
<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>402 - Требуется оплата</h1>
        <p>Этот код зарезервирован для будущего использования.</p>
        <p>Для доступа к ресурсу требуется оплата :-(</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 402


@lab1.route("/test/400")
def test_400():
    return '''
<!doctype html>
<html>
    <head>
        <title>400 Bad Request</title>
    </head>
    <body>
        <h1>400 - Плохой запрос</h1>
        <p>Сервер не может понять или обработать запрос клиента из-за синтаксической ошибки в запросе, 
        некорректных данных или недопустимых символов</p>
        <p>Проверьте правильность введенных данных и повторите попытку!</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 400


@lab1.route("/test/401")
def test_401():
    return '''
<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>401 - Не авторизован</h1>
        <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
        <p>Пожалуйста, войдите в систему с действительными учетными данными!</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 401


@lab1.route("/test/403")
def test_403():
    return '''
<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 - Запрещено</h1>
        <p>У вас нет прав доступа к запрашиваемому ресурсу!</p>
        <p>Сервер понял запрос, но отказывается его авторизовать.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 403


@lab1.route("/test/405")
def test_405():
    return '''
<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 - Метод не поддерживается</h1>
        <p>Метод HTTP-запроса, используемый в запросе, не разрешен для указанного ресурса.</p>
        <p>Возможна: некорректная логика приложения.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 405


@lab1.route("/test/418")
def test_418():
    return '''
<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 - Я чайник</h1>
        <p>Сервер отказывается заваривать вам кофе, потому что он является чайником ;-)</p>
        <p>Это шуточный код ошибки из April Fools' jokes (RFC 2324), просьба не обижаться!</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 418


@lab1.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>

        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2/">Вторая лабораторная</a></li>
            </ul>
        </nav>
        
        <footer>
            <hr>
            <p>Малых Виктория Евгеньевна, ФБИ-32, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''


@lab1.route("/lab1")
def lab():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <header>
            <h1>Лабораторная работа 1</h1>
        </header>
        
        <main>
            <p>
                Flask — фреймворк для создания веб-приложений на языке
                программирования Python, использующий набор инструментов
                Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                называемых микрофреймворков — минималистичных каркасов
                веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
            </p>

            <h2>Список роутов</h2>
            <ul>
                <li><a href="/lab1/web">/lab1/web</a> - Web сервер</li>
                <li><a href="/lab1/author">/lab1/author</a> - Об авторе</li>
                <li><a href="/lab1/image">/lab1/image</a> - Изображение дуба</li>
                <li><a href="/lab1/counter">/lab1/counter</a> - Счетчик посещений</li>
                <li><a href="/lab1/reset_counter">/lab1/reset_counter</a> - Сброс счетчика</li>
                <li><a href="/lab1/info">/lab1/info</a> - Перенаправление на автора</li>
                <li><a href="/lab1/created">/lab1/created</a> - Страница создания</li>
                <li><a href="/test/400">/test/400</a> - Тест ошибки 400</li>
                <li><a href="/test/401">/test/401</a> - Тест ошибки 401</li>
                <li><a href="/test/402">/test/402</a> - Тест ошибки 402</li>
                <li><a href="/test/403">/test/403</a> - Тест ошибки 403</li>
                <li><a href="/test/405">/test/405</a> - Тест ошибки 405</li>
                <li><a href="/test/418">/test/418</a> - Тест ошибки 418</li>
                <li><a href="/test/500">/test/500</a> - Тест ошибки 500</li>
            </ul>
        </main>
        
        <footer>
            <hr>
            <a href="/">На главную страницу</a>
        </footer>
    </body>
</html>
'''


@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/lab1/author">author</a>
            </body>
        </html>""", 201, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }


@lab1.route("/lab1/author")
def author():
    name = "Малых Виктория Евгеньевна"
    group = "ФБИ-32"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""


@lab1.route("/lab1/image")
def image():
    css_path = url_for("static", filename="lab1/lab1.css")
    image_path = url_for("static", filename="lab1/oak.jpg")
    headers = {
        'Content-Language': 'ru-RU, en-US, zh-CN, es-ES',
        'X-Custom-Header-1': 'Hello-World',
        'X-Custom-Header-2': 'Flask-lab1'
    }
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Дуб</h1>
            <img src="{image_path}">
        </div>
    </body>
</html>
''', 200, headers


count = 0

@lab1.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + str(url) + '''<br>
        Ваш IP адрес: ''' + str(client_ip) + '''<br>
        <hr>
        <a href="/lab1/reset_counter">Сбросить счетчик</a> | 
    </body>
</html>
'''


@lab1.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201