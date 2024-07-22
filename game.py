from player import Player
from logs import logger

import wands

from random import shuffle, randint
from typing import List


class Game:
    def __init__(self, players: List[str]) -> None:
        self.players: List[Player] = []

        for i in range(len(players)):
            self.players.append(Player(name=players[i], order=(i + 1)))

        self.total_players = len(self.players)

        self.all_wands = wands.all_wands
        self.dices = wands.dices

    def pick_wands(self):
        for player in self.players:
            shuffle(self.all_wands)
            player.pick_wand(self.all_wands.pop()())

    def pick_dices(self):
        for player in self.players:
            shuffle(self.dices)
            player.pick_dice(self.dices.pop())

    def simulate(self, repeats: int):
        winners = []

        for _ in range(repeats):
            turns = 0
            last_turn_hp = []

            while not self.is_only_one_alive:
                if turns % self.total_players == 0:
                    # TODO: fix
                    if last_turn_hp == self.players_hp:
                        break
                    last_turn_hp = self.players_hp
                    logger.info(f"-------------ROUND {turns // self.total_players + 1}-----------")

                source_player = self.players[turns % self.total_players]
                target_player = source_player
                while target_player == source_player or target_player.is_dead:
                    target_player = self.players[randint(1, self.total_players) - 1]

                other_players = []
                for player in self.players:
                    if player not in [source_player, target_player]:
                        other_players += [player]

                source_player.cast(target=target_player, others=other_players)
                logger.info("\n")
                turns += 1

            winner = self.check_if_winner

            logger.info(f"Game is finished. Winner is {winner}")
            winners += [winner]

            for player in self.players:
                player.reset_hp()

        for player in self.players:
            player_configs = f"{player.name}:{player.wand.name}:{player.dice}"
            player_percent = winners.count(player.name) / repeats * 100
            player_results = f"{winners.count(player.name)} ({player_percent}%)"
            print(f"{player_configs} = {player_results}")

    @property
    def players_hp(self) -> List[int]:
        hps = []
        for player in self.players:
            hps += [player.hp]
        return hps

    @property
    def is_only_one_alive(self):
        winners = []
        for player in self.players:
            if not player.is_dead:
                winners.append(player)

        if len(winners) == 1:
            return True
        elif len(winners) > 1:
            return False
        else:
            return True

    @property
    def check_if_winner(self):
        winners = []
        for player in self.players:
            if not player.is_dead:
                winners.append(player)

        if len(winners) == 1:
            return winners[0].name
        else:
            max_dice = 0
            winner = None
            for player in self.players:
                if player.dice > max_dice:
                    max_dice = player.dice
                    winner = player.name

            return winner
