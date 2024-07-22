from game import Game


def single_simulation():
    num_of_game = 1

    game = Game(players=["Yevhen", "Nastya", "Shasha", "Maxik"])
    game.pick_wands()
    game.pick_dices()

    game.simulate(repeats=num_of_game)
