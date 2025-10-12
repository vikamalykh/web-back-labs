from flask import Blueprint, url_for, request, render_template, make_response, redirect

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
                         date=date, shelf_name=shelf_names[shelf],
                         bedding=bedding, luggage=luggage, insurance=insurance,
                         ticket_type=ticket_type, total_price=total_price)