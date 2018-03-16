#!/usr/bin/python3.4

import os
import curses
import sys
from tkinter import *

level = [
        "+------------------+",
        "|    |             |",
        "|  + |       +     |",
        "|  | +----+  |     |",
        "|  |      |  |     |",
        "|  |      +--+     |",
        "|  +---+   ------+ |",
        "|      |         | |",
        "|      |    +    | |",
        "|      |    |    | |",
        "|      |    |    + |",
        "|      |-  -|      |",
        "|           |   |  |",
        "|  +--------+   |  |",
        "|  |               |",
        "|  |    +----------|",
        "|  |              O|",
        "+------------------+",
        ]

def afficher_labyrinthe(lab, perso, pos_perso, win, coul):
    """
    Affiche un Labyrinthe

    lab : Variable contenant le labyrinthe
    perso : caractere representant le perso
    pos_perso : coordonnees
    """
    n_ligne = 0
    for ligne in lab:
        if pos_perso[1] == n_ligne:
            win.addstr(n_ligne + 1, 10, ligne[0:pos_perso[0]] + perso + ligne[pos_perso[0] + 1:])
            win.addstr(n_ligne + 1, 10 + pos_perso[0], perso, color("RED", coul))
        else:
            win.addstr(n_ligne + 1, 10, ligne)
        n_ligne += 1

def verification_deplacement(lab, pos_col, pos_ligne):
    """
    Indique si la deplacement du perso est valide

    lab : labyrinthe
    pos_col : col du perso
    pos_ligne : ligne du perso
    """
    n_cols = len(lab[0])
    n_lignes = len(lab)
    if pos_ligne <= 0 or pos_col <= 0 or pos_ligne >= (n_lignes - 1) or \
            pos_col >= (n_cols - 1):
                return None
    elif lab[pos_ligne][pos_col] == "O":
        return [-1, -1]
    elif lab[pos_ligne][pos_col] != " ":
        return None
    else:
        return [pos_col, pos_ligne]

def choix_joueur(lab, pos_perso, win):
    """
    demande au joueur de saisir son deplacement et verifie s'il est possible

    lab : labyrinthe
    pos_perso : coordonnees
    """
    dep = None
    choix = win.getch()
    if choix == curses.KEY_UP:
        dep = verification_deplacement(lab, pos_perso[0], pos_perso[1] - 1)
    elif choix == curses.KEY_DOWN:
        dep = verification_deplacement(lab, pos_perso[0], pos_perso[1] + 1)
    elif choix == curses.KEY_LEFT:
        dep = verification_deplacement(lab, pos_perso[0] - 1, pos_perso[1])
    elif choix == curses.KEY_RIGHT:
        dep = verification_deplacement(lab, pos_perso[0] + 1, pos_perso[1])
    elif choix == 27:
        close_curses()
        exit(0)
    if dep != None:
        pos_perso[0] = dep[0]
        pos_perso[1] = dep[1]

def jeu(level, perso, pos_perso, win, coul):
    """
    Boucle principale du jeu

    level : labyrynthe
    perso : caractere representant le perso
    pos_perso : pos
    """
    while True:
        afficher_labyrinthe(level, perso, pos_perso, win, coul)
        choix_joueur(level, pos_perso, win)
        if pos_perso == [-1, -1]:
            win.addstr(22, 1, "Vous avez reussi le labyrinthe!", color("RED", coul))
            close_curses()
            break

def init_curses(lignes, cols, pos):
    curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    window = curses.newwin(lignes, cols, pos[0], pos[1])
    window.border(0)
    window.keypad(1)
    return window

def close_curses():
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)
    curses.endwin()

def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
    return ["RED", "GREEN", "BLUE"]

def color(code, l_color):
    return curses.color_pair(l_color.index(code) + 1)


if __name__ == "__main__":
    perso = "X"
    pos_perso = [1, 1]
    win = init_curses(25, 41, (0,0))
    coul = init_colors()
    jeu(level, perso, pos_perso, win, coul)
    win.getch()
    close_curses()
