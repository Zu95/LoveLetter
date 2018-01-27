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
    game = classgame.Game(mode=1, p1=name)
    game.init_game()
    for a in game.players:
        for j in range(2):
            try:
                x = game.player1.cardsInHand[j]
            except:
                a = cards.One()
                game.player1.cardsInHand.append(a)

        for i in range(4):
            try:
                x = game.player1.cardsPlayed[i]
            except:
                a = cards.One()
                game.player1.cardsPlayed.append(a)

    player_me = {'username': game.players[0].name, 'points': game.player1.points,
                 'cardinhand1': game.player1.cardsInHand[0].value, 'cardinhand2': game.player1.cardsInHand[1].value,
                 'cardplayed1': game.player1.cardsPlayed[0].value, 'cardplayed2': game.player1.cardsPlayed[1].value, 'cardplayed3': game.player1.cardsPlayed[2].value, 'cardplayed4': game.player1.cardsPlayed[3].value,
                 'info': game.player1.privateInfo}
    player_1 = {'username': 'Roman',
                'cardplayed1': '2', 'cardplayed2': '3', 'cardplayed3': '4', 'cardplayed4': '6'}
    player_2 = {'username': 'Andrzej',
                'cardplayed1': '2', 'cardplayed2': '3', 'cardplayed3': '4', 'cardplayed4': '6'}
    player_3 = {'username': 'Andżelika',
                'cardplayed1': '2', 'cardplayed2': '3', 'cardplayed3': '4', 'cardplayed4': '6'}
    cards_remaining = game.cards_in_deck()
    info = game.currentInfo
    return render_template('index.html', player_me=player_me, player_1=player_1,
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