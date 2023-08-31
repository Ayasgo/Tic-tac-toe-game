from .board import Board
from .constants import *
from copy import deepcopy
from math import inf

class Robot:
    def __init__(self,player):
        self.robot_symbole=player
        self.player_symbole= 1+ player%2

    def actions(self,state)->list:
        #return legal moves in state s
        return state.empty_boxes()

    def result(self,state: Board, symbole, action)->Board:
        #return state after action a taken in state s
        new_state=deepcopy(state)
        new_state.add_symbole_to_position(symbole,action)
        return new_state

    def terminal(self,state:Board)->bool:
        #checks if state is terminal
        return state.is_here_a_winner()[0] or not len(state.empty_boxes())

    def utility(self,state:Board)->int:
        #final numerical value for terminal state
        is_here_a_winner, _, winner= state.is_here_a_winner()
        if is_here_a_winner:
            return 1 if winner==self.robot_symbole else -1
        return 0

    def max_value(self,state)->tuple:
        if self.terminal(state):
            return self.utility(state),None
        v=-inf
        best_move=None
        for action in self.actions(state):
            m=self.min_value(self.result(state, self.robot_symbole, action))[0]
            if v<m:
                v=m
                best_move=action
        return v,best_move

    def min_value(self,state)->tuple:
        if self.terminal(state):
            return self.utility(state),None
        v=inf
        best_move=None
        for action in self.actions(state):
            m=self.max_value(self.result(state, self.player_symbole, action))[0]
            if v>m:
                v=m
                best_move=action
        return v,best_move
    
    def get_the_best_move_value(self,state:Board)->tuple:
        return reversed(self.max_value(state))
