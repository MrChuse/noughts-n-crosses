#!/usr/bin/env python3

import socket
import argparse

from core import TheGame
from net import make_message, send_message, recv_message, TYPE_FIELD, TYPE_GAME_OVER, TYPE_MOVE

parser = argparse.ArgumentParser(description='Start game server')
parser.add_argument(
    '-f',
    '--field-size',
    default=3,
    type=int,
    help='Field size'
)

parser.add_argument(
    '-r',
    '--row-length',
    default=3,
    type=int,
    help='Row length'
)

parser.add_argument(
    '-H',
    '--host',
    default='',
    help='Address to bind to'
)

parser.add_argument(
    '-p',
    '--port',
    type=int,
    default=8081,
    help='Port to listen to'
)

args = parser.parse_args()

g = TheGame(args.field_size, args.row_length)

sock = socket.create_server((args.host, args.port))

print('Waiting for client #1')
client1, addr1 = sock.accept()

print('Waiting for client #2')
client2, addr2 = sock.accept()


def make_field_message(g):
    return make_message(TYPE_FIELD, g.get_field())


def make_move_message():
    return make_message(TYPE_MOVE, None)


def make_game_is_over_message():
    return make_message(TYPE_GAME_OVER, None)


msg_len, msg = make_field_message(g)

send_message(client1, msg_len, msg)
send_message(client2, msg_len, msg)

clients = client1, client2
crosses_move = True

while not g.is_over():
    while True:
        try:
            send_message(clients[0], *make_move_message())
            msg_type, msg = recv_message(clients[0])

            if msg_type != TYPE_MOVE:
                raise Exception()
            print(g.make_a_move(crosses_move, msg['x'], msg['y']))
        except:
            continue
        break

    msg_len, msg = make_field_message(g)

    send_message(client1, msg_len, msg)
    send_message(client2, msg_len, msg)

    clients = clients[1], clients[0]
    crosses_move = not crosses_move

print(11111)
msg_len, msg = make_game_is_over_message()

send_message(client1, msg_len, msg)
send_message(client2, msg_len, msg)

client1.close()
client2.close()

sock.close()
