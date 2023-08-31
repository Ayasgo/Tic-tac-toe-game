import numpy as np
import random
# Bot : the maximizer --> the evaluate function must return 1 if the bot win
# Player : the minimizer --> the evaluate function must return -1 if the player win
# Tie : the evaluate function must return 0
class Symbols:
    EMPTY = 0
    BOT = 1
    PLAYER = 2
    PLAYERS = BOT, PLAYER

class TicTacToeGame:
    def __init__(self, board):
        self.minimax = Minimax()
        self.board = np.array(board, dtype=int)

    def is_valid_move(self, position):
        return position in self.minimax.actions(self.board)
    
    def make_player_move(self, position):        
        self.board[position] = Symbols.PLAYER

    def make_bot_move(self):
        best_move = self.minimax.best_move(self.board)
        self.board[best_move] = Symbols.BOT
        
    def make_player_move__isTerminal(self, position):
        self.make_player_move(position)
        return self.is_terminal()
    
    def make_bot_move__isTerminal(self):
        self.make_bot_move()
        return self.is_terminal()

    def is_terminal(self):
        return self.minimax.terminal(self.board)
    
    def get_winner(self):
        score = self.minimax.utility(self.board)
        if score == 1:
            return 'bot'
        elif score == -1:
            return 'player'
        else :
            return 'tie'
        
    def get_winning_combination(self):
        for cmb in self.minimax.winning_combinations:
            if all(self.board[ list(cmb) ] == Symbols.BOT) or (self.board[ list(cmb) ] == Symbols.PLAYER ).all():
                return cmb
        return None


class Minimax:
    def __init__(self):
        self.S0 = np.full(9, Symbols.EMPTY, dtype= int)
        self.start_the_game = False

        self.winning_combinations = (
            # Rows
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            # Columns
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            # Diagonals
            (0, 4, 8),
            (2, 4, 6),
        )

    def player(self, s:np.full):
        # Return which player to move in state s
        bot_moves = np.count_nonzero(s == Symbols.BOT)
        player_moves = np.count_nonzero(s == Symbols.PLAYER)
        if bot_moves > player_moves :
            return Symbols.PLAYER
        elif bot_moves < player_moves: 
            return Symbols.BOT
        else :
            return Symbols.BOT if self.start_the_game else Symbols.PLAYER

    def actions(self, s):
        # Return legale moves in state s
        return [ i for i in range(9) if s[i] == Symbols.EMPTY]

    def result(self, s, a):
        # Return state after action a taken in state s
        current_player = self.player(s)
        new_s = s.copy()
        new_s[a] = current_player
        return new_s

    def utility(self, s):
        # Return final numerical value for terminal state
        
        for cmb in self.winning_combinations:
            if all(s[ list(cmb) ] == Symbols.BOT):
                # The bot wins
                return 1
            elif (s[ list(cmb) ] == Symbols.PLAYER ).all():
                # The player wins
                return -1
        
        # Tie
        return 0

    def terminal(self, s):
        # Checks if state s is a terminal state
        return Symbols.EMPTY not in s or self.utility(s) != 0

    def max_value(self, state):
        if self.terminal(state):
            return self.utility(state), None
        v = -float('inf')
        best_move = None
        for action in self.actions(state):
            new_v = self.min_value(self.result(state, action))[0]
            if new_v > v:
                best_move = action
                v = new_v

        return v, best_move
    
    def min_value(self, state):
        if self.terminal(state):
            return self.utility(state), None
        v = float('inf')
        best_move = None
        for action in self.actions(state):
            new_v = self.max_value(self.result(state, action))[0]
            if new_v < v:
                best_move = action
                v = new_v
        return v, best_move
    
    def best_move(self, state):
        # Find the best move for the current state
        if np.array_equal(state, self.S0) :
            best_move = random.randrange(9)
        else:
            _, best_move = self.max_value(state)

        return best_move