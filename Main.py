import pygame
from Nodes.board import Board
from Nodes.Consants import *
pygame.init()
FPS = 60
WIN = pygame.display.set_mode((WINDOWWIDTH + 200, WINDOWHEIGHT))
pygame.display.set_caption('A Star')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    if x > WINDOWWIDTH:
        return -1, -1
    return row,col

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board(WIN)

    pygame.font.init()
    myfont = pygame.font.SysFont("monospace", 16)
    Found = False

    while run:
        clock.tick(FPS)
        
        pygame.draw.rect(WIN, WHITE, (WINDOWWIDTH, 0, 200, WINDOWHEIGHT))
        if Found:
            board.DrawFound()
        else:
            board.drawBoard()
        pygame.draw.rect(WIN, BLACK, (WINDOWWIDTH, 0 , 5, WINDOWHEIGHT))

        #Text Drawing
        StartText = myfont.render("Start: {0}, {1}".format(str(board.start.current.x), str(board.start.current.y)), 0, BLACK)
        GoalText = myfont.render("Goal : {0}, {1}".format(str(board.goal.current.x), str(board.goal.current.y)), 0, BLACK)
        Instructions = myfont.render("Enter To Go ", 0, BLACK)
        Instructions2 = myfont.render("Backspace To Reset", 0, BLACK)
        Path = myfont.render("Path:", 0, BLACK)

        WIN.blit(StartText, (WINDOWWIDTH + 10, 10))
        WIN.blit(GoalText, (WINDOWWIDTH + 10, 25))
        WIN.blit(Instructions, (WINDOWWIDTH + 10, 40))
        WIN.blit(Instructions2, (WINDOWWIDTH + 10, 55))
        WIN.blit(Path, (WINDOWWIDTH + 10, 70))



        if Found:
            counter = 1
            for Cord in board.Path:
                if not(70 + counter * 15 > WINDOWHEIGHT):
                    text = myfont.render("{0}: {1}".format(counter, str(Cord)), 0, BLACK)
                    WIN.blit(text, (WINDOWWIDTH + 10, 70 + counter * 15))
                    counter += 1
        

        pygame.display.update()

        #Event Loop
        keysPressed = pygame.key.get_pressed()

        board.changeNodeState(keysPressed)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
            
            '''if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                if row != -1 and col != -1:
                    board.changeNodeState(col, row)
            '''


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if board.runSimulation():
                        Found = True
                if event.key == pygame.K_BACKSPACE:
                    Found = False
                    board.reset()

    pygame.quit()

main()