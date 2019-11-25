#!/usr/bin/env python3

import socket
from threading import Thread

from .common import TYPE_FIELD,TYPE_GAME_OVER, TYPE_MOVE, recv_message, make_message, send_message

import logging

def make_move_message(x, y):
    return make_message(TYPE_MOVE, {'x': x, 'y': y})


class Client:
    def __init__(self, host, port):
        self.logger = logging.getLogger('Client')
        self.logger.info('Creating client')
        self.logger.debug(f'Client parameters: ({host}, {port})')

        self.host = host
        self.port = port

        self.on_field_received = self.clb_on_field_received
        self.on_move_required = self.clb_on_move_required
        self.on_game_over = self.clb_on_game_over

    def clb_on_field_received(self, field):
        self.logger.debug(f'Field: {field}')

    def clb_on_move_required(self, field, crosses_turn, turn_number):
        raise NotImplementedError('Callback «on_move_required» is not set')

    def clb_on_game_over(self, crosses_won):
        winner = '-' if crosses_won is None else ('X' if crosses_won else 'O')
        self.logger.info(f'Game over: {winner}')

    def do_work(self):
        sock = socket.socket()
        sock.connect((self.host, self.port))

        try:
            while True:
                msg_type, msg = recv_message(sock)

                if msg_type == TYPE_FIELD:
                    self.on_field_received(msg)
                elif msg_type == TYPE_MOVE:
                    x, y = self.on_move_required(msg)

                    send_message(sock, *make_move_message(x, y))
                elif msg_type == TYPE_GAME_OVER:
                    self.on_game_over(msg)
                    break
        finally:
            sock.close()

    def start(self, wait=True):
        self.thread = Thread(target=self.do_work)
        self.thread.start()

        if wait:
            self.wait()

    def wait(self):
        self.thread.join()
