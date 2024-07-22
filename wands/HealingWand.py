from wands.Wand import Wand
from player import Player

from logs import logger

from typing import List

class HealingWand(Wand):
    def __init__(self) -> None:
        super().__init__(
            success=self.success,
            failure=self.failure,
            critical_success=self.critical_success,
            critical_failure=self.critical_failure,
        )
        self.name = "HealingWand"

    def success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Healing {target.name}...")
        target.heal(roll_result)

    def failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Nothing happend to {target.name}...")

    def critical_success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Healing {target.name}...")
        target.heal(5)

    def critical_failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Healing all...")
        self.heal_group(
            value=1,
            players=[source, target]+others
        )