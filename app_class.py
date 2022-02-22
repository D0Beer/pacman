import sys
from player_class import *
from enemy_class import *
from settings import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH // COLS
        self.cell_height = MAZE_HEIGHT // ROWS
        self.walls = []
        self.coins = []
        self.fruits = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        self.load()
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()

        self.logo_image = pygame.image.load("images\logo2.png")
        self.logo_rect = self.logo_image.get_rect()
        self.logo_rect.x = 60
        self.logo_rect.y = HEIGHT - 500
        self.scaled_logo_image = pygame.transform.scale(self.logo_image, (500, 130))

        self.final_image = pygame.image.load("images\gameover.png")
        self.final_rect = self.final_image.get_rect()
        self.final_rect.x = 50
        self.final_rect.y = HEIGHT - 600
        self.scaled_final_image = pygame.transform.scale(self.final_image, (500, 250))
    
    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    ########################## HELP FUNCTIONS ###########################

    def draw_text(self, words, screen, pos, size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('sprites\maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # opening walls file
        # creating walls list with co-ords of walls
        with open("data\walls.txt", "r") as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "F":
                        self.fruits.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK,
                                         (xidx * self.cell_width, yidx * self.cell_height,
                                          self.cell_width, self.cell_height))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY, (x * self.cell_width, 0),
                             (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x * self.cell_height),
                             (WIDTH, x * self.cell_height))

        # for coin in self.coins:
        #     pygame.draw.rect(self.background, (167, 179, 34),
        #                      (coin.x * self.cell_width, coin.y * self.cell_height,
        #                       self.cell_width, self.cell_height))

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0

        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        self.fruits = []
        with open("data\walls.txt", "r") as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
                    if char == "F":
                        self.fruits.append(vec(xidx, yidx))
        self.state = 'playing'

    ########################## INTRO FUNCTIONS ##########################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.scaled_logo_image, self.logo_rect)
        self.draw_text('PUSH SPACE BAR TO START!', self.screen, [WIDTH // 2, HEIGHT // 2],
                        START_TEXT_SIZE, (255,215,0), START_FONT, centered=True)
        self.draw_text('CREATED BY DOBER', self.screen, [WIDTH // 2, HEIGHT - 30],
                        14, (44, 167, 198), START_FONT, centered=True)
        self.draw_text(f'HIGH SCORE: {self.player.high_score}', self.screen,
                       [4, 0], 16, (255, 255, 255), START_FONT)
        pygame.display.update()

    ########################## PLAYING FUNCTIONS ##########################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                    self.player.angle = 180
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                    self.player.angle = 0
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                    self.player.angle = 90
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))
                    self.player.angle = 270

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background,
                         (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        self.draw_fruits()
        # self.draw_grid()
        self.draw_text(f'CURRENT SCORE: {self.player.current_score}',
                       self.screen, [60, 0], 18, WHITE, START_FONT)
        self.draw_text(f'HIGH SCORE: {self.player.high_score}', self.screen,
                       [WIDTH // 2 + 60, 0], 18, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = 'game over'
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (255, 215, 0),
                (int(coin.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                int(coin.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 4)

    def draw_fruits(self):
        for fruit in self.fruits:
            pygame.draw.circle(self.screen, (255, 0, 0),
                (int(fruit.x * self.cell_width) + self.cell_width // 2 + TOP_BOTTOM_BUFFER // 2,
                int(fruit.y * self.cell_height) + self.cell_height // 2 + TOP_BOTTOM_BUFFER // 2), 7)
    ########################## GAME OVER FUNCTIONS ##########################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.scaled_final_image, self.final_rect)
        quit_text = 'Press the ESCAPE button to QUIT'
        again_text = 'Press the SPACE bar to PLAY AGAIN'
        self.draw_text(again_text, self.screen, [WIDTH // 2, HEIGHT // 2], 27,
                    (255,215,0),'arial', centered=True)
        self.draw_text(quit_text, self.screen, [WIDTH // 2, HEIGHT // 1.7], 27,
                    (255,215,0),'arial', centered=True)
        self.draw_text(f"Your score: {self.player.current_score}           Your Highscore: {self.player.high_score}",
                    self.screen, [WIDTH // 2, HEIGHT // 2 + 150], 27,
                    RED,'arial', centered=True)
        pygame.display.update()