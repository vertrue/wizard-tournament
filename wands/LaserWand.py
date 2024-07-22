from wands.Wand import Wand
from player import Player

from logs import logger

from typing import List

class LaserWand(Wand):
    def __init__(self) -> None:
        super().__init__(
            success=self.success,
            failure=self.failure,
            critical_success=self.critical_success,
            critical_failure=self.critical_failure,
        )
        self.name = "LaserWand"

    def success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Damaging {target.name}...")
        target.damage(roll_result)

    def failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Nothing happend to {target.name}...")

    def critical_success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Damaging {target.name}...")
        target.kill()

    def critical_failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Damaging {source.name}...")
        source.kill()