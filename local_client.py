#!/usr/bin/env python3
import argparse

from core import TheGame
from utils import print_field

parser = argparse.ArgumentParser(description='Play the game')
parser.add_argument(
    '-f',
    '--field-size',
    required=True,
    type=int,
    help='Field size'
)
parser.add_argument(
    '-r',
    '--row-length',
    required=True,
    type=int,
    help='Row length'
)

args = parser.parse_args()

try:
    g = TheGame(args.field_size, args.row_length)
except Exception as e:
    exit(f'Bad arguments: {e}')


f = True

while not g.is_over():
    print_field(g)
    try:
        x, y = map(int, input('Enter move: ').split())
        if g.make_a_move(f, x, y) is not None:
            print_field(g)
            print(f"{'Crosses' if f else 'Noughts'}'ve won")
            break
    except Exception as e:
        print(f'Invalid move: {e}')
    f = not f

