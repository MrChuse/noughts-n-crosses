#!/usr/bin/env python3

import socket
import argparse

from net import TYPE_FIELD,TYPE_GAME_OVER, TYPE_MOVE, recv_message, make_message, send_message

from utils import print_field

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

args = parser.parse_args()

sock = socket.socket()
sock.connect((args.host, args.port))

file = None

def make_move_message(x, y):
    return make_message(TYPE_MOVE, {'x': x, 'y': y})


while True:
    msg_type, msg = recv_message(sock)

    if msg_type == TYPE_FIELD:
        print_field(msg)
    elif msg_type == TYPE_MOVE:
        while True:
            try:
                x, y = map(int, input('Enter move: ').split())
            except Exception as e:
                print(f'Invalid move: {e}')
                continue
            break

        send_message(sock, *make_move_message(x, y))
    elif msg_type == TYPE_GAME_OVER:
        print(msg)
        break

sock.close()