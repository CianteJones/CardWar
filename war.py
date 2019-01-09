# A class that will wrap all our game data together
import random
from deck import Deck
from hand import Hand


class War:

    def __init__(self, num_players=2):

        self.num_players = num_players

        self.hands = [Hand for _ in range(num_players)]
        self.deck = Deck()

    def deal_cards(self):
        # Distributes the cards from the deck to the player
        self.deck.shuffle()
        hands = [[] for _ in range(self.num_players)]
        i = 0
        # If 52 isn't divisible by num_players, then we will have extra cards
        while(len(self.deck) != 0):
            player = i % self.num_players
            hands[player] += self.deck.draw_card()
            i += 1

        # Creates hand objects with the list of cards in them
        for i in range(self.num_players):
            self.hands[i] = Hand(hands[i])

        return self.hands

    def round_winner(self):
        ''' Checks to see which player is winner and grants them cards '''
        # Keeps check of the values of the cards played.
        played_cards = []
        for i in range(self.num_players):
            played_cards += self.hands[i].play_cards()

        # need to do this so I can keep track of index
        highest_card = played_cards[0].value
        winners = [0]
        for i in range(1, self.num_players):
            # ensures that there is a high card
            if highest_card < played_cards[i].value:
                highest_card = played_cards[i]
                # Want the first index of the list to be the winner
                winners[0] = i
            if highest_card == played_cards[i].value:
                # Will pass a list into war so that we can have war with all winners
                winners.append(i)
        # if the highest card is tied, go to war
        if(len(winners) > 1):
            winners.insert(0, self.round_war(winners))

        winner_index = winners[0]
        self.hands[winner_index].discard(played_cards)

        print(winners)

        print(f'Player {winner_index} won this round.')

    def round_war(self, winning_indexes):
        '''Called when values equal each other
           winning_index is a list of the winners for war to initiate
        '''
        # Keeps check of the values of the cards played.
        print('War has been initiated')
        played_cards = [[] for i in range(len(winning_indexes))]
        winner = [winning_indexes[0]]
        for i in range(len(winning_indexes)):
            played_cards[i] = self.hands[winning_indexes[i]].play_cards(3)

        # Checks the last card playeds value
        highest_card = played_cards[0][-1].value

        for i in range(1, len(winning_indexes)):
            # ensures that there is a high card
            if highest_card < played_cards[i][-1].value:
                highest_card = played_cards[i][-1]
                # Want the first index of the list to be the winner
                winner.insert(0, i)
            if highest_card == played_cards[i][-1].value:
                # Will pass a list into war so that we can have war with all winners
                winner.append(i)
        if(winner.count(winner[0] > 1)):
            winner.insert(0, self.round_war(winner))

        return winner[0]

    def check_winner(self):
        ''' Checks to see if there was a winner in the game yet. '''
        winners = [len(c) == len(Deck.fullDeck) for c in self.hands]
        if sum(winners) == 0:
            return -1
        return winners.index(True)
