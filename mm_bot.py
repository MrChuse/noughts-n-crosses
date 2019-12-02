#!/usr/bin/env python3

import argparse
import logging
import random

from utils import print_field

from network import Client

parser = argparse.ArgumentParser(description='Connect to game server')

parser.add_argument(
    '-H',
    '--host',
    default='',
    help='Server host to connect to'
)

parser.add_argument(
    '-p',
    '--port',
    type=int,
    default=8081,
    help='Port to connect to'
)

parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='Be verbose'
)

args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

field = None
settings = None

def game_start(msg):
    global field, settings
    print('game_start', msg)
    field = msg[0]
    settings = msg[1]

def save_field(field_):
    global field
    field = field_
    print_field(field_)

def touching(pos, field):
    for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]:
        new_i = pos[0] + di
        new_j = pos[1] + dj
        if 0 <= new_i < len(field) and 0 <= new_j < len(field[0]):
           if field[new_i][new_j] is not None:
               return True
    return False

def get_possible_moves(field):
    pos = []
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == None:
                if touching((i, j), field):
                    pos.append((i, j))
    return pos

def random_move(field):
    valid = []
    for i in range(len(field)):
        for j in range(len(field)):
            if field[i][j] is None:
                valid.append((j+1, i+1))
    move = random.choice(valid)
    return move

def check_win(row_len, field):
    directions = [
        ((0, -1), (0, 1)),
        ((-1, 0), (1, 0)),
        ((-1, -1), (1, 1)),
        ((-1, 1), (1, -1))
    ]
    won = False
    has_empty = False
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] is None:
                has_empty = True
                continue
            player = field[i][j]
            for d in directions:
                s = 1
                for di, dj in d:
                    _i = i + di
                    _j = j + dj
                    while 0 <= _i < len(field) and 0 <= _j < len(field[0]):
                        if field[_i][_j] == player:
                            s += 1
                            if s >= row_len:
                                break
                        else:
                            break
                        _i += di
                        _j += dj
                    if s >= row_len:
                        won = True
                        break
                else:
                    continue
                break

            if won: #if found a line return
                return 1 if player else -1
    if not has_empty: #if didn't find a line and no empty cells left
        return 0
    return None #if didn't find a line anywhere and there are empty cells

def minimax(player, row_len, field, depth):
    ch_win = check_win(row_len, field)
    #print(ch_win, 'ch_win')
    if ch_win is not None:
        return None, (10000 - depth) * ch_win

    best_move = None
    best_score = 1000000 * (-1 if player else 1)
    possible_moves = get_possible_moves(field)
    for move in possible_moves:
        field[move[0]][move[1]] = player
        ret_move, score = minimax(not player, row_len, field, depth+1)

        if (player and score > best_score) or ((not player and score < best_score)):
                best_score = score
                best_move = move

        field[move[0]][move[1]] = None
    return best_move, best_score

def get_next_move(field):
    global settings
    print((settings, 'settings'))
    possible_moves = get_possible_moves(field)
    if len(possible_moves) == 0:
        return random_move(field)
    else:
        move, score = minimax(settings[0], settings[2], field, 0) # current_player, row_len, field, recursion depth of 0
    return move[1]+1, move[0]+1

def make_move(crosses_turn):
    global field
    move = get_next_move(field)
    print((move, 'move'))
    return move


def game_over(crosses_won):
    if crosses_won is None:
        print('Draw')
    else:
        print('Winner:', 'crosses' if crosses_won else 'noughts')


client = Client(args.host, args.port)
client.on_start_received = game_start
client.on_field_received = save_field
client.on_move_required = make_move
client.on_game_over = game_over

client.start()
