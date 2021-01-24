import pygame
import os
import random

# Global  Constants
SMALE_CACTUS = [pygame.image.load(os.path.join('image', 'cactusS.png'))]
SMALE_MANY_CACTUS = [pygame.image.load(os.path.join('image', 'cactusSM.png'))]
BIG_CACTUS = [pygame.image.load(os.path.join('image', 'cactusB.png'))]
BIRDS = [
    pygame.image.load(os.path.join('image', 'bird1.png')),
    pygame.image.load(os.path.join('image', 'bird2.png')),
]
CLOUD = [pygame.image.load(os.path.join('image', 'cloud.png'))]


class Object:
    SIZE = 2

    def __init__(self, SCREEN, image, type=0):
        self.screen = SCREEN
        self.type = type
        self.is_obstacle = type > 1
        self.image = image
        self.rect = self.image[random.randint(0, len(image) - 1)].get_rect()
        self.rect.x = 1100
        self.step = 0

    def update(self, game_speed):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            return True
        return False

    def draw(self):
        self.screen.blit(self.image[(self.step // 5) % len(self.image)], self.rect)
        self.step += 1


class SmallCactus(Object):
    def __init__(self, SCREEN):
        image = pygame.transform.scale(
            SMALE_CACTUS[0],
            (SMALE_CACTUS[0].get_width() // self.SIZE, SMALE_CACTUS[0].get_height() // self.SIZE)
        ),
        super().__init__(SCREEN, image, 2)
        self.rect.y = 380


class SmallManyCactus(Object):
    def __init__(self, SCREEN):
        image = pygame.transform.scale(
            SMALE_MANY_CACTUS[0],
            (SMALE_MANY_CACTUS[0].get_width() // self.SIZE, SMALE_MANY_CACTUS[0].get_height() // self.SIZE)
        ),
        super().__init__(SCREEN, image, 2)
        self.rect.y = 380


class LargeCactus(Object):
    def __init__(self, SCREEN):
        image = pygame.transform.scale(
            BIG_CACTUS[0],
            (BIG_CACTUS[0].get_width() // self.SIZE, BIG_CACTUS[0].get_height() // self.SIZE)
        ),
        super().__init__(SCREEN, image, 2)
        self.rect.y = 370


class Bird1(Object):
    def __init__(self, SCREEN):
        images = [
            pygame.transform.scale(BIRDS[0], (BIRDS[0].get_width() // 3, BIRDS[0].get_height() // 3)),
            pygame.transform.scale(BIRDS[1], (BIRDS[1].get_width() // 3, BIRDS[1].get_height() // 3)),
        ]
        super().__init__(SCREEN, images, 3)
        self.rect.y = 350


class Bird2(Object):
    def __init__(self, SCREEN):
        images = [
            pygame.transform.scale(BIRDS[0], (BIRDS[0].get_width() // 3, BIRDS[0].get_height() // 3)),
            pygame.transform.scale(BIRDS[1], (BIRDS[1].get_width() // 3, BIRDS[1].get_height() // 3)),
        ]
        super().__init__(SCREEN, images, 1)
        self.rect.y = 320

class Bird3(Object):
    def __init__(self, SCREEN):
        images = [
            pygame.transform.scale(BIRDS[0], (BIRDS[0].get_width() // 3, BIRDS[0].get_height() // 3)),
            pygame.transform.scale(BIRDS[1], (BIRDS[1].get_width() // 3, BIRDS[1].get_height() // 3)),
        ]
        super().__init__(SCREEN, images, 2)
        self.rect.y = 380


class Cloud(Object):
    def __init__(self, SCREEN):
        images = [
            pygame.transform.scale(CLOUD[0], (CLOUD[0].get_width(), CLOUD[0].get_height())),
        ]
        super().__init__(SCREEN, images, 0)
        self.rect.y = 250


class Obstacle:
    OBSTACLES = []
    CLOUDS = []

    def __init__(self, SCREEN):
        self.screen = SCREEN
        self.OBSTACLES = []
        self.CLOUDS = []

    def build(self, points):

        if points % 10 == 0:
            if random.randint(0, 2) == 1:
                self.OBSTACLES.append(Cloud(self.screen))

        if points % 20 == 0:
            if len(self.OBSTACLES) < 6:
                random_int = random.randint(0, 5)
                if random_int == 0:
                    self.OBSTACLES.append(SmallCactus(self.screen))
                elif random_int == 1:
                    self.OBSTACLES.append(LargeCactus(self.screen))
                elif random_int == 2:
                    self.OBSTACLES.append(SmallManyCactus(self.screen))
                # elif random_int == 3:
                #     self.OBSTACLES.append(Bird1(self.screen))
                elif random_int == 4:
                    self.OBSTACLES.append(Bird2(self.screen))
                elif random_int == 5:
                    self.OBSTACLES.append(Bird3(self.screen))

    def update(self, game_speed):
        for obstacle in self.OBSTACLES:
            obstacle.draw()
            if obstacle.update(game_speed):
                self.OBSTACLES.pop(0)

    def check(self, dinosaur):
        for obstacle in self.OBSTACLES:
            if dinosaur.rect.colliderect(obstacle.rect):
                return True

        return False
