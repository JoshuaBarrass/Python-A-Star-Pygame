import pygame
import random
import time
from .Consants import *
from .Node import Node

class Board:

    def __init__(self, win):
        self.win = win
        self._Init()
    
    def _Init(self):
        self.start = Node(random.randint(0, ROWS-1), random.randint(0, COLS-1), None, True)
        self.goal = Node(random.randint(0, ROWS-1), random.randint(0, COLS-1), None, False, True)
        self.start.SetDistance(self.goal)
        self.board = self._createBoard()
        self.OpenNodes = []
        self.VisitedNodes = []
        self.Path = []
        self.Found = []
        self.delay = 0.05
        self.LastPress = time.time()
    
    def reset(self):
        self._Init()

    def _createBoard(self):
        board = []
        for row in range(ROWS):
            Newrow = []
            
            for col in range(COLS):
                if self.start.current.x == row and self.start.current.y == col:
                    Newrow.append("A")
                elif self.goal.current.x == row and self.goal.current.y == col:
                    Newrow.append("B")
                else:
                    Newrow.append("")
            
            board.append(Newrow)
        
        return board

    def drawBoard(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == "A":
                    pygame.draw.rect(self.win, STARTCOL, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif self.board[row][col] == "B":
                    pygame.draw.rect(self.win, GOALCOL, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif self.board[row][col] == "K":
                    pygame.draw.rect(self.win, BLUE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(self.win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        
        for x in range(0, WINDOWWIDTH, SQUARE_SIZE):
            pygame.draw.line(self.win, BLACK, (x, 0), (x, WINDOWHEIGHT), 1)
            pygame.draw.line(self.win, BLACK, (0, x), (WINDOWWIDTH, x), 1)

        ''' def changeNodeState(self, X, Y):
        if self.board[X][Y] == "K":
            self.board[X][Y] = ""
        
        elif self.board[X][Y] == "":
            self.board[X][Y] = "K"
            '''

    def changeNodeState(self, keysPressed):
        Y, X = self._get_row_col_from_mouse(pygame.mouse.get_pos())
        if keysPressed[pygame.K_DELETE]:
                
            if self.board[X][Y] == "K":
                self.board[X][Y] = ""

        elif keysPressed[pygame.K_SPACE]:
            if self.board[X][Y] == "":
                self.board[X][Y] = "K"

    def _get_row_col_from_mouse(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        if x > WINDOWWIDTH:
            return -1, -1
        return row,col

    def _DrawRunningBoard(self):
        TempBoard = self.board
        for node in (self.VisitedNodes + self.OpenNodes):
            TempBoard[node.current.x][node.current.y] = "X"

        for row in range(ROWS):
            for col in range(COLS):
                if TempBoard[row][col] == "A":
                    pygame.draw.rect(self.win, STARTCOL, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif TempBoard[row][col] == "B":
                    pygame.draw.rect(self.win, GOALCOL, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif TempBoard[row][col] == "K":
                    pygame.draw.rect(self.win, BLUE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif TempBoard[row][col] == "X":
                    pygame.draw.rect(self.win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(self.win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for x in range(0, WINDOWWIDTH, SQUARE_SIZE):
            pygame.draw.line(self.win, BLACK, (x, 0), (x, WINDOWHEIGHT), 1)
            pygame.draw.line(self.win, BLACK, (0, x), (WINDOWWIDTH, x), 1)
        
        pygame.display.update()

    def DrawFound(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.Found[row][col] == "A":
                    pygame.draw.rect(self.win, STARTCOL, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif self.Found[row][col] == "B":
                    pygame.draw.rect(self.win, GOALCOL, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif self.Found[row][col] == "K":
                    pygame.draw.rect(self.win, BLUE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif self.Found[row][col] == "X":
                    pygame.draw.rect(self.win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif self.Found[row][col] == "*":
                    pygame.draw.rect(self.win, GREEN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(self.win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        
        for x in range(0, WINDOWWIDTH, SQUARE_SIZE):
            pygame.draw.line(self.win, BLACK, (x, 0), (x, WINDOWHEIGHT), 1)
            pygame.draw.line(self.win, BLACK, (0, x), (WINDOWWIDTH, x), 1)

    def runSimulation(self):
        self.OpenNodes.append(self.start)

        while self.OpenNodes != []:

            CheckNode = self._OrderNodeList(True)

            if CheckNode.current.x == self.goal.current.x and CheckNode.current.y == self.goal.current.y:
                print("Destination Reached")
                node = CheckNode
                while True:
                    if self.board[node.current.x][node.current.y] == "" or self.board[node.current.x][node.current.y] == "X":
                        NewMapRow = self.board[node.current.x]
                        NewMapRow[node.current.y] = str("*")
                        self.board[node.current.x] = NewMapRow
                        self.Path.append("{0}, {1}".format(node.current.x, node.current.y))

                    node = node.Previous
                    if node == None:
                        self.Found = self.board
                        self.drawBoard()
                        return True
                        
                break


            self.VisitedNodes.append(CheckNode)
            self.OpenNodes.remove(CheckNode)

            self._DrawRunningBoard()

            NextNodes = self._GetNeighbourNodes(CheckNode)

            for nextNode in NextNodes:
                if self._CheckOpenForNode(nextNode, self.VisitedNodes):
                    continue

                elif self._CheckOpenForNode(nextNode, self.OpenNodes):
                    
                    ExistingNode = self._CheckOpenForNode(nextNode,self.OpenNodes, True)

                    if ExistingNode.DistanceScore > CheckNode.DistanceScore:
                        self.OpenNodes.remove(ExistingNode)
                        self.VisitedNodes.append(nextNode)
                
                else:
                    self.OpenNodes.append(nextNode)
            
        print("No Path Found")

    def _CheckOpenForNode(self, Node, NodeList, GetNode = False):
        for node in NodeList:
            if node.current.x == Node.current.x and node.current.y == Node.current.y:
                if GetNode:
                    return node
                else:
                    return True
        
        return False


    def _GetNeighbourNodes(self, CurrentNode):

        NewNodes = []
        NewNodes.append( Node(CurrentNode.current.x, CurrentNode.current.y - 1, CurrentNode) )
        NewNodes.append( Node(CurrentNode.current.x, CurrentNode.current.y + 1, CurrentNode) )
        NewNodes.append( Node(CurrentNode.current.x - 1, CurrentNode.current.y, CurrentNode) )
        NewNodes.append( Node(CurrentNode.current.x + 1, CurrentNode.current.y, CurrentNode) )

        for node in NewNodes:
            node.SetDistance(self.goal)

        ValidNodes = []

        for node in NewNodes:
            if node.current.x >= 0 and node.current.x < ROWS and node.current.y >=0 and node.current.y < COLS:
                if self.board[node.current.x][node.current.y] == "" or self.board[node.current.x][node.current.y] == "B":
                    ValidNodes.append(node)
        
        return ValidNodes

    def _ReturnListSort(self, e):
        return e.DistanceScore

    def _OrderNodeList(self, returnFirst = False):
        SortedNodes = self.OpenNodes
        SortedNodes.sort(key=self._ReturnListSort)
        '''
        for node in self.OpenNodes: #Takes node from OpenNodes
            if SortedNodes == []:   # Checks if sortedNodes is empty
                SortedNodes.append(node) #Adds node if empty
            else:
                for x in range(len(SortedNodes)): # For every Node in SortedNodes
                    if SortedNodes[x].DistanceScore > node.DistanceScore:  #Is the distance score of the node in sorted more the nour node
                        SortedNodes.insert(x, node) #if yes plac eour node where is was and push that one one up
                    elif x == len(SortedNodes)-1: #else if there at the last item in the list
                        SortedNodes.append(node) #Just add the node at the end
        '''
        
        if returnFirst:
            return SortedNodes[0]
        else:
            return SortedNodes


