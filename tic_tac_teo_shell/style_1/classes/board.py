import numpy as np
from .constants import *

class Board:
    def __init__(self):
        self.board=np.zeros((3,3)).astype(int)

    def number_to_position(self,n)->tuple:
        return divmod(n,3)

    def add_symbole_to_position(self,symbole,position)->None:
        i,j=self.number_to_position(position)
        self.board[i,j]=symbole

    def is_this_a_winner(self,i,j,k)->bool:
        #checks if there is a winner at the position (i,j,k)
        i=self.number_to_position(i)
        j=self.number_to_position(j)
        k=self.number_to_position(k)
        return self.board[i]==self.board[j]==self.board[k]!=0

    def is_here_a_winner(self)->tuple:
        #(True, posWinner, the_winner) if there is a winner else : (False, None, None)
        
        #vertical checking
        l=[ (0,3,6),
            (1,4,7),
            (2,5,8)]
        for pos in l:
            if self.is_this_a_winner(*pos):
                return True, pos, self.board[self.number_to_position(pos[0])]

        #horizantal checking
        l=[ (0,1,2),
            (3,4,5),
            (6,7,8)]
        for pos in l:
            if self.is_this_a_winner(*pos):
                return True, pos, self.board[self.number_to_position(pos[0])]

        #oblique checking
        l=[ (0,4,8),
            (2,4,6)]
        for pos in l:
            if self.is_this_a_winner(*pos):
                return True, pos, self.board[self.number_to_position(pos[0])]

        #No winner yet
        return False, None, None

    def print_board(self)->None:
        #print the board with indexes in the empty boxes and x or o in the full boxes
        for count1,l in enumerate(self.board):
            print(end="\n\t  ")
            for count2,sym in enumerate(l):
                if not sym:
                    sym= 3*count1+count2
                else:
                    sym=PLAYER_TO_SYMBOLE[sym]

                print(sym,end=(' | ' if count2!=2 else '') )
            print(end=('\n\t-------------' if count1!=2 else ''))

    def empty_boxes(self)->list:
        #return a list of indexes of the empty boxes
        l=[]
        for i in range(9):
            if not self.board[self.number_to_position(i)]:
                l.append(i)
        return l
