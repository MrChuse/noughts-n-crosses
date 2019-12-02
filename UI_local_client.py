#!/usr/bin/env python3
import argparse

from core import TheGame
from utils import print_field

parser = argparse.ArgumentParser(description='Play the game')
parser.add_argument(
    '-f',
    '--field-size',
    type=int,
    default=3,
    help='Field size'
)
parser.add_argument(
    '-r',
    '--row-length',
    type=int,
    default=3,
    help='Row length'
)

args = parser.parse_args()

try:
    g = TheGame(args.field_size, args.row_length)
except Exception as e:
    exit(f'Bad arguments: {e}')


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

current_player = True



class GridWindow(Gtk.Window):

    def __init__(self, grid_size=3):
        Gtk.Window.__init__(self, title="Grid Example")

        grid = Gtk.Grid()
        self.add(grid)
        
        self.buttons = []
        self.bottom_text = Gtk.Label('game is going')
        grid.attach(self.bottom_text, 0, grid_size, grid_size, 1)
        for i in range(grid_size):
            for j in range(grid_size):
                self.buttons.append(Gtk.Button(label="-"))
                self.buttons[grid_size * i + j].connect("clicked", self.click_a_button, (i+1, j+1, self.bottom_text))
                self.buttons[grid_size * i + j].set_hexpand(True)
                self.buttons[grid_size * i + j].set_vexpand(True)
                grid.attach(self.buttons[grid_size * i + j], i, j, 1, 1)
        
    def click_a_button(self, button, data):
        global current_player
        try:
            if g.make_a_move(current_player, data[0], data[1]) is not None:
                data[2].set_label('GAME IS OVER')
                for button_ in self.buttons:
                    button_.set_sensitive(False)
            button.set_label('X' if current_player else 'O')
            button.set_sensitive(False)
            current_player = not current_player
        except Exception as e:
            print(f'Invalid move: {e}')

win = GridWindow(args.field_size)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()


