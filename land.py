import pygame
import os

pygame.font.init()

# Global  Constants
BG = pygame.image.load(os.path.join('image', 'ground.png'))
FONT = pygame.font.Font('font/OpenSans.ttf', 20)

class Land:
    STEP = 1
    POINTS = 0
    X_POS_BG = 0
    Y_POS_BG = 410
    GAME_SPEED = 20

    def __init__(self, SCREEN):
        self.screen = SCREEN
        self.STEP = 1
        self.POINTS = 0
        self.GAME_SPEED = 20

    def score(self):
        self.POINTS += self.STEP
        if self.POINTS % 100 == 0:
            self.GAME_SPEED += 1
        text = FONT.render(f'Points: {str(self.POINTS)}', True, (255, 255, 255))
        self.screen.blit(text, (950, 50))

    def background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.X_POS_BG, self.Y_POS_BG))
        self.screen.blit(BG, (image_width + self.X_POS_BG, self.Y_POS_BG))
        if self.X_POS_BG <= - image_width:
            self.X_POS_BG = 0
        self.X_POS_BG -= self.GAME_SPEED