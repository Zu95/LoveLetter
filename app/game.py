from app import cards
from app import player
from random import randint


class Game:
    """
    Klasa zawiera wszystkie informacje o danej rozgrywce
    """
    def __init__(self, name='gra', mode=1, p1='', p2='Darth Vader', p3='Palpatine', p4='Jabba the Hutt'):
        self.name = name
        self.turn = 0
        self.currentTurn = ''
        #muszę stworzyć obiekty poszczególnych kart
        self.card1a = cards.One()
        self.card1b = cards.One()
        self.card1c = cards.One()
        self.card1d = cards.One()
        self.card1e = cards.One()
        self.card2a = cards.Two()
        self.card2b = cards.Two()
        self.card3a = cards.Three()
        self.card3b = cards.Three()
        self.card4a = cards.Four()
        self.card4b = cards.Four()
        self.card5a = cards.Five()
        self.card5b = cards.Five()
        self.card6 = cards.Six()
        self.card7 = cards.Seven()
        self.card8 = cards.Eight()
        self.deck = [self.card6, self.card7, self.card8,
                     self.card5a, self.card5b,
                     self.card4a, self.card4b,
                     self.card3a, self.card3b,
                     self.card2a, self.card2b,
                     self.card1a, self.card1b, self.card1c, self.card1d, self.card1e] #inicuję talię
        if(mode == 1): # jeden gracz vs 3 komputery,
            self.player1 = player.Player(name=p1, id=0)
            self.player2 = player.Computer(name=p2, race='computer', id=1) #komputer
            self.player3 = player.Computer(name=p3, race='computer', id=2) #komputer
            self.player4 = player.Computer(name=p4, race='computer', id=3) #komputer
        elif(mode == 2): #dwóch graczy vs 2 komputery
            self.player1 = player.Player(name=p1, id=0)
            self.player2 = player.Player(name=p2, id=1)
            self.player3 = player.Computer(name=p3, race='computer', id=2) #komputer
            self.player4 = player.Computer(name=p4, race='computer', id=3) #komputer
        elif(mode == 3): #trzech graczy vs 1 komputer
            self.player1 = player.Player(name=p1, id=0)
            self.player2 = player.Player(name=p2, id=1)
            self.player3 = player.Player(name=p3, id=2)
            self.player4 = player.Computer(name=p4, race='computer', id=3) #komputer
        elif (mode == 4): #czterech graczy
            self.player1 = player.Player(name=p1, id=0)
            self.player2 = player.Player(name=p2, id=1)
            self.player3 = player.Player(name=p3, id=2)
            self.player4 = player.Player(name=p4, id=3)

        self.players = [self.player1, self.player2, self.player3, self.player4] #tworzę listę 4 graczy
        self.currentInfo = ['Witamy w grze!']
        self.gameon = True
        self.winner = 0

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
        removed = self.choose()
        self.deck.remove(removed)
        for x in self.players:
            random = self.choose()
            x.add_card(random)
            self.deck.remove(random)
