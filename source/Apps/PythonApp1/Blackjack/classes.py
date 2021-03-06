'''Blackjack game classes'''

import os

def clear():
    '''Clear console'''
    os.system('cls')

SUITS = ('c', 'd', 'h', 's')
SUIT_NAMES = {'c': 'Clubs', 'd':'Diamonds', 'h':'Hearts', 's':'Spades'}
RANK_CARDS = ('J', 'Q', 'K', 'A')

class Card():
    '''
    Card class
    '''
    def __init__(self, suit, value, rank=False):
        self.suit = suit
        self.value = value
        self.rank = rank

    def __str__(self):
        return f'{self.value} {SUIT_NAMES[self.suit]}'

class Deck():
    '''
    Deck class
    '''
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for i in range(2, 11):
                card = Card(suit, i)
                self.cards.append(card)
            for rank in RANK_CARDS:
                card = Card(suit, rank, True)
                self.cards.append(card)
        self.shuffle()

    def shuffle(self):
        '''Shuffle the deck'''
        import random
        random.shuffle(self.cards)

    def draw_card(self):
        '''Give a card'''
        return self.cards.pop()

class Hand():
    '''
    Hand class
    '''
    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card: Card):
        '''Hit'''
        self.cards.append(card)
        self.value += self.get_card_value(card)

    def get_card_value(self, card: Card):
        '''Get card value'''
        if card.value == 'A' and self.value + 11 > 21:
            return 1
        if card.value == 'A':
            return 11
        if card.rank:
            return 10
        return card.value

    def __str__(self):
        result = ''
        for card in self.cards:
            result += str(card)
            result += '\n'
        result += f'Value: {self.value}'
        return result

class Player():
    '''
    Player class
    '''
    def __init__(self, name, start_cash):
        self.name = name
        self.cash = start_cash
        self.bets = 0
        self.wins = 0
        self.hand = Hand()

    def bet(self, amount):
        '''Make a bet'''
        self.bets += amount
        self.cash -= amount

    def win(self, amount):
        '''Receive prize'''
        self.wins += amount
        self.cash += amount

    def add_cash(self, amount):
        '''Your wife is kind today'''
        self.cash += amount

    def draw_card(self, card: Card):
        '''Get a card'''
        self.hand.add_card(card)

    def clear_hand(self):
        '''Create new hand'''
        self.hand = Hand()

    def __str__(self):
        return f'{self.name} - {self.cash}, bets: {self.bets}, win: {self.wins}'

class Dealer():
    '''
    Dealer class
    '''
    def __init__(self):
        self.name = 'Dealer'
        self.bets = 0
        self.wins = 0
        self.hand = Hand()

    def bet(self, amount):
        '''Make a bet'''
        self.bets += amount

    def win(self, amount):
        '''Receive prize'''
        self.wins += amount

    def draw_card(self, card: Card):
        '''Get a card'''
        self.hand.add_card(card)

    def clear_hand(self):
        '''Create new hand'''
        self.hand = Hand()

    def __str__(self):
        return f'{self.name}, bets: {self.bets}, win: {self.wins}'

class BlackjackGame():
    '''
    Game class
    '''
    def __init__(self):
        self.players = []
        self.dealer = Dealer()
        self.dealer_plays = False
        self.deck = None

    def invite_players(self):
        '''Invite players'''
        players_count, play_with_dealer = self.__ask_human_players_count_and_dealer()
        self.__create_human_players(players_count)
        self.dealer_plays = play_with_dealer

    def play(self):
        '''Lap'''
        clear()
        self.__print_players()
        self.__clear_hands()
        bet = self.__make_bets()
        clear()
        self.__print_players()
        self.deck = Deck()
        self.__original_hand()
        if self.dealer_plays:
            self.__show_dealer()
        for player in self.players:
            self.__turn(player)
            print('========================')
        best_player = None
        best_hand_value = None
        not_busted = list(filter(lambda p: p.hand.value <= 21, self.players))
        if not_busted:
            best_player = max(not_busted, key=lambda p: p.hand.value)
            best_hand_value = best_player.hand.value
        best_players = list(filter(lambda p: p.hand.value == best_hand_value, not_busted))
        if self.dealer_plays:
            self.__dealer_turn(best_hand_value)
            print('========================')
        self.__finish_lap(best_players, bet)

    def __clear_hands(self):
        '''Clear hands'''
        for player in self.players:
            player.clear_hand()
        if self.dealer_plays:
            self.dealer.clear_hand()

    def __original_hand(self):
        for player in self.players:
            self.__draw_two_cards(player)
        if self.dealer_plays:
            self.__draw_two_cards(self.dealer)

    def __draw_two_cards(self, player):
        player.draw_card(self.deck.draw_card())
        player.draw_card(self.deck.draw_card())

    def __finish_lap(self, best_players, current_bet):
        win = current_bet * len(self.players)
        if self.dealer_plays:
            win += current_bet
        if not best_players:
            print(f'{self.dealer.name} wins {win}')
        else:
            #multiple best hands
            if self.dealer_plays:
                if self.dealer.hand.value == best_players[0].hand.value:
                    print('Draw')
                    #draw multiple players
                    win /= 1 + len(best_players)
                    self.dealer.win(win)
                    print(f'{self.dealer.name} wins {win}')
                    for best_player in best_players:
                        best_player.win(win)
                        print(f'{best_player.name}, you win {win}')
                elif self.dealer.hand.value <= 21:
                    self.dealer.win(win)
                    print(f'{self.dealer.name} wins {win}')
                else:
                    win /= len(best_players)
                    for best_player in best_players:
                        best_player.win(win)
                        print(f'{best_player.name}, you win {win}')
            else:
                print('Draw')
                win /= len(best_players)
                for best_player in best_players:
                    best_player.win(win)
                    print(f'{best_player.name}, you win {win}')

    def __make_bets(self):
        while True:
            try:
                bet_value = int(input('Current bet: '))
            except ValueError:
                print('Invalid bet value')
            else:
                break
        for player in self.players:
            player.bet(bet_value)
        if self.dealer_plays:
            self.dealer.bet(bet_value)
        return bet_value

    def __turn(self, player):
        play = True
        while play:
            print(f'{player.name}, your hand:')
            print(player.hand)
            if player.hand.value == 21:
                print(f'{player.name}, BLACKJACK.:')
                return
            draw_card = ''
            while draw_card not in ['y', 'n']:
                draw_card = input('Next card? (y/n)')
            if draw_card == 'y':
                player.draw_card(self.deck.draw_card())
                if player.hand.value > 21:
                    print(player.hand)
                    print(f'{player.name}, BUST.')
                    play = False
            else:
                play = False
            print('------------------------')

    def __dealer_turn(self, best_hand_value):
        if best_hand_value is None:
            return
        print(f"{self.dealer.name}'s turn:")
        print(f"{self.dealer.name}'s hand:")
        print(self.dealer.hand)
        from time import sleep
        while self.dealer.hand.value < best_hand_value:
            print(f'{self.dealer.name} take a card...')
            self.dealer.draw_card(self.deck.draw_card())
            print(self.dealer.hand)
            sleep(3)
            print('------------------------')

    def __ask_human_players_count_and_dealer(self):
        players_count_str = ''
        while players_count_str not in ['1', '2', '3', '4', '5']:
            players_count_str = input('How many human players will play (max 5)?')
        players_count = int(players_count_str)

        if players_count == 1:
            return players_count, True

        play_with_dealer_str = ''
        while play_with_dealer_str not in ['y', 'n']:
            play_with_dealer_str = input('Play with dealer (y/n)?')
        play_with_dealer = play_with_dealer_str == 'y'

        return players_count, play_with_dealer

    def __create_human_players(self, players_count):
        for i in range(1, players_count + 1):
            new_player = self.__create_player(i)
            self.players.append(new_player)

    def __create_player(self, player_index):
        name = input(f"Player {player_index}, what's your name? ")
        while True:
            try:
                player_cash = int(input(f"{name}, input you start cash: "))
            except ValueError:
                print('Invalid cash amount')
            else:
                return Player(name, player_cash)

    def __print_players(self):
        if self.players:
            for player in self.players:
                print(player)
            if self.dealer_plays:
                print(self.dealer)
        else:
            print('No players')

    def __show_dealer(self):
        print(self.dealer.name)
        print('[?]')
        print(self.dealer.hand.cards[1])
