from wands.Wand import Wand
from player import Player

from logs import logger

from typing import List

class FireBallWand(Wand):
    def __init__(self) -> None:
        super().__init__(
            success=self.success,
            failure=self.failure,
            critical_success=self.critical_success,
            critical_failure=self.critical_failure,
        )
        self.name = "FireBallWand"

    def success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Damaging all...")
        target.damage(roll_result)
        self.damage_group(
            value=1,
            players=others+[source]
        )

    def failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Damaging all...")
        self.damage_group(
            value=3,
            players=others+[source, target]
        )

    def critical_success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Damaging {target.name}...")
        source.damage(1)
        self.damage_group(
            value=4,
            players=others+[target]
        )

    def critical_failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Damaging all...")
        source.damage(4)
        self.damage_group(
            value=1,
            players=others+[target]
        )