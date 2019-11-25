#!/usr/bin/env python3

import argparse

from network import Server

import signal

import logging


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

parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='Be verbose'
)

args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)


server = Server(
    args.field_size,
    args.row_length,
    args.host,
    args.port
)


def signal_handler(sig, frame):
    server.stop()


signal.signal(signal.SIGINT, signal_handler)

server.start()
