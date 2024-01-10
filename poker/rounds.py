import poker
import rank


def give_hands(players, deck):
    hands = poker.deal_hand(deck, len(players), 2)
    for i in range(len(players)):
        players[i]['hand'] = []
        players[i]['hand'].append(hands[i][0])
        players[i]['hand'].append(hands[i][1])
    return hands


def nsame_bet(players):
    x = players[-1]['bet']
    for i in players[:-1]:
        if i['bet'] != x:
            return True
    return False


def ENTER_GAME(IN_WAIT,IN_GAME):
    i = 0
    while len(IN_GAME) < 11:
        if i > len(IN_WAIT) or IN_WAIT == []:
            return (IN_WAIT, IN_GAME)
        if IN_WAIT[i]['money'] > 0:
            IN_GAME.append(IN_WAIT.pop(i))
        else:
            i += 1
    return (IN_WAIT, IN_GAME)
    

def QUIT_GAME(player, IN_GAME, IN_WAIT):
    if player in IN_GAME:
        IN_GAME.pop(IN_GAME.index(player))
    if player in IN_WAIT:
        IN_WAIT.pop(IN_WAIT.index(player))

def IS_TURN_FINISH(plIN_GAME, folded):
    for i in IN_GAME:
        if True:
            True




def gotoIN_WAIT(session, IN_GAME, IN_WAIT):
    if session['user_name'] not in IN_GAME:
        if session['user_name'] not in IN_WAIT:
            return True
    return False


def Start_Game(IN_GAME):
    deck = poker.generate_deck()
    hands = deal_hand(deck, len(IN_GAME))


