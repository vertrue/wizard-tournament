from wands.Wand import Wand
from player import Player

from logs import logger

from typing import List


class ButterflyWand(Wand):
    def __init__(self) -> None:
        super().__init__(
            success=self.success,
            failure=self.failure,
            critical_success=self.critical_success,
            critical_failure=self.critical_failure,
        )
        self.name = "ButterflyWand"

    def success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info("Butterflies...")

    def failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info("Butterflies...")

    def critical_success(
        self, roll_result: int, source: Player, target: Player, others: List[Player]
    ):
        logger.info("Butterflies...")

    def critical_failure(
        self, roll_result: int, source: Player, target: Player, others: List[Player]
    ):
        logger.info("Butterflies...")
