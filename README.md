# Wizard Tournament Game

## Game Rules

For detailed game rules, please refer to the [rules/README.md](rules/README.md) file.


## Roadmap

- [x] game rules
- [x] wands description
- [x] generate players
- [ ] pick wands for the generation
- [ ] visual simulation for a round
- [ ] statistic for the simulation
- [ ] `n` numbers of the rounds
- [ ] config base of the wands
- [ ] balance wands
- [ ] wizards types
- [ ] multiplayer in window
- [ ] API
- [ ] browser multiplayer
- [ ] AI for wizards

## How to run the simulation

Simulation is available in 2 modes:
- *single*: creates 4 players with random wands and simulates it
- *multi*: creates 4 players with random wands and simulates it `x` times

To run simulations use the following command:
- `python3 main.py animated` for single round animation
- `python3 main.py single` for single round text-only 
- `python3 main.py multi x` where x is the number of simulated games.