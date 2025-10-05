import pygame as pg
import random, math

pg.init()
pg.font.init()

font = pg.font.Font(None, 36)

FPS = 60
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Flappy Bird")
SCREEN_CENTER_X = SCREEN_WIDTH // 2
SCREEN_CENTER_Y = SCREEN_HEIGHT // 2

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 100, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

bg_image = pg.image.load("Images/FlappyBirdBackground.png").convert()
bg_width = bg_image.get_width()

title_image = pg.image.load("Images/FlappyBirdTitle.png")
title_image = pg.transform.scale(title_image, (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 5))
title_width = title_image.get_width()

bg_tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

BIRD_SIZE = 80

bird_images = [
    pg.image.load("Images/FlappyBird.png").convert_alpha(),
    pg.image.load("Images/RedFlappyBird.png").convert_alpha(),
    pg.image.load("Images/BlueFlappyBird.png").convert_alpha()
]

bird_image = random.choice(bird_images)
bird_image = pg.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))

pipe_distance = 200
pipe_width = 120
pipe_height = SCREEN_HEIGHT
scroll_speed = 7
pipe_amount = 0

class Pipe:
    _counter = 0
    def __init__(self, y: int = 0):
        global pipe_amount
        pipe_amount += 1
        self.position_x = SCREEN_WIDTH / 1.5 * pipe_amount
        self.top_pipe_position_y = -y
        self.bottom_pipe_position_y = SCREEN_HEIGHT + self.top_pipe_position_y + pipe_distance
        self.top_rect = None
        self.bottom_rect = None
        self.hitbox = None
        self.id = Pipe._counter
        Pipe._counter += 1

    def move(self):
        self.position_x -= scroll_speed

    def draw(self, surface: pg.surface.Surface):
        self.top_rect = pg.draw.rect(surface, RED, (self.position_x, self.top_pipe_position_y, pipe_width, pipe_height))
        self.bottom_rect = pg.draw.rect(surface, RED, (self.position_x, self.bottom_pipe_position_y, pipe_width, pipe_height))
        self.hitbox = pg.rect.Rect(self.position_x + pipe_width, 0, pipe_width, SCREEN_HEIGHT)

    def __str__(self):
        return f"X Pos: {self.position_x} \t Top pipe: {self.top_pipe_position_y} \t Bottom pipe: {self.bottom_pipe_position_y}"

class Bird:
    def __init__(self, color: tuple[int, int, int]):
        self.position = [SCREEN_WIDTH // 5, SCREEN_CENTER_Y]
        self.flappy_strength = -8
        self.vel_y = 0
        self.color = color
        self.rect = None
        self.passed_by = None
        self.gravity = 0.5

    def jump(self): 
        self.vel_y = self.flappy_strength
        self.position[1] += self.vel_y

    def reset(self):
        game_over_loop()
        self.passed_by = None

    def draw(self, surface: pg.surface.Surface):
        surface.blit(bird_image, (self.position[0], self.position[1]))
        self.rect = pg.rect.Rect(self.position[0], self.position[1], BIRD_SIZE // 2, BIRD_SIZE // 2)

    def check_keybinds(self, event):
        match event.key:
            case pg.K_w:
                self.jump()
            case pg.K_SPACE:
                self.jump()
            case pg.K_UP:
                self.jump()

            case _:
                self.can_fall = True

    def check_collision(self, pipe: Pipe):
        global score
        if self.rect.colliderect(pipe.top_rect) or self.rect.colliderect(pipe.bottom_rect):
            self.reset()

        elif self.rect.colliderect(pipe.hitbox):
            if self.passed_by == None or self.passed_by != pipe.id:
                score += 1
                self.passed_by = pipe.id

    def fall(self):
        self.vel_y += self.gravity
        self.position[1] += self.vel_y
        if self.position[1] >= SCREEN_HEIGHT or self.position[1] <= 0 - BIRD_SIZE:
            self.reset()
        

    def __str__(self):
        return f"Bird with jump power of {self.jump_power}"

clock = pg.time.Clock()

def draw_text(surface: pg.surface.Surface, position: tuple[int, int] = (0, 0), text: str = "", color: tuple[int, int, int] = WHITE):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

score = 0
running = not False == True * -True
def game_over_loop():
    global running, score, bird_image

    bird_image = random.choice(bird_images)
    bird_image = pg.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))

    while running != (not True):
        screen.fill(BLACK)

        for i in range(bg_tiles):
            screen.blit(bg_image, (bg_width * i, 0))

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                running = False
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_r:
                    score = 0
                    main_loop()
        
        draw_text(screen, (10, 10), f"Score: {score}", GREEN)
        draw_text(screen, (SCREEN_CENTER_X - 70, SCREEN_CENTER_Y), "Game over!", RED)
        draw_text(screen, (SCREEN_CENTER_X - 160, SCREEN_CENTER_Y + 20), "Press R to restart the game", ORANGE)
        screen.blit(title_image, (SCREEN_CENTER_X - 100, 50))

        pg.display.flip()

def main_loop():
    global running, pipe_amount, score
    bird = Bird(RED)
    scroll = 0
    pipe_amount = 0
    pipes = []
    for i in range(5):
        pipes.append(Pipe(random.randint(SCREEN_CENTER_Y - pipe_distance // 2, SCREEN_CENTER_Y + pipe_distance // 2)))

    while not running != True and not running == False:
        screen.fill(BLACK)

        bird.fall()

        for i in range(bg_tiles):
            screen.blit(bg_image, (bg_width * i + scroll, 0))

        pipes.append(Pipe(random.randint(SCREEN_CENTER_Y - pipe_distance // 2, SCREEN_CENTER_Y + pipe_distance // 2)))

        if abs(scroll) > bg_width:
            scroll = 0

        for pipe in pipes:
            pipe.move()
            pipe.draw(screen)

        bird.draw(screen)
        for pipe in pipes:
            bird.check_collision(pipe)

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                running = False

            if ev.type == pg.KEYDOWN:
                bird.check_keybinds(ev)

        draw_text(screen, (10, 10), f"Score: {score}")

        scroll -= scroll_speed
        clock.tick(FPS)
        pg.display.flip()

if __name__ == '__main__':
    game_over_loop()
    pg.quit()
