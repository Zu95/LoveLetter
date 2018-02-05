class One:
    """
    Klasa dla karty 1
    """
    def __init__(self):
        self.value = 1
        self.name = 'C3PO'
        self.description = 'C3PO pomaga Ci zgadnąć kartę w ręce innego gracza, jeżeli macie rację - odpadnie on z rundy.'

    def effect(self, player, chosen_player, card):
        """
        Funkcja sprawdza, czy gracz zgadł poprawnie kartę przeciwnika.
        Jeżeli tak, usuwa przeciwnika z gry.
        Jeżeli nie, nic się nie dzieje.
        :param player: object player
        :param chosen_player: object player
        :param card: string
        :return: 1 jeśli zgadł, 0 jeśli nie
        """
        if (chosen_player.cardsInHand[0].value == card):
            chosen_player.active = False
            chosen_player.cardsPlayed.append(chosen_player.cardsInHand[0]) #jego karta w ręce jest wykładana na stół
            return 1
        else:
            return 0



class Two:
    """
    Klasa dla karty 2
    """
    def __init__(self):
        self.value = 2
        self.name = 'R2D2'
        self.description = 'R2D2 wykradnie dla Ciebie informacje o karcie w ręce wybranego gracza.'

    def effect(self, player, chosen_player): #gracz pierwszy dostaje informację o karcie w ręce gracza drugiego
        player.privateInfo += 'Karta w ręce gracza '+ chosen_player.name +' to '+chosen_player.cardsInHand[0].name
        return 1


class Three:
    """
    Klasa dla karty 3
    """
    def __init__(self):
        self.value = 3
        self.name = 'Jedi'
        self.description = 'Walczysz na miecze świetlne z przeciwnikiem. Porównajcie w sekrecie karty - ten z niższą wartością odpada.'

    def effect(self, player, chosen_player): #porównuje karty w ręce dwóch graczy, kto ma niższą odpada
        """
        Funkcja porównuje karty w rękach dwóch graczy.
        Gracz z wyższą kartą odpada.
        Jeżeli karty są identyczne, nic się nie dzieje.
        :param player: object player
        :param chosen_player: object player
        :return: 1 jeśli wygra gracz, którego to jest runda, 2 jeśli przeciwnik, 0 jeżeli żaden
        """
        if (player.cardsInHand[0].value > chosen_player.cardsInHand[0].value):
            chosen_player.active = False
            card = chosen_player.cardsInHand[0]
            chosen_player.cardsInHand.remove(card)
            chosen_player.cardsPlayed.append(card)
            return 1 #akcja na korzyść playera
        elif (player.cardsInHand[0].value < chosen_player.cardsInHand[0].value):
            player.active = False
            card = player.cardsInHand[0]
            player.cardsInHand.remove(card)
            player.cardsPlayed.append(card)
            return 2 #akcja na korzyść chosen_playera
        else:
            return 0 #nic się nie dzieje


class Four:
    """
    Klasa dla karty 4
    """
    def __init__(self):
        self.value = 4
        self.name = 'Sokół Millenium'
        self.description = 'Sokół Millenium wchodzi w nadświetlną! Nikt nie może Ci nic zrobić do następnej Twojej kolejki.'

    def effect(self, player, game): #ustala dla danego gracza ochronę
        """
        Funkcja ustala ochronę dla danego gracza na czas rundy
        :param player:
        :return: 1
        """
        player.protected = True
        game.currentInfo.append(player.name+' jest chroniony do następnej swojej tury')
        return 1


class Five:
    """
    Klasa dla karty 5
    """
    def __init__(self):
        self.value = 5
        self.name = 'Wookie'
        self.description = 'Wookie wytrąca kuszą kartę z ręki innego gracza, musi on dobrać nową.'

    def effect(self, chosen_player, game): #wybrany gracz odrzuca kartę i losuje nową
        """
        Funkcja odrzuca kartę wybranego gracza z ręki i dobiera mu nową z talii.
        Karta ląduje na stole jako odrzucona przez gracza, ale nie daje mu punktów
        :param chosen_player: object player
        :param game: object game
        :return: 1
        """
        card = chosen_player.cardsInHand[0]
        chosen_player.cardsInHand.remove(card)  # usuwa kartę z ręki danego gracza
        chosen_player.cardsPlayed.append(card)  # dodaje kartę do listy odrzuconych kart przez gracza
        if (game.cards_in_deck()>0):
            cardfromdeck=game.choose()
            game.deck.remove(cardfromdeck)
            chosen_player.add_card(cardfromdeck) #dobiera nową kartę dla gracza
        else:
            game.gameon = False
            game.currentInfo.append('Koniec gry')
        return 1


class Six:
    """
    Klasa dla karty 6
    """
    def __init__(self):
        self.value = 6
        self.name = 'Yoda'
        self.description = 'Yoda używa mocy, żeby zamienić kartę w Twojej ręce z kartą w ręce innego gracza.'

    def effect(self, player, chosen_player):
        """
        Funkcja zamienia karty w rękach graczy
        :param player: object player
        :param chosen_player: object player
        :return: 1
        """
        tmp = player.cardsInHand[0]
        player.cardsInHand[0] = chosen_player.cardsInHand[0]
        chosen_player.cardsInHand[0] = tmp
        return 1


class Seven:
    """
    Klasa dla karty 7
    """
    def __init__(self):
        self.value = 7
        self.name = 'Bobba Fett'
        self.description = 'Bobba Fett jest super, ale boi się dziwnych stworzeń. Musisz go odrzucić, jeżeli masz w ręce Yodę albo Wookiego.'

    def effect(self, player, game):
        """
        Funkcja nic nie robi, zwraca że ok
        :return: 1
        """

        return 1


class Eight:
    """
    Klasa dla karty 8
    """
    def __init__(self):
        self.value = 8
        self.name = 'Pokój w galaktyce'
        self.description = 'Musisz utrzymać pokój w galaktyce, żeby zakon Jedi nie zginął. Jeżeli odrzucisz tą kartę - przegrasz.'

    def effect(self, player, game):
        """
        Funkcja zabija gracza, który ją zagrał
        :param player: object player
        :return: 1
        """
        player.active = False
        card = player.cardsInHand[0]
        player.cardsInHand.remove(card)  # usuwa z ręki wybraną kartę
        player.cardsPlayed.append(card)  # dodaje ją do listy wyrzuconych kart, bez rozpatrzenia
        game.currentInfo.append(player.name+' odpada z rundy, bo nie utrzymał pokoju w galaktyce')
        return 1

