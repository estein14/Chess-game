
import pygame as p
import logic
import time

WIDTH = HEIGHT = 600
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION #50
MAX_FPS = 15 #Animations
IMAGES = {}

#Load in the Images
def load_images():
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("pieces/" + piece + ".png"), ((SQ_SIZE - 4), (SQ_SIZE - 4)))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = logic.Game_State()
    valid_moves = gs.all_valid_moves()
    move_made = False
    load_images()
    running = True
    piece_chosen = ()
    turn = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                cur_location = p.mouse.get_pos()
                col = cur_location[0] // SQ_SIZE
                row = cur_location[1] // SQ_SIZE
                # Chosing same piece twice unclicks
                if piece_chosen == (row, col):
                    piece_chosen = ()
                    turn = []
                # first piece chosen
                else:
                    piece_chosen = (row, col)
                    turn.append(piece_chosen)

                    # Highlight red if wrong move
                    # p.draw.rect(screen, p.Color("Red"), p.Rect(row * SQ_SIZE, col * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    # time.sleep(2)
                # Second sqaure chosen
                if len(turn) == 2:
                    move = gs.Single_Move(turn[0], turn[1], gs.board)
                    
                    if move in valid_moves:
                        gs.move_piece(move)
                        move_made = True
                        piece_chosen = ()
                        turn = []
                    else:
                        piece_chosen = ()
                        turn = []
                    
            # Backspace undoes moves
            elif e.type == p.KEYDOWN:
                keys_pressed = p.key.get_pressed()
                if keys_pressed[p.K_BACKSPACE]:
                    gs.undo_move_piece()
                    move_made = True
                    valid_moves = gs.all_valid_moves()

                elif keys_pressed[p.K_r]:
                    gs.redo_move_piece()
                    move_made = True
                    valid_moves = gs.all_valid_moves()


        if move_made:
            valid_moves = gs.all_valid_moves()
            move_made = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

        
# Drawing all the graphics for gamestate
def drawGameState(screen, gs):
    drawSquares(screen, gs)

    # Add in highliting or loop suggestions or something
    drawPieces(screen, gs)

def drawSquares(screen, gs):
    colors = [p.Color("white"), p.Color("gray")]
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            color = colors[((x + y) % 2)]
            p.draw.rect(screen, color, p.Rect(y * SQ_SIZE, x * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, gs):
    # if gs.whites_turn:
        for x in range(DIMENSION):
            for y in range(DIMENSION):
                piece = gs.board[x][y]
                if piece != "e":
                    screen.blit(IMAGES[piece], p.Rect(y * SQ_SIZE, x * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    # else:
    #     for x in range(DIMENSION):
    #         for y in range(DIMENSION):
    #             piece = gs.board[x][y]
    #             if piece != "e":
    #                 screen.blit(IMAGES[piece], p.Rect((7 - y) * SQ_SIZE, (7 - x) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    
if __name__ == "__main__":
    main()
