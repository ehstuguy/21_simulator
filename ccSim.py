#!/usr/bin/env python3

# libraries needed
import random
import itertools

# starting globals
leave_table = False
min_bet = 5
max_bet = 100

# simple dict
players_dict = {
    2: '_NPC 2', 3: '_NPC 3', 4: '_NPC 4', 5: '_NPC 5',
    1: 'User 1', 'D': 'Dealer'}

choice_dict = {
    'hit': 'Hit', 'HIT': 'Hit', 'Hit': 'Hit', 'h': 'Hit',
    'double': 'Double Down', 'dd': 'Double Down',
    'DD': 'Double Down', 'Double Down': 'Double Down',
    'Stay': 'Stay', 'stay': 'Stay', 'STAY': 'Stay', 's': 'Stay',
    'split': 'Split', 'Split': 'Split', 'SPLIT': 'Split', 'sp': 'Split'}

# Classes in session
# ==========================================================================


class Player:
    def __init__(self, id_num, money):
        self.double_down = 0
        self.id_tag = id_num
        self.money = money
        self.split = False

        if self.id_tag == 1:
            self.User = True
            self.NPC = False
        else:
            self.User = False
            self.NPC = True


# Function with gumption
# ==========================================================================


def make_user():
    user_id = 1
    user_money = int(input('\nWhat is your starting amount? '))
    return (user_id, user_money)


def make_npc(npc_id):
    npc_money = random.randint(150, 900)
    return (npc_id, npc_money)


def reshuffle(num_decks):
    # suits = ['diamonds', 'clubs', 'spades', 'hearts']
    suits = ['♦', '♣', '♠', '♥']
    ranks = [2, 3, 4, 5, 6, 7, 8, 10, 'J', 'Q', 'K', 'A']
    deck = list(itertools.product(ranks, suits)) * num_decks
    random.shuffle(deck)
    return deck, []


def count_discard(discard_pile):
    count = 0
    for card in discard_pile:
        if card[0] in [10, 'J', 'Q', 'K', 'A']:
            count += -1
        elif card[0] in [7, 8, 9]:
            count += 0
        elif card[0] in [2, 3, 4, 5, 6]:
            count += 1
    return count


def hit(deck):
    new_card = deck[0]
    discard_pile.append(deck[0])
    deck.remove(deck[0])
    return [new_card]


def count_hand(player_hand):
    hand = player_hand
    # create initial variables
    aces = 0
    hand_value = 0
    first_ace = False

    print(hand)

    # counts each card in hand and adding to initial value of '0'
    for card, suit in hand:
        print(hand_value)

        if card in [10, 'Q', 'J', 'K']:
            hand_value += 10
            if hand_value > 21 and aces == 1 and first_ace == False:
                hand_value += -10
                first_ace = True
        elif card == 'A' and hand_value > 11:
            hand_value += 1
            aces += 1
            first_ace = True
        elif card == 'A' and hand_value < 11:
            hand_value += 11
            aces += 1        
        else:
            hand_value += card
            if hand_value > 11 and aces == 1 and first_ace == False:
                hand_value += -10
                first_ace = True

    if hand_value > 21:
        bust = True
    else:
        bust = False
    return hand_value, bust


def compare(player, dealer):
    if player.hand_value < dealer.hand_value:
        return False, 'Dealer has the higher hand'
    elif player.hand_value == dealer.hand_value:
        return False, 'Dealer wins the tie'
    else:
        return True, 'Player has the higer hand'


def deal_cards(all_playing, dealer):
    deal_order = all_playing + [dealer]
    # deal first card to everyone
    for player in deal_order:
        if player.User == True:
            player.bet = correctr_user_bet()
        else:
            player.bet = random.randint(min_bet, max_bet)
        player.hand = []
        player.hand += [deck[0]]
        discard_pile.append(deck[0])
        deck.remove(deck[0])
    # deal second card to everyone
    for player in deal_order:
        player.hand += [deck[0]]
        discard_pile.append(deck[0])
        deck.remove(deck[0])
    # count hand value
    for player in deal_order:
        player.hand_value, player.bust = count_hand(player.hand)


def correctr_user_bet():
    correct_bet = False
    while correct_bet == False:
        bet_amount = int(
            input('Enter a number between $ 5 and $ 100: '))

        if bet_amount < 5:
            bet_amount = int(
                input('\n\nBet is TOO LOW, please bet between '
                      '$ 5 and $ 100: '))
            correct_bet = False
        elif bet_amount > 100:
            bet_amount = int(
                input('\n\nBet is TOO HIGH, please bet between '
                      '$ 5 and $ 100: '))
            correct_bet = False
        else:
            correct_bet = True
    return bet_amount


# Whose turn is it anyway?
# ========================================================================


def take_turns(player):

    if len(player.hand) == 2 and player.hand_value == 21:
        player.blackjack = True
        if player.User == True:
            print('\n\\nBlackJack!\n\n')
    else:
        player.blackjack = False

    print('\n', players_dict[player.id_tag], '\t', player.hand, '\n')
    if player.User == True:
        User_turn(player)
    elif player.NPC == True:
        NPC_turn(player)


# NPC TURN
# ========================================================================


def NPC_turn(player):
    if player.hand[0][0] == player.hand[1][0]:
        player.split = True
        print('\n', players_dict[player.id_tag],
              '\t', player.hand, '\n')
        NPC_split(player)
    else:
        NPC_hand(player)


def NPC_hand(player):
    while player.hand_value < 17:
        player.hand += hit(deck)
        player.hand_value, player.bust = count_hand(player.hand)
        print('\n', players_dict[player.id_tag],
              '\t', player.hand, '\n')


def NPC_split(player):
    # setup first split
    player.split_h1 = [player.hand[0]]
    player.split_hv1, player.split_b1 = count_hand(player.split_h1)
    # hit on first split
    while player.split_hv1 < 17:
        player.split_h1 += hit(deck)
        player.split_hv1, player.split_b1 = count_hand(player.split_h1)
        print('\n', players_dict[player.id_tag],
              '\t', player.split_h1, '\n')

    # setup second split
    player.split_h2 = [player.hand[1]]
    player.split_hv2, player.split_b2 = count_hand(player.split_h2)
    # hit on second split
    while player.split_hv2 < 17:
        player.split_h2 += hit(deck)
        player.split_hv2, player.split_b2 = count_hand(player.split_h2)
        print('\n', players_dict[player.id_tag],
              '\t', player.split_h2, '\n')


# ========================================================================


def User_turn(player):
    user_choice = choice_dict[input(
        'Choose: (Hit, Double Down, Split, or Stay) - ')]
    resolved = False

    while resolved == False:
        if user_choice == 'Split' \
           and player.hand[0][0] != player.hand[1][0]:
            resolved = False
            user_choice = choice_dict[input(
                'Choose: (Hit, Double Down, or Stay) - ')]
        elif user_choice == 'Split' \
             and player.hand[0][0] == player.hand[1][0]:
            resolved = True
            player.split = True
            User_split(player)
        elif user_choice == 'Hit':
            resolved = True
            User_hand(player, user_choice)
        elif user_choice == 'Double Down':
            resolved = True
            User_DD(player, user_choice)
        elif user_choice == 'Stay':
            resolved = True
            print('User Stays')


def User_hand(player, user_choice):
    while user_choice != 'Stay':
        player.hand += hit(deck)
        player.hand_value, player.bust = count_hand(player.hand)
        # End if player busts
        if player.bust == True:
            user_choice = 'Stay'
        else:
            # Let player decide what to do again
            print('\n', players_dict[player.id_tag],
                  '\t', player.hand, '\n')
            user_choice = choice_dict[input('Choose: (Hit or Stay) - ')]


def User_DD(player, user_choice):
    player.bet = player.bet * 2
    player.hand += hit(deck)
    player.hand_value, player.bust = count_hand(player.hand)


def User_split(player):
    player.split_h1 = [player.hand[0]]
    player.split_hv1, player.split_b1 = count_hand(player.split_h1)
    player.split_h2 = [player.hand[1]]
    player.split_hv2, player.split_b2 = count_hand(player.split_h2)

    print('\n', players_dict[player.id_tag], '\t', player.split_h1)
    print("User's first split\n")
    first_split = choice_dict[input('Choose: (Hit or Stay) - ')]
    while first_split != 'Stay':
        player.split_h1 += hit(deck)
        player.split_hv1, player.split_b1 = count_hand(player.split_h1)

        # End if player busts
        if player.split_b1 == True:
            print('Bust on first split!')
            first_split = 'Stay'
        else:
            # Let player decide what to do again
            print('\n', players_dict[player.id_tag],
                  '\t', player.split_h1)
            first_split = choice_dict[input('Choose: (Hit or Stay) - ')]


    print('\n', players_dict[player.id_tag], '\t', player.split_h2)
    print("User's second split\n")
    second_split = choice_dict[input('Choose: (Hit or Stay) - ')]
    while second_split != 'Stay':
        player.split_h2 += hit(deck)
        player.split_hv2, player.split_b2 = count_hand(player.split_h2)

        # End if player busts
        if player.split_b2 == True:
            print('Bust on second split!')
            second_split = 'Stay'
        else:
            # Let player decide what to do again
            print('\n', players_dict[player.id_tag],
                  '\t', player.split_h2)
            second_split = choice_dict[input('Choose: (Hit or Stay) - ')]




# ========================================================================


def compare_hand(player, dealer):
    if player.blackjack == True and dealer.blackjack == False:
        dealer.money = dealer.money - player.bet * 1.5
        player.money = player.money + player.bet * 1.5
    elif player.blackjack == True and dealer.blackjack == True:
        dealer.money = dealer.money
        player.money = player.money
    elif player.bust == True:
        dealer.money = dealer.money + player.bet
        player.money = player.money - player.bet
    elif dealer.bust == True:
        dealer.money = dealer.money - player.bet
        player.money = player.money + player.bet
    elif player.hand_value > dealer.hand_value:
        dealer.money = dealer.money - player.bet
        player.money = player.money + player.bet
    else:
        dealer.money = dealer.money + player.bet
        player.money = player.money - player.bet


def compare_player_split(player, dealer):
    if player.split_b1 == True:
        dealer.money = dealer.money + player.bet
        player.money = player.money - player.bet
    elif dealer.bust == True:
        dealer.money = dealer.money - player.bet
        player.money = player.money + player.bet
    elif player.split_hv1 <= dealer.hand_value:
        dealer.money = dealer.money + player.bet
        player.money = player.money - player.bet
    else:
        dealer.money = dealer.money - player.bet
        player.money = player.money + player.bet

    # player splits must be a separate event
    if player.split_b2 == True:
        dealer.money = dealer.money + player.bet
        player.money = player.money - player.bet
    elif dealer.bust == True:
        dealer.money = dealer.money - player.bet
        player.money = player.money + player.bet
    elif player.split_hv2 <= dealer.hand_value:
        dealer.money = dealer.money + player.bet
        player.money = player.money - player.bet
    else:
        dealer.money = dealer.money - player.bet
        player.money = player.money + player.bet


def compare_dealer_split(player, dealer):
    if player.blackjack == True:
        dealer.money = dealer.money - player.bet * 1.5
        player.money = player.money + player.bet * 1.5
    elif player.bust == True:
        dealer.money = dealer.money + player.bet
        player.money = player.money - player.bet
    elif dealer.split_b1 == True and dealer.split_b2 == True:
        dealer.money = dealer.money - player.bet
        player.money = player.money + player.bet
    elif dealer.split_b1 == True and dealer.split_hv2 < player.hand_value:
        dealer.money = dealer.money - player.bet
        player.money = player.money + player.bet
    elif dealer.split_b2 == True and dealer.split_hv1 < player.hand_value:
        dealer.money = dealer.money - player.bet
        player.money = player.money + player.bet
    else:
        dealer.money = dealer.money + player.bet
        player.money = player.money - player.bet


def compare_both_split(player, dealer):
    if player.split_b1 == True:
        dealer.money = dealer.money + player.bet
        player.money = player.money - player.bet
    elif dealer.split_b1 == True \
         and dealer.split_b1 == True:
        dealer.money = dealer.money - player.bet
        player.money = player.money + player.bet
    elif player.split_hv1 > dealer.split_hv1 \
         and player.split_hv1 > dealer.split_hv2:
        dealer.money = dealer.money - player.bet
        player.money = player.money + player.bet
    elif player.split_hv2 > dealer.split_hv1 \
         and player.split_hv1 > dealer.split_hv2:
        dealer.money = dealer.money - player.bet
        player.money = player.money + player.bet
    else:
        dealer.money = dealer.money + player.bet
        player.money = player.money - player.bet


def print_after_deal(all_playing, dealer):
    deal_order = all_playing
    for player in deal_order:
        print(players_dict[player.id_tag], '\t', player.hand,
              '  ', player.hand_value)
    print(players_dict[dealer.id_tag], '\t', [dealer.hand[0]])


def print_after_turn(all_playing, dealer):
    deal_order = all_playing
    for player in deal_order:
        if player.split == False:
            print(players_dict[player.id_tag], '\t', player.hand,
                  '  ', player.hand_value)
        else:
            print(players_dict[player.id_tag], '\t', player.split_h1,
                  '  ', player.split_hv1, '\t', player.split_h2, '  ',
                  player.split_hv2)
    if dealer.split == False:
        print(players_dict[dealer.id_tag], '\t', dealer.hand, '  ',
              dealer.hand_value)
    else:
        print(players_dict[dealer.id_tag], '\t', dealer.split_h1,
              '  ', dealer.split_hv1, '\t', dealer.split_h2, '  ',
              dealer.split_hv2)


# ========================================================================


if __name__ == "__main__":
    num_decks = 6
    # global deck, discard_pile
    deck, discard_pile = reshuffle(num_decks)
    # initiate player lists with user
    user_id, user_money = make_user()
    User = Player(user_id, user_money)

    # generate random number of NPCs
    rand_npcs = random.sample([2, 3, 4, 5], random.randint(0, 4))
    npcs = [make_npc(npc_id) for npc_id in rand_npcs]
    # make an object list of all the players recently defined
    all_playing = [User] + [Player(id_num, mula) for id_num, mula in npcs]
    random.shuffle(all_playing)
    # Dealer  ith  thspecial  >.<
    dealer = Player('D', 999999999)

    # Loop for as long as User can or wants to play
    while leave_table == False:
        # deal out first hand
        deal_cards(all_playing, dealer)
        print_after_deal(all_playing, dealer)
        # time for turns
        turn_order = all_playing + [dealer]
        for player in turn_order:
            take_turns(player)

        print_after_turn(all_playing, dealer)

        for player in all_playing:
            print('\n', players_dict[player.id_tag], 'Outcome:\n')
            print(dealer.money, '\t', player.money)

            if player.split == False and dealer.split == False:
                compare_hand(player, dealer)
            if player.split == True and dealer.split == False:
                compare_player_split(player, dealer)
            if player.split == False and dealer.split == True:
                compare_dealer_split(player, dealer)
            if player.split == True and dealer.split == True:
                compare_both_split(player, dealer)

            print(dealer.money, '\t', player.money)

            if player.money < 5:
                if player.NPC == True:
                    all_playing.remove(player)
                else:
                    pass

        print('\n\n', discard_pile, '\n\n', count_discard(discard_pile))
        # reshuffle feature
        if len(deck) < random.randint(36, 70):
            deck, discard_pile = reshuffle(num_decks)

        if User.money < 5:
            print(
                "\nUser is out of money. "
                "\nThere's an ATM in the hallway if you wanted "
                "to play some more. \nHope to see you around!")
            exit()

        keep_playing = input(
            '\nDo you wish to play another hand? (y/n) ')

        if keep_playing == 'y':
            leave_table = False
        else:
            leave_table = True
            print('\nRemember to tip your dealer.\n'
                  'User has left the table. See you again soon! <3')
