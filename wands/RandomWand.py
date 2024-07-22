import wands
from player import Player

from random import choice

from logs import logger

from typing import List

class RandomWand(wands.Wand.Wand):
    def __init__(self) -> None:
        super().__init__(
            success=self.success,
            failure=self.failure,
            critical_success=self.critical_success,
            critical_failure=self.critical_failure,
        )
        self.name = "RandomWand"

    def success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        random_wand = choice(wands.possible_wands)
        while random_wand == RandomWand:
            random_wand = choice(wands.possible_wands)
        random_wand = random_wand()
        logger.info(f"Casting {random_wand.name} instead!")
        random_wand.success(roll_result, source, target, others)

    def failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        random_wand = choice(wands.possible_wands)
        while random_wand == RandomWand:
            random_wand = choice(wands.possible_wands)
        random_wand = random_wand()
        logger.info(f"Casting {random_wand.name} instead!")
        random_wand.failure(roll_result, source, target, others)

    def critical_success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        random_wand = choice(wands.possible_wands)
        while random_wand == RandomWand:
            random_wand = choice(wands.possible_wands)
        random_wand = random_wand()
        logger.info(f"Casting {random_wand.name} instead!")
        random_wand.critical_success(roll_result, source, target, others)

    def critical_failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        random_wand = choice(wands.possible_wands)
        while random_wand == RandomWand:
            random_wand = choice(wands.possible_wands)
        random_wand = random_wand()
        logger.info(f"Casting {random_wand.name} instead!")
        random_wand.critical_failure(roll_result, source, target, others)