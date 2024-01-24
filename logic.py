

class Game_State:
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
        self.undo_log = []
        self.move_log = []


    # Moves a single piece
    def move_piece(self, move):
        self.board[move.from_sq_row][move.from_sq_col] = "e"
        self.board[move.to_sq_row][move.to_sq_col] = move.piece_moved
        self.move_log.append(move)
        self.whites_turn = not self.whites_turn

    #Undoes a single piece move
    def undo_move_piece(self):
        if len(self.move_log) > 0:
            last_move = self.move_log.pop()
            taken_piece = last_move.piece_taken
            undo_move = self.Single_Move((last_move.to_sq_row, last_move.to_sq_col), (last_move.from_sq_row, last_move.from_sq_col), self.board)
            self.move_piece(undo_move)
            self.move_log.pop()
            self.board[last_move.to_sq_row][last_move.to_sq_col] = taken_piece
            self.undo_log.append(undo_move)

    def redo_move_piece(self):
        if len(self.undo_log) > 0:
            print("here")
            redo_move = self.undo_log.pop()
            self.move_piece(redo_move)
            self.whites_turn = not self.whites_turn

    # Returns a list of every possible valid move
    def all_valid_moves(self):
        all_moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                color = self.board[r][c][0]
                if (color == 'w' and self.whites_turn) or (color == 'b' and not self.whites_turn):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        all_moves.extend(self.get_pawn_moves(r=r, c=c))
                    elif piece == 'R':
                        all_moves.extend(self.get_rook_moves(r=r, c=c))
                    elif piece == 'N':
                        all_moves.extend(self.get_knight_moves(r=r, c=c))
                    elif piece == 'B':
                        all_moves.extend(self.get_bishop_moves(r=r, c=c))
                    elif piece == 'Q':
                        all_moves.extend(self.get_queen_moves(r=r, c=c))
                    elif piece == 'K':
                        all_moves.extend(self.get_king_moves(r=r, c=c))

        return all_moves


    def display_black_turn(self):
        black_board = self.board[::-1]
        for col in black_board:
            col = col[::-1]
        return black_board

    # All pawn moves
    # One square forward, two if first move until blocked, takes diagonally one space
    def get_pawn_moves(self, r, c):
        pawn_moves = []
        # White Paws
        if self.whites_turn and (r - 1 >= 0):
            if self.board[r - 1][c] == 'e':
                pawn_moves.append(self.Single_Move((r, c), (r - 1, c), self.board))

                if (r == 6) and self.board[r - 2][c] == 'e':
                    pawn_moves.append(self.Single_Move((r, c), (r - 2, c), self.board))

            # Cover taking diagonally
            if (c - 1 >=  0) and self.board[r - 1][c - 1][0] == 'b':
                pawn_moves.append(self.Single_Move((r, c), (r - 1, c - 1), self.board))

            if (c + 1 < 8) and self.board[r - 1][c + 1][0] == 'b':
                pawn_moves.append(self.Single_Move((r, c), (r - 1, c + 1), self.board))

        elif not self.whites_turn and (r + 1 < 8):
            if self.board[r + 1][c] == 'e':
                pawn_moves.append(self.Single_Move((r, c), (r + 1, c), self.board))

                if (r == 1) and self.board[r + 1][c] == 'e':
                    pawn_moves.append(self.Single_Move((r, c), (r + 2, c), self.board))

            # Cover taking diagonally
            if (c - 1 >=  0) and self.board[r + 1][c - 1][0] == 'w':
                pawn_moves.append(self.Single_Move((r, c), (r + 1, c - 1), self.board))

            if (c + 1 < 8) and self.board[r + 1][c + 1][0] == 'w':
                pawn_moves.append(self.Single_Move((r, c), (r + 1, c + 1), self.board))

        return pawn_moves


    # All moves that a rook can make
    # Up, down, left, right - as far as possible until blocked or takes
    def get_rook_moves(self, r, c):
        rook_moves = []

        # Rook moves up
        up = 1
        while (up < 8) and (r - up >= 0):
            if self.board[r - up][c] == 'e':
                rook_moves.append(self.Single_Move((r, c), (r - up, c), self.board))

            if ((self.whites_turn and self.board[r - up][c][0] == 'b') or 
                (not self.whites_turn and self.board[r - up][c][0] == 'w')):
                rook_moves.append(self.Single_Move((r, c), (r - up, c), self.board))
                break

            if ((self.whites_turn and self.board[r - up][c][0] == 'w') or 
                (not self.whites_turn and self.board[r - up][c][0] == 'b')):
                break
            up += 1

        # Rook moves down
        down = 1
        while (down < 8) and (r + down < 8):
            if self.board[r + down][c] == 'e':
                rook_moves.append(self.Single_Move((r, c), (r + down, c), self.board))

            if ((self.whites_turn and self.board[r + down][c][0] == 'b') or 
                (not self.whites_turn and self.board[r + down][c][0] == 'w')):
                rook_moves.append(self.Single_Move((r, c), (r + down, c), self.board))
                break

            if ((self.whites_turn and self.board[r + down][c][0] == 'w') or 
                (not self.whites_turn and self.board[r + down][c][0] == 'b')):
                break
            down += 1

        # Rook moves right
        right = 1
        while (right < 8) and (c + right < 8):
            if self.board[r][c + right] == 'e':
                rook_moves.append(self.Single_Move((r, c), (r, c + right), self.board))

            if ((self.whites_turn and self.board[r][c + right][0] == 'b') or 
                (not self.whites_turn and self.board[r][c + right][0] == 'w')):
                rook_moves.append(self.Single_Move((r, c), (r, c + right), self.board))
                break

            if ((self.whites_turn and self.board[r][c + right][0] == 'w') or 
                (not self.whites_turn and self.board[r][c + right][0] == 'b')):
                break
            right += 1

        # Rook moves left
        left = 1
        while (left < 8) and (c - left >= 0):
            if self.board[r][c - left] == 'e':
                rook_moves.append(self.Single_Move((r, c), (r, c - left), self.board))

            if ((self.whites_turn and self.board[r][c - left][0] == 'b') or 
                (not self.whites_turn and self.board[r][c - left][0] == 'w')):
                rook_moves.append(self.Single_Move((r, c), (r, c - left), self.board))
                break

            if ((self.whites_turn and self.board[r][c - left][0] == 'w') or 
                (not self.whites_turn and self.board[r][c - left][0] == 'b')):
                break
            left += 1

        return rook_moves


    # All Knight moves
    # Moves two squares in one direction then one square perpendicularly
    # Can take, can jump
    def get_knight_moves(self, r, c):
        knight_moves = []

        if (r - 2 >= 0) and (c - 1 >= 0):
            if ((self.board[r - 2][c - 1] == 'e') or
                (self.whites_turn and self.board[r - 2][c - 1][0] == 'b') or 
                (not self.whites_turn and self.board[r - 2][c - 1][0] == 'w')):
                knight_moves.append(self.Single_Move((r, c), (r - 2, c - 1), self.board))

        if (r - 1 >= 0) and (c - 2 >= 0):
            if ((self.board[r - 1][c - 2] == 'e') or
                (self.whites_turn and self.board[r - 1][c - 2][0] == 'b') or 
                (not self.whites_turn and self.board[r - 1][c - 2][0] == 'w')):
                knight_moves.append(self.Single_Move((r, c), (r - 1, c - 2), self.board))

        if (r - 2 >= 0) and (c + 1 < 8):
            if ((self.board[r - 2][c + 1] == 'e') or
                (self.whites_turn and self.board[r - 2][c + 1][0] == 'b') or 
                (not self.whites_turn and self.board[r - 2][c + 1][0] == 'w')):
                knight_moves.append(self.Single_Move((r, c), (r - 2, c + 1), self.board))

        if (r - 1 >= 0) and (c + 2 < 8):
            if ((self.board[r - 1][c + 2] == 'e') or
                (self.whites_turn and self.board[r - 1][c + 2][0] == 'b') or 
                (not self.whites_turn and self.board[r - 1][c + 2][0] == 'w')):
                knight_moves.append(self.Single_Move((r, c), (r - 1, c + 2), self.board))

        if (r + 2 < 8) and (c - 1 >= 0):
            if ((self.board[r + 2][c - 1] == 'e') or
                (self.whites_turn and self.board[r + 2][c - 1][0] == 'b') or 
                (not self.whites_turn and self.board[r + 2][c - 1][0] == 'w')):
                knight_moves.append(self.Single_Move((r, c), (r + 2, c - 1), self.board))

        if (r + 1 < 8) and (c - 2 >= 0):
            if ((self.board[r + 1][c - 2] == 'e') or
                (self.whites_turn and self.board[r + 1][c - 2][0] == 'b') or 
                (not self.whites_turn and self.board[r + 1][c - 2][0] == 'w')):
                knight_moves.append(self.Single_Move((r, c), (r + 1, c - 2), self.board))

        if (r + 2 < 8) and (c + 1 < 8):
            if ((self.board[r + 2][c + 1] == 'e') or
                (self.whites_turn and self.board[r + 2][c + 1][0] == 'b') or 
                (not self.whites_turn and self.board[r + 2][c + 1][0] == 'w')):
                knight_moves.append(self.Single_Move((r, c), (r + 2, c + 1), self.board))

        if (r + 1 < 8) and (c + 2 < 8):
            if ((self.board[r + 1][c + 2] == 'e') or
                (self.whites_turn and self.board[r + 1][c + 2][0] == 'b') or 
                (not self.whites_turn and self.board[r + 1][c + 2][0] == 'w')):
                knight_moves.append(self.Single_Move((r, c), (r + 1, c + 2), self.board))
    
        return knight_moves


    def get_bishop_moves(self, r, c):
        bishop_moves = []

        up_left = 1
        while (up_left < 8) and (r - up_left >= 0) and (c - up_left >= 0):
            if self.board[r - up_left][c - up_left] == 'e':
                bishop_moves.append(self.Single_Move((r, c), (r - up_left, c - up_left), self.board))


            if ((self.whites_turn and self.board[r - up_left][c - up_left][0] == 'b') or 
                (not self.whites_turn and self.board[r - up_left][c - up_left][0] == 'w')):
                bishop_moves.append(self.Single_Move((r, c), (r - up_left, c - up_left), self.board))
                break

            if ((self.whites_turn and self.board[r - up_left][c - up_left][0] == 'w') or 
                (not self.whites_turn and self.board[r - up_left][c - up_left][0] == 'b')):
                break
            up_left +=1 

        up_right = 1
        while (up_right < 8) and (r - up_right >= 0) and (c + up_right < 8):
            if self.board[r - up_right][c + up_right] == 'e':
                bishop_moves.append(self.Single_Move((r, c), (r - up_right, c + up_right), self.board))


            if ((self.whites_turn and self.board[r - up_right][c + up_right][0] == 'b') or 
                (not self.whites_turn and self.board[r - up_right][c + up_right][0] == 'w')):
                bishop_moves.append(self.Single_Move((r, c), (r - up_right, c + up_right), self.board))
                break

            if ((self.whites_turn and self.board[r - up_right][c + up_right][0] == 'w') or 
                (not self.whites_turn and self.board[r - up_right][c + up_right][0] == 'b')):
                break
            up_right += 1

        down_left = 1
        while (down_left < 8) and (r + down_left < 8) and (c - down_left >= 0):
            if self.board[r + down_left][c - down_left] == 'e':
                bishop_moves.append(self.Single_Move((r, c), (r + down_left, c - down_left), self.board))


            if ((self.whites_turn and self.board[r + down_left][c - down_left][0] == 'b') or 
                (not self.whites_turn and self.board[r + down_left][c - down_left][0] == 'w')):
                bishop_moves.append(self.Single_Move((r, c), (r + down_left, c - down_left), self.board))
                break

            if ((self.whites_turn and self.board[r + down_left][c - down_left][0] == 'w') or 
                (not self.whites_turn and self.board[r + down_left][c - down_left][0] == 'b')):
                break
            down_left +=1 


        down_right = 1
        while (down_right < 8) and (r + down_right < 8) and (c + down_right < 8):
            if self.board[r + down_right][c + down_right] == 'e':
                bishop_moves.append(self.Single_Move((r, c), (r + down_right, c + down_right), self.board))


            if ((self.whites_turn and self.board[r + down_right][c + down_right][0] == 'b') or 
                (not self.whites_turn and self.board[r + down_right][c + down_right][0] == 'w')):
                bishop_moves.append(self.Single_Move((r, c), (r + down_right, c + down_right), self.board))
                break

            if ((self.whites_turn and self.board[r + down_right][c + down_right][0] == 'w') or 
                (not self.whites_turn and self.board[r + down_right][c + down_right][0] == 'b')):
                break
            down_right +=1 


        return bishop_moves

    def get_queen_moves(self, r, c):
        queen_moves = []
        queen_moves.extend(self.get_bishop_moves(r=r, c=c))
        queen_moves.extend(self.get_rook_moves(r=r, c=c))
        return queen_moves

    def get_king_moves(self, r, c):
        king_moves = []

        if (r - 1 >= 0):
            if ((self.board[r - 1][c][0] == 'e') or 
                    (self.whites_turn and self.board[r - 1][c][0] == 'b') or 
                    (not self.whites_turn and self.board[r - 1][c][0] == 'w')):
                    king_moves.append(self.Single_Move((r, c), (r - 1, c), self.board))

            if (c - 1 >= 0):
                if ((self.board[r - 1][c - 1][0] == 'e') or 
                    (self.whites_turn and self.board[r - 1][c - 1][0] == 'b') or 
                    (not self.whites_turn and self.board[r - 1][c - 1][0] == 'w')):
                    king_moves.append(self.Single_Move((r, c), (r - 1, c - 1), self.board))


            if (c + 1 < 8):
                if ((self.board[r - 1][c + 1][0] == 'e') or 
                    (self.whites_turn and self.board[r - 1][c + 1][0] == 'b') or 
                    (not self.whites_turn and self.board[r - 1][c + 1][0] == 'w')):
                    king_moves.append(self.Single_Move((r, c), (r - 1, c + 1), self.board))

        
        if (r + 1 < 8):
            if ((self.board[r + 1][c][0] == 'e') or 
                (self.whites_turn and self.board[r + 1][c][0] == 'b') or 
                (not self.whites_turn and self.board[r + 1][c][0] == 'w')):
                king_moves.append(self.Single_Move((r, c), (r + 1, c), self.board))

            if (c - 1 >= 0):
                if ((self.board[r + 1][c - 1][0] == 'e') or 
                    (self.whites_turn and self.board[r + 1][c - 1][0] == 'b') or 
                    (not self.whites_turn and self.board[r + 1][c - 1][0] == 'w')):
                    king_moves.append(self.Single_Move((r, c), (r + 1, c - 1), self.board))

            if (c + 1 < 8):
                if ((self.board[r + 1][c + 1][0] == 'e') or 
                    (self.whites_turn and self.board[r + 1][c + 1][0] == 'b') or 
                    (not self.whites_turn and self.board[r + 1][c + 1][0] == 'w')):
                    king_moves.append(self.Single_Move((r, c), (r + 1, c + 1), self.board))

        if (c + 1 < 8):
            if ((self.board[r][c + 1][0] == 'e') or 
                (self.whites_turn and self.board[r][c + 1][0] == 'b') or 
                (not self.whites_turn and self.board[r][c + 1][0] == 'w')):
                king_moves.append(self.Single_Move((r, c), (r, c + 1), self.board))

        if (c - 1 >= 0):
            if ((self.board[r][c - 1][0] == 'e') or 
                (self.whites_turn and self.board[r][c - 1][0] == 'b') or 
                (not self.whites_turn and self.board[r][c - 1][0] == 'w')):
                king_moves.append(self.Single_Move((r, c), (r, c - 1), self.board))

        return king_moves


    class Single_Move:
        def __init__(self, from_sq, to_sq, board):
            self.from_sq_row = from_sq[0]
            self.from_sq_col = from_sq[1]
            self.to_sq_row = to_sq[0]
            self.to_sq_col = to_sq[1]

            self.piece_moved = board[self.from_sq_row][self.from_sq_col]
            self.piece_taken = board[self.to_sq_row][self.to_sq_col]

        def __eq__(self, other):
            if isinstance(other, type(self)):
                if ((self.from_sq_col == other.from_sq_col) and 
                   (self.from_sq_row == other.from_sq_row) and 
                   (self.to_sq_col == other.to_sq_col) and 
                   (self.to_sq_row == other.to_sq_row)):
                   return True
                else:
                    return False


