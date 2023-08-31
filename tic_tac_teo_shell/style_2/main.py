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
    printed_symbols = {
            BOT : 'X',
            PLAYER : 'O',
        }

class TicTacToeGame:
    def __init__(self):
        self.minimax = Minimax()
        self.board = self.minimax.S0.copy()
        
    def display_board(self):
        for i in range(0,9,3):
            print(' | '.join( [ Symbols.printed_symbols.get(n) or str(i+j+1) for j,n in enumerate(self.board[i : i+3]) ] ))
            if i<6:
                print('-' * 9)
        print()

    def is_valid_move(self, position):
        return position in self.minimax.actions(self.board)
    
    def make_move(self, position, player):
        # Check if the position is valid
        if not self.is_valid_move(position):
            raise ValueError("Invalid position !")
        
        # Check if the player is valid
        if not player in Symbols.PLAYERS :
            raise ValueError("Invalid player")
        
        self.board[position] = player
    
    def play_game(self):
        while True:
            # Check if the state is terminal
            if self.minimax.terminal(self.board):
                break
            #self.display_board()
            current_player = self.minimax.player(self.board)
            if current_player == Symbols.PLAYER:
                position = int(input('Enter you move (1-9): ')) - 1
                if self.is_valid_move(position):
                    self.make_move(position, Symbols.PLAYER)
                    self.display_board()
                else:
                    print("Invalid move, try again!")
                    continue
            else:
                best_move = self.minimax.best_move(self.board)
                self.make_move( best_move, Symbols.BOT )
                self.display_board()
        
        score = self.minimax.utility(self.board)
        if score == 1:
            print("The bot wins!")
        elif score == -1:
            print("The player wins!")
        else :
            print("It's a tie!")


class Minimax:
    def __init__(self):
        self.S0 = np.full(9, Symbols.EMPTY, dtype= int)
        self.start_the_game = False

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
        winning_combinations = (
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
        for cmb in winning_combinations:
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
            print(f"The bot choices the position {best_move + 1} as a random move !")
        else:
            _, best_move = self.max_value(state)
            print(f"The bot choices the position {best_move + 1} as the best move !")

        return best_move

if __name__ == "__main__":	
    game = TicTacToeGame()
    game.play_game()