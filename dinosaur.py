import pygame
import os
import random

# Global  Constants
RUNNING = [
    pygame.image.load(os.path.join('image', 'run1.png')),
    pygame.image.load(os.path.join('image', 'run2.png')),
]
DUCKING = [
    pygame.image.load(os.path.join('image', 'duck1.png')),
    pygame.image.load(os.path.join('image', 'duck2.png')),
]
JUMPING = pygame.image.load(os.path.join('image', 'jump.png'))
DEAD = pygame.image.load(os.path.join('image', 'dead.png'))
DINO = pygame.image.load(os.path.join('image', 'dino.png'))


class Dinosaur:
    SIZE = 2
    X_POS = 80
    Y_POS = 370
    JUMP_VEL = 5
    RUNNING = [
        pygame.transform.scale(RUNNING[0], (RUNNING[0].get_width() // SIZE, RUNNING[0].get_height() // SIZE)),
        pygame.transform.scale(RUNNING[1], (RUNNING[1].get_width() // SIZE, RUNNING[1].get_height() // SIZE)),
    ]
    DUCKING = [
        pygame.transform.scale(DUCKING[0], (DUCKING[0].get_width() // SIZE, DUCKING[0].get_height() // SIZE)),
        pygame.transform.scale(DUCKING[1], (DUCKING[1].get_width() // SIZE, DUCKING[1].get_height() // SIZE)),
    ]
    JUMPING = pygame.transform.scale(JUMPING, (JUMPING.get_width() // SIZE, JUMPING.get_height() // SIZE))
    DEAD = pygame.transform.scale(DEAD, (RUNNING[0].get_width() // SIZE, RUNNING[0].get_height() // SIZE))
    DINO = pygame.transform.scale(DINO, (RUNNING[0].get_width() // SIZE, RUNNING[0].get_height() // SIZE))

    def __init__(self, SCREEN):
        self.screen = SCREEN
        self.image = self.DINO
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.dino_dead = False
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, self.image.get_width(), self.image.get_height())
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step = 0

    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()
        if self.dino_dead:
            self.dead()

    def jump(self):
        self.image = self.JUMPING
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

    def run(self):
        self.image = self.RUNNING[(self.step // 5) % 2]
        self.jump_vel = self.JUMP_VEL
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self.step += 1

    def duck(self):
        self.image = self.DUCKING[(self.step // 5) % 2]
        self.jump_vel = self.JUMP_VEL
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS + 20
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self.step += 1

    def dead(self):
        self.image = DEAD

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
