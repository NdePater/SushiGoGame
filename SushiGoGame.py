import neat
from Deck import Deck
from Player import Player
import math

class SushiGoGame():   
    
    def __init__(self, n_players= 2, deck = None, player_hands = [], open_cards = []):
        self.n_players = n_players
        self.player_hands = player_hands
        self.open_cards = [[],[]]
        self.end_of_round = False
        self.round = 0
        self.puddings = []*n_players

        self.set_deck(deck)
        self.deal_cards()
        pass

    def get_inputs(self):
        hands = self.get_hands()
        print(hands)
        open_cards = self.get_open_cards()
        print(open_cards)
        inputs = []
        card_dictionary = {'tempura':0,
                           'sashimi':1,
                           'dumpling':2,
                           'maki_1':3,
                           'maki_2':4,
                           'maki_3':5,
                           'nig_ei':6,
                           'nig_zalm':7,
                           'nig_inkt':8,
                           'pudding':9,
                           'wasabi':10,
                           'eetstokjes':11,
                           'soja_saus':12,}
        for i in range(self.n_players):
            input_hand = [0]*len(card_dictionary)
            input_open = [0]*len(card_dictionary)
            print(input_hand)
            for card in hands[i]:
                input_hand[card_dictionary[card]] += 1  
            if open_cards[i]!=[]:
                for card in open_cards[i]:
                    input_open[card_dictionary[card]] += 1
            inputs += input_hand + input_open
        print(inputs)
        return inputs

    def new_round(self):
        self.increase_round()
        self.end_of_round   = False

        self.set_deck(None, sum(self.puddings))
        self.open_cards     = []*self.n_players
        self.player_hands   = []
        self.deal_cards()

    def increase_round(self):
        self.round += 1

    def get_hands(self):
        return self.player_hands
    
    def get_open_cards(self):
        return self.open_cards

    def play_moves(self, moves):
        illegals = []
        for i, move in enumerate(moves):
            if move not in self.player_hands[i]:
                illegals.append(i, False)
                move = self.player_hands[i][0]

            self.player_hands[i].remove(move)
            self.open_cards.append(move)
        
        if len(self.player_hands[0]) == 0:
            self.end_of_round = True

        return output
        #players pass cards to next player

    def set_deck(self, cards, exclude_pudding = 0):
        if cards == None:
            tempura         = ['tempura']* 14
            sashimi         = ['sashimi']* 14
            dumpling        = ['dumpling']* 14
            one_maki        = ['maki_1' ]* 6
            two_maki        = ['maki_2'] * 12
            three_maki      = ['maki_3'] * 8
            ei_nigiri       = ['nig_ei'] * 5
            zalm_nigiri     = ['nig_zalm'] * 10
            inktvis_nigiri  = ['nig_inkt'] * 5
            pudding         = ['pudding'] * 10
            wasabi          = ['wasabi' ]* 6
            eetstokjes      = ['eetstokjes'] * 4
            soja_saus       = ['soja_saus'] * 4

            cards = tempura + sashimi + dumpling + two_maki + three_maki + one_maki + zalm_nigiri + inktvis_nigiri + ei_nigiri + pudding + wasabi + eetstokjes+ soja_saus
        for i in range(exclude_pudding):
            cards.remove("pudding")
        
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
        # check game end
        if len(hands[0])>0:
            print('game not finished')
            return
        
        scores  = [0]*self.n_players
        makis   = [0]*self.n_players
        # calculate scores for played cards
        for i, played_cards in enumerate(open_cards):
            makis[i] += played_cards.count('maki_1') + 2*played_cards.count('maki_2') + 3*played_cards.count('maki_3')
            
            tempura     = 0
            sashimi     = 0
            nig_ei      = 0
            nig_zalm    = 0
            nig_inkt    = 0
            wasabi      = False
            wasabi_score= 0
            dumpling_count = 0
            for card in played_cards:
                if card == 'wasabi':
                    wasabi = True
                else:
                    wasabi = False
                
                match card:
                    case 'tempura':
                        tempura+=1
                    case 'sashimi':
                        sashimi+=1
                    case 'nig_ei':
                        wasabi_score += 2*wasabi
                        nig_ei+=1
                    case 'nig_zalm':
                        wasabi_score += 4*wasabi
                        nig_zalm+=1
                    case 'nig_inkt':
                        wasabi_score += 6*wasabi
                        nig_inkt+=1
                    case 'dumpling':
                        dumpling_count+=1
                    case 'pudding':
                        self.puddings[i]+=1
        
            scores[i]+= tempura//2*5
            scores[i]+= sashimi//3*10
            scores[i]+= min(math.factorial(dumpling_count),15)
        
        # maki count
        max_makis = max(makis)
        for i, maki in enumerate(makis):
            if maki == max_makis:
                scores[i] += 6
            else:
                scores[i] += 3
        
        # pudding count
        if self.round == 3:
            max_pudding = max(self.puddings)
            # with 4 players subtract points!
            for i, pudding in enumerate(self.puddings):
                if pudding == max_pudding:
                    scores[i] += 6
        
        return scores

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:
            inputs = self.get_inputs()
            output1 = net1.activate(inputs)
            decision1 = output1.index(max(output1))

            output2 = net2.activate(inputs)
            decision2 = output2.index(max(output2))
            
            moves = [decision1, decision2]
            legal1, legal2 = self.play_moves(moves)

            if not legal:
                if player == 0:
                    genome1.fitness -= 10
                    genome2.fitness = 0
                else:
                    genome1.fitness = 0
                    genome2.fitness -= 10
                run = False

            self.pass_cards()


            round_end = self.end_of_round

            if round_end == True:
                if self.round == 3:
                    run = False
                    scores = self.calculate_scores()
                    genome1.fitness = scores[0]
                    genome2.fitness = scores[1]
                else:
                    self.new_round()