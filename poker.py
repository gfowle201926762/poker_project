from os import set_blocking
import random
import numpy
from numpy.core.defchararray import isnumeric

players = 3
bb = 2
sb = 1
starting_chips = 200
deck = []

# Create the deck
for value in range(2, 15):
    for suit in range(0, 4):
        card = f"{value}, {suit}"
        deck.append(card)

random.shuffle(deck)

# Give values to each potential hole
# each hole needs to be given an equity percentage
#graph = numpy.full((13, 13), 0)




class player:
    def __init__(self, hand, position, bet, chips, playing, turn, required, set, cards, type):
        self.hand = hand
        self.position = position
        self.bet = bet
        self.chips = chips
        self.playing = playing
        self.turn = turn
        self.required = required
        self.set = set
        self.cards = cards
        self.type = type

    def check(self):
        if self.bet >= self.required:
            pass
        else:
            print(f"You need to match the required amount of {self.required}. This means you need to bet at least an additional {self.required - self.bet}.")
            print("what would you like to do? Enter check, raise or fold.")
            self.go()

    def call(self):
        x = self.required - self.bet
        if x <= 0:
            print("You have already bet the required amount.")
        if x > self.chips:
            print(f"You cannot call the full amount. To continue, you must go all in with an additional {self.chips} chips. Enter continue, or fold.")
            i = input("")
            if i == "continue":
                self.bet += self.chips
                self.chips = 0
            if i == "fold":
                self.fold()
            else:
                print("Your input was not understood. Please enter a selected option.")
                self.call()
        elif x <= self.chips and x > 0:
            self.bet += x
            self.chips -= x
            print(f"You have called: {x} chips have been put in to meet the required amount of {self.required}.")

    def fold(self):
        self.playing = False

    def increase(self):
        y = self.required - self.bet
        if y > self.chips:
            print("You cannot raise, as you cannot call the full amount. To continue, you must go all in with an additional {self.chips} chips. Enter continue, or fold.")
            i = input("")
            if i == "continue":
                self.bet += self.chips
                self.chips = 0
            if i == "fold":
                self.fold()
            else:
                print("Your input was not understood. Please enter a selected option.")
                self.increase()


        if y <= self.chips:
            
            print(f"You have selected raise. The required amount to call is {y}. How much would you like to raise in addition to this?")
            amount = input("")
            x = int(amount)

            if x > (self.chips - y):
                print("You do not have that many chips to bet. Please raise by a smaller amount.")
                self.increase()

            elif x <= (self.chips - y):
                self.bet += y
                self.chips -= y
                self.bet += x
                self.chips -= x
                self.required = self.bet
                return "raise"
        return None

    def introduce(self):
        print("\n\n")
        print(f"Player {self.position}")
        print(f"This is your hand: {self.hand}")
        print(f"You have {self.chips} chips, and you have currently bet {self.bet}. The required betting amount to continue is {self.required}.")

        print("what would you like to do? Enter check, call, raise, or fold.")
        if self.type == "unknown":
            d = self.go()
        if self.type == "known":
            d = self.think()
        self.turn += 1
        return self.required, d

    def go(self):
        x = input("")
        if x == "check" or x == "":
            self.check()
            return None
        elif x == "fold":
            self.fold()
            return None
        elif x == "raise":
            d = self.increase()
            return d
        elif x == "call":
            self.call()
            return None
        else:
            print("please enter one of the presented options.")
            self.go()

    def straight(self):
        high_straight_card_list = []
        for value in self.cards[0]:
                                
            if value > 5:
                straight = True
                for num in range((value - 4), (value)):
                    if num not in self.cards[0]:
                        straight = False
                                            
                if straight == True:
                    high_straight_card = value
                    high_straight_card_list.append(high_straight_card)

            if value < 10:
                straight = True
                for num in range((value + 1), (value + 5)):
                    if num not in self.cards[0]:
                        straight = False

                if straight == True:
                    high_straight_card = value + 4
                    high_straight_card_list.append(high_straight_card)

        if int(len(high_straight_card_list)) == 0:
            straight = False
            return straight, None

        if int(len(high_straight_card_list)) > 0:
            straight = True
            high_straight = max(high_straight_card_list)
            return straight, high_straight

    def flush(self):
        spades = 0
        hearts = 0
        diamonds = 0
        clubs = 0
        spades_list = []
        hearts_list = []
        diamonds_list = []
        clubs_list = []
        count = 0
        for suit in self.cards[1]:
            if suit == 0:
                spades += 1
                value = self.cards[0, count]
                spades_list.append(value)
            if suit == 1:
                hearts += 1
                value = self.cards[0, count]
                hearts_list.append(value)
            if suit == 2:
                diamonds += 1
                value = self.cards[0, count]
                diamonds_list.append(value)
            if suit == 3:
                clubs += 1
                value = self.cards[0, count]
                clubs_list.append(value)
            count += 1

        flush = False

        if spades >= 5:
            flush = True
            spades_list.sort(reverse=True)
            return flush, spades_list
            
        if hearts >= 5:
            hearts_list.sort(reverse=True)
            flush = True
            return flush, hearts_list
            
        if diamonds >= 5:
            diamonds_list.sort(reverse=True)
            flush = True
            return flush, diamonds_list
        
        if clubs >= 5:
            clubs_list.sort(reverse=True)
            flush = True
            return flush, clubs_list

        return flush, None
        
    def kind(self):
        values = self.cards[0]
        four_count = 0
        four_rank = None
        three_count = 0
        three_rank = None
        two_count = 0
        two_ranks = []
        two_rank = None
        kicker_list = []
        for num in range(0, 15):
            x = (values == num).sum()
            if x == 4:
                four_count += 1
                four_rank = num
                kicker_list = []
                for k in self.cards[0]:
                    if k != num:
                        kicker_list.append(k)
                kicker = max(kicker_list)
                kicker_list = [kicker]
                break
            if x == 3:
                three_count += 1
                three_rank = num
                break
            if x == 2:
                two_count += 1
                two_ranks.append(num)
                if two_count == 2:
                    break

        # changing pair ranking definitions
        if int(len(two_ranks)) == 1:
            two_rank = two_ranks[0]
            
        if int(len(two_ranks)) == 2:
            two_rank = two_ranks
            two_rank.sort(reverse=True)


        # three of a kind kickers (2)
        if three_count == 1 and two_count == 0:
            for k in self.cards[0]:
                if k != three_rank:
                    kicker_list.append(k)
            kicker_list.sort(reverse=True)
            kicker_list.pop(-1)
            kicker_list.pop(-1)

        # double pair kicker (1)
        if two_count == 2:
            for k in self.cards[0]:
                if k not in two_rank:
                    kicker_list.append(k)
            kicker = max(kicker_list)
            kicker_list = [kicker]

        # single pair kickers (3)
        if two_count == 1 and three_count == 0:
            for k in self.cards[0]:
                if k != two_rank:
                    kicker_list.append(k)
            kicker_list.sort(reverse=True)
            kicker_list.pop(-1)
            kicker_list.pop(-1)

        # high card on nothing
        if four_count == 0 and three_count == 0 and two_count == 0:
            for k in self.cards[0]:
                kicker_list.append(k)
            kicker_list.sort(reverse=True)
            kicker_list.pop(-1)
            kicker_list.pop(-1)

        return four_count, four_rank, three_count, three_rank, two_count, two_rank, kicker_list

    def showdown(self):

        print(f"\nPlayer {self.position} showdown!")
        print(self.cards)

        score = 0
        #detect straights
        straight, high = self.straight()

        #detect flushes
        flush, flush_list = self.flush()

        #detect kinds
        four_count, four_rank, three_count, three_rank, two_count, two_rank, kicker_list = self.kind()


        # Straight-flush
        if straight == True and flush == True:
            score += (1000 + high)
            if high == 14:
                print("Royal flush!!")
            else:
                print(f"Straight flush with high card {high}")

        # four of a kind
        elif four_count == 1:
            score += (900 + four_rank + (kicker_list[0] / 100))
            print(f"Four of a kind with rank {four_rank} and kicker {kicker_list[0]}.")

        # full house
        elif three_count == 1 and two_count == 1:
            score += (800 + three_rank + (two_rank / 100))
            print(f"Full house with triple {three_rank} and pair {two_rank}.")

        # simple flush
        elif flush == True:
            score += (700 + flush_list[0] + (flush_list[1] / 100) + (flush_list[2] / 10000) + (flush_list[3] / 1000000) + (flush_list[4] / 100000000))
            print(f"Flush with high card {flush_list[0]}.")

        # simple straight
        elif straight == True:
            score += (600 + high)
            print(f"Straight with high card {high}.")

        # three of a kind
        elif three_count == 1:
            score += (500 + three_rank + (kicker_list[0] / 100) + (kicker_list[1] / 10000))
            print(f"Three of a kind of rank {three_rank} and kicker {kicker_list[0]}.")

        # double pair
        elif two_count == 2:
            score += (400 + two_rank[0] + (two_rank[1] / 100) + (kicker_list[0] / 10000))
            print(f"Double pair with high pair {two_rank[0]} and low pair {two_rank[1]}, and kicker {kicker_list[0]}.")

        # single pair
        elif two_count == 1:
            score += (300 + two_rank + (kicker_list[0] / 100) + (kicker_list[1] / 10000) + (kicker_list[2] / 1000000))
            print(f"Single pair of {two_rank} and kicker {kicker_list[0]}.")

        elif two_count == 0 and three_count == 0 and four_count == 0 and straight == False and flush == False:
            score += (kicker_list[0] + (kicker_list[1] / 100) + (kicker_list[2] / 10000) + (kicker_list[3] / 1000000) + (kicker_list[4] / 100000000))
            print(f"High card {kicker_list[0]}")


        return score

    def think(self):

        '''
        Create a numpy array with the card square. (A global object?)
        Assign each hole a value.
        '''

        values = self.cards[0]
        suits = self.cards[1]

        s = False
        o = True

        pair = False
        
        if suits[0] == suits[1]:
            s = True
            o = False

        if values[0] == values[1]:
            pair = True

        #1 straight flush
        #2 four of a kind
        #3 full house
        #4 simple flush
        #5 simple straight
        #6 three of a kind
        #7 double pair
        #8 single pair
        
        

        

        

        '''What do we need?
        Calculate the likelyhood of each player having a better hand than yours.
        This needs to be done at each stage: pre-flop, flop, turn, river.

        We need to know:
        Strength of our own cards at each stage.
        What our likely improvements would be at each stage.
        What board position we are in.

        Output:
        Either fold, check, call, or raise (and by how much)
        
        '''






cards = None
hand = None

player_1 = player(hand, 1, 0, starting_chips, True, 1, 0, [], cards, "unknown")
player_2 = player(hand, 2, 0, starting_chips, True, 1, 0, [], cards, "unknown")
if players > 2:
    player_3 = player(hand, 3, 0, starting_chips, True, 1, 0, [], cards, "unknown")
    player_list = [player_1, player_2, player_3]
if players > 3:
    player_4 = player(hand, 4, 0, starting_chips, True, 1, 0, [], cards, "unknown")
    player_list = [player_1, player_2, player_3, player_4]
if players > 4:
    player_5 = player(hand, 5, 0, starting_chips, True, 1, 0, [], cards, "unknown")
    player_list = [player_1, player_2, player_3, player_4, player_5]
if players > 5:
    player_6 = player(hand, 6, 0, starting_chips, True, 1, 0, [], cards, "unknown")
    player_list = [player_1, player_2, player_3, player_4, player_5, player_6]
if players > 6:
    player_7 = player(hand, 7, 0, starting_chips, True, 1, 0, [], cards, "unknown")
    player_list = [player_1, player_2, player_3, player_4, player_5, player_6, player_7]
if players > 7:
    player_8 = player(hand, 8, 0, starting_chips, True, 1, 0, [], cards, "unknown")
    player_list = [player_1, player_2, player_3, player_4, player_5, player_6, player_7, player_8]





class table:
    def __init__(self, board, deck, pot):
        self.board = board
        self.deck = deck
        self.pot = pot

    def numpyify(self, player, size):
        player.cards = numpy.full((2, size), 0)
        card_count = 0
        for card in player.set:
            count = 0
            for char in card:
                if char == ",":
                    break
                count += 1
            if count == 1: #1 digit
                v = card[0]
                value = int(v)
            if count == 2: #2 digits
                v = card[0:2]
                value = int(v)
            suit = card[-1]
            player.cards[0, card_count] = value
            player.cards[1, card_count] = suit
            card_count += 1

    def flop(self):
        self.board = self.deck[0:3]
        del self.deck[0:3]
        for player in player_list:
            if player.playing == True:
                player.set = player.hand + self.board
                self.numpyify(player, 5)
        print(f"\n\nHERE IS THE FLOP: {self.board}\n\n")

    def turn(self):
        x = self.deck[0]
        self.board.append(x)
        del self.deck[0]
        for player in player_list:
            if player.playing == True:
                player.set = player.hand + self.board
                self.numpyify(player, 6)
        print(f"\n\nHERE IS THE TURN: {self.board}\n\n")

    def river(self):
        x = self.deck[0]
        self.board.append(x)
        del self.deck[0]
        for player in player_list:
            if player.playing == True:
                player.set = player.hand + self.board
                self.numpyify(player, 7)
        print(f"\n\nHERE IS THE RIVER: {self.board}\n\n")

    def clear(self, winner_list, tie):
        x = self.board[0:5]
        self.deck = self.deck + x
        self.board = []
        for player in player_list:
            self.deck = self.deck + player.hand
            player.hand = None
            player.set = None
            self.pot += player.bet
            player.bet = 0
            player.turn = 1
            player.required = 0
            player.playing = True

        for winner in winner_list:
            winnings = self.pot / tie
            winner.chips += winnings
            print(f"Player {winner.position} has won {winnings} chips.")
        self.pot = 0

    def deal(self):
        for player in player_list:
            player.hand = self.deck[0:2]
            del self.deck[0:2]
            player.set = player.hand
            self.numpyify(player, 2)
            if player.position == 1:
                player.chips -= sb
                player.bet += sb
            if player.position == 2:
                player.chips -= bb
                player.bet += bb
            player.required = bb

    def decide(self, scores, full_list):
        high = max(scores)
        tie = scores.count(high)
        position_list = []
        for num in range(0, int(len(full_list) / 2)):
            if full_list[num * 2] == high:
                position = full_list[(num * 2) + 1]
                position_list.append(position)
        return position_list, tie

    def play(self, stage):
        playing = True
        d_count = 0
        start = True
        while playing == True:
            for player in player_list:
                if player.playing == True:
                    if start == False:
                        player_count = 0
                        for p in player_list:
                            if p.playing == True:
                                player_count += 1
                        if d_count == (player_count - 1):
                            break
                    x, d = player.introduce()
                    d_count += 1
                    if d == "raise":
                        d_count = 0
                    for player in player_list:
                        player.required = x
            start = False
            equalised = True
            for player in player_list:
                if player.playing == True:
                    if player.bet != x:
                        equalised = False

            if equalised == True:
                stage += 1
                if stage == 3:
                    self.turn()
                    start = True
                if stage == 4:
                    self.river()
                    start = True
                if stage == 5:
                    full_list = []
                    scores = []
                    for player in player_list:
                        if player.playing == True:
                            score = player.showdown()
                            scores.append(score)
                            full_list.append(score)
                            full_list.append(player)
                    
                    winner_list, tie = self.decide(scores, full_list)

                    if tie == 1:
                        winner = winner_list[0]
                        print(f"\nWinner of this round is Player {winner.position}")

                    if tie > 1:
                        print(f"\nThere is a tie between:")
                        for x in range(0, tie):
                            winner = winner_list[x]
                            print(f"Player {winner.position}")

                    self.clear(winner_list, tie)
                    playing = False
        print("Enter any key and hit enter to start next round.")
        again = input("")
        self.start()

    def start(self):
        stage = 1
        self.deal()
        equalised = False
        d_count = 0
        start = True
        while equalised == False:
            for player in player_list:
                if player.position != 1 and player.position != 2:
                    if start == False:
                        player_count = 0
                        for p in player_list:
                            if p.playing == True:
                                player_count += 1
                        if d_count == (player_count - 1):
                            break
                    x, d = player.introduce()
                    d_count += 1
                    if d == "raise":
                        d_count = 0
                    for player in player_list:
                        player.required = x
            for player in player_list:
                if player.position == 1 or player.position == 2:
                    if start == False:
                        player_count = 0
                        for p in player_list:
                            if p.playing == True:
                                player_count += 1
                        if d_count == (player_count - 1):
                            break
                    x, d = player.introduce()
                    d_count +=1
                    if d == "raise":
                        d_count = 0
                    for player in player_list:
                        player.required = x

            start = False

            equalised = True
            for player in player_list:
                if player.playing == True:
                    if player.bet != x:
                        equalised = False

        stage += 1
        self.flop()
        self.play(stage)
            

board = []
gametable = table(board, deck, 0)


gametable.start()