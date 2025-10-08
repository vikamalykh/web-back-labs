from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from werkzeug.exceptions import HTTPException
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)

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
                <li><a href="/lab2/">Вторая лабораторная</a></li>
            </ul>
        </nav>
        
        <footer>
            <hr>
            <p>Малых Виктория Евгеньевна, ФБИ-32, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['Пион', 'Ромашка', 'Саранка', 'Незабудка']

flower_prices = {
    'Пион': 300,
    'Ромашка': 250, 
    'Саранка': 280,
    'Незабудка': 200
}

books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Сатоси Ягисава', 'title': 'Дни в книжном Морисаки', 'genre': 'Роман', 'pages': 354},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Эрих Мария Ремарк', 'title': 'Три товарища', 'genre': 'Роман', 'pages': 1410},
    {'author': 'Джоан Роулинг', 'title': 'Гарри Поттер и Философский камень', 'genre': 'Фэнтези', 'pages': 309},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 283},
    {'author': 'Антуан де Сент-Экзюпери', 'title': 'Маленький принц', 'genre': 'Сказка', 'pages': 128},
    {'author': 'Ева Меркачёва', 'title': 'Я иду искать', 'genre': 'Детектив', 'pages': 333},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 416},
    {'author': 'Борис Бедный', 'title': 'Девчата', 'genre': 'Комедия', 'pages': 308},
    {'author': 'Марк Твен', 'title': 'Приключения Тома Сойера', 'genre': 'Проза', 'pages': 233}
]

dogs = [
    {
        'name': 'Лабрадор-ретривер',
        'image': 'labrador.jpg',
        'description': 'Дружелюбная, активная и умная порода. Хорошо ладит с детьми, раз смогла поладить с моей племянницей.',
        'size': 'Крупная',
        'lifespan': '10-12 лет'
    },
    {
        'name': 'Немецкая овчарка',
        'image': 'german_shepherd.jpg',
        'description': 'Умная, преданная и служебная порода собак. На НТВ стала популярной.',
        'size': 'Крупная',
        'lifespan': '9-13 лет'
    },
    {
        'name': 'Золотистый ретривер',
        'image': 'golden_retriever.jpg',
        'description': 'Добродушная, терпеливая и очень умная собака. Нынче набирает особую популярность.',
        'size': 'Крупная',
        'lifespan': '10-12 лет'
    },
    {
        'name': 'Французский бульдог',
        'image': 'french_bulldog.jpg',
        'description': 'Компактная, дружелюбная и адаптивная собака. Даже не скажешь, что её предки были бойцовскими псами.',
        'size': 'Маленькая',
        'lifespan': '10-12 лет'
    },
    {
        'name': 'Бигль',
        'image': 'beagle.jpg',
        'description': 'Любопытная, веселая и отличная охотничья порода. Настоящий зверь на охоте за кролками и зайцами.',
        'size': 'Средняя',
        'lifespan': '12-15 лет'
    },
    {
        'name': 'Пудель',
        'image': 'poodle.jpg',
        'description': 'Умная и элегантная порода собак. Интересный факт: с немецкого  Pudel, от puddeln — «плескаться в воде».',
        'size': 'Разная',
        'lifespan': '12-15 лет'
    },
    {
        'name': 'Ротвейлер',
        'image': 'rottweiler.jpg',
        'description': 'Сильная, преданная и уверенная в себе порода собак. Уже больше похож на родственников бойцовских псов.',
        'size': 'Крупная',
        'lifespan': '8-10 лет'
    },
    {
        'name': 'Йоркширский терьер',
        'image': 'yorkie.jpg',
        'description': 'Миниатюрная, энергичная и смелая порода собак. Одним словом - аристократка.',
        'size': 'Маленькая',
        'lifespan': '13-16 лет'
    },
    {
        'name': 'Боксер',
        'image': 'boxer.jpg',
        'description': 'Энергичная, игривая и преданная порода. Если верить источникам, очень умная, поэтому бояться не стоит, наверно...',
        'size': 'Крупная',
        'lifespan': '10-12 лет'
    },
    {
        'name': 'Такса',
        'image': 'dachshund.jpg',
        'description': 'Смелая, любопытная и известная у нас своей длинной спиной. Хотя в Германии предназначена для охоты на барсуков и других норных животных.',
        'size': 'Маленькая',
        'lifespan': '12-16 лет'
    },
    {
        'name': 'Сибирский хаски',
        'image': 'husky.jpg',
        'description': 'Энергичная, дружелюбная и выносливая порода. По фото видно, что из Сибири.',
        'size': 'Крупная',
        'lifespan': '12-14 лет'
    },
    {
        'name': 'Доберман',
        'image': 'doberman.jpg',
        'description': 'Умная, бдительная и преданная порода собак. Одним словосочетанием - моя мечта.',
        'size': 'Крупная',
        'lifespan': '10-12 лет'
    },
    {
        'name': 'Австралийская овчарка',
        'image': 'australian_shepherd.jpg',
        'description': 'Умная, активная и разновидность "постушьих" собак. Слишком милая для НТВ.',
        'size': 'Средняя',
        'lifespan': '13-15 лет'
    },
    {
        'name': 'Ши-тцу',
        'image': 'shih_tzu.jpg',
        'description': 'Ласковая, дружелюбная и декоративная порода. Произошла от тибетских священных собак, похожих на львов. Оно и видно.',
        'size': 'Маленькая',
        'lifespan': '10-16 лет'
    },
    {
        'name': 'Бостон-терьер',
        'image': 'boston_terrier.jpg',
        'description': 'Дружелюбная, умная и компактная собачка. Близкий родственник французского бульдога.',
        'size': 'Маленькая',
        'lifespan': '11-13 лет'
    },
    {
        'name': 'Вельш-корги',
        'image': 'corgi.jpg',
        'description': 'Умная, весёлая и преданная порода. Изначально были пастушьими собаками, из-за коротких лапок, потом дослужились до королевских.',
        'size': 'Маленькая',
        'lifespan': '12-15 лет'
    },
    {
        'name': 'Мопс',
        'image': 'pug.jpg',
        'description': 'Ласковая, общительная и компактная порода. Они не любят одиночество, поэтому прежде чем уйти из дома, взгляните на эту моську.',
        'size': 'Маленькая',
        'lifespan': '13-15 лет'
    },
    {
        'name': 'Акита-ину',
        'image': 'akita.jpg',
        'description': 'Достойная, преданная и сильная японская порода. Настолько преданная, что довела весь мир до слёз.',
        'size': 'Крупная',
        'lifespan': '10-13 лет'
    },
    {
        'name': 'Чихуахуа',
        'image': 'chihuahua.jpg',
        'description': 'Маленькая, смелая и преданная собачка. Думаю, может защитить даже от Ротвейлера.',
        'size': 'Маленькая',
        'lifespan': '14-16 лет'
    },
    {
        'name': 'Бернский зенненхунд',
        'image': 'bernese.jpg',
        'description': 'Спокойная, нежная и красивая швейцарская порода. Вы будете "Счастливы вместе" с ней.',
        'size': 'Крупная',
        'lifespan': '7-10 лет'
    }
]

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    else:
        return render_template('specific_flower.html', 
                             flower=flower_list[flower_id], 
                             flower_id=flower_id,
                             total_flowers=len(flower_list))

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return render_template('add_flowers.html', 
                         name=name, 
                         count=len(flower_list), 
                         flower_list=flower_list)

@app.route('/lab2/flowers')
def all_flowers():
    total = 0
    for flower in flower_list:
        total += flower_prices.get(flower, 300)
    
    return render_template('flowers.html', 
                         flowers=flower_list,
                         flower_prices=flower_prices,
                         total_price=total)

@app.route('/lab2/add_flower/')
def add_flower_400():
    return render_template('error_400_flower.html'), 400

@app.route('/lab2/flowers/rewrite')
def clear_flowers():
    flower_list.clear()
    flower_list.extend(['Пион', 'Ромашка', 'Саранка', 'Незабудка'])
    return render_template('rewrite_flower.html')

@app.route('/lab2/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    
    flower_list.pop(flower_id)
    return redirect('/lab2/flowers')

@app.route('/lab2/add_flower_form', methods=['POST'])
def add_flower_form():
    name = request.form.get('flower_name', '').strip()
    if name:
        flower_list.append(name)
        flower_prices[name] = 300
    return redirect('/lab2/flowers')

@app.route('/lab2/del_all_flowers')
def delete_all_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers')

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

@app.route('/lab2/filters')
def filters():
    phrase = "О, <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    try:
        divide_result = a / b
    except ZeroDivisionError:
        divide_result = 'Ошибка: деление на ноль'
    
    operations = {
        'sum': a + b,
        'subtract': a - b,
        'multiply': a * b,
        'divide': divide_result,
        'power': a ** b
    }
    return render_template('calc.html', a=a, b=b, operations=operations)

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

@app.route('/lab2/books')
def books_list():
    total_books = len(books)
    total_pages = sum(book['pages'] for book in books)
    
    return render_template('books.html', 
                         books=books, 
                         total_books=total_books,
                         total_pages=total_pages)

@app.route('/lab2/dogs')
def dogs_list():
    total_dogs = len(dogs)
    large_dogs = len([dog for dog in dogs if dog['size'] == 'Крупная'])
    medium_dogs = len([dog for dog in dogs if dog['size'] == 'Средняя'])
    small_dogs = len([dog for dog in dogs if dog['size'] == 'Маленькая'])
    
    return render_template('dogs.html', 
                         dogs=dogs, 
                         total_dogs=total_dogs,
                         large_dogs=large_dogs,
                         medium_dogs=medium_dogs,
                         small_dogs=small_dogs)
