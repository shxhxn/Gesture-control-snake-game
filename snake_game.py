
import pygame  # library which is used to create graphics, sound, game events.
import random  # here, just to add food randomly throughout the gamescreen.
import sys     # for clean quitting of the game
import math    # for calculations
from collections import deque # this allows us to append data from both end, remove or add element from both the left and right


CELL_SIZE = 20  
GRID_WIDTH = 28  
GRID_HEIGHT = 20  
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT + 80  
FPS = 7          # game speed (frames per second)

# Colors
WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRAY = (120, 120, 130)
DARK = (15, 15, 20)
GREEN = (90, 200, 120)
RED = (240, 80, 80)
GOLD = (255, 200, 0)
GLASS = (255, 255, 255, 40)

# Directions
DIRS = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


# --- Utility drawing functions ---
def draw_rounded_rect(surface, rect, color, radius=6):
    x, y, w, h = rect
    pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
    pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
    pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Neon Snake — gesture-ready")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("Segoe UI", 36, bold=True)
        self.font_med = pygame.font.SysFont("Segoe UI", 20)
        self.font_small = pygame.font.SysFont("Segoe UI", 16)
        self.reset()
        self.gesture_override = None  # external code can set this to override direction
        self.running = True

    def reset(self):
        self.score = 0
        self.highscore = 0
        self.direction = 'RIGHT'
        self.pending_dir = None
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.snake = deque([(start_x - i, start_y) for i in range(3)])  # head at leftmost
        self.spawn_food()
        self.game_over = False
        self.paused = False
        self.flash = 0.0

    def spawn_food(self):
        while True:
            pos = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
            if pos not in self.snake:
                self.food = pos
                break

    def set_direction(self, dir_str):
        """External interface for CV/gestures: call set_direction('UP') etc.
           This only sets pending direction which will be validated in the game loop.
        """
        dir_str = dir_str.upper()
        if dir_str in DIRS:
            self.pending_dir = dir_str

    def _apply_pending_dir(self):
        if not self.pending_dir:
            return
        # Prevent 180-degree reversals
        cur = self.direction
        new = self.pending_dir
        if (cur == 'UP' and new == 'DOWN') or (cur == 'DOWN' and new == 'UP') or \
           (cur == 'LEFT' and new == 'RIGHT') or (cur == 'RIGHT' and new == 'LEFT'):
            self.pending_dir = None
            return
        self.direction = new
        self.pending_dir = None

    def step(self):
        if self.game_over or self.paused:
            return
        # If gesture override is provided (set externally), use it:
        if self.gesture_override:
            self.set_direction(self.gesture_override)

        self._apply_pending_dir()
        dx, dy = DIRS[self.direction]
        head_x, head_y = self.snake[0]
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)  # wrap-around

        # Collision with self leads to game over
        if new_head in self.snake:
            self.game_over = True
            self.highscore = max(self.highscore, self.score)
            return

        self.snake.appendleft(new_head)

        # Eating food?
        if new_head == self.food:
            self.score += 10
            self.flash = 0.8
            self.spawn_food()
        else:
            self.snake.pop()

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_UP, pygame.K_w):
                self.set_direction('UP')
            elif e.key in (pygame.K_DOWN, pygame.K_s):
                self.set_direction('DOWN')
            elif e.key in (pygame.K_LEFT, pygame.K_a):
                self.set_direction('LEFT')
            elif e.key in (pygame.K_RIGHT, pygame.K_d):
                self.set_direction('RIGHT')
            elif e.key == pygame.K_p:
                self.paused = not self.paused
            elif e.key == pygame.K_ESCAPE:
                self.running = False
            elif e.key == pygame.K_r and self.game_over:
                self.reset()

        elif e.type == pygame.QUIT:
            self.running = False

    def draw_background(self):
        # soft vertical gradient
        for i in range(WINDOW_HEIGHT):
            t = i / WINDOW_HEIGHT
            r = int(DARK[0] + (30 - DARK[0]) * t)
            g = int(DARK[1] + (40 - DARK[1]) * t)
            b = int(DARK[2] + (60 - DARK[2]) * t)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (WINDOW_WIDTH, i))

        # subtle grid
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (20, 20, 25), (x, 0), (x, WINDOW_HEIGHT - 80))
        for y in range(0, WINDOW_HEIGHT - 80, CELL_SIZE):
            pygame.draw.line(self.screen, (20, 20, 25), (0, y), (WINDOW_WIDTH, y))

    def draw_ui_panel(self):
        panel_rect = (8, WINDOW_HEIGHT - 72, WINDOW_WIDTH - 16, 64)
        draw_rounded_rect(self.screen, panel_rect, (18, 18, 24), radius=8)
        # glass effect
        s = pygame.Surface((panel_rect[2], panel_rect[3]), pygame.SRCALPHA)
        s.fill((255, 255, 255, 10))
        self.screen.blit(s, (panel_rect[0], panel_rect[1]))

        # score text
        score_surf = self.font_med.render(f"Score: {self.score}", True, WHITE)
        hs_surf = self.font_small.render(f"Highscore: {self.highscore}", True, GRAY)
        instr_surf = self.font_small.render("Arrows/WASD = Move   P = Pause   R = Restart (on Game Over)", True, GRAY)
        self.screen.blit(score_surf, (panel_rect[0] + 12, panel_rect[1] + 10))
        self.screen.blit(hs_surf, (panel_rect[0] + 12, panel_rect[1] + 36))
        self.screen.blit(instr_surf, (panel_rect[0] + 220, panel_rect[1] + 20))

    def draw_snake_and_food(self):
        # food: draw a glowing circle
        fx, fy = self.food
        fxp = fx * CELL_SIZE + CELL_SIZE // 2
        fyp = fy * CELL_SIZE + CELL_SIZE // 2
        # glow
        for i, a in enumerate([120, 60, 30]):
            r = CELL_SIZE // 2 + i * 4
            surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (GOLD[0], GOLD[1], GOLD[2], a), (r, r), r)
            self.screen.blit(surf, (fxp - r, fyp - r))
        # core
        pygame.draw.circle(self.screen, RED, (fxp, fyp), CELL_SIZE // 3)

        # snake body: draw gradient along the body
        n = len(self.snake)
        for idx, (sx, sy) in enumerate(self.snake):
            t = idx / max(1, n - 1)
            # head is brighter
            col = (int(GREEN[0] * (1 - t) + 30 * t), int(GREEN[1] * (1 - t) + 200 * t), int(GREEN[2] * (1 - t) + 80 * t))
            rect = (sx * CELL_SIZE + 2, sy * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            pygame.draw.rect(self.screen, col, rect, border_radius=6)
            # small eye on the head
            if idx == 0:
                hx = sx * CELL_SIZE + CELL_SIZE // 2
                hy = sy * CELL_SIZE + CELL_SIZE // 2
                eye_offset = (DIRS[self.direction][0] * 6, DIRS[self.direction][1] * 6)
                pygame.draw.circle(self.screen, BLACK, (hx + eye_offset[0] - 3, hy + eye_offset[1] - 3), 3)
                pygame.draw.circle(self.screen, BLACK, (hx + eye_offset[0] + 3, hy + eye_offset[1] + 3), 3)

    def draw_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - 80), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))
        txt = self.font_big.render("Game Over", True, WHITE)
        sub = self.font_med.render(f"Score: {self.score}    Highscore: {self.highscore}", True, GRAY)
        self.screen.blit(txt, (WINDOW_WIDTH // 2 - txt.get_width() // 2, WINDOW_HEIGHT // 2 - 60))
        self.screen.blit(sub, (WINDOW_WIDTH // 2 - sub.get_width() // 2, WINDOW_HEIGHT // 2 - 10))
        hint = self.font_small.render("Press R to restart or ESC to quit", True, GRAY)
        self.screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT // 2 + 30))

    def draw_paused(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - 80), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))
        txt = self.font_big.render("Paused", True, WHITE)
        self.screen.blit(txt, (WINDOW_WIDTH // 2 - txt.get_width() // 2, WINDOW_HEIGHT // 2 - 20))

    def update(self):
        self.step()
        if self.flash > 0:
            self.flash = max(0.0, self.flash - 0.04)

    def render(self):
        self.draw_background()
        self.draw_snake_and_food()
        self.draw_ui_panel()
        if self.paused:
            self.draw_paused()
        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        tick = 0
        while self.running:
            # Event handling
            for e in pygame.event.get():
                self.handle_event(e)

            # update
            self.update()
            self.render()
            self.clock.tick(FPS)
            tick += 1

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()

