import pygame

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mario Game Adventure")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(50, WINDOW_HEIGHT - 60))
        self.horizontal_speed = 0
        self.vertical_speed = 0
        self.in_air = False

    def move(self):
        if self.in_air:
            self.vertical_speed += 0.8  
        self.rect.x += self.horizontal_speed
        self.rect.y += self.vertical_speed

        if self.rect.bottom > WINDOW_HEIGHT - 30:
            self.rect.bottom = WINDOW_HEIGHT - 30
            self.in_air = False
            self.vertical_speed = 0

        self.rect.x = max(0, min(WINDOW_WIDTH - self.rect.width, self.rect.x))

    def leap(self):
        if not self.in_air:
            self.vertical_speed = -15
            self.in_air = True

class GoalFlag(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(WINDOW_WIDTH - 120, WINDOW_HEIGHT - 70, 40, 40)
    
    def render(self, surface):
        
        points = [
            (self.rect.centerx, self.rect.top),  
            (self.rect.left, self.rect.bottom),  
            (self.rect.right, self.rect.bottom)  
        ]
        pygame.draw.polygon(surface, GREEN, points)

class MovingEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 10
        self.rect = pygame.Rect(400, WINDOW_HEIGHT - 40, self.radius * 2, self.radius * 2)
        self.movement_direction = 1
        self.speed = 3

    def patrol(self):
        self.rect.x += self.movement_direction * self.speed
        if self.rect.right >= WINDOW_WIDTH - 100 or self.rect.left <= 100:
            self.movement_direction *= -1
    def render(self, surface):
        pygame.draw.circle(surface, BLUE, self.rect.center, self.radius)

def begin():
    clock = pygame.time.Clock()
    player = Character()
    goal = GoalFlag()
    enemy = MovingEnemy()
    game_running = True
    victory = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_running:
                    player.leap()
                elif event.key == pygame.K_RETURN and not game_running:  
                    player.rect.topleft = (50, WINDOW_HEIGHT - 60)
                    game_running = True
                    victory = False

        if game_running:
            keys = pygame.key.get_pressed()
            player.horizontal_speed = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
            player.move()
            enemy.patrol()

           
            if player.rect.colliderect(enemy.rect):
                game_running = False
            if player.rect.colliderect(goal.rect):
                victory = True
                game_running = False

        
        screen.fill(WHITE)
        pygame.draw.rect(screen, BROWN, (0, WINDOW_HEIGHT - 30, WINDOW_WIDTH, 30))  

        screen.blit(player.image, player.rect.topleft)
        goal.render(screen)
        enemy.render(screen)

        
        font = pygame.font.Font(None, 50)
        if not game_running:
            message = "You Won! Press Enter to restart" if victory else "Game Over! Press Enter to restart"
            text = font.render(message, True, GREEN if victory else RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    begin()
