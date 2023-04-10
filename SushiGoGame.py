import neat
from Deck import Deck
from Player import Player

class SushiGoGame():   
    
    def __init__(self, n_players= 2, deck = None, player_hands = [], open_cards = []):
        self.n_players = n_players
        #self.players = [Player(i) for i in range(n_players)]
        self.player_hands = player_hands
        self.open_cards = []*n_players
        self.game_info = True
        self.round = 0

        self.set_deck(deck)
        self.deal_cards()
        pass

    def increase_round(self):
        self.round += 1

    def get_hands(self):
        return self.player_hands
    
    def get_open_cards(self):
        return self.open_cards

    def play_moves(self, moves):
        for i, move in enumerate(moves):
            self.player_hands[i].remove(self.deck.removeCard())
            self.open_cards.append(move)
        
        if len(self.player_hands[0]) == 0:
            self.game_info = False
        #players pass cards to next player

    def set_deck(self, cards):
        if cards == None:
            tempura         = ['tempura']* 14
            sashimi         = ['sashimi']* 14
            dumpling        = ['dumpling']* 14
            two_maki        = ['maki_2'] * 12
            three_maki      = ['maki_3'] * 8
            one_maki        = ['maki_1' ]* 6
            zalm_nigiri     = ['nig_zalm'] * 10
            inktvis_nigiri  = ['nig_inkt'] * 5
            ei_nigiri       = ['nig_ei'] *5
            pudding         = ['pudding'] * 10
            wasabi          = ['wasabi' ]* 6
            eetstokjes      = ['eetstokjes'] * 4
            soja_saus       = ['soja_saus'] * 4

            cards = tempura + sashimi + dumpling + two_maki + three_maki + one_maki + zalm_nigiri + inktvis_nigiri + ei_nigiri + pudding + wasabi + eetstokjes+ soja_saus
        self.deck = Deck(cards)

    def pass_cards(self):
        temp = self.player_hands[0]
        for i in range(self.n_players):
            if i == self.n_players-1:
                self.player_hands[i] = temp
            else:
                self.player_hands[i] = self.player_hands[i+1]

    def deal_cards(self):
        for i in range(self.n_players):
            self.player_hands.append([])
            for j in range(self.get_initial_hand_size()):
                self.player_hands[i].append(self.deck.removeCard())

    def get_initial_hand_size(self):
        return 12- self.n_players
    
    def calculate_scores(self):
        hands       = self.get_hands()
        open_cards  = self.get_open_cards()
        if len(hands[0])>0:
            print('game not finished')
            return
        scores  = [0]*self.n_players
        makis   = [0]*self.n_players

        for i, played_cards in enumerate(open_cards):
            makis[i] += played_cards.count('maki_1') + 2*played_cards.count('maki_2') + 3*played_cards.count('maki_3')

        # the player with the most makis gets plus 6, the other plus 3. In case of a draw, both get 3 points added
        max_makis = max(makis)
        for i, maki in enumerate(makis):
            if maki == max_makis:
                scores[i] += 6
            else:
                scores[i] += 3



        pass

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:
            output1 = net1.activate(inputs)
            decision1 = output1.index(max(output1))

            output2 = net2.activate(inputs)
            decision2 = output2.index(max(output2))
            
            moves = [decision1, decision2]
            self.play_moves(moves)
            self.pass_cards()


            game_info = self.game_info

            if game_info.end == True:
                run = False
                scores = self.calculate_scores()