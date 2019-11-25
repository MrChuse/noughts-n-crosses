#!/usr/bin/env python3

import argparse
import logging

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


def make_move(crosses_turn):
    while True:
        try:
            return tuple(map(int, input('Enter move: ').split()))
        except Exception as e:
            print(f'Invalid move: {e}')


def game_over(crosses_won):
    if crosses_won is None:
        print('Draw')
    else:
        print('Winner:', 'crosses' if crosses_won else 'noughts')


client = Client(args.host, args.port)
client.on_field_received = print_field
client.on_move_required = make_move
client.on_game_over = game_over

client.start()
