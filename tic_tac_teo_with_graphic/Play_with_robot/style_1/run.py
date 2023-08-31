from flask import Flask, render_template, request, jsonify
from json import load
from random import randrange
import bot
app = Flask(__name__)

def get_context(board, player_move):
    # is_terminal : boolean
    # winner : bot| player| tie | (None if not terminal)
    context = {
        'is_terminal' : False,
        'winner' : None,
        'winning_combination' : None,
        'new_board' : None,
    }
    xo_game = bot.TicTacToeGame(board)
    if xo_game.is_terminal():
        context['is_terminal'] = True
        context['winner'] = xo_game.get_winner()
        context['winning_combination'] = xo_game.get_winning_combination()

    elif xo_game.is_valid_move(player_move):
        # make the player's move then bot's move and check if it is terminal
        if xo_game.make_player_move__isTerminal(player_move) or xo_game.make_bot_move__isTerminal():
            context['is_terminal'] = True
            context['winner'] = xo_game.get_winner()
            context['winning_combination'] = xo_game.get_winning_combination()
    
    context['new_board'] = xo_game.board.tolist()
    return context

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player_move = int(request.json.get('player_move'))
        board = request.json.get('board')
        #return jsonify(dict())
        return get_context(board, player_move)
    
    with open("static/colors.json", 'r') as json_file:
        colors = load(json_file)
    color_index = randrange(len(colors['box_bg']))
    context = { key:value[color_index] for key, value in colors.items() }

    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(debug=True)