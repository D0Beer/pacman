import pygame
from settings import *
from enemy_class import *

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.high_score = self.read_high_score()
        self.speed = 2
        self.lives = 3
        self.angle = 0

        self.image = pygame.image.load("sprites\player.png")
        self.rect = self.image.get_rect()
        self.scaled_image = None

        self.lives_image = pygame.image.load("sprites\player.png")
        self.lives_rect = self.lives_image.get_rect()
        self.lives_scaled_image = None

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed

        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        # setting grid position in reference to pixel position
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER
                            + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER
                            + self.app.cell_height // 2) // self.app.cell_height + 1

        if self.on_coin():
            self.eat_coin()

        if self.on_fruit():
            self.eat_fruit()

    def draw(self):

        self.rect.x = int(self.pix_pos.x) - 29
        self.rect.y = int(self.pix_pos.y) - 25
        self.scaled_image = pygame.transform.scale(self.image, (55, 55))
        self.rotated_image = pygame.transform.rotate(self.scaled_image, self.angle)
        self.app.screen.blit(self.rotated_image, self.rect)

        # pygame.draw.circle(self.app.screen, PLAYER_COLOR,
        #                    (int(self.pix_pos.x), int(self.pix_pos.y)),
        #                    self.app.cell_width // 2 - 2)

        # drawing player lives
        for x in range(self.lives):
            self.lives_rect.x = 15 + 25 * x
            self.lives_rect.y = HEIGHT - 37
            self.lives_scaled_image = pygame.transform.scale(self.lives_image, (50, 50))
            self.app.screen.blit(self.lives_scaled_image, self.lives_rect)
            # pygame.draw.circle(self.app.screen, PLAYER_COLOR, (30 + 20 * x, HEIGHT - 15), 7)

        # drawing the grid pos rect
        # pygame.draw.rect(self.app.screen, RED,
        #                  (self.grid_pos[0] * self.app.cell_width + TOP_BOTTOM_BUFFER // 2,
        #                   self.grid_pos[1] * self.app.cell_height + TOP_BOTTOM_BUFFER // 2,
        #                   self.app.cell_width, self.app.cell_height), 1)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

        if self.current_score >= int(self.high_score):
            self.write_high_score(str(self.current_score))

    def on_fruit(self):
        if self.grid_pos in self.app.fruits:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_fruit(self):
        self.app.fruits.remove(self.grid_pos)
        self.current_score += 50

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width)
                   + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height)
                   + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)
        # print(self.grid_pos, self.pix_pos)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True

    def read_high_score(self):
        with open("data_files\highscore.txt", 'r') as file:
            high_score = file.read()

        return high_score

    def write_high_score(self, score):
        with open("data_files\highscore.txt", 'w') as file:
            file.write(score)
