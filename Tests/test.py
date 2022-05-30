import json
import random
import string
import os

from battleship_runner import BattleshipGame

MAX_BOARD_SIZE = 26
MAX_FLEET_LENGTH = 26
DEFAULT_FLEET = {
    "battleship": {"size": 8, "quantity": 1},
    "heavy_cruiser": {"size": 3, "quantity": 2},
    "destroyer": {"size": 2, "quantity": 3},
    "submarine": {"size": 1, "quantity": 4},
    "aircraft_carrier": {"size": 8, "quantity": 1},
    "light_cruiser": {"size": 6, "quantity": 2},
    "boat": {"size": 1, "quantity": 4},
    "yatch": {"size": 1, "quantity": 6},
    "steam_boat": {"size": 3, "quantity": 2},
    "gunboat": {"size": 6, "quantity": 2},
    "minelayer": {"size": 1, "quantity": 1},
    "minesweeper": {"size": 1, "quantity": 2},
    "corvette": {"size": 2, "quantity": 3}
}


# shots=()

class All_Test(object):

    def __init__(self):
        x = 1
        # for x in range(ord('A'), ord('Z') + 1):
        #     # Print the alphabet
        #     for y in range(1, game_configuration.size + 1):
        #         obj = chr(x) + str(y)
        #         print(obj)

    # def run(self):
    #     game = BattleshipGame(test=True, test_info=test_info)
    #     game.play()


def create_configuration():
    placement = {}
    temp_fleet = {}
    for i in range(2, MAX_BOARD_SIZE + 1):
        for fleet in DEFAULT_FLEET.items():
            if fleet[1]['size'] <= i and fleet[1]['size'] * fleet[1]['quantity'] < (i * i) - 2:
                temp_fleet[fleet[0]] = fleet[1]
        board_size = i
        te = {}
        temp = []
        for j in string.ascii_uppercase[:board_size]:
            for k in range(1, board_size + 1):
                temp.append(k)
            te[j] = temp
            temp = []
        create_shotfile(board_size, te)
        for pp in temp_fleet.items():
            sub = ()
            for l in range(1, pp[1]['quantity'] + 1):
                for m in range(ord('A'), ord(list(te.keys())[-1]) + 1):
                    # print(chr(m))
                    if pp[1]['size'] == 1:
                        for n in range(1, board_size + 1):
                            loca = (chr(m) + str(n),)
                            sub = sub + loca
                    else:
                        for n in range(1, len(te[chr(m)]) + 1):
                            if len(te[chr(m)]) - n <= pp[1]['size']:
                                for o in range(1, board_size + 2):
                                    for p in range(board_size + 1, 0, -1):
                                        if o >= p:
                                            if o - p == pp[1]['size']:
                                                # print(p, o - 1)
                                                loca = (chr(m) + str(p) + '-' + chr(m) + str(o - 1),)
                                                sub = sub + loca
                                        if o < p:
                                            if p - o == pp[1]['size']:
                                                # print(o, p - 1)
                                                loca = (chr(m) + str(o) + '-' + chr(m) + str(p - 1),)
                                                sub = sub + loca
        for ii in range(len(temp_fleet)):
            placement['Fleet{}'.format(ii)] = {'board_size':i,'fleet_name': pp[0],'fleet_size': pp[1]['size'], 'quantity': pp[1]['quantity'],
                                                     'location': set(sub)}
            print(placement)


def create_shotfile(board_size, location, shots=tuple):
    temp = ()
    for m in range(ord('A'), ord(list(location.keys())[-1]) + 1):
        # print(chr(m))
        for n in range(1, board_size + 1):
            temp += (chr(m) + str(n),)
    shots = tuple(temp)
    p1_open = open("test_P1_shots.txt", "w+")
    p2_open = open("test_P2_shots.txt", "w+")
    sample1 = random.sample(shots, int(len(shots) / 2))
    sample2 = random.sample(shots, int(len(shots) / 2))
    for P1_shot in sample1:
        p1_open.write(P1_shot + " ")
    p1_open.close()
    for P2_shot in sample2:
        p2_open.write(P2_shot + " ")
    p1_open.close()
    # for x in range(ord('A'), ord('Z') + 1):
    #     Print the alphabet


#     for y in range(1, game_configuration.size + 1):
#         obj = chr(x) + str(y)
#         print(obj)

create_configuration()
# Test=All_Test()
# Test.run()
