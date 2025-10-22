from flask import Blueprint, url_for, request, render_template, make_response, redirect
from datetime import datetime

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    age = request.cookies.get('age')
    name_color = request.cookies.get('name_color')

    if name is None:
        name = "Аноним"

    if age is None:
        age = "Не указан"
    else:
        age = f"{age} лет"

    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/forml')
def forml():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/forml.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)



@lab3.route("/lab3/settings")
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    text_shadow = request.args.get('text_shadow')

    if any([color, bg_color, font_size, text_shadow]):
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if text_shadow:
            resp.set_cookie('text_shadow', text_shadow)
        return resp
    
    color = request.cookies.get('color', '#000000')
    bg_color = request.cookies.get('bg_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16')
    text_shadow = request.cookies.get('text_shadow', 'none')
    
    resp = make_response(render_template('lab3/settings.html', 
                                        color=color, 
                                        bg_color=bg_color, 
                                        font_size=font_size, 
                                        text_shadow=text_shadow))
    return resp


@lab3.route("/lab3/settings/reset")
def reset_settings():
    resp = make_response(redirect('/lab3/settings'))
    
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('text_shadow')
    return resp


@lab3.route('/lab3/ticket')
def ticket_form():
    errors = {}
    fio = request.args.get('fio', '')
    age = request.args.get('age', '')
    departure = request.args.get('departure', '')
    destination = request.args.get('destination', '')
    date = request.args.get('date', '')
    shelf = request.args.get('shelf', 'lower')
    bedding = request.args.get('bedding', '')
    luggage = request.args.get('luggage', '')
    insurance = request.args.get('insurance', '')
    
    return render_template('lab3/ticket.html', errors=errors,
                         fio=fio, age=age,
                         departure=departure, destination=destination,
                         date=date, shelf=shelf,
                         bedding=bedding, luggage=luggage, insurance=insurance)


@lab3.route('/lab3/result_ticket')
def result_ticket():
    errors = {}
    
    fio = request.args.get('fio', '')
    age = request.args.get('age', '')
    departure = request.args.get('departure', '')
    destination = request.args.get('destination', '')
    date = request.args.get('date', '')
    shelf = request.args.get('shelf', 'lower')
    bedding = request.args.get('bedding') == 'on'
    luggage = request.args.get('luggage') == 'on'
    insurance = request.args.get('insurance') == 'on'
    
    if not fio:
        errors['fio'] = 'Заполните ФИО'
    if not age:
        errors['age'] = 'Заполните возраст'
    elif not age.isdigit() or not (1 <= int(age) <= 120):
        errors['age'] = 'Возраст должен быть от 1 до 120 лет'
    if not departure:
        errors['departure'] = 'Заполните пункт выезда'
    if not destination:
        errors['destination'] = 'Заполните пункт назначения'
    if not date:
        errors['date'] = 'Выберите дату'
    
    if errors:
        return render_template('lab3/ticket.html',
                             errors=errors,
                             fio=fio, age=age,
                             departure=departure, destination=destination,
                             date=date, shelf=shelf,
                             bedding='on' if bedding else '',
                             luggage='on' if luggage else '',
                             insurance='on' if insurance else '')
    
    formatted_date = date
    if date:
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d.%m.%Y')
        except ValueError:
            formatted_date = date

    age_int = int(age)
    if age_int < 18:
        base_price = 700
        ticket_type = "Детский билет"
    else:
        base_price = 1000
        ticket_type = "Взрослый билет"
    
    additional_price = 0
    if shelf in ['lower', 'lower_side']:
        additional_price += 100
    if bedding:
        additional_price += 75
    if luggage:
        additional_price += 250
    if insurance:
        additional_price += 150
    
    total_price = base_price + additional_price
    
    shelf_names = {
        'lower': 'Нижняя',
        'upper': 'Верхняя',
        'upper_side': 'Верхняя боковая',
        'lower_side': 'Нижняя боковая'
    }
    
    return render_template('lab3/result_ticket.html',
                         fio=fio, age=age,
                         departure=departure, destination=destination,
                         date=formatted_date, shelf_name=shelf_names[shelf],
                         bedding=bedding, luggage=luggage, insurance=insurance,
                         ticket_type=ticket_type, total_price=total_price)


CHOCOLATES = [
    {"name": "Alpen Gold Молочный", "price": 80, "filling": "Молочный", "brand": "Alpen Gold"},
    {"name": "Alpen Gold Ореховый", "price": 85, "filling": "С лесным орехом", "brand": "Alpen Gold"},
    {"name": "Alpen Gold Клубника", "price": 90, "filling": "С клубникой", "brand": "Alpen Gold"},
    {"name": "Milka Молочный", "price": 120, "filling": "Молочный", "brand": "Milka"},
    {"name": "Milka С фундуком", "price": 130, "filling": "С фундуком", "brand": "Milka"},
    {"name": "Milka С клубникой", "price": 135, "filling": "С клубникой", "brand": "Milka"},
    {"name": "Milka С печеньем", "price": 140, "filling": "С печеньем", "brand": "Milka"},
    {"name": "Ritter Sport Молочный", "price": 150, "filling": "Молочный", "brand": "Ritter Sport"},
    {"name": "Ritter Sport Марципан", "price": 160, "filling": "С марципаном", "brand": "Ritter Sport"},
    {"name": "Ritter Sport Йогурт", "price": 155, "filling": "С йогуртом", "brand": "Ritter Sport"},
    {"name": "Lindt Excellence 70%", "price": 250, "filling": "Горький 70%", "brand": "Lindt"},
    {"name": "Lindt Excellence 85%", "price": 270, "filling": "Горький 85%", "brand": "Lindt"},
    {"name": "Lindt Молочный", "price": 220, "filling": "Молочный", "brand": "Lindt"},
    {"name": "Бабаевский Горький", "price": 110, "filling": "Горький", "brand": "Бабаевский"},
    {"name": "Бабаевский Элитный", "price": 130, "filling": "Горький 75%", "brand": "Бабаевский"},
    {"name": "Россия Щедрая душа", "price": 70, "filling": "Молочный", "brand": "Россия"},
    {"name": "Россия Горький", "price": 75, "filling": "Горький", "brand": "Россия"},
    {"name": "Красный Октябрь Аленка", "price": 95, "filling": "Молочный", "brand": "Аленка"},
    {"name": "Ferrero Rocher", "price": 450, "filling": "С фундуком", "brand": "Ferrero"},
    {"name": "Raffaello", "price": 420, "filling": "Кокосовый", "brand": "Ferrero"},
    {"name": "Twix", "price": 60, "filling": "Карамельный", "brand": "Mars"},
    {"name": "Snickers", "price": 65, "filling": "Арахисовый", "brand": "Mars"},
    {"name": "Bounty", "price": 70, "filling": "Кокосовый", "brand": "Mars"},
    {"name": "KitKat", "price": 55, "filling": "Вафельный", "brand": "Nestle"}
]

@lab3.route('/lab3/chocolate')
def chocolate_search():
    min_price_cookie = request.cookies.get('min_price', '')
    max_price_cookie = request.cookies.get('max_price', '')
    
    all_prices = [choco['price'] for choco in CHOCOLATES]
    min_placeholder = min(all_prices)
    max_placeholder = max(all_prices)
    
    show_results = False
    chocolates = []
    
    if min_price_cookie or max_price_cookie:
        show_results = True
        chocolates = filter_chocolates(min_price_cookie, max_price_cookie)
    
    return render_template('lab3/chocolate_search.html',
                         min_price=min_price_cookie,
                         max_price=max_price_cookie,
                         min_placeholder=min_placeholder,
                         max_placeholder=max_placeholder,
                         chocolates=chocolates,
                         show_results=show_results,
                         all_chocolates=CHOCOLATES,
                         total_count=len(CHOCOLATES))

@lab3.route('/lab3/chocolate_results')
def chocolate_results():
    action = request.args.get('action', 'search')
    
    if action == 'reset':
        resp = make_response(redirect('/lab3/chocolate'))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp
    
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    
    chocolates = filter_chocolates(min_price, max_price)
    
    all_prices = [choco['price'] for choco in CHOCOLATES]
    min_placeholder = min(all_prices)
    max_placeholder = max(all_prices)
    
    resp = make_response(render_template('lab3/chocolate_search.html',
                                       min_price=min_price,
                                       max_price=max_price,
                                       min_placeholder=min_placeholder,
                                       max_placeholder=max_placeholder,
                                       chocolates=chocolates,
                                       show_results=True,
                                       all_chocolates=CHOCOLATES,
                                       total_count=len(CHOCOLATES)))
    
    if min_price:
        resp.set_cookie('min_price', min_price)
    if max_price:
        resp.set_cookie('max_price', max_price)
    
    return resp

def filter_chocolates(min_price_str, max_price_str):
    """шоколадки по цене"""
    filtered_chocolates = CHOCOLATES.copy()
    
    #обработка цены для смены
    if min_price_str:
        try:
            min_price = float(min_price_str)
            filtered_chocolates = [choco for choco in filtered_chocolates if choco['price'] >= min_price]
        except ValueError:
            pass
    
    if max_price_str:
        try:
            max_price = float(max_price_str)
            filtered_chocolates = [choco for choco in filtered_chocolates if choco['price'] <= max_price]
        except ValueError:
            pass
    
    if min_price_str and max_price_str:
        try:
            min_price = float(min_price_str)
            max_price = float(max_price_str)
            if min_price > max_price:
                #фильтруем заново
                filtered_chocolates = [choco for choco in CHOCOLATES 
                                     if max_price <= choco['price'] <= min_price]
        except ValueError:
            pass
    
    return filtered_chocolates