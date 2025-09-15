from flask import Flask, url_for, request, redirect, abort
import datetime
from werkzeug.exceptions import HTTPException
app = Flask(__name__)

###
@app.errorhandler(402)
def payment_required(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>402 - Требуется оплата</h1>
        <p>Этот код зарезервирован для будущего использования.</p>
        <p>Изначально предполагалось использовать для цифровых платежных систем.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 402

@app.errorhandler(404)
def not_found(err):
    return "Нет такой страницы :-(", 404

@app.errorhandler(400)
def bad_request(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>400 Bad Request</title>
    </head>
    <body>
        <h1>400 - Плохой запрос</h1>
        <p>Сервер не может обработать запрос из-за неверного синтаксиса.</p>
        <p>Проверьте правильность введенных данных и повторите попытку.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 400

@app.errorhandler(401)
def unauthorized(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>401 - Не авторизован</h1>
        <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
        <p>Пожалуйста, войдите в систему с действительными учетными данными.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 401

@app.errorhandler(403)
def forbidden(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 - Запрещено</h1>
        <p>У вас нет прав доступа к запрашиваемому ресурсу.</p>
        <p>Сервер понял запрос, но отказывается его авторизовать.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 403

@app.errorhandler(405)
def method_not_allowed(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 - Метод не разрешен</h1>
        <p>Метод запроса известен серверу, но не поддерживается для целевого ресурса.</p>
        <p>Например, POST запрос к ресурсу, который поддерживает только GET.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 405

@app.errorhandler(418)
def im_a_teapot(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 - Я чайник</h1>
        <p>Сервер отказывается заваривать кофе, потому что он является чайником.</p>
        <p>Это шуточный код ошибки из April Fools' jokes (RFC 2324).</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 418

@app.route("/test/400")
def test_400():
    abort(400)

@app.route("/test/401")
def test_401():
    abort(401)

@app.route("/test/402")
def test_402():
    abort(402)

@app.route("/test/403")
def test_403():
    abort(403)

@app.route("/test/405")
def test_405():
    abort(405)

@app.route("/test/418")
def test_418():
    abort(418)

@app.route("/")
@app.route("/index")
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
            </ul>
        </nav>
        
        <footer>
            <hr>
            <p>Малых Виктория Евгеньевна, ФБИ-32, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''

@app.route("/lab1")
def lab1():
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
        </main>
        
        <footer>
            <hr>
            <a href="/">На главную страницу</a>
        </footer>
    </body>
</html>
'''

@app.route("/lab1/web")
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

@app.route("/lab1/author")
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

@app.route("/lab1/image")
def image():
    css_path = url_for("static", filename="lab1.css")
    image_path = url_for("static", filename="oak.jpg")
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
'''

count = 0
@app.route("/lab1/counter")
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

@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
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