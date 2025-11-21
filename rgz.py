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
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM rgz_furniture ORDER BY id")
    else:
        cur.execute("SELECT * FROM rgz_furniture ORDER BY id")
    
    furniture_items = cur.fetchall()
    db_close(conn, cur)
    
    registered = request.args.get('registered')
    
    return render_template('rgz/main.html', furniture_items=furniture_items, registered=registered)


@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login or password):
        return render_template('rgz/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM rgz_users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM rgz_users WHERE login=?;", (login,))
    
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('rgz/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password)
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO rgz_users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO rgz_users (login, password) VALUES (?, ?);", (login, password_hash))

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM rgz_users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM rgz_users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    db_close(conn, cur)

    session['login'] = login
    session['user_id'] = user['id'] if current_app.config['DB_TYPE'] == 'postgres' else user[0]
    
    return redirect('/rgz/?registered=true')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login or password):
        return render_template('rgz/login.html', error='Заполните поля')
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM rgz_users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM rgz_users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    session['user_id'] = user['id'] if current_app.config['DB_TYPE'] == 'postgres' else user[0]
    
    db_close(conn, cur)
    return redirect('/rgz/')

@rgz.route('/rgz/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    return redirect('/rgz/')