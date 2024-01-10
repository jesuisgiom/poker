import random as rn
import rank


def generate_deck():
    to_return = []
    for i in ['H','D','C','S']:
        for j in range(2,15):
            to_return.append(str(j)+i)
    rn.shuffle(to_return)
    return to_return


def deal_hand(deck, num_players):
    hands = [[] for _ in range(num_players)]
    for _ in range(2):
        for player in range(num_players):
            card = deck.pop()
            hands[player].append(card)
    return hands


def Best_hand(hands, river):
    isum = -1
    irank = -1
    hand_name_list = [
        'Invalid hand',
        'High card',
        'One pair',
        'Two pair',
        'Three of a kind',
        'Straight',
        'Flush',
        'Full house',
        'Four of a kind',
        'Straight flush',
        'Royal flush'
        ]
    player_hand=[]
    for i in hands:
        player_hand.append(rank.get_best_hand(i+river))
    bests = []
    best = 0
    for i in range(1,len(player_hand)):
        comp = compare(player_hand[i], player_hand[best])
        if type(comp) == list:
            bests.append(i)
        elif comp:
            best = i
            bests = []
    bests.append(best)
    return bests









def list_of_winner(player_hand, river, irank, isum):
    lst = []
    for i in range(len(player_hand)):
        if isum == sum(rank.get_ranks(player_hand[i])) and irank == rank.evaluate_hand(player_hand[i]):
            lst.append(i)
    return lst





def River(deck):
    return [deck.pop() for i in range(5)]



def compare(hand1, hand2):
    hand_name_list = [
        'Invalid hand',
        'High card',
        'One pair',
        'Two pair',
        'Three of a kind',
        'Straight',
        'Flush',
        'Full house',
        'Four of a kind',
        'Straight flush',
        'Royal flush'
        ]
    power1 = hand_name_list.index(rank.evaluate_hand(hand1)) 
    power2 = hand_name_list.index(rank.evaluate_hand(hand2)) 
    if power1 > power2:
        return True
    if power1 == power2:
        maxs1 = toptier(hand1, power1)
        maxs2 = toptier(hand2, power2)
        for i in range(len(maxs1)-1):
            if len(maxs1[-(i+1)]) == len(maxs2[-(i+1)]):
                for j in range(len(maxs1[-(i+1)])):
                    if maxs1[-(i+1)][j] != maxs2[-(i+1)][j]:
                        if maxs1[-(i+1)][j] > maxs2[-(i+1)][j]:
                            return True
                        return False
            if len(maxs1[-(i+1)]) > len(maxs2[-(i+1)]):
                return True
        return [hand1, hand2]
    return False



def toptier(hand, power):
    ranks = [int(card[0:-1]) for card in hand]
    lst = [(ranks.count(x)) for x in ranks]
    to_rtn = [None,[],[],[],[]]
    for i in range(len(lst)):
        if ranks[i] not in to_rtn[lst[i]]:
            to_rtn[lst[i]].append(ranks[i])
    for i in lst:
        sorted(to_rtn[i])
    return to_rtn
    
