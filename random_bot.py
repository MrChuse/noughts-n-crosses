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

def get_next_move(field):
    valid = []
    for i in range(len(field)):
        for j in range(len(field)):
            if field[i][j] is None:
                valid.append((j+1, i+1))
    print(field, 'field')
    print(valid, 'valid')
    move = random.choice(valid)
    return move

def make_move(crosses_turn):
    global field
    move = get_next_move(field)
    logging.info(move)
    return move


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
