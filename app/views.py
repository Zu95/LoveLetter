from app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    player_me = {'username': 'Zuza',
                 'cardinhand1': '1', 'cardinhand2': '2',
                 'cardplayed1': '2', 'cardplayed2': '3', 'cardplayed3': '4', 'cardplayed4': 'test'}
    player_1 = {'username': 'Roman'}
    player_2 = {'username': 'Andrzej'}
    player_3 = {'username': 'Andżelika'}
    cards_remaining = 2
    return render_template('index.html', player_me=player_me, player_1=player_1,
                           player_2=player_2, player_3=player_3, cards_remaining=cards_remaining)