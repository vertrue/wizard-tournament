from logs import logger
from random import sample

from config import random_wizard_names


class Player:
    def __init__(self, name: str, order: int) -> None:
        self.hp = 5
        self.name = name
        self.order = order

        self.wand = None
        self.dice = None
        self.skip = False

    def pick_wand(self, wand):
        self.wand = wand

    def pick_dice(self, dice: int):
        self.dice = dice

    def damage(self, hits: int):
        self.hp -= hits
        if self.is_dead:
            logger.info(f"Player {self.name} is dead!")
        else:
            logger.info(f"Player {self.name} left with {self.hp} hp!")

    def heal(self, hits):
        self.hp += hits
        if self.hp > 5:
            self.hp = 5
        logger.info(f"Player {self.name} is healed by {hits} and left with {self.hp} hp!")

    def kill(self):
        self.hp = 0
        logger.info(f"Player {self.name} is dead!")

    def brake_wand(self):
        self.wand.is_broken = True

    def skip_next_turn(self):
        self.skip = True

    def cast(self, target, others):
        if self.is_dead:
            logger.info(f"Player {self.name} is dead and cannot cast!")
            return
        if self.skip:
            logger.info(f"Player {self.name} is flozen!")
            self.skip = False
            return
        if self.wand.is_broken:
            logger.info(f"{self.name}'s wand is broken and player cannot cast!")
            return
        logger.info(f"Player {self.name} is casting with {self.wand.name} and d{self.dice}!")
        self.wand.cast(dice=self.dice, source=self, target=target, others=others)

    def reset_hp(self):
        self.hp = 5

    @property
    def is_dead(self):
        if self.hp <= 0:
            return True
        else:
            return False


def generate_players(number_of_players: int):
    return sample(random_wizard_names, number_of_players)
