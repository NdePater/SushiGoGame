class Player:
    #the player is a class
    def __init__(self, player_id):#, strategy):
        self.new_hand = []
        self.old_hand = []
        self.played_cards = []
        self.id = player_id
        
        self.totalPoints = 0
        self.winCount = 0
        self.wasabi = False
        self.pudding = 0
        self.makis = 0
        self.colour_count = 0
        # self.strategy = strategy

    #A player draws a card from the deck
    def addCard(self, card):
        self.new_hand.append(card)

    #The amount of cards in the hand is determined
    def __len__(self):
        return len(self.new_hand)

    #The card is removed from the hand 
    def playCard(self, card):
        return self.hand.remove(card)

    def new_round(self):
        self.played_cards = []
        self.new_hand = []
        self.old_hand = []
        self.makis = 0
        self.colour_count = 0
