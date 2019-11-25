#!/usr/bin/env python3

import socket
import logging

from threading import Thread

from core import TheGame
from network.common import make_message, send_message, recv_message, TYPE_FIELD, TYPE_GAME_OVER, TYPE_MOVE


def make_field_message(g):
    return make_message(TYPE_FIELD, g.get_field())


def make_move_message(crosses_turn):
    return make_message(TYPE_MOVE, crosses_turn)


def make_game_is_over_message(winner):
    return make_message(TYPE_GAME_OVER, winner)


class Server:
    def __init__(self, field_size=3, row_length=3, host='', port=8081):
        self.logger = logging.getLogger('Server')
        self.logger.info('Creating server')
        self.logger.debug(f'Server parameters: field_size={field_size}, row_length={row_length}, address=({host}, {port})')
        self.field_size = field_size
        self.row_length = row_length
        self.host = host
        self.port = port

    def play_match(self, client1, client2):
        g = TheGame(self.field_size, self.row_length)
        msg_len, msg = make_field_message(g)

        send_message(client1, msg_len, msg)
        send_message(client2, msg_len, msg)

        clients = client1, client2
        crosses_turn = True
        winner = None

        while not g.is_over():
            while True:
                try:
                    send_message(clients[0], *make_move_message(crosses_turn))
                    msg_type, msg = recv_message(clients[0])

                    if msg_type != TYPE_MOVE:
                        raise Exception()
                    winner = g.make_a_move(crosses_turn, msg['x'], msg['y'])
                except:
                    continue
                break

            msg_len, msg = make_field_message(g)

            send_message(client1, msg_len, msg)
            send_message(client2, msg_len, msg)

            clients = clients[1], clients[0]
            crosses_turn = not crosses_turn

        msg_len, msg = make_game_is_over_message(winner)

        send_message(client1, msg_len, msg)
        send_message(client2, msg_len, msg)

        client1.close()
        client2.close()

    def do_work(self):
        try:
            while True:
                self.logger.info('Waiting for client #1')
                client1, addr1 = self.sock.accept()

                self.logger.info('Waiting for client #2')
                client2, addr2 = self.sock.accept()

                self.logger.info(f'Starting match between {addr1} and {addr2}')

                Thread(
                    target=self.play_match,
                    args=(client1, client2)
                ).start()
        except:
            self.logger.info('Server terminated')

    def start(self, wait=True):
        self.sock = socket.create_server((self.host, self.port))
        thread = Thread(target=self.do_work)
        thread.start()

        if wait:
            thread.join()

    def stop(self):
        self.sock.shutdown(socket.SHUT_RDWR)
