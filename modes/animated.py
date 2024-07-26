from game import AnimatedGame
from player import generate_players


def animated_simulation():
    game = AnimatedGame(players=generate_players(number_of_players=4))
    game.pick_wands()
    game.pick_dices()

    game.simulate()
