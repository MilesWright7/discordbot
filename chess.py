'''

Game has a board 8x8 with pieces each can do certain moves.
each piece is owned by a player. 

'''

import math


colNames = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

class Piece():
    def __init__(self):
        self.value = 0
        self.letter = '_'

    def __repr__(self):
        return self.letter

class King(Piece):

    def __init__(self, col, row):
        self.value = 100
        self.letter = 'K'
        self.positoin = (col, row)

class Queen(Piece):

    def __init__(self, col, row):
        self.value = 8
        self.letter = 'Q'
        self.position = (col, row)

class Rook(Piece):

    def __init__(self, col, row):
        self.value = 5
        self.letter = 'R'
        self.position = (col, row)

class Bishop(Piece):
    def __init__(self, col, row):
        self.value = 3
        self.letter = 'B'
        self.position = (col, row)

class Knight(Piece):
    def __init__(self, col, row):
        self.value = 3
        self.letter = 'N'
        self.position = (col, row)

class Pawn(Piece):
    def __init__(self, col, row):
        self.value = 1
        self.letter = 'P'
        self.position = (col, row)



class Player():

    def __init__(self, name):
        self.name = name




class Game():

    def __init__(self, p1, p2):
        self.board = [[Rook('a',1), Knight('b',1), Bishop('c', 1), Queen('d',1), King('e',1), Bishop('f',1), Knight('e', 1), Rook('f', 1)]] +\
                    [[Pawn(col, 2) for col in colNames.keys()]] +\
                    [[Piece() for i in range(8)] for j in range(4)] +\
                    [[Pawn(col, 7) for col in colNames.keys()]] +\
                    [[Rook('a',8), Knight('b',8), Bishop('c', 8),Queen('d',8), King('e',8), Bishop('f',8), Knight('e', 8), Rook('f', 8)]]
        self.black = p1
        self.white = p2
        self.moveList = []

    def __repr__(self):
        string = ''
        for i in range(8):
            for j in range(8):
                string += repr(self.board[i][j])
                string += '|'
            string += '\n'
        return string


def main():
    x = Game(1, 2)
    print(x)

if __name__ == '__main__':
    main()