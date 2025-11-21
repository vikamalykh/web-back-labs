from flask import Blueprint, url_for, request, render_template, make_response, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
from os import path

rgz = Blueprint('rgz', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='viktoriya_malykh_knowledge_base',
            user='viktoriya_malykh_knowledge_base',
            password='1234567'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@rgz.route('/rgz/')
def main():
    conn, cur = db_connect()
    
    # Получаем все товары
    cur.execute("SELECT * FROM rgz_furniture")
    furniture = cur.fetchall()
    
    db_close(conn, cur)
    
    login = session.get('login')
    return render_template('rgz/rgz.html', furniture=furniture, login=login)


@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('rgz/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    
    # Проверяем, нет ли уже такого пользователя
    cur.execute("SELECT * FROM rgz_users WHERE login=%s", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('rgz/register.html', error='Пользователь уже существует')
    
    # Хешируем пароль и сохраняем пользователя
    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO rgz_users (login, password) VALUES (%s, %s)", 
                (login, password_hash))
    
    db_close(conn, cur)
    return render_template('rgz/register_success.html', login=login)

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('rgz/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    
    cur.execute("SELECT * FROM rgz_users WHERE login=%s", (login,))
    user = cur.fetchone()
    
    if not user or not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Неверный логин или пароль')
    
    db_close(conn, cur)
    
    # Сохраняем пользователя в сессии
    session['login'] = login
    session['user_id'] = user['id']
    
    return redirect('/rgz/')

@rgz.route('/rgz/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    return redirect('/rgz/')