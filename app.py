from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from db import db
from werkzeug.exceptions import HTTPException
from db.models import users
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from rgz import rgz

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'vika_malykh_orm'
    db_user = 'vika_malykh_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "vika_malykh_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(rgz)

@app.route("/")
@app.route("/start")
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
                <li><a href="/lab2/">Вторая лабораторная</a></li>
                <li><a href="/lab3/">Третья лабораторная</a></li>
                <li><a href="/lab4/">Четвёртая лабораторная</a></li>
                <li><a href="/lab5/">Пятая лабораторная</a></li>
                <li><a href="/lab6/">Шестая лабораторная</a></li> 
                <li><a href="/lab7/">Седьмая лабораторная</a></li>
                <li><a href="/lab8/">Восьмая лабораторная</a></li>
                <li><a href="/rgz/">Расчётно-графическая работа</a></li>
            </ul>
        </nav>
        
        <footer>
            <hr>
            <p>Малых Виктория Евгеньевна, ФБИ-32, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''

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
    
    css_path = url_for("static", filename="lab1/error.css")
    image_path = url_for("static", filename="lab1/poisk.jpg")
    
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


@app.errorhandler(500)
def internal_server_error(err):
    css_path = url_for("static", filename="lab1/error500.css")
    return f'''
<!doctype html>
<html>
    <head>
        <title>500</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body class="body">
        <div class="container">
            <h1>500</h1>
            <h2>Ошибка сервера</h2>
            
            <div class="details">
                <p>На сервере произошла непредвиденная ошибка</p>
                <p>Пожалйста, подождите, скоро она будет исправлена</p>
            </div>
            
            <a href="/" class="button">Вернуться на главную</a>
            
            <div class="contact">
                Если проблема повторяется, свяжитесь с поддержкой сайта!
            </div>
        </div>
    </body>
</html>
''', 500

@app.route("/test/500")
def test_500():
    result = 52 / 0
    return "Этот код никогда не выполнится"
