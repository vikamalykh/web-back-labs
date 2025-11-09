from flask import Blueprint, url_for, request, render_template, make_response, redirect, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    #подключаемся к БД
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='viktoriya_malykh_knowledge_base',
        user='viktoriya_malykh_knowledge_base',
        password='1234567'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    #проверка существования пользователя
    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password)
    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password_hash}');")
    conn.commit() #сохранение данных
    cur.close()
    conn.close()
    
    return render_template('lab5/success.html', login=login)