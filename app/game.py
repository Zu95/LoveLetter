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

        self.players = [self.player1, self.player2, self.player3, self.player4] #tworzę listę 4 graczy
        self.currentInfo = 'Witamy w grze'
        self.gameon = True

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

            if (card_played.value == 1):
                """
                Akcja przy zagraniu karty 1
                """
                player.privateInfo = 'Wybierz gracza'
                choose_player = self.player3 #tu gracz podaje którego gracza wybiera
                player.privateInfo = 'Zgadnij kartę tego gracza'
                choose_card = 'R2D2' #tu gracz podaje, jaką kartę zgaduje, w formacie string

                if (choose_player.protected == False):
                    self.currentInfo = 'Gracz myśli, że '+choose_player.name+' ma kartę '+choose_card
                    if ((card_played.effect(player=player, chosen_player=choose_player, card=choose_card))==1):
                        self.currentInfo += ' I ma rację, '+choose_player.name+' odpada'
                    elif ((card_played.effect(player=player, chosen_player=choose_player, card=choose_card))==0):
                        self.currentInfo += ' I nie ma racji, nic się nie dzieje'
                else:
                    self.currentInfo = 'Gracz '+choose_player.name+' jest chroniony'

            elif (card_played.value == 2):
                """
                Akcja przy zagraniu karty 2
                """
                player.privateInfo = 'Wybierz gracza'
                choose_player = self.player3  # tu gracz podaje którego gracza wybiera
                if (choose_player.protected == False):
                    card_played.effect(player=player, chosen_player=choose_player)
                    self.currentInfo = 'Gracz '+player.name+' podejrzał kartę gracza '+choose_player.name
                else:
                    self.currentInfo = 'Gracz '+choose_player.name+' jest chroniony i nie można podejrzeć jego karty'

            elif (card_played.value == 3):
                """
                Akcja przy zagraniu karty 3
                """
                player.privateInfo = 'Wybierz gracza'
                choose_player = self.player3  # tu gracz podaje którego gracza wybiera
                if (choose_player.protected == False):
                    self.currentInfo = player.name+' pojedynkuje się z '+choose_player.name
                    if ((card_played.effect(player=player, chosen_player=choose_player))==1):
                        self.currentInfo += ' i wygrywa, ' + choose_player.name + ' odpada'
                    elif ((card_played.effect(player=player, chosen_player=choose_player))==2):
                        self.currentInfo += 'i przegrywa, ' + player.name + ' odpada'
                    elif ((card_played.effect(player=player, chosen_player=choose_player))==0):
                        self.currentInfo += 'i jest remis, nic się nie dzieje.'
                else:
                    self.currentInfo = 'Gracz '+choose_player.name+' jest chroniony i nie można się z nim pojedynkować'

            elif (card_played.value == 4):
                """
                Akcja przy zagraniu karty 4
                """
                card_played.effect(player=player) #akcja dla 4
                self.currentInfo = player.name+' jest chroniony do następnej swojej tury.'

            elif (card_played.value == 5):
                """
                Akcja przy zagraniu karty 5
                """
                player.privateInfo = 'Wybierz gracza'
                choose_player = self.player3  # tu gracz podaje którego gracza wybiera
                if (choose_player.protected == False):
                    card_played.effect(chosen_player=choose_player, game=self)
                    self.currentInfo = choose_player.name+' ma nową kartę w ręce.'
                else:
                    self.currentInfo = 'Gracz '+choose_player.name+' jest chroniony i nie można wymienić jego kart.'

            elif (card_played.value == 6):
                """
                Akcja przy zagraniu karty 6
                """
                player.privateInfo = 'Wybierz gracza'
                choose_player = self.player3  # tu gracz podaje którego gracza wybiera
                if (choose_player.protected == False):
                    card_played.effect(player=player, chosen_player=choose_player) #akcja dla 6
                    self.currentInfo = player.name+' i '+choose_player.name+' zamienili się kartami.'
                else:
                    self.currentInfo = 'Gracz '+choose_player.name+' jest chroniony i nie można się z nim wymienić kartą.'

            elif (card_played.value == 7):
                """
                Akcja przy zagraniu karty 7
                """
                card_played.effect() #akcja dla 7
                self.currentInfo = player.name+' odrzucił kartę, nic to nie zmienia.'

            elif (card_played.value == 8):
                """
                Akcja przy zagraniu karty 8
                """
                card_played.effect(player=player) #akcja dla 8
                self.currentInfo = player.name+' odpada z rundy, bo nie utrzymał pokoju w galaktyce.'

        else:
            pass #kolejka następnego gracza
