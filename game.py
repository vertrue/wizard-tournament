from player import Player
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
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.center = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.font = pygame.font.SysFont(None, 24)
        self.large_font = pygame.font.SysFont(None, 72)
        self.player_colors = [
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for _ in players
        ]

        super().__init__(players)

        self.player_positions = []
        self.wand_positions = []
        self.current_player = None
        self.target_player = None

    def draw_players(self):
        radius = min(self.screen.get_width(), self.screen.get_height()) * 0.3
        angle_step = 2 * math.pi / len(self.players)
        self.player_positions = []
        self.wand_positions = []

        for i, player in enumerate(self.players):
            angle = i * angle_step
            x = self.center.x + radius * math.cos(angle)
            y = self.center.y + radius * math.sin(angle)
            self.player_positions.append((int(x), int(y)))
            self.wand_positions.append(
                (
                    int(x + 30 * math.cos(angle + math.pi / 4)),
                    int(y + 30 * math.sin(angle + math.pi / 4)),
                )
            )

        for i, pos in enumerate(self.player_positions):
            pygame.draw.circle(self.screen, self.player_colors[i], pos, 20)
            if self.current_player == self.players[i]:
                arrow_end = (
                    self.center.x + 0.5 * (pos[0] - self.center.x),
                    self.center.y + 0.5 * (pos[1] - self.center.y),
                )
                pygame.draw.line(self.screen, (255, 0, 0), self.center, arrow_end, 3)
                pygame.draw.polygon(
                    self.screen,
                    (255, 0, 0),
                    [
                        (arrow_end[0] - 5, arrow_end[1] - 5),
                        (arrow_end[0] + 5, arrow_end[1] - 5),
                        (arrow_end[0], arrow_end[1] + 5),
                    ],
                )
            if self.target_player == self.players[i]:
                pygame.draw.circle(self.screen, (255, 0, 0), pos, 25, 3)
            health_text = self.font.render(str(self.players[i].hp), True, (0, 0, 0))
            self.screen.blit(health_text, (pos[0] - 10, pos[1] - 30))

        for i, pos in enumerate(self.wand_positions):
            pygame.draw.circle(self.screen, self.player_colors[i], pos, 10)
            wand_text = self.font.render(self.players[i].wand.name, True, (0, 0, 0))
            self.screen.blit(wand_text, (pos[0] - 40, pos[1] + 15))
            dice_text = self.font.render(f"d{self.players[i].dice}", True, (0, 0, 0))
            self.screen.blit(dice_text, (pos[0] - 40, pos[1] + 30))

    def animate_damage(self, player):
        for _ in range(5):
            self.screen.fill((255, 255, 255))
            index = self.players.index(player)
            original_pos = self.player_positions[index]
            offset = 5 if _ % 2 == 0 else -5
            self.player_positions[index] = (original_pos[0] + offset, original_pos[1])
            self.draw_players()
            pygame.display.flip()
            self.clock.tick(10)
        self.player_positions[index] = original_pos

    def simulate(self, repeats: int = 1):
        winners = []

        for _ in range(repeats):
            turns = 0
            last_turn_hp = []

            while not self.is_only_one_alive:
                pygame.time.delay(500)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                if turns % self.total_players == 0:
                    if last_turn_hp == self.players_hp:
                        break
                    last_turn_hp = self.players_hp
                    logger.info(f"-------------ROUND {turns // self.total_players + 1}-----------")

                self.current_player = self.players[turns % self.total_players]
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

                self.screen.fill((255, 255, 255))
                self.draw_players()
                pygame.display.flip()
                pygame.time.delay(500)

                if self.target_player.hp < last_turn_hp[self.players.index(self.target_player)]:
                    self.animate_damage(self.target_player)
                turns += 1

                self.screen.fill((255, 255, 255))
                self.draw_players()
                pygame.display.flip()
                self.clock.tick(60)

            winner = self.check_if_winner
            logger.info(f"Game is finished. Winner is {winner}")
            winners += [winner]

            for player in self.players:
                player.reset_hp()

        self.output_game_results(winners=winners, repeats=repeats)

        winner = self.players[0]
        for player in self.players:
            if not player.is_dead:
                winner = player

        self.screen.fill((255, 255, 255))
        winner_text = self.large_font.render(f"Winner: {winner.name}", True, (0, 0, 0))
        wand_text = self.large_font.render(f"with {winner.wand.name}", True, (0, 0, 0))
        self.screen.blit(
            winner_text, (self.center.x - winner_text.get_width() // 2, self.center.y - 40)
        )
        self.screen.blit(
            wand_text, (self.center.x - wand_text.get_width() // 2, self.center.y + 40)
        )
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
