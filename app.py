from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

error_404_log = []


@app.errorhandler(404)
def not_found(err):
    #информация о текущем запросе
    client_ip = request.remote_addr
    access_time = datetime.datetime.now()
    requested_url = request.url
    
    #запись в лог
    log_entry = f'[{access_time.strftime("%Y-%m-%d %H:%M:%S.%f")}, пользователь {client_ip}] зашёл на адрес: {requested_url}'
    error_404_log.append(log_entry)
    
    css_path = url_for("static", filename="error.css")
    image_path = url_for("static", filename="poisk.jpg")
    
    #HTML для журнала
    journal_html = ''
    for entry in reversed(error_404_log[-10:]):
        journal_html += f'<div class="log-entry">{entry}</div>'
    
    return f'''
<!doctype html>
<html>
    <head>
        <title>404 Страница не найдена</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body class="err-body">
        <div class="err-container">
            <h1 class="err-code">404</h1>
            <h2 class="err-title">Ой! Кажется мы потеряли вашу страницу :-(</h2>
            
            <div class="info-use">
                <h3>Информация о запросе:</h3>
                <p class="info-item"><strong>IP-адрес:</strong> {client_ip}</p>
                <p class="info-item"><strong>Дата и время:</strong> {access_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p class="info-item"><strong>Запрошенный URL:</strong> {requested_url}</p>
            </div>
            
            <div class="err-image-container">
                <img src="{image_path}" alt="Поиск" class="err-image">
            </div>
            
            <p class="err-mess">
                Не переживайте, возможно, она скоро вернётся!
            </p>
            
            <div class="err-suggestions">
                <h3>Как решить проблему?</h3>
                <ul>
                    <li>Проверить правильность URL-адреса</li>
                    <li>Вернуться на предыдущую страницу</li>
                    <li>Вернуться на главную страницу</li>
                    <li>Сообщите об ошибке, если мы вам не помогли :-(</li>
                </ul>
            </div>
            
            <a href="/" class="err-button">Вернуться на главную</a>
            
            <div class="error-journal">
                <h3 class="journal-title">Журнал:</h3>
                <div class="log-entries">
                    {journal_html if journal_html else '<p>Пока нет записей в журнале</p>'}
                </div>
            </div>
        </div>
    </body>
</html>
''', 404

@app.route("/test/402")
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

@app.route("/test/400")
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

@app.route("/test/401")
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

@app.route("/test/403")
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

@app.route("/test/405")
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


@app.route("/test/418")
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

@app.errorhandler(500)
def test500_error(err):
    css_path = url_for("static", filename="error500.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>500 - Внутренняя ошибка сервера</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body class="error-500-body">
        <div class="error-500-container">
            <h1 class="error-500-title">500 - Внутренняя ошибка сервера</h1>
            <p class="error-500-text">К сожалению, на сервере произошла непредвиденная ошибка.</p>
            
            <div class="error-500-details">
                <strong>Что случилось?</strong>
                <p>Сервер столкнулся с проблемой при обработке вашего запроса.</p>
                <p>Это может быть временной проблемой! Попробуйте обновить страницу позже.</p>
            </div>
            
            <p class="error-500-text">Мы уже работаем над исправлением ошибки :-)</p>
            
            <a href="/" class="error-500-home-button">Вернуться на главную</a>
            
            <div class="error-500-contact">
                Если проблема повторяется, свяжитесь с технической поддержкой!
            </div>
        </div>
    </body>
</html>
''', 500
@app.route("/test/500")
def test_500():
    result = 10 / 0
    return "Этот код не выполнится"

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
    headers = {
        'Content-Language': 'ru-RU, en-US, zh-CN, es-ES',
        'X-Custom-Header-1': 'Hello-World',
        'X-Custom-Header-2': 'Flask-App'
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


@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['Пион', 'Ромашка', 'Саранка', 'Незабудка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "Цветок: " + flower_list[flower_id]

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name}</p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name, number, group, course = "Виктория Малых", 2, "ФБИ-32", "3 курс" 
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'бананы', 'price': 150},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины','price': 130},
        {'name': 'манго', 'price': 160}
    ]
    return render_template('example.html', name=name, number=number, group=group, course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')