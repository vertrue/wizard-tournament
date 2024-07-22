from game import Game
from player import generate_players


def single_simulation():
    num_of_game = 1

    game = Game(players=generate_players(number_of_players=4))
    game.pick_wands()
    game.pick_dices()

    game.simulate(repeats=num_of_game)
