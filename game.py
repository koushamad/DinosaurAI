import pygame
import sys
import math
import random
import neat

from dinosaur import Dinosaur
from land import Land
from obstacle import Obstacle

# Global  Constants
SCREEN_HECHT = 600
SCREEN_WIDTH = 1100
FONT = pygame.font.Font('font/OpenSans.ttf', 20)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HECHT))
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.clock = pygame.time.Clock()
        self.land = Land(self.screen)
        self.obstacle = Obstacle(self.screen)
        self.dinosaurs = []
        self.genomes = []
        self.nets = []

    def start(self, genomes, config, generation=1):

        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            genome.fitness = 0
            self.dinosaurs.append(Dinosaur(self.screen))
            self.genomes.append(genome)
            self.nets.append(net)

        while True:
            self.land.score()
            self.land.background()
            self.obstacle.build(self.land.POINTS)
            self.obstacle.update(self.land.GAME_SPEED)

            for i, dinosaur in enumerate(self.dinosaurs):
                self.draw(dinosaur, generation)
                self.listener(self.nets[i], dinosaur)
                dinosaur.draw()
                dinosaur.update()
                if self.check(self.genomes[i], dinosaur):
                    self.dinosaurs.pop(i)
                    self.genomes.pop(i)
                    self.nets.pop(i)

            self.clock.tick(30)
            pygame.display.update()
            self.screen.fill(color=(0, 0, 0))
            if len(self.dinosaurs) == 0:
                break

        return self.land.POINTS

    def draw(self, dinosaur, generation):
        # pygame.draw.rect(self.screen, dinosaur.color,
        #                  (dinosaur.rect.x, dinosaur.rect.y, dinosaur.rect.width, dinosaur.rect.height), 2)

        for obstacle in self.obstacle.OBSTACLES:
            if obstacle.type > 0 and len(self.dinosaurs) < 100:
                pygame.draw.rect(self.screen, dinosaur.color, (obstacle.rect.x + 22, obstacle.rect.y, obstacle.rect.width, obstacle.rect.height),2)

                pygame.draw.line(self.screen, dinosaur.color, (dinosaur.rect.topright[0] - 18, dinosaur.rect.topright[1] + 8), obstacle.rect.bottomleft, 2)
                pygame.draw.line(self.screen, dinosaur.color, (dinosaur.rect.topright[0] - 18, dinosaur.rect.topright[1] + 8), obstacle.rect.topleft, 2)
                if len(self.dinosaurs) > 3:
                    break

        text_1 = FONT.render(f'dinosaur.number: {str(len(self.dinosaurs))}', True, dinosaur.color)
        text_2 = FONT.render(f'game.speed: {str(self.land.GAME_SPEED)}', True, dinosaur.color)
        text_3 = FONT.render(f'generation: {str(generation)}', True, dinosaur.color)

        self.screen.blit(text_1, (50, 440))
        self.screen.blit(text_2, (50, 460))
        self.screen.blit(text_3, (50, 480))

    def check(self, genome, dinosaur):
        if self.obstacle.check(dinosaur):
            dinosaur.dino_dead = True
            dinosaur.dino_jump = False
            dinosaur.dino_run = False
            dinosaur.dino_duck = False
            genome.fitness = self.land.POINTS
            return True
        return False

    def distance(self, pos_a, pos_b):
        dx = pos_a[0] - pos_b[0]
        dy = pos_a[1] - pos_b[1]
        return math.sqrt(dx ** 2 + dy ** 2)

    def listener(self, net, dinosaur):

        for obstacle in self.obstacle.OBSTACLES:
            if obstacle.is_obstacle:
                output = net.activate((
                    dinosaur.rect.y,
                    obstacle.type,
                    obstacle.rect.topleft[0],
                    obstacle.rect.topleft[1],
                    obstacle.rect.bottomleft[1],
                    self.distance((dinosaur.rect.x, dinosaur.rect.y), obstacle.rect.midtop),
                ))

                if dinosaur.rect.y == dinosaur.Y_POS:

                    if output[0] > 0.5:
                        if output[1] > 0.5:
                            dinosaur.dino_jump = False
                            dinosaur.dino_run = False
                            dinosaur.dino_duck = True
                        else:
                            dinosaur.dino_jump = False
                            dinosaur.dino_run = True
                            dinosaur.dino_duck = False
                    else:
                        if output[1] > 0.5:
                            dinosaur.dino_jump = True
                            dinosaur.dino_run = False
                            dinosaur.dino_duck = False
                        else:
                            dinosaur.dino_jump = False
                            dinosaur.dino_run = True
                            dinosaur.dino_duck = False
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dinosaur.rect.y == dinosaur.Y_POS:
                    dinosaur.dino_jump = True
                    dinosaur.dino_run = False
                    dinosaur.dino_duck = False
                if event.key == pygame.K_DOWN and dinosaur.rect.y == dinosaur.Y_POS:
                    dinosaur.dino_jump = False
                    dinosaur.dino_run = False
                    dinosaur.dino_duck = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dinosaur.dino_jump = False
                    dinosaur.dino_run = True
                    dinosaur.dino_duck = False
