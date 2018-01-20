from app import cards
from app import player
from random import randint


class Game:
    """
    Klasa zawiera wszystkie informacje o danej rozgrywce
    """
    def __init__(self, name, mode=1, p1='', p2='Anakin Skywalker', p3='Han Solo', p4='Jabba the Hutt'):
        self.name = name
        self.deck = [cards.Eight(), cards.Seven(), cards.Six(),
                     cards.Five(), cards.Five(),
                     cards.Four(), cards.Four(),
                     cards.Three(), cards.Three(),
                     cards.Two(), cards.Two(),
                     cards.One(), cards.One(), cards.One(), cards.One(), cards.One()] #inicuję talię
        if(mode == 1): # jeden gracz vs 3 komputery, opcja domyślna
            self.player1 = player.Player(p1)
            self.player2 = player.Computer(p2, race='computer') #komputer
            self.player3 = player.Computer(p3, race='computer') #komputer
            self.player4 = player.Computer(p4, race='computer') #komputer
        elif(mode == 2): #dwóch graczy vs 2 komputery
            self.player1 = player.Player(p1)
            self.player2 = player.Player(p2)
            self.player3 = player.Computer(p3, race='computer') #komputer
            self.player4 = player.Computer(p4, race='computer') #komputer
        elif(mode == 3): #trzech graczy vs 1 komputer
            self.player1 = player.Player(p1)
            self.player2 = player.Player(p2)
            self.player3 = player.Player(p3)
            self.player4 = player.Computer(p4, race='computer') #komputer
        elif (mode == 4): #czterech graczy
            self.player1 = player.Player(p1)
            self.player2 = player.Player(p2)
            self.player3 = player.Player(p3)
            self.player4 = player.Player(p4)
        else:
            print('Nie ma takiego typu gry')

        self.players = [self.player1, self.player2, self.player3, self.player4] #tworzę listę 4 graczy
        self.currentInfo = 'Witamy w grze'

    def cards_in_deck(self):
        """
        Funkcja zwraca aktualną liczbę kart w talii
        :return: int
        """
        return len(self.deck)

    def choose(self):
        """
        Funkcja losuje kartę z talii
        :return: object card
        """
        x = randint(0, (self.cards_in_deck()-1)) #losuję in między 0 a liczbą kart w talii
        card = self.deck[x]
        return card

    def init_game(self):
        """
        Funkcja rozdaje karty na początek gry, najpierw usuwa jedną losową kartę z talii
        :return:
        """
        self.deck.remove(self.choose())
        self.player1.add_card(self.choose())
        self.player2.add_card(self.choose())
        self.player3.add_card(self.choose())
        self.player4.add_card(self.choose())

    def human_turn(self, player): #funkcja pokazuje co się dzieje w trakcie tury gracza człowieka
        """
        Funkcja obsługuje turę danego gracza
        :param player: object player
        :return:
        """
        if (player.active == True):
            self.currentInfo = 'Tura gracza ' + player.name #publiczne info
            player.privateInfo = 'Teraz Twoja kolej, zagraj jedną z dwóch kart' #nasz gracz dostaje info, że to jego kolej
            player.protected = False #kończy mu się ochrona jeśli ją miał
            player.add_card(self.choose()) #dobiera losową kartę z talii
            card_played = player.cardsInHand[0] #w tym miejscu gracz podaje, którą kartę chce zagrać, teraz jest to pierwsza lepsza
            player.play_card(card=card_played) #zagrywa kartę z ręki

            if (card_played.value == 1): #jeżeli gracz zagra kartę 1
                player.privateInfo = 'Wybierz gracza'
                choose_player = self.player3 #tu gracz podaje którego gracza wybiera
                player.privateInfo = 'Zgadnij kartę tego gracza'
                choose_card = 'R2D2' #tu gracz podaje, jaką kartę zgaduje, teraz domyślnie R2D2
                self.currentInfo = 'Gracz myśli, że '+choose_player.name+' ma kartę '+choose_card #info dla pozostałych graczy
                card_played.effect(player=player, chosen_player=choose_player, card=choose_card)
            elif (card_played.value == 2): #jeżeli gracz zagra kartę 2
                card_played.effect() #akcja dla 2
            elif (card_played.value == 3):  # jeżeli gracz zagra kartę 3
                card_played.effect() #akcja dla 3
            elif (card_played.value == 4):  # jeżeli gracz zagra kartę 4
                card_played.effect() #akcja dla 4
            elif (card_played.value == 5):  # jeżeli gracz zagra kartę 5
                card_played.effect() #akcja dla 5
            elif (card_played.value == 6):  # jeżeli gracz zagra kartę 6
                card_played.effect() #akcja dla 6
            elif (card_played.value == 7):  # jeżeli gracz zagra kartę 7
                card_played.effect() #akcja dla 7
            elif (card_played.value == 8):  # jeżeli gracz zagra kartę 8
                card_played.effect() #akcja dla 8




        else: pass # kolejka następnego gracza