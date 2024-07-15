from wands.Wand import Wand
from players.Player import Player

from logs import logger

from typing import List

class GlassWand(Wand):
    def __init__(self) -> None:
        super().__init__(
            success=self.success,
            failure=self.failure,
            critical_success=self.critical_success,
            critical_failure=self.critical_failure,
        )
        self.name = "GlassWand"

    def success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Breaking {target.name}'s wand...")
        target.brake_wand()

    def failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Switching wands...")
        self.switch_wands(players=others+[target, source])

    def critical_success(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Breaking {source.name}'s wand...")
        source.brake_wand()   

    def critical_failure(self, roll_result: int, source: Player, target: Player, others: List[Player]):
        logger.info(f"Breaking {source.name}'s wand...")
        source.brake_wand()