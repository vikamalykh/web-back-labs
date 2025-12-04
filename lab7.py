from flask import Blueprint, url_for, abort, request, render_template, make_response, redirect, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from os import path

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


films = [
    {
        "title": "How the Grinch Stole Christmas",
        "title_ru": "Гринч — похититель Рождества",
        "year": 2000,
        "description": "В волшебном городке Ктограде все жители очень любят Рождество. Все, кроме Гринча — зелёного мохнатого отшельника, который живёт в пещере высоко в горах и терпеть не может этот праздник. Вместе со своим верным псом Максом он решает украсть Рождество у всех жителей городка."
    },
    {
        "title": "Krampus",
        "title_ru": "Крампус",
        "year": 2015,
        "description": "Американская семья готовится к Рождеству, но праздничное настроение портится из-за постоянных ссор. Младший сын разочаровывается в духе Рождества и невольно вызывает Крампуса — древнего демона, который наказывает тех, кто потерял веру в праздник. Теперь семье придётся объединиться, чтобы выжить в кошмарную рождественскую ночь."
    },
    {
        "title": "Home Alone",
        "title_ru": "Один дома",
        "year": 1990,
        "description": "Восьмилетний Кевин Маккаллистер случайно остаётся один дома, когда его большая семья уезжает в рождественское путешествие в Париж. Поначалу мальчик радуется свободе, но вскоре ему приходится защищать дом от двух незадачливых грабителей, устраивая для них хитроумные ловушки по всему дому."
    }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return films[id]