

class Game_State():
    def __init__(self):
        #8 X 8 board
        # "e" is empty
        # first char is color, second is Piece 
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["e", "e", "e", "e", "e", "e", "e", "e"],
            ["e", "e", "e", "e", "e", "e", "e", "e"],
            ["e", "e", "e", "e", "e", "e", "e", "e"],
            ["e", "e", "e", "e", "e", "e", "e", "e"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.whites_turn = True
        self.move_log = []


    def move_piece(self, move):
        self.board[move.from_sq_row][move.from_sq_col] = "e"
        self.board[move.to_sq_row][move.to_sq_col] = move.piece_moved
        self.move_log.append(move)
        self.whites_turn = not self.whites_turn


    class Single_Move():
        def __init__(self, from_sq, to_sq, board):
            self.from_sq_row = from_sq[0]
            self.from_sq_col = from_sq[1]
            self.to_sq_row = to_sq[0]
            self.to_sq_col = to_sq[1]

            self.piece_moved = board[self.from_sq_row][self.from_sq_col]
            self.piece_taken = board[self.to_sq_row][self.to_sq_col]

