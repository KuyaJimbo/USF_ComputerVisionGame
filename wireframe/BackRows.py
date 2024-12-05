import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BALL_RADIUS = 10
RECT_WIDTH = 150
RECT_HEIGHT = 20
SPEED = 3
GRAVITY = 0.3  # Gravity force for ball falling
JUMP_VELOCITY = -5  # Velocity for ball's jump upwards
STUN_TIME = 1.5  # Time for NPCs to be stunned in seconds

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.y_velocity = 0
        self.x_velocity = 0
        self.y_position = self.rect.centery
        self.side = 'lower'  # 'upper' or 'lower'
        self.bouncing = False

    def move_y(self):
        """Move the ball vertically under the influence of gravity and upwards when bouncing."""
        if not self.bouncing:
            self.y_velocity += GRAVITY
            self.rect.centery += self.y_velocity

            # Prevent the ball from falling below the screen
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                self.y_velocity = 0

        else:
            self.y_velocity = JUMP_VELOCITY
            self.rect.centery += self.y_velocity
            self.rect.centerx += self.x_velocity

            # Bounce back down when reaching max height
            if self.rect.centery <= 100:  # Max height is 100 pixels from the top
                self.bouncing = False

    def collide(self, npc_rects):
        """Check if the ball collides with the NPC rectangles."""
        for npc in npc_rects:
            if self.rect.colliderect(npc.rect) and not npc.stunned and self.y_velocity > 0:
                npc.stunned = True
                npc.stun_start_time = time.time()
                self.bouncing = True  # Make the ball bounce upwards

                # if ball is on left side, give it a random x velocity to the right (1-3)
                if self.rect.centerx < SCREEN_WIDTH // 2:
                    self.x_velocity = random.randint(2, 5)
                # if ball is on right side, give it a random x velocity to the left (-3 to -1)
                else:
                    self.x_velocity = random.randint(-5, -2)
                # Reverse the ball's Y velocity to bounce it upwards
                return True
        return False

# NPC_Rect class
class NPC_Rect(pygame.sprite.Sprite):
    def __init__(self, y_position):
        super().__init__()
        self.image = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, y_position)
        self.stunned = False
        self.stun_start_time = 0

    def move_x(self, ball):
        """Move the NPC rectangle to follow the ball horizontally if not stunned."""
        if not self.stunned:
            if self.rect.centerx < ball.rect.centerx:
                self.rect.centerx += SPEED
            elif self.rect.centerx > ball.rect.centerx:
                self.rect.centerx -= SPEED
        else:
            # Check if the stun duration has passed
            if time.time() - self.stun_start_time >= STUN_TIME:
                self.stunned = False

# Main game loop
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Ball and NPC Rects')

    # Create ball and NPC Rects
    ball = Ball()
    npc_upper = NPC_Rect(SCREEN_HEIGHT // 3)
    npc_lower = NPC_Rect(SCREEN_HEIGHT * 2 // 3)
    
    npc_rects = [npc_upper, npc_lower]
    all_sprites = pygame.sprite.Group()
    all_sprites.add(ball, npc_upper, npc_lower)

    running = True
    clock = pygame.time.Clock()
    
    while running:
        screen.fill(WHITE)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Ball movement and collision
        ball.move_y()
        ball.collide(npc_rects)

        # NPC movement
        npc_upper.move_x(ball)
        npc_lower.move_x(ball)

        # Draw all sprites
        all_sprites.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
