from app import app
from flask import render_template, request, redirect, url_for
from app import game as classgame
import pickle

@app.route('/')
@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/newgame', methods=['GET', 'POST'])
def newgame():
    modeid = int(request.args.get('mode'))
    name = str(request.args.get('name'))
    game = classgame.Game(mode=modeid, p1=name)
    game.init_game()
    pickle.dump(game, open('game.pkl', 'wb'))
    return redirect(url_for('game'))


@app.route('/state')
def game():
    game = pickle.load(open('game.pkl', 'rb'))
    currentplayer = game.turn % 4
    game.players[currentplayer].add_card(game.choose())
    renderplayer = []
    for a in game.players:
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

    cards_remaining = game.cards_in_deck()

    game.currentInfo = 'Ruch gracza '+game.players[currentplayer].name
    return render_template('index.html', player_me=renderplayer[currentplayer], player_1=renderplayer[(currentplayer+1)%4],
                           player_2=renderplayer[(currentplayer+2)%4], player_3=renderplayer[(currentplayer+3)%4], cards_remaining=cards_remaining, info=game.currentInfo)

@app.route('/play/<id>', methods=['GET', 'POST'])
def playcard(id):
    game = pickle.load(open('game.pkl', 'rb'))
    playerid = game.turn%4 #który gracz się ruszył
    a = int(id)

    game.players[playerid].play_card(a)
    pickle.dump(game, open('game.pkl', 'wb'))
    return redirect(url_for('game'))

