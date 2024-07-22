from wands.Wand import Wand
from player import Player

from logs import logger

from typing import List

class MorphWand(Wand):
    def __init__(self) -> None:
        super().__init__(
            success=self.success,
            failure=self.failure,
            critical_success=self.critical_success,
            critical_failure=self.critical_failure,
        )
        self.name = "MorphWand"

    def success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Morphing {target.name}...")
        target.kill()

    def failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Nothing happend...")

    def critical_success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Damaging all...")
        self.kill_group(
            players=others+[source, target]
        )

    def critical_failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Damaging all...")
        self.kill_group(
            players=others+[source, target]
        )