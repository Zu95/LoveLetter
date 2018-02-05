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
    name1 = str(request.args.get('name1'))
    name2 = str(request.args.get('name2'))
    name3 = str(request.args.get('name3'))
    name4 = str(request.args.get('name4'))
    game = classgame.Game(mode=modeid, p1=name1, p2=name2, p3=name3, p4=name4)
    game.init_game()
    pickle.dump(game, open('game.pkl', 'wb'))
    return redirect(url_for('game'))


@app.route('/game')
def game():
    """
    Funkcja renderuje aktualny widok gry po każdym ruchu i po każdej zmianie.
    Sprawdza czy gra się nie zakończyła.
    Sprawdza, czy ktoś nie wygrał.
    Daje graczowi, którego jest kolej kartę do ręki.
    Zmienia komunikat.

    :return:
    """
    game = pickle.load(open('game.pkl', 'rb'))
    currentplayer = game.turn % 4
    if (game.players[currentplayer].active == False):
        game.turn += 1
        pickle.dump(game, open('game.pkl', 'wb'))
        return redirect(url_for('game'))
    game.currentTurn = 'Ruch gracza ' + game.players[currentplayer].name
    if (game.cards_in_deck()>0): #jeżeli jest jeszcze chociaż jedna karta do dobrania to gramy dalej
        card = game.choose()
        game.players[currentplayer].add_card(card)
        game.deck.remove(card)
    else: #jeżeli skończyły się karty to znaczy że koniec gry
        game.gameon = False
        game.currentInfo.append('Koniec gry')
        pickle.dump(game, open('game.pkl', 'wb'))
        return redirect(url_for('isgameon'))
    game.players[currentplayer].protected = False #już go nie chroni karta 4
    renderplayer = render_player(game=game)
    pickle.dump(game, open('game.pkl', 'wb'))
    return render_template('index.html', player_me=renderplayer[currentplayer], player_1=renderplayer[(currentplayer+1)%4],
                           player_2=renderplayer[(currentplayer+2)%4], player_3=renderplayer[(currentplayer+3)%4],
                           cards_remaining=game.cards_in_deck(), info=game.currentInfo, turn=game.currentTurn)


@app.route('/isgameon')
def isgameon():
    """
    Funkcja sprawdza, czy gra trwa dalej
    :return:
    """
    game = pickle.load(open('game.pkl', 'rb'))
    if (game.gameon == False): #jeżeli zostaliśmy tu przekierowani z jakiegoś zakończenia gry
        activeplayers = []
        for player in game.players: #zliczamy aktywnych graczy
            if (player.active == True):
                if (len(player.cardsInHand) > 0):
                    activeplayers.append(player)
                else:
                    player.active = False
            else:
                pass
        #sprawdzenie, który gracz wygrał
        game.winner = activeplayers[0]
        for player in activeplayers: #wybieramy zwycięzcę z aktywnych graczy, po kartach, które mają w ręce
            if player.cardsInHand[0].value > game.winner.cardsInHand[0].value:
                game.winner = player
        pickle.dump(game, open('game.pkl', 'wb'))
        currentplayer = game.turn % 4
        renderplayer = render_player(game=game)
        return render_template('winner.html', activeplayers=activeplayers,
                               winner=game.winner.name, winnercard=game.winner.cardsInHand[0].value,
                               winnerinfo='i to jest karta o najwyższej wartości',
                               player_me=renderplayer[currentplayer], player_1=renderplayer[(currentplayer+1)%4],
                               player_2=renderplayer[(currentplayer+2)%4], player_3=renderplayer[(currentplayer+3)%4],
                               cards_remaining=game.cards_in_deck(), info=game.currentInfo, turn=game.currentTurn) #przekierowanie do widoku zwycięstwa
    else:
        #sprawdzenie, ilu graczy pozostało w grze
        activeplayers = []
        for player in game.players:
            if (player.active == True):
                activeplayers.append(player)

        if (len(activeplayers)==1):
            game.gameon = False
            game.winner = activeplayers[0]
            pickle.dump(game, open('game.pkl', 'wb'))
            currentplayer = game.turn % 4
            renderplayer = render_player(game=game)
            return render_template('winner.html', winner=game.winner.name, winnercard=game.winner.cardsInHand[0].value,
                                   winnerinfo= 'i jako jedyny pozostał w grze',
                                   player_me=renderplayer[currentplayer],
                                   player_1=renderplayer[(currentplayer + 1) % 4],
                                   player_2=renderplayer[(currentplayer + 2) % 4],
                                   player_3=renderplayer[(currentplayer + 3) % 4],
                                   cards_remaining=game.cards_in_deck(), info=game.currentInfo, turn=game.currentTurn)
        else:
            pickle.dump(game, open('game.pkl', 'wb'))
            return redirect(url_for('game')) #przekierowuje do gry


@app.route('/play/<id>', methods=['GET', 'POST'])
def playcard(id):
    game = pickle.load(open('game.pkl', 'rb'))
    currentplayer = game.turn % 4
    a = int(id)
    card_played = game.players[currentplayer].cardsInHand[a]
    if (game.players[currentplayer].play_card(card=card_played)==True):

        if (bool(card_played.value==1) or bool(card_played.value ==2) or bool(card_played.value == 3) or bool(card_played.value==5) or bool(card_played.value==6)):
            pickle.dump(game, open('game.pkl', 'wb'))
            return redirect(url_for('chooseplayer', id=id)) #zażądaj wybrania gracza
        elif (bool(card_played.value ==4) or bool(card_played.value == 7) or bool(card_played.value==8)): #jeżeli karta działa tylko na jednego gracza
            card_played.effect(player=game.players[currentplayer], game=game)
        game.turn += 1
        pickle.dump(game, open('game.pkl', 'wb'))
        return redirect(url_for('isgameon'))
    else:
        return render_template('start.html')


@app.route('/play/<id>/chooseplayer')
def chooseplayer(id):
    game = pickle.load(open('game.pkl', 'rb'))
    currentplayer = game.turn % 4  # który gracz się ruszył
    playedcardvalue = game.players[currentplayer].lastCard.value
    activeplayers = []
    renderplayer = render_player(game=game)
    for player in game.players:  # zliczamy aktywnych graczy, spośród których można wybierać
        if (player.active == True):
            activeplayers.append(player)  # lista activeplayers
        else:
            pass
    if (playedcardvalue == 1):
        # ten widok przekieruje nas do wytypowania karty
        return render_template('chooseplayerfor1.html', activeplayers=activeplayers, id=id, player_me=renderplayer[currentplayer], player_1=renderplayer[(currentplayer+1)%4],
                           player_2=renderplayer[(currentplayer+2)%4], player_3=renderplayer[(currentplayer+3)%4],
                           cards_remaining=game.cards_in_deck(), info=game.currentInfo, turn=game.currentTurn)
    else:
        # widok przekieruje nas od razu do akcji danej karty
        return render_template('chooseplayer.html', activeplayers=activeplayers, id=id, player_me=renderplayer[currentplayer], player_1=renderplayer[(currentplayer+1)%4],
                           player_2=renderplayer[(currentplayer+2)%4], player_3=renderplayer[(currentplayer+3)%4],
                           cards_remaining=game.cards_in_deck(), info=game.currentInfo, turn=game.currentTurn)


@app.route('/play/<id>/chooseplayer/<chosenplayerid>')
def cardseffect(id, chosenplayerid):
    """
    Wykonuję akcję dla kart 2, 3, 5, 6 po wybraniu przeciwnika
    :param currentplayerid:
    :param cardvalue:
    :param chosenplayerid:
    :return:
    """
    game = pickle.load(open('game.pkl', 'rb'))
    currentplayerid = game.turn % 4  # id gracza który gracz się ruszył
    chosen_player = int(chosenplayerid) #id gracza, który został wybrany

    player = game.players[currentplayerid] #obiekt gracza
    choose_player = game.players[chosen_player] #obiekt wybranego gracza

    card_played = game.players[currentplayerid].lastCard # wybrana karta
    if (choose_player.protected == False):
        if (card_played.value==2): #podejrzenie karty przeciwnika
            card_played.effect(player=player, chosen_player=choose_player)
            game.currentInfo.append('Gracz ' + player.name + ' podejrzał kartę gracza ' + choose_player.name)
        elif (card_played.value==3): #porównanie wartości kart
            game.currentInfo.append(player.name + ' pojedynkuje się z ' + choose_player.name)
            if ((card_played.effect(player=player, chosen_player=choose_player)) == 1):
                game.currentInfo.append(' i wygrywa, ' + choose_player.name + ' odpada')
            elif ((card_played.effect(player=player, chosen_player=choose_player)) == 2):
                game.currentInfo.append(' i przegrywa, ' + player.name + ' odpada')
            elif ((card_played.effect(player=player, chosen_player=choose_player)) == 0):
                game.currentInfo.append(' i jest remis, nic się nie dzieje.')
        elif (card_played.value==5): #wymiana karty w rece wybranego gracza
            card_played.effect(chosen_player=choose_player, game=game)
            game.currentInfo.append(choose_player.name + ' ma nową kartę w ręce.')
        elif (card_played.value==6): #zamiana kart w rękach graczy
            card_played.effect(player=player, chosen_player=choose_player)  # akcja dla 6
            game.currentInfo.append(player.name + ' i ' + choose_player.name + ' zamienili się kartami.')

    else:
        game.currentInfo.append('Gracz ' + choose_player.name + ' jest chroniony')
    game.turn += 1
    pickle.dump(game, open('game.pkl', 'wb'))
    return redirect(url_for('isgameon'))  # przekierowuje do gry


@app.route('/play/<id>/chooseplayer/<chosenplayerid>/choosecard')
def choosecard(id, chosenplayerid):
    game = pickle.load(open('game.pkl', 'rb'))
    currentplayer = game.turn % 4  # który gracz się ruszył
    renderplayer = render_player(game=game)
    return render_template('choosecard.html', current_player=currentplayer, chosen_player=chosenplayerid, id=id, player_me=renderplayer[currentplayer], player_1=renderplayer[(currentplayer+1)%4],
                           player_2=renderplayer[(currentplayer+2)%4], player_3=renderplayer[(currentplayer+3)%4],
                           cards_remaining=game.cards_in_deck(), info=game.currentInfo, turn=game.currentTurn)


@app.route('/play/<id>/chooseplayer/<chosenplayerid>/choosecard/<chosencardvalue>')
def card1effect(id, chosenplayerid, chosencardvalue):
    """
    Wykonuję akcję dla karty 1 po wybraniu przeciwnika i wytypowaniu karty
    :param currentplayerid:
    :param chosenplayerid:
    :param chosencardid:
    :return:
    """
    chosen_player = int(chosenplayerid)
    game = pickle.load(open('game.pkl', 'rb'))
    currentplayerid = game.turn % 4  # który gracz się ruszył
    choose_player = game.players[chosen_player]
    choose_card = int(chosencardvalue)
    player = game.players[currentplayerid]
    card_played = game.players[currentplayerid].lastCard
    if (choose_player.protected == False):
        game.currentInfo.append('Gracz '+ player.name+' myśli, że ' + choose_player.name + ' ma kartę ' + str(choose_card))
        if ((card_played.effect(player=player, chosen_player=choose_player, card=choose_card)) == 1):
            game.currentInfo.append(' i ma rację, ' + choose_player.name + ' odpada ')
        elif ((card_played.effect(player=player, chosen_player=choose_player, card=choose_card)) == 0):
            game.currentInfo.append(' i nie ma racji, nic się nie dzieje ')
    else:
        game.currentInfo.append('Gracz ' + choose_player.name + ' jest chroniony')
    game.turn += 1
    pickle.dump(game, open('game.pkl', 'wb'))
    return redirect(url_for('isgameon'))  # przekierowuje do gry


def render_player(game):
    renderplayer = []
    for a in game.players:
        thisplayer = {'username': a.name, 'points': a.points, 'info': a.privateInfo}
        for j in range(2):
            try:
                thisplayer['cardinhand' + str(j + 1)] = a.cardsInHand[j].value
                thisplayer['cardinhand' + str(j + 1) + 'info'] = a.cardsInHand[j].description
            except:
                thisplayer['cardinhand' + str(j + 1)] = 0

        for i in range(4):
            try:
                thisplayer['cardplayed' + str(i + 1)] = a.cardsPlayed[i].value
            except:
                thisplayer['cardplayed' + str(i + 1)] = 0
        renderplayer.append(thisplayer)

    return renderplayer