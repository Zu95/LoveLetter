from app import app
from flask import render_template, request, redirect
from app import game as classgame, cards


@app.route('/')
@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/game', methods=['GET', 'POST'])
def game():
    modeid = int(request.args.get('mode'))
    name = str(request.args.get('name'))
    newgame = classgame.Game(mode=1, p1=name)
    newgame.init_game()
    renderplayer = []
    for a in newgame.players:
        thisplayer = {'username': a.name, 'points': a.points, 'info': a.privateInfo}
        for j in range(2):
            try:
                thisplayer['cardinhand' + str(j+1)] = a.cardsInHand[j].value
                thisplayer['cardinhand' + str(j+1)+'info'] = a.cardsInHand[j].description
            except:
                thisplayer['cardinhand' + str(j+1)] = 0

        for i in range(4):
            try:
                thisplayer['cardplayed' + str(i + 1)] = a.cardsPlayed[i].value
            except:
                thisplayer['cardplayed' + str(i + 1)] = 0
        renderplayer.append(thisplayer)

    player_2 = {'username': 'Andrzej',
                'cardplayed1': '2', 'cardplayed2': '3', 'cardplayed3': '4', 'cardplayed4': '6'}
    player_3 = {'username': 'Andżelika',
                'cardplayed1': '2', 'cardplayed2': '3', 'cardplayed3': '4', 'cardplayed4': '6'}
    cards_remaining = newgame.cards_in_deck()
    info = newgame.currentInfo
    return render_template('index.html', player_me=renderplayer[0], player_1=renderplayer[1],
                           player_2=player_2, player_3=player_3, cards_remaining=cards_remaining, info=info)

def index():
    player_me = {'username': 'Zuza',
                 'cardinhand1': '1', 'cardinhand2': '2',
                 'cardplayed1': '2', 'cardplayed2': '3', 'cardplayed3': '4', 'cardplayed4': '6'}
    player_1 = {'username': 'Roman',
                'cardplayed1': '2', 'cardplayed2': '3', 'cardplayed3': '4', 'cardplayed4': '6'}
    player_2 = {'username': 'Andrzej',
                'cardplayed1': '2', 'cardplayed2': '3', 'cardplayed3': '4', 'cardplayed4': '6'}
    player_3 = {'username': 'Andżelika',
                'cardplayed1': '2', 'cardplayed2': '3', 'cardplayed3': '4', 'cardplayed4': '6'}
    cards_remaining = 2
    return render_template('index.html', player_me=player_me, player_1=player_1,
                           player_2=player_2, player_3=player_3, cards_remaining=cards_remaining)