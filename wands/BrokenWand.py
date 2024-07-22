from wands.Wand import Wand
from player import Player

from logs import logger

from typing import List


class BrokenWand(Wand):
    def __init__(self) -> None:
        super().__init__(
            success=self.success,
            failure=self.failure,
            critical_success=self.critical_success,
            critical_failure=self.critical_failure,
        )
        self.name = "BrokenWand"

    def success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Nothing happened with {target.name}...")

    def failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Damaging {target.name}...")
        target.damage(1)

    def critical_success(
        self, roll_result: int, source: Player, target: Player, others: List[Player]
    ):
        logger.info(f"Killing {source.name}...")
        source.kill()

    def critical_failure(
        self, roll_result: int, source: Player, target: Player, others: List[Player]
    ):
        logger.info(f"Killing {target.name}...")
        target.kill()
