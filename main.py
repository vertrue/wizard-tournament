from Game import Game


# full random simulation
# make sure to comment line 8 in logs.py

num_of_game = 10000

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




# single random logged play
# uncomment these and line 8 in logs.py

# num_of_game = 1

# game = Game(
#     players=[
#         "Yevhen",
#         "Nastya",
#         "Shasha",
#         "Maxik"
#     ]
# )
# game.pick_wands()
# game.pick_dices()

# game.simulate(repeats=num_of_game)