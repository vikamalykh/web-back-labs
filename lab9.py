from flask import Blueprint, render_template, session, jsonify, request, current_app
import random
import uuid

lab9 = Blueprint('lab9', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='viktoriya_malykh_knowledge_base',
            user='viktoriya_malykh_knowledge_base',
            password='1234567'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        import sqlite3
        from os import path
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

@lab9.route('/lab9/')
def main():
    conn, cur = db_connect()

    if 'lab9_user_id' not in session:
        session['lab9_user_id'] = str(uuid.uuid4())
    
    user_id = session['lab9_user_id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM lab9_users WHERE id = %s", (user_id,))
    else:
        cur.execute("SELECT id FROM lab9_users WHERE id = ?", (user_id,))
    
    if not cur.fetchone():
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO lab9_users (id) VALUES (%s)", (user_id,))
        else:
            cur.execute("INSERT INTO lab9_users (id) VALUES (?)", (user_id,))
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT COUNT(*) as count FROM lab9_gifts WHERE user_id = %s", (user_id,))
    else:
        cur.execute("SELECT COUNT(*) as count FROM lab9_gifts WHERE user_id = ?", (user_id,))
    
    count_result = cur.fetchone()
    
    if count_result['count'] == 0:
        congratulations = [
            "С Новым Годом! Пусть сбудутся все мечты!",
            "Пусть бой курантов исполнит самое заветное!",
            "Мандариновой сладости и волшебства в новом году!",
            "Удачи во всех начинаниях!",
            "Пусть под ёлкой окажется самое нужное!",
            "Искрящегося снега, горячих огней и веры в чудо!",
            "Исполнения самых заветных желаний!",
            "Чтобы год нёс радость, как сани — Деда Мороза!",
            "Света гирлянд в душе весь год!",
            "Пусть сказка заглянет к вам в дом и останется!"
        ]
        
        gift_images = [
            "present1.jpg", "present2.jpg", "present3.jpg", 
            "present4.jpg", "present5.jpg", "present6.jpg",
            "present7.jpg", "present8.jpg", "present9.jpg", 
            "present10.jpg"
        ]

        box_images = [
            "box1.png", "box2.png", "box3.png", "box4.png", "box5.png",
            "box6.png", "box7.png", "box8.png", "box9.png", "box10.png"
        ]
        
        for i in range(10):
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    INSERT INTO lab9_gifts 
                    (user_id, position_id, top_position, left_position, message, image, box_image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (user_id, i, random.randint(10, 85), random.randint(5, 85), 
                     congratulations[i], gift_images[i], box_images[i]))
            else:
                cur.execute("""
                    INSERT INTO lab9_gifts 
                    (user_id, position_id, top_position, left_position, message, image, box_image)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, i, random.randint(10, 85), random.randint(5, 85),
                     congratulations[i], gift_images[i], box_images[i]))

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT position_id, top_position, left_position, opened, message, image, box_image FROM lab9_gifts WHERE user_id = %s ORDER BY position_id", (user_id,))
    else:
        cur.execute("SELECT position_id, top_position, left_position, opened, message, image, box_image FROM lab9_gifts WHERE user_id = ? ORDER BY position_id", (user_id,))
    
    gifts = cur.fetchall()
    
    # Считаем открытые
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT COUNT(*) as count FROM lab9_gifts WHERE user_id = %s AND opened = TRUE", (user_id,))
    else:
        cur.execute("SELECT COUNT(*) as count FROM lab9_gifts WHERE user_id = ? AND opened = TRUE", (user_id,))
    
    opened_result = cur.fetchone()
    opened_count = opened_result['count']
    remaining = 10 - opened_count
    
    db_close(conn, cur)
    
    return render_template('lab9/index.html', gifts=gifts, opened_count=opened_count, remaining=remaining)

@lab9.route('/lab9/open_gift', methods=['POST'])
def open_gift():
    user_id = session.get('lab9_user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Пользователь не найден'})
    
    data = request.json
    gift_id = data.get('gift_id')
    
    conn, cur = db_connect()
    
    try:
        # Проверяем сколько открыто
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT COUNT(*) as count FROM lab9_gifts WHERE user_id = %s AND opened = TRUE", (user_id,))
        else:
            cur.execute("SELECT COUNT(*) as count FROM lab9_gifts WHERE user_id = ? AND opened = TRUE", (user_id,))
        
        opened_result = cur.fetchone()
        opened_count = opened_result['count']
        
        if opened_count >= 3:
            return jsonify({
                'success': False,
                'message': 'Вы уже открыли максимальное количество подарков (3)!'
            })
        
        # Проверяем подарок (правильные имена столбцов)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT opened, message, image, box_image FROM lab9_gifts WHERE user_id = %s AND position_id = %s", (user_id, gift_id))
        else:
            cur.execute("SELECT opened, message, image, box_image FROM lab9_gifts WHERE user_id = ? AND position_id = ?", (user_id, gift_id))
        
        gift = cur.fetchone()
        
        if not gift:
            return jsonify({'success': False, 'message': 'Подарок не найден'})
        
        if gift['opened']:
            return jsonify({'success': False, 'message': 'Этот подарок уже открыт!'})
        
        # Открываем подарок
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE lab9_gifts SET opened = TRUE WHERE user_id = %s AND position_id = %s", (user_id, gift_id))
        else:
            cur.execute("UPDATE lab9_gifts SET opened = TRUE WHERE user_id = ? AND position_id = ?", (user_id, gift_id))
        
        new_opened_count = opened_count + 1
        remaining = 10 - new_opened_count
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': gift['message'],
            'image': gift['image'],  # Исправлено с gift_image на image
            'box_image': gift['box_image'],
            'opened_count': new_opened_count,
            'remaining': remaining
        })
        
    except Exception as e:
        print(f"Ошибка при открытии подарка: {e}")
        conn.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при открытии подарка'})
    finally:
        db_close(conn, cur)

@lab9.route('/lab9/reset', methods=['POST'])
def reset():
    user_id = session.get('lab9_user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Пользователь не найден'})
    
    conn, cur = db_connect()
    
    try:
        # Сбрасываем все подарки и обновляем позиции
        for i in range(10):
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    UPDATE lab9_gifts 
                    SET opened = FALSE, 
                        top_position = %s, 
                        left_position = %s
                    WHERE user_id = %s AND position_id = %s
                """, (random.randint(10, 85), random.randint(5, 85), user_id, i))
            else:
                cur.execute("""
                    UPDATE lab9_gifts 
                    SET opened = FALSE, 
                        top_position = ?, 
                        left_position = ?
                    WHERE user_id = ? AND position_id = ?
                """, (random.randint(10, 85), random.randint(5, 85), user_id, i))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': '🎅 Дедушка Мороз наполнил все подарки снова!'
        })
        
    except Exception as e:
        print(f"Ошибка при сбросе подарков: {e}")
        conn.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при сбросе подарков'})
    finally:
        db_close(conn, cur)