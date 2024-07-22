from Game import Game

def multi_simulation(num_of_game: int):

    game = Game(
        players=[
            "Yevhen",
            "Nastya",
            "Shasha",
            "Maxik"
        ]
    )
    game.pick_wands()
    game.pick_dices()

    game.simulate(repeats=num_of_game)