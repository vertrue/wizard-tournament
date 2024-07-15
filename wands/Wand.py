from players.Player import Player

from random import randint
from typing import List
from copy import copy

from logs import logger

class Wand():
    def __init__(self, success, failure, critical_success, critical_failure) -> None:
        self.success = success
        self.failure = failure
        self.critical_success = critical_success
        self.critical_failure = critical_failure

        self.is_broken = False

    def cast_results(self, dice: int, roll_result: int, *args):
        if roll_result == 1:
            self.critical_failure(roll_result, *args)
        elif roll_result == dice:
            self.critical_success(roll_result, *args)
        elif 2 <= roll_result <= 5:
            self.success(roll_result, *args)
        else:
            self.failure(roll_result, *args)

    def cast(self, dice: int, source: Player, target: Player, others: List[Player]):
        roll_result = self.roll(dice)
        self.cast_results(dice, roll_result, source, target, others)
        
    def roll(self, dice: int):
        roll_result = randint(1, dice)
        logger.info(f"Roll result: {roll_result}")
        return roll_result
    
    def damage_group(self, value, players: List[Player]):
        for player in players:
            if not player.is_dead:
                player.damage(value)

    def heal_group(self, value, players: List[Player]):
        for player in players:
            if not player.is_dead:
                player.heal(value)

    def kill_group(self, players: List[Player]):
        for player in players:
            if not player.is_dead:
                player.kill()

    def freeze_group(self, value, players: List[Player]):
        for player in players:
            if not player.is_dead:
                player.skip_next_turn()

    def switch_wands(self, players: List[Player]):
        def sort_key(el: Player):
            return el.order
        players.sort(key=sort_key)

        alive_players = []
        for player in players:
            if not player.is_dead:
                alive_players.append(player)
                logger.info(player.name)

        last_wand = copy(alive_players[-1].wand)
        for i in range(len(alive_players) - 1, 0, -1):
            alive_players[i].wand = copy(alive_players[i - 1].wand)
        alive_players[0].wand = last_wand
