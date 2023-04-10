import random
from collections import deque

class Deck:
    def __init__(self, cards):
        self.deck = deque(cards)
        random.shuffle(self.deck)

    def removeCard(self):
        return self.deck.pop()

    def __len__(self):
        return len(self.deck)



tempura = ['tempura']* 14
sashimi = ['sashimi']* 14
dumpling =[ 'dumpling']* 14
two_maki = ['two_maki'] * 12
three_maki = ['three_maki'] * 8
one_maki = ['one_maki' ]* 6
zalm_nigiri = ['zalm_nigiri'] * 10
inktvis_nigiri = ['inktvis_nigiri'] * 5
ei_nigiri = ['ei_nigiri'] *5
pudding = ['pudding'] * 10
wasabi = ['wasabi' ]* 6
eetstokjes = ['eetstokjes'] * 4
soja_saus = ['soja_saus'] * 4

all_cards = tempura + sashimi + dumpling + two_maki + three_maki + one_maki + zalm_nigiri + inktvis_nigiri + ei_nigiri + pudding + wasabi + eetstokjes+ soja_saus
  
