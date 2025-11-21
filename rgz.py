from flask import Blueprint, url_for, request, render_template, make_response, redirect, session, current_app, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
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
        cur.execute("SELECT * FROM rgz_furniture")
    else:
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
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM rgz_users WHERE login=%s", (login,))
    else:
        cur.execute("SELECT * FROM rgz_users WHERE login=?", (login,))
    
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('rgz/register.html', error='Пользователь уже существует')

    password_hash = generate_password_hash(password)
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO rgz_users (login, password) VALUES (%s, %s)", 
                    (login, password_hash))
    else:
        cur.execute("INSERT INTO rgz_users (login, password) VALUES (?, ?)", 
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
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM rgz_users WHERE login=%s", (login,))
    else:
        cur.execute("SELECT * FROM rgz_users WHERE login=?", (login,))
    
    user = cur.fetchone()
    
    if not user or not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Неверный логин или пароль')
    
    db_close(conn, cur)

    session['login'] = login
    session['user_id'] = user['id']
    
    return redirect('/rgz/')

@rgz.route('/rgz/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    return redirect('/rgz/')

@rgz.route('/rgz/cart')
def cart():
    return render_template('rgz/cart.html')

@rgz.route('/rgz/api', methods=['POST'])
def api():
    if request.method != 'POST':
        return jsonify({
            "jsonrpc": "2.0",
            "error": {
                "code": -32600,
                "message": "Invalid Request"
            },
            "id": None
        })
    
    data = request.get_json()

    if not data or 'jsonrpc' not in data or data['jsonrpc'] != '2.0' or 'method' not in data:
        return jsonify({
            "jsonrpc": "2.0",
            "error": {
                "code": -32600,
                "message": "Invalid Request"
            },
            "id": data.get('id') if data else None
        })
    
    method = data.get('method')
    params = data.get('params', {})
    request_id = data.get('id')
    
    if method == 'get_furniture':
        return get_furniture(params, request_id)
    elif method == 'add_to_cart':
        return add_to_cart(params, request_id)
    elif method == 'get_cart':
        return get_cart(params, request_id)
    elif method == 'remove_from_cart':
        return remove_from_cart(params, request_id)
    elif method == 'create_order':
        return create_order(params, request_id)
    else:
        return jsonify({
            "jsonrpc": "2.0",
            "error": {
                "code": -32601,
                "message": "Method not found"
            },
            "id": request_id
        })

def json_rpc_response(result=None, error=None, request_id=None):
    response = {
        "jsonrpc": "2.0",
        "id": request_id
    }
    
    if error:
        response["error"] = error
    else:
        response["result"] = result
    
    return jsonify(response)

def get_furniture(params, request_id):
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM rgz_furniture ORDER BY name")
        else:
            cur.execute("SELECT * FROM rgz_furniture ORDER BY name")
        
        furniture = []
        for item in cur.fetchall():
            furniture.append(dict(item))
        
        return json_rpc_response(furniture, None, request_id)
    except Exception as e:
        return json_rpc_response(None, {"code": -32000, "message": str(e)}, request_id)
    finally:
        db_close(conn, cur)


def add_to_cart(params, request_id):
    login = session.get('login')
    user_id = session.get('user_id')
    
    if not login:
        return json_rpc_response(None, {"code": 1, "message": "Необходима авторизация"}, request_id)
    
    furniture_id = params.get('furniture_id')
    if not furniture_id:
        return json_rpc_response(None, {"code": -32602, "message": "Invalid params"}, request_id)
    
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM rgz_furniture WHERE id = %s", (furniture_id,))
        else:
            cur.execute("SELECT * FROM rgz_furniture WHERE id = ?", (furniture_id,))
        
        furniture = cur.fetchone()
        if not furniture:
            return json_rpc_response(None, {"code": 2, "message": "Товар не найден"}, request_id)
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM rgz_cart WHERE user_id = %s AND furniture_id = %s", 
                       (user_id, furniture_id))
        else:
            cur.execute("SELECT * FROM rgz_cart WHERE user_id = ? AND furniture_id = ?", 
                       (user_id, furniture_id))
        
        existing_item = cur.fetchone()
        
        if existing_item:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE rgz_cart SET quantity = quantity + 1 WHERE id = %s", 
                           (existing_item['id'],))
            else:
                cur.execute("UPDATE rgz_cart SET quantity = quantity + 1 WHERE id = ?", 
                           (existing_item['id'],))
        else:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("INSERT INTO rgz_cart (user_id, furniture_id, quantity) VALUES (%s, %s, 1)", 
                           (user_id, furniture_id))
            else:
                cur.execute("INSERT INTO rgz_cart (user_id, furniture_id, quantity) VALUES (?, ?, 1)", 
                           (user_id, furniture_id))
        
        return json_rpc_response({"success": True}, None, request_id)
    except Exception as e:
        return json_rpc_response(None, {"code": -32000, "message": str(e)}, request_id)
    finally:
        db_close(conn, cur)

def get_cart(params, request_id):
    login = session.get('login')
    user_id = session.get('user_id')
    
    if not login:
        return json_rpc_response(None, {"code": 1, "message": "Необходима авторизация"}, request_id)
    
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT c.*, f.name, f.price, f.image 
                FROM rgz_cart c 
                JOIN rgz_furniture f ON c.furniture_id = f.id 
                WHERE c.user_id = %s
            """, (user_id,))
        else:
            cur.execute("""
                SELECT c.*, f.name, f.price, f.image 
                FROM rgz_cart c 
                JOIN rgz_furniture f ON c.furniture_id = f.id 
                WHERE c.user_id = ?
            """, (user_id,))
        
        cart_items = []
        total = 0
        for item in cur.fetchall():
            item_dict = dict(item)
            item_total = float(item_dict['price']) * item_dict['quantity']
            item_dict['total'] = item_total
            total += item_total
            cart_items.append(item_dict)
        
        return json_rpc_response({
            "items": cart_items,
            "total": total
        }, None, request_id)
    except Exception as e:
        return json_rpc_response(None, {"code": -32000, "message": str(e)}, request_id)
    finally:
        db_close(conn, cur)

def remove_from_cart(params, request_id):
    login = session.get('login')
    user_id = session.get('user_id')
    
    if not login:
        return json_rpc_response(None, {"code": 1, "message": "Необходима авторизация"}, request_id)
    
    cart_item_id = params.get('cart_item_id')
    if not cart_item_id:
        return json_rpc_response(None, {"code": -32602, "message": "Invalid params"}, request_id)
    
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM rgz_cart WHERE id = %s AND user_id = %s", 
                       (cart_item_id, user_id))
        else:
            cur.execute("SELECT * FROM rgz_cart WHERE id = ? AND user_id = ?", 
                       (cart_item_id, user_id))
        
        cart_item = cur.fetchone()
        
        if not cart_item:
            return json_rpc_response(None, {"code": 3, "message": "Товар не найден в корзине"}, request_id)
        

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM rgz_cart WHERE id = %s", (cart_item_id,))
        else:
            cur.execute("DELETE FROM rgz_cart WHERE id = ?", (cart_item_id,))
        
        return json_rpc_response({"success": True}, None, request_id)
    except Exception as e:
        return json_rpc_response(None, {"code": -32000, "message": str(e)}, request_id)
    finally:
        db_close(conn, cur)

def create_order(params, request_id):
    """Создание заказа из корзины"""
    login = session.get('login')
    user_id = session.get('user_id')
    
    if not login:
        return json_rpc_response(None, {"code": 1, "message": "Необходима авторизация"}, request_id)
    
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT c.*, f.name, f.price 
                FROM rgz_cart c 
                JOIN rgz_furniture f ON c.furniture_id = f.id 
                WHERE c.user_id = %s
            """, (user_id,))
        else:
            cur.execute("""
                SELECT c.*, f.name, f.price 
                FROM rgz_cart c 
                JOIN rgz_furniture f ON c.furniture_id = f.id 
                WHERE c.user_id = ?
            """, (user_id,))
        
        cart_items = cur.fetchall()
        
        if not cart_items:
            return json_rpc_response(None, {"code": 4, "message": "Корзина пуста"}, request_id)

        total_amount = 0
        for item in cart_items:
            total_amount += float(item['price']) * item['quantity']

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO rgz_orders (user_id, total_amount) 
                VALUES (%s, %s) 
                RETURNING id
            """, (user_id, total_amount))

            order_result = cur.fetchone()
            if not order_result:
                return json_rpc_response(None, {"code": 5, "message": "Не удалось создать заказ"}, request_id)
            order_id = order_result['id']
        else:
            cur.execute("INSERT INTO rgz_orders (user_id, total_amount) VALUES (?, ?)", 
                       (user_id, total_amount))
            order_id = cur.lastrowid

        for item in cart_items:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    INSERT INTO rgz_order_items (order_id, furniture_id, quantity, price) 
                    VALUES (%s, %s, %s, %s)
                """, (order_id, item['furniture_id'], item['quantity'], item['price']))
            else:
                cur.execute("""
                    INSERT INTO rgz_order_items (order_id, furniture_id, quantity, price) 
                    VALUES (?, ?, ?, ?)
                """, (order_id, item['furniture_id'], item['quantity'], item['price']))

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM rgz_cart WHERE user_id = %s", (user_id,))
        else:
            cur.execute("DELETE FROM rgz_cart WHERE user_id = ?", (user_id,))
        
        return json_rpc_response({
            "order_id": order_id,
            "total_amount": total_amount
        }, None, request_id)
    except Exception as e:
        return json_rpc_response(None, {"code": -32000, "message": str(e)}, request_id)
    finally:
        db_close(conn, cur)
