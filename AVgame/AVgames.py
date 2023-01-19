import random

hand = []
ini_hand= ["セックス", "に", "は", "と", "が", "を", "の", "より", "だけの", "!", "?"]
all_hand = []
deli_hand = []
index_word = []
ini_ad = []
deli_ad = []
all_ad = []

deli_num = 20
ini_num = len(ini_hand)

def make_hand(words):
    hand.clear()
    deli_hand.clear()
    all_hand.clear()
    index_word.clear()
    for i in range(len(words)):
        words[i] = words[i].split(" ")
    while True:
        num = random.randint(1, len(words))
        if len(hand) == deli_num:
            break
        if num not in hand:
            hand.append(num)
    for i in range(deli_num):
        hand_word = words[int(hand[i]-1)][1].splitlines()
        deli_hand.append(' '.join(hand_word))
    num = random.randint(1, len(words))
    return deli_hand

def union(ini_hand, words):
    all_hand.extend(ini_hand)
    for i in range(deli_num):
        hand_word = words[int(hand[i]-1)][1].splitlines()
        index_word.append(words[int(hand[i]-1)][1].splitlines())
        all_hand.append(' '.join(hand_word))
    return all_hand

#未実装辞書関数
def dic(ini_hand, deli_hand, all_hand):
    for i in range(ini_num):
        ini_ad.append(i+1)
    for i in range(deli_num):
        deli_ad.append(i+1)
    for i in range(ini_num + deli_num):
        all_ad.append(i+1)

    ini_dict = dict(zip(ini_ad, ini_hand))
    deli_dict = dict(zip(deli_ad, deli_hand))
    all_dict = dict(zip(all_ad, all_hand))

    return ini_dict, deli_dict, all_dict