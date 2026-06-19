from itertools import chain
from tkinter import *
import time

class Board:
    def __init__(self, canvas, sq_size):
        self.canvas = canvas
        self.sq_size = sq_size
        self.figures = {'P': '♟', 'R': '♜', 'N': '♞', 'K': '♚', 'Q': '♛', 'B': '♝'}
        self.black_king = King(0, 4, 'black')
        self.white_king = King(7, 4, 'white')
        self.board = [
            [Rook(0, 0, 'black'), Knight(0, 1, 'black'), Bishop(0, 2, 'black'), Queen(0, 3, 'black'), self.black_king, Bishop(0, 5, 'black'), Knight(0, 6, 'black'), Rook(0, 7, 'black')],
            [Pawn(1, i, 'black') for i in range(8)],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            [Pawn(6, i, 'white') for i in range(8)],
            [Rook(7, 0, 'white'), Knight(7, 1, 'white'), Bishop(7, 2, 'white'), Queen(7, 3, 'white'), self.white_king, Bishop(7, 5, 'white'), Knight(7, 6, 'white'), Rook(7, 7, 'white')]
        ]
        self.game_over = False
        self.circles = []
        self.pieces = []
        self.turn = 'white'
        self.canvas.bind("<Button-1>", self.click1)

    def get_cords(self, evt):
        if type(evt) in [Pawn, Rook, Knight, Bishop, King, Queen]:
            return (evt.x, evt.y)
        return evt.x // self.sq_size, evt.y // self.sq_size

    def click1(self, evt):
        x, y = self.get_cords(evt)
        if self.board[y][x] != '' and self.board[y][x].color == self.turn:
            possible = self.get_possible_moves(evt)
            for j, i in possible:
                self.circles.append(self.canvas.create_oval(self.sq_size * (i + 0.4), self.sq_size * (j + 0.4),
                                                                self.sq_size * (i + 0.6), self.sq_size * (j + 0.6),
                                                                fill='lightgreen'))
            if possible:
                self.canvas.bind("<Button-1>", lambda evt: self.click2(evt, x, y, possible))

    def click2(self, evt, old_x, old_y, possible):
        x, y = self.get_cords(evt)
        if [y, x] in possible:
            self.board[y][x] = self.board[old_y][old_x]
            self.board[old_y][old_x] = ''
            piece = self.board[y][x]
            piece.x = x
            piece.y = y
            if type(piece) == King or type(piece) == Rook:
                piece.moved = True
            if type(piece) == Pawn:
                if (piece.color == 'white' and y == 0) or (piece.color == 'black' and y == 7):
                    choose_menu = Tk()
                    choose_menu.title('Choose the piece')
                    choose_menu.wm_attributes('-topmost', 1)
                    choose_menu.resizable(False, False)
                    Q_button = Button(choose_menu, font=('Courier', self.sq_size // 2), text='♛',
                                      command=lambda: self.choose(piece, choose_menu, Queen))
                    R_button = Button(choose_menu, font=('Courier', self.sq_size // 2), text='♜',
                                      command=lambda: self.choose(piece, choose_menu, Rook))
                    B_button = Button(choose_menu, font=('Courier', self.sq_size // 2), text='♝',
                                      command=lambda: self.choose(piece, choose_menu, Bishop))
                    Kn_button = Button(choose_menu, font=('Courier', self.sq_size // 2), text='♞',
                                      command=lambda: self.choose(piece, choose_menu, Knight))
                    Q_button.pack(side=LEFT)
                    R_button.pack(side=LEFT)
                    B_button.pack(side=LEFT)
                    Kn_button.pack(side=LEFT)
            self.game_ended()
            self.turn = 'black' if self.turn == 'white' else 'white'
        self.show()
        self.canvas.bind("<Button-1>", self.click1)

    def choose(self, piece, ch_menu, type):
        self.board[piece.y][piece.x] = type(piece.y, piece.x, piece.color)
        ch_menu.destroy()
        self.show()

    def game_ended(self):
        a = [self.get_possible_moves(piece) for piece in chain(*self.board) if piece != '' and piece.color == 'black']
        if not any(a):
            if self.check() == 'black':
                text = f'{self.turn.upper()} WON!'
            else:
                text = 'STALEMATE'
            print(text)
            self.game_over = True

    def get_all_moves(self, x, y):
        piece = self.board[y][x]
        moves = piece.get_moves()
        possible = []
        if type(piece) == Pawn:
            for j, i in moves:
                if ((self.board[j][i] == '' and x == i) or
                        (self.board[j][i] != '' and self.board[j][i].color != piece.color and x != i)):
                    possible.append([j, i])
        else:
            for item in moves:
                for j, i in item:
                    if self.board[j][i] == '':
                        possible.append([j, i])
                    else:
                        if self.board[j][i].color != piece.color:
                            possible.append([j, i])
                        break
        return possible

    def check(self):
        for piece in filter(None, chain(*self.board)):
            if abs(self.white_king.x - self.black_king.x) <= 1 and abs(self.white_king.y - self.black_king.y) <= 1:
                return self.turn
            if piece.color == 'white' and [self.black_king.y, self.black_king.x] in self.get_all_moves(piece.x, piece.y):
                return 'black'
            elif piece.color == 'black' and [self.white_king.y, self.white_king.x] in self.get_all_moves(piece.x, piece.y):
                return 'white'
        return False

    def get_possible_moves(self, evt):
        x, y = self.get_cords(evt)
        piece = self.board[y][x]
        if type(piece) == str:
            return
        possible = self.get_all_moves(x, y)
        answ = []
        for j, i in possible:
            old_board = [[j for j in i] for i in self.board]
            self.board[j][i] = self.board[y][x] = piece
            self.board[y][x] = ''
            piece.x = i
            piece.y = j
            if self.check() != piece.color:
                answ.append([j, i])
            self.board = [[j for j in i] for i in old_board]
            piece.x = x
            piece.y = y
        return answ

    def show(self):
        for piece in self.pieces:
            self.canvas.delete(piece)
        for circle in self.circles:
            self.canvas.delete(circle)
        self.pieces = []
        for i in range(8):
            for j in range(8):
                if self.board[j][i] == '':
                    continue
                self.pieces.append(self.canvas.create_text(self.sq_size * (i + 0.5),
                                                           self.sq_size * (j + 0.6),
                                                           text=self.board[j][i].shape,
                                                           font=('Courier', int(self.sq_size * 0.6)),
                                                           fill=self.board[j][i].color))

class Pawn:
    def __init__(self, y, x, color):
        self.y, self.x = y, x
        self.color = color
        self.shape = '♟'
        self.step = -1 if self.color == 'white' else 1

    def get_moves(self):
        moves = [[self.y + self.step, self.x], [self.y + self.step, self.x - 1], [self.y + self.step, self.x + 1]]
        if (self.y == 6 and self.color == 'white') or (self.y == 1 and self.color == 'black'):
            moves.append([self.y + 2 * self.step, self.x])
        return [[y, x] for y, x in moves if 0 <= y <= 7 and 0 <= x <= 7]

class Queen:
    def __init__(self, y, x, color):
        self.y, self.x = y, x
        self.color = color
        self.shape = '♛'

    def get_moves(self):
        return Rook(self.y, self.x, self.color).get_moves() + Bishop(self.y, self.x, self.color).get_moves()

class Rook:
    def __init__(self, y, x, color):
        self.y, self.x = y, x
        self.color = color
        self.shape = '♜'
        self.moved = False

    def get_moves(self):
        moves = []
        colm_up, colm_down = [], []
        row_back, row_for = [], []
        for i in range(1, 8):
            if 0 <= self.y + i <= 7 and 0 <= self.x <= 7: colm_down.append([self.y + i, self.x])
            if 0 <= self.y - i <= 7 and 0 <= self.x <= 7: colm_up.append([self.y - i, self.x])
            if 0 <= self.y <= 7 and 0 <= self.x - i <= 7: row_back.append([self.y, self.x - i])
            if 0 <= self.y <= 7 and 0 <= self.x + i <= 7: row_for.append([self.y, self.x + i])
        moves.append(colm_up)
        moves.append(colm_down)
        moves.append(row_back)
        moves.append(row_for)
        return moves

class Bishop:
    def __init__(self, y, x, color):
        self.y, self.x = y, x
        self.color = color
        self.shape = '♝'

    def get_moves(self):
        moves = []
        up_left, up_right = [], []
        down_left, down_right = [], []
        for i in range(1, 8):
            if 0 <= self.y - i <= 7 and 0 <= self.x + i <= 7: up_right.append([self.y - i, self.x + i])
            if 0 <= self.y - i <= 7 and 0 <= self.x - i <= 7: up_left.append([self.y - i, self.x - i])
            if 0 <= self.y + i <= 7 and 0 <= self.x + i <= 7: down_right.append([self.y + i, self.x + i])
            if 0 <= self.y + i <= 7 and 0 <= self.x - i <= 7: down_left.append([self.y + i, self.x - i])
        moves.append(up_right)
        moves.append(up_left)
        moves.append(down_right)
        moves.append(down_left)
        return moves

class King:
    def __init__(self, y, x, color):
        self.y, self.x = y, x
        self.color = color
        self.shape = '♚'
        self.moved = False

    def get_moves(self):
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= self.y - i <= 7 and 0 <= self.x - j <= 7 and not i == j == 0:
                    moves.append([[self.y - i, self.x - j]])
        return moves

class Knight:
    def __init__(self, y, x, color):
        self.y, self.x = y, x
        self.color = color
        self.shape = '♞'

    def get_moves(self):
        moves = []
        for i in [-2, -1, 1, 2]:
            for j in [-2, -1, 1, 2]:
                if 0 <= self.y + i <= 7 and 0 <= self.x + j <= 7 and not abs(i) == abs(j):
                    moves.append([[self.y + i, self.x + j]])
        return moves

tk = Tk()
tk.title('Python Chess')
tk.wm_attributes('-topmost', 1)
tk.resizable(False, False)
square_size = 60
canvas = Canvas(tk, width = square_size * 8, height = square_size * 8)
canvas.pack()
for x in range(8):
    for y in range(8):
        canvas.create_rectangle(x * square_size, y * square_size, (x + 1) * square_size, (y + 1) * square_size,
                                fill = 'brown' if (x + y) % 2 != 0 else 'gray70')
for x in range(1, 9):
    canvas.create_text(square_size * (x - 0.2), square_size * 7.8, text=chr(ord('a') + x - 1))
    canvas.create_text(square_size * 7.9, square_size * (x - 0.2), text=9 - x)
    canvas.create_text(square_size * 0.1, square_size * (x - 0.2), text=x - 1, fill='yellow')
    canvas.create_text(square_size * (x - 0.2), square_size * 0.2, text=x - 1, fill='yellow')

game = Board(canvas, square_size)
game.show()

while not game.game_over:
    tk.update()
    time.sleep(0.01)
