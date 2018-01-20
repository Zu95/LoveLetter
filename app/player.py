class Player:
    """
    Klasa obsługuje gracza
    """
    def __init__(self, name='', race='human'):
        self.name = name
        self.active = True
        self.protected = False
        self.cardsInHand = []
        self.cardsPlayed = []
        self.LastCard = 0
        self.points = 0
        self.race = race
        self.privateInfo = ''

    def add_card(self, card):
        """
        Klasa daje graczowi kartę do ręki
        :param card:
        :return:
        """
        self.cardsInHand.append(card) #dodaje do ręki kartę podaną jako zmienną (będzie to rand z talii)

    def play_card(self, card):
        """
        Klasa obsługuje wszystkie zmiany, które zachodzą po zagraniu karty.
        1. Usuwa daną kartę z ręki
        2. Dodaje ją do listy zagranych kart
        3. Ustala ją jako ostatnio zagraną kartę
        4. Dodaje graczowi punkty za tą kartę
        :param card: object card
        :return:
        """
        self.cardsInHand.remove(card) #usuwa z ręki wybraną kartę
        self.cardsPlayed.append(card) #dodaje ją do listy zagranych kart
        self.LastCard = card #ustala ją jako ostatnią zagrana kartę
        self.points += card.value #dodaje punkty za kartę


class Computer(Player):
    """
    Klasa odpowiada za myślenie komputera.
    """
    def remember(self, game):
        """
        Klasa przechowuje w głowie komputera informacje na temat graczy w danej rozgrywce.
        :return:
        """
        pass

    def decide(self):
        """
        Klasa pomaga komputerowi wybrać, którą kartę ma zagrać.
        :return: object card
        """

        if(self.cardsInHand[0].value >= self.cardsInHand[1].value): #wybiera mniejszą kartę
            return self.cardsInHand[0]
        else:
            return self.cardsInHand[1]

