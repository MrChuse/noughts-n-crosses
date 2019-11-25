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

def save_field(field_):
    global field
    field = field_
    print_field(field_)

def random_move(field):
    valid = []
    for i in range(len(field)):
        for j in range(len(field)):
            if field[i][j] is None:
                valid.append((j+1, i+1))
    move = random.choice(valid)
    return move

directions = [
    ((0, -1), (0, 1)),
    ((-1, 0), (1, 0)),
    ((-1, -1), (1, 1)),
    ((-1, 1), (1, -1))
]
wins = 3


def check_win(turn, field):
    global directions
    for i in range(len(field)):
        for j in range(len(field)):
            if field[i][j] != turn: #check for cells without my (turn's) mark then skip
                continue
            for d in directions: # if my cell, check 4 directions
                s = 1
                for di, dj in d: # 2 ways in a direction
                    _i = i + di
                    _j = j + dj
                    while 0 <= _i < len(field) and 0 <= _j < len(field): #travel in those ways
                        if field[_i][_j] == turn: #compare cells
                            s+=1
                            if s >= wins - 1: #if close to win
                                # move = where to move
                                    
                                


def make_move(crosses_turn):
    global field
    move = check_win(crosses_turn, field)
    if move is not None:
        return move
    move = check_lose(crosses_turn, field)
    if move is not None:
        return move
    return random_move(field)

def game_over(crosses_won):
    if crosses_won is None:
        print('Draw')
    else:
        print('Winner:', 'crosses' if crosses_won else 'noughts')


client = Client(args.host, args.port)
client.on_field_received = save_field
client.on_move_required = make_move
client.on_game_over = game_over

client.start()
