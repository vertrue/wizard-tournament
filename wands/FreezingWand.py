from wands.Wand import Wand
from player import Player

from logs import logger

from typing import List


class FreezingWand(Wand):
    def __init__(self) -> None:
        super().__init__(
            success=self.success,
            failure=self.failure,
            critical_success=self.critical_success,
            critical_failure=self.critical_failure,
        )
        self.name = "FreezingWand"

    def success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Freezing and damaging {target.name}...")
        target.skip_next_turn()
        target.damage(1)

    def failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Nothing happend to {target.name}...")

    def critical_success(
        self, roll_result: int, source: Player, target: Player, others: List[Player]
    ):
        logger.info(f"Freezing and damaging all except {source.name}...")
        self.freeze_group(value=1, players=others + [target])
        self.damage_group(value=1, players=others + [target])

    def critical_failure(
        self, roll_result: int, source: Player, target: Player, others: List[Player]
    ):
        logger.info(f"Freezing {source.name}...")
        source.skip_next_turn()
