from player import Player
from player import AnimatedPlayer
from logs import logger

import wands

import pygame
import math
import random
from random import shuffle, randint
from typing import List
from prettytable import PrettyTable


class Game:
    def __init__(self, players: List[str]) -> None:
        self.players: List[Player] = []

        for i in range(len(players)):
            self.players.append(Player(name=players[i], order=(i + 1)))

        self.total_players = len(self.players)

        self.all_wands = wands.all_wands
        self.dices = wands.dices

    def pick_wands(self):
        for player in self.players:
            shuffle(self.all_wands)
            player.pick_wand(self.all_wands.pop()())

    def pick_dices(self):
        for player in self.players:
            shuffle(self.dices)
            player.pick_dice(self.dices.pop())

    def simulate(self, repeats: int):
        winners = []

        for _ in range(repeats):
            turns = 0
            last_turn_hp = []

            while not self.is_only_one_alive:
                if turns % self.total_players == 0:
                    # TODO: fix
                    if last_turn_hp == self.players_hp:
                        break
                    last_turn_hp = self.players_hp
                    logger.info(f"-------------ROUND {turns // self.total_players + 1}-----------")

                source_player = self.players[turns % self.total_players]
                target_player = source_player
                while target_player == source_player or target_player.is_dead:
                    target_player = self.players[randint(1, self.total_players) - 1]

                other_players = []
                for player in self.players:
                    if player not in [source_player, target_player]:
                        other_players += [player]

                source_player.cast(target=target_player, others=other_players)
                logger.info("\n")
                turns += 1

            winner = self.check_if_winner

            logger.info(f"Game is finished. Winner is {winner}")
            winners += [winner]

            for player in self.players:
                player.reset_hp()

        self.output_game_results(winners=winners, repeats=repeats)

    def output_game_results(self, winners, repeats: int):
        table = PrettyTable(["name", "wand", "dice", "won", "winrate"])
        for player in self.players:
            table.add_row(
                [
                    player.name,
                    player.wand.name,
                    f"d{player.dice}",
                    f"{winners.count(player.name)}",
                    f"{winners.count(player.name) / repeats * 100}%",
                ]
            )
        logger.info(table)

    @property
    def players_hp(self) -> List[int]:
        hps = []
        for player in self.players:
            hps += [player.hp]
        return hps

    @property
    def is_only_one_alive(self):
        winners = []
        for player in self.players:
            if not player.is_dead:
                winners.append(player)

        if len(winners) == 1:
            return True
        elif len(winners) > 1:
            return False
        else:
            return True

    @property
    def check_if_winner(self):
        winners = []
        for player in self.players:
            if not player.is_dead:
                winners.append(player)

        if len(winners) == 1:
            return winners[0].name
        else:
            max_dice = 0
            winner = None
            for player in self.players:
                if player.dice > max_dice:
                    max_dice = player.dice
                    winner = player.name

            return winner


class AnimatedGame(Game):
    def __init__(self, players: List[str]) -> None:
        pygame.init()
        self.scale = 1.3
        self.screen = pygame.display.set_mode((1000, 1000))
        self.clock = pygame.time.Clock()
        self.center = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.font = pygame.font.SysFont(None, int(16 * self.scale))
        self.large_font = pygame.font.SysFont(None, int(24 * self.scale))
        self.players_radius = (
            min(self.screen.get_width(), self.screen.get_height()) * 0.3 * self.scale
        )

        self.players: List[AnimatedPlayer] = []

        for i in range(len(players)):
            self.players.append(AnimatedPlayer(name=players[i], order=(i + 1)))

        for player in self.players:
            player.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.total_players = len(self.players)

        self.all_wands = wands.all_wands
        self.dices = wands.dices

        self.current_player = None
        self.target_player = None

    def draw_players(self, star=True):
        radius = min(self.screen.get_width(), self.screen.get_height()) * 0.25
        angle_step = 2 * math.pi / len(self.players)

        # positions
        for i, player in enumerate(self.players):
            angle = i * angle_step

            player.position = (
                int(self.center.x + radius * math.cos(angle)),
                int(self.center.y + radius * math.sin(angle)),
            )
            player.wand_position = (
                int(self.center.x + radius * math.cos(angle)) + 30 * self.scale,
                int(self.center.y + radius * math.sin(angle)),
            )

        for i, player in enumerate(self.players):
            mage_image = pygame.image.load("media/mage.png").convert_alpha()
            if player.is_dead:
                mage_image = pygame.transform.grayscale(mage_image)
            mage_image = pygame.transform.scale(mage_image, (60 * self.scale, 60 * self.scale))
            self.screen.blit(mage_image, mage_image.get_rect(center=player.position))

            if self.current_player == player and star:
                star = pygame.image.load("media/star.png").convert_alpha()
                star = pygame.transform.scale(star, (15 * self.scale, 15 * self.scale))
                self.screen.blit(
                    star,
                    star.get_rect(
                        center=(
                            player.position[0] - 25 * self.scale,
                            player.position[1] - 20 * self.scale,
                        )
                    ),
                )

        for i, player in enumerate(self.players):
            wand_image = pygame.image.load("media/wand.png").convert_alpha()
            wand_image = pygame.transform.scale(wand_image, (20 * self.scale, 20 * self.scale))
            self.screen.blit(wand_image, wand_image.get_rect(center=player.wand_position))

            # pygame.draw.circle(self.screen, player.color, player.wand_position, 10)
            wand_text = self.font.render(
                f"d{self.players[i].dice} {player.wand.name}", True, (0, 0, 0)
            )
            wand_text.get_rect
            self.screen.blit(
                wand_text,
                wand_text.get_rect(
                    center=(player.position[0], player.position[1] - 43 * self.scale)
                ),
            )

        self.draw_health()

    def draw_health(self):
        for player in self.players:
            heart_positions = [
                (
                    player.position[0] - 15 * i * self.scale + 30 * self.scale,
                    player.position[1] + 40 * self.scale,
                )
                for i in range(5)
            ]

            full_hp = 5
            player_hp = max(0, player.hp)
            pos_ind = 0

            for i in range(player_hp, full_hp):
                broken_image = pygame.image.load("media/empty_heart.jpg").convert_alpha()
                broken_image = pygame.transform.scale(
                    broken_image, (15 * self.scale, 15 * self.scale)
                )
                self.screen.blit(
                    broken_image, broken_image.get_rect(center=heart_positions[pos_ind])
                )
                pos_ind += 1

            for i in range(player_hp):
                heart_image = pygame.image.load("media/full_heart.jpg").convert_alpha()
                heart_image = pygame.transform.scale(
                    heart_image, (15 * self.scale, 15 * self.scale)
                )
                self.screen.blit(heart_image, heart_image.get_rect(center=heart_positions[pos_ind]))
                pos_ind += 1

    def move_towards(self, source, target, speed):
        src_x, src_y = source
        tgt_x, tgt_y = target

        vector_x, vector_y = tgt_x - src_x, tgt_y - src_y

        distance = math.hypot(vector_x, vector_y)

        if distance < speed:
            return target

        direction_x, direction_y = vector_x / distance, vector_y / distance

        new_x = src_x + direction_x * speed
        new_y = src_y + direction_y * speed

        return (new_x, new_y)

    def move_around_circle(self, current_pos, center, radius, speed, angle_step):
        current_x, current_y = current_pos
        center_x, center_y = center

        # Calculate the angle between current position and center
        angle = math.atan2(current_y - center_y, current_x - center_x)

        # Increase the angle by the angle step to simulate movement
        angle += speed * angle_step

        # Calculate the new position on the circle
        new_x = center_x + radius * math.cos(angle)
        new_y = center_y + radius * math.sin(angle)

        return (new_x, new_y)

    def damage(self, source: AnimatedPlayer, targets: List[AnimatedPlayer]):
        speed = 10
        proj_positions = []
        proj_target = []

        for _ in targets:
            proj_positions += [source.wand_position]

        for target in targets:
            proj_target += [target.position]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            for i in range(len(proj_positions)):
                proj_positions[i] = self.move_towards(proj_positions[i], proj_target[i], speed)

            if all(proj_positions[i] == proj_target[i] for i in range(len(proj_positions))):
                break

            for i in range(len(proj_positions)):
                if proj_positions[i] == proj_target[i]:
                    proj_positions[i] = (-1000, -1000)
                    proj_target[i] = (-1000, -1000)

            self.screen.fill((255, 255, 255))
            self.draw_players()

            for pos in proj_positions:
                pygame.draw.circle(
                    self.screen, (0, 0, 0), (int(pos[0]), int(pos[1])), 5 * self.scale
                )

            pygame.display.flip()
            self.clock.tick(60)

    def game_results(self, winner: str):
        self.screen.fill((255, 255, 255))
        winner_text = self.large_font.render(
            f"Winner: {winner.name} with {winner.wand.name}", True, (0, 0, 0)
        )
        self.screen.blit(winner_text, (20, 20))
        self.draw_players()

    def simulate(self, repeats: int = 1):
        winners = []

        for _ in range(repeats):
            turns = 0
            last_turn_hp = []
            last_round_hp = []

            while not self.is_only_one_alive:

                if turns % self.total_players == 0:
                    if last_round_hp == self.players_hp:
                        break
                    last_round_hp = self.players_hp
                    logger.info(f"-------------ROUND {turns // self.total_players + 1}-----------")

                last_turn_hp = self.players_hp

                self.current_player = self.players[turns % self.total_players]
                if self.current_player.is_dead:
                    turns += 1
                    continue

                pygame.time.delay(500)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                target_player = self.current_player
                while target_player == self.current_player or target_player.is_dead:
                    target_player = self.players[random.randint(1, self.total_players) - 1]

                self.target_player = target_player

                self.screen.fill((255, 255, 255))
                self.draw_players()
                pygame.display.flip()
                pygame.time.delay(500)

                other_players = []
                for player in self.players:
                    if player not in [self.current_player, self.target_player]:
                        other_players += [player]

                self.current_player.cast(target=self.target_player, others=other_players)
                logger.info("\n")

                damage_targets = []
                for i in range(len(self.players_hp)):
                    if self.players_hp[i] != last_turn_hp[i] and last_turn_hp[i] > 0:
                        damage_targets += [self.players[i]]

                self.damage(source=self.current_player, targets=damage_targets)

                self.screen.fill((255, 255, 255))
                self.draw_players()
                pygame.display.flip()
                pygame.time.delay(500)

                turns += 1

                self.screen.fill((255, 255, 255))
                self.draw_players()
                pygame.display.flip()
                self.clock.tick(60)

            winner = self.check_if_winner
            logger.info(f"Game is finished. Winner is {winner}")
            winners += [winner]

        self.output_game_results(winners=winners, repeats=repeats)

        winner = self.players[0]
        for player in self.players:
            if not player.is_dead:
                winner = player

        self.game_results(winner=winner)
        pygame.display.flip()

        pygame.time.delay(500)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
