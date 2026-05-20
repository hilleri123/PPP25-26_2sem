from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

Pos = Tuple[int, int]
Color = str


class Piece(ABC):
    _color: Color
    _symbol: str
    _has_moved: bool

    def __init__(self, color: Color, symbol: str) -> None:
        self._color = color
        self._symbol = symbol
        self._has_moved = False

    @property
    def color(self) -> Color:
        return self._color

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def has_moved(self) -> bool:
        return self._has_moved

    @abstractmethod
    def get_pseudo_legal_moves(self, board: Board) -> List[Pos]:
        pass

    def mark_moved(self) -> None:
        self._has_moved = True

    def _slide(
        self, board: Board, directions: List[Tuple[int, int]]
    ) -> List[Pos]:
        r, c = board.get_pos_of(self)
        moves: List[Pos] = []
        for dr, dc in directions:
            tr, tc = r + dr, c + dc
            while board.is_on_board((tr, tc)):
                target = board.get_piece((tr, tc))
                if not target:
                    moves.append((tr, tc))
                else:
                    if target.color != self.color:
                        moves.append((tr, tc))
                    break
                tr += dr
                tc += dc
        return moves

    def _step(
        self, board: Board, deltas: List[Tuple[int, int]]
    ) -> List[Pos]:
        r, c = board.get_pos_of(self)
        moves: List[Pos] = []
        for dr, dc in deltas:
            tr, tc = r + dr, c + dc
            if board.is_on_board((tr, tc)):
                t = board.get_piece((tr, tc))
                if not t or t.color != self.color:
                    moves.append((tr, tc))
        return moves


class Rook(Piece):
    def __init__(self, color: Color) -> None:
        sym = "♖" if color == "white" else "♜"
        super().__init__(color, sym)

    def get_pseudo_legal_moves(self, board: Board) -> List[Pos]:
        return self._slide(board, [(0, 1), (0, -1), (1, 0), (-1, 0)])


class Bishop(Piece):
    def __init__(self, color: Color) -> None:
        sym = "♗" if color == "white" else "♝"
        super().__init__(color, sym)

    def get_pseudo_legal_moves(self, board: Board) -> List[Pos]:
        return self._slide(board, [(1, 1), (1, -1), (-1, 1), (-1, -1)])


class Queen(Piece):
    def __init__(self, color: Color) -> None:
        sym = "♕" if color == "white" else "♛"
        super().__init__(color, sym)

    def get_pseudo_legal_moves(self, board: Board) -> List[Pos]:
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0),
                (1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._slide(board, dirs)


class Knight(Piece):
    def __init__(self, color: Color) -> None:
        sym = "♘" if color == "white" else "♞"
        super().__init__(color, sym)

    def get_pseudo_legal_moves(self, board: Board) -> List[Pos]:
        deltas = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                  (1, 2), (1, -2), (-1, 2), (-1, -2)]
        return self._step(board, deltas)


class King(Piece):
    def __init__(self, color: Color) -> None:
        sym = "♔" if color == "white" else "♚"
        super().__init__(color, sym)

    def get_pseudo_legal_moves(self, board: Board) -> List[Pos]:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]
        moves = self._step(board, deltas)
        if not self.has_moved:
            row = 7 if self.color == "white" else 0
            if self._can_castle(board, row, 4, 7):
                moves.append((row, 6))
            if self._can_castle(board, row, 4, 0):
                moves.append((row, 2))
        return moves

    def _can_castle(
        self, board: Board, row: int, k_col: int, r_col: int
    ) -> bool:
        rook = board.get_piece((row, r_col))
        if not rook or not isinstance(rook, Rook) or rook.has_moved:
            return False
        step = 1 if r_col > k_col else -1
        for c in range(k_col + step, r_col, step):
            if board.get_piece((row, c)):
                return False
        return True


class Pawn(Piece):
    def __init__(self, color: Color) -> None:
        sym = "♙" if color == "white" else "♟"
        super().__init__(color, sym)

    def get_pseudo_legal_moves(self, board: Board) -> List[Pos]:
        r, c = board.get_pos_of(self)
        moves: List[Pos] = []
        step_dir = -1 if self.color == "white" else 1
        start = 6 if self.color == "white" else 1

        fwd = (r + step_dir, c)
        if board.is_on_board(fwd) and not board.get_piece(fwd):
            moves.append(fwd)
            if r == start:
                fwd2 = (r + 2 * step_dir, c)
                if board.is_on_board(fwd2) and not board.get_piece(fwd2):
                    moves.append(fwd2)

        for dc in [-1, 1]:
            tr, tc = r + step_dir, c + dc
            if board.is_on_board((tr, tc)):
                t = board.get_piece((tr, tc))
                if t and t.color != self.color:
                    moves.append((tr, tc))
                elif (tr, tc) == board.en_passant_target:
                    moves.append((tr, tc))
        return moves


class Centaur(Piece):
    def __init__(self, color: Color) -> None:
        sym = "🦄" if color == "white" else "🦅"
        super().__init__(color, sym)

    def get_pseudo_legal_moves(self, board: Board) -> List[Pos]:
        moves_k = Knight(self.color).get_pseudo_legal_moves(board)
        moves_r = Rook(self.color).get_pseudo_legal_moves(board)
        return list(set(moves_k + moves_r))


class Amazon(Piece):
    def __init__(self, color: Color) -> None:
        sym = "👸" if color == "white" else "🤴"
        super().__init__(color, sym)

    def get_pseudo_legal_moves(self, board: Board) -> List[Pos]:
        moves_q = Queen(self.color).get_pseudo_legal_moves(board)
        moves_k = Knight(self.color).get_pseudo_legal_moves(board)
        return list(set(moves_q + moves_k))


class Wazir(Piece):
    def __init__(self, color: Color) -> None:
        sym = "🪙" if color == "white" else "🥉"
        super().__init__(color, sym)

    def get_pseudo_legal_moves(self, board: Board) -> List[Pos]:
        return self._step(board, [(0, 1), (0, -1), (1, 0), (-1, 0)])


class Move:
    def __init__(
        self, from_pos: Pos, to_pos: Pos, piece: Piece,
        captured: Optional[Piece], special: str = ""
    ) -> None:
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece = piece
        self.captured = captured
        self.special = special

    def undo(self, board: Board) -> None:
        board.grid[self.from_pos[0]][self.from_pos[1]] = self.piece
        board.grid[self.to_pos[0]][self.to_pos[1]] = self.captured
        self.piece._has_moved = False

        if self.special == "en_passant" and self.captured:
            cr = self.to_pos[0]
            cr += 1 if self.piece.color == "white" else -1
            board.grid[cr][self.to_pos[1]] = self.captured

        if self.special == "castle":
            if self.to_pos[1] == 6:
                rf: Pos = (self.to_pos[0], 7)
                rt: Pos = (self.to_pos[0], 5)
            else:
                rf = (self.to_pos[0], 0)
                rt = (self.to_pos[0], 3)
            board.grid[rt[0]][rt[1]] = board.grid[rf[0]][rf[1]]
            board.grid[rf[0]][rf[1]] = None
            rp = board.grid[rt[0]][rt[1]]
            if rp:
                rp._has_moved = False


class Board:
    def __init__(self) -> None:
        self.grid: List[List[Optional[Piece]]] = [[None] * 8 for _ in range(8)]
        self.turn: Color = "white"
        self.history: List[Move] = []
        self.en_passant_target: Optional[Pos] = None

    def setup(self) -> None:
        self.grid[0][0] = Rook("black")
        self.grid[0][1] = Knight("black")
        self.grid[0][2] = Bishop("black")
        self.grid[0][3] = Queen("black")
        self.grid[0][4] = King("black")
        self.grid[0][5] = Bishop("black")
        self.grid[0][6] = Knight("black")
        self.grid[0][7] = Rook("black")
        for c in range(8):
            self.grid[1][c] = Pawn("black")
        for c in range(8):
            self.grid[6][c] = Pawn("white")
        self.grid[7][0] = Rook("white")
        self.grid[7][1] = Knight("white")
        self.grid[7][2] = Bishop("white")
        self.grid[7][3] = Queen("white")
        self.grid[7][4] = King("white")
        self.grid[7][5] = Bishop("white")
        self.grid[7][6] = Knight("white")
        self.grid[7][7] = Rook("white")

    def is_on_board(self, pos: Pos) -> bool:
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8

    def get_piece(self, pos: Pos) -> Optional[Piece]:
        if self.is_on_board(pos):
            return self.grid[pos[0]][pos[1]]
        return None

    def get_pos_of(self, p: Piece) -> Pos:
        for r in range(8):
            for c in range(8):
                if self.grid[r][c] is p:
                    return (r, c)
        return (-1, -1)

    def get_pseudo_legal_moves(self, pos: Pos) -> List[Pos]:
        p = self.get_piece(pos)
        if p and p.color == self.turn:
            return p.get_pseudo_legal_moves(self)
        return []

    def is_king_in_check(self, color: Color) -> bool:
        kp: Optional[Pos] = None
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if isinstance(piece, King) and piece.color == color:
                    kp = (r, c)
                    break
            if kp:
                break
        if not kp:
            return False

        enemy = "black" if color == "white" else "white"
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if piece and piece.color == enemy:
                    if kp in piece.get_pseudo_legal_moves(self):
                        return True
        return False

    def get_valid_moves(self, pos: Pos) -> List[Pos]:
        pseudo = self.get_pseudo_legal_moves(pos)
        p = self.get_piece(pos)
        if not p:
            return []
        valid: List[Pos] = []
        for t in pseudo:
            self.make_move(pos, t)
            if not self.is_king_in_check(p.color):
                valid.append(t)
            self.undo_last_move()
        return valid

    def make_move(
        self, from_pos: Pos, to_pos: Pos, promo: Optional[str] = None
    ) -> None:
        piece = self.get_piece(from_pos)
        if not piece:
            return
        captured = self.get_piece(to_pos)
        special = ""

        is_ep = isinstance(piece, Pawn)
        is_ep = is_ep and to_pos == self.en_passant_target
        is_ep = is_ep and not captured
        if is_ep:
            cr = to_pos[0] + (1 if piece.color == "white" else -1)
            special = "en_passant"
            captured = self.grid[cr][to_pos[1]]
            self.grid[cr][to_pos[1]] = None

        if isinstance(piece, King) and abs(from_pos[1] - to_pos[1]) == 2:
            if to_pos[1] == 6:
                rf: Pos = (to_pos[0], 7)
                rt: Pos = (to_pos[0], 5)
            else:
                rf = (to_pos[0], 0)
                rt = (to_pos[0], 3)
            self.grid[rt[0]][rt[1]] = self.grid[rf[0]][rf[1]]
            self.grid[rf[0]][rf[1]] = None
            rp = self.grid[rt[0]][rt[1]]
            if rp:
                rp.mark_moved()
            special = "castle"

        self.grid[to_pos[0]][to_pos[1]] = piece
        self.grid[from_pos[0]][from_pos[1]] = None
        piece.mark_moved()

        if isinstance(piece, Pawn) and to_pos[0] in (0, 7):
            special = "promotion"
            choice = (promo or "Q").upper()
            if choice == "Q":
                new_piece: Piece = Queen(piece.color)
            elif choice == "R":
                new_piece = Rook(piece.color)
            elif choice == "B":
                new_piece = Bishop(piece.color)
            else:
                new_piece = Knight(piece.color)
            self.grid[to_pos[0]][to_pos[1]] = new_piece

        self.en_passant_target = None
        if isinstance(piece, Pawn) and abs(from_pos[0] - to_pos[0]) == 2:
            mid = (from_pos[0] + to_pos[0]) // 2
            self.en_passant_target = (mid, from_pos[1])

        self.history.append(Move(from_pos, to_pos, piece, captured, special))
        self.turn = "black" if self.turn == "white" else "white"

    def undo_last_move(self) -> bool:
        if not self.history:
            return False
        m = self.history.pop()
        m.undo(self)
        self.turn = "black" if self.turn == "white" else "white"
        return True

    def get_threatened_positions(self, color: Color) -> List[Pos]:
        enemy = "black" if color == "white" else "white"
        thr: set[Pos] = set()
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == enemy:
                    thr.update(p.get_pseudo_legal_moves(self))
        return list(thr)

    def display(
        self, hints: Optional[List[Pos]] = None,
        threats: Optional[List[Pos]] = None
    ) -> None:
        print("  a b c d e f g h")
        for r in range(8):
            line = f"{8-r} "
            for c in range(8):
                p = self.grid[r][c]
                cell = "." if not p else p.symbol
                if hints and (r, c) in hints:
                    cell = f"\033[92m[{cell}]\033[0m"
                elif threats and (r, c) in threats:
                    if p and p.color == self.turn:
                        cell = f"\033[91m<{cell}>\033[0m"
                line += cell + " "
            print(line)
        print()


class ChessGame:
    def __init__(self) -> None:
        self.board = Board()
        self.board.setup()
        self.running = True

    @staticmethod
    def parse_pos(s: str) -> Optional[Pos]:
        if len(s) != 2:
            return None
        try:
            c = ord(s[0]) - 97
            r = 8 - int(s[1])
            if 0 <= r < 8 and 0 <= c < 8:
                return (r, c)
        except ValueError:
            pass
        return None

    def run(self) -> None:
        print("Ходы: e2 e4 | Команды: hints, undo, exit")
        while self.running:
            chk = "ШАХ!" if self.board.is_king_in_check(
                self.board.turn) else ""
            thr = self.board.get_threatened_positions(self.board.turn)
            self.board.display(threats=thr)
            print(f"Ход: {self.board.turn} {chk}")
            try:
                cmd = input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nЗавершение.")
                return

            if cmd == "exit":
                self.running = False
            elif cmd == "undo" and self.board.undo_last_move():
                print("Отменено.")
            elif cmd == "hints":
                print("Подсказки вкл/выкл.")
            else:
                parts = cmd.split()
                if len(parts) == 2:
                    f = self.parse_pos(parts[0])
                    t = self.parse_pos(parts[1])
                    if f and t:
                        p = self.board.get_piece(f)
                        if not p or p.color != self.board.turn:
                            print("Не ваша фигура.")
                        elif t not in self.board.get_valid_moves(f):
                            print("Ход недопустим.")
                        else:
                            pr: Optional[str] = None
                            is_pawn = isinstance(p, Pawn)
                            if is_pawn and t[0] in (0, 7):
                                try:
                                    pr = input("Q/R/B/N [Q]: ").strip()
                                    pr = pr or "Q"
                                except (EOFError, KeyboardInterrupt):
                                    pr = "Q"
                            self.board.make_move(f, t, pr)
                    else:
                        print("Формат: a1 b2")
                else:
                    print("Введите ход или команду.")


if __name__ == "__main__":
    ChessGame().run()
