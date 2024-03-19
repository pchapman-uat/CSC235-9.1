import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def move(self):
        head = self.body[0]
        x, y = head
        dx, dy = self.direction
        new_head = ((x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT)
        if new_head in self.body[1:]:
            return False
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True

    def grow_snake(self):
        self.grow = True

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def draw(self, surface):
        for segment in self.body:
            x, y = segment
            pygame.draw.rect(surface, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        x, y = self.position
        pygame.draw.rect(surface, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    high_score = 0  # Initialize high score
    play_again = True
    
    while play_again:
        # Set up display
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        clock = pygame.time.Clock()

        # Load apple texture
        apple_texture = pygame.image.load("apple.jpg").convert_alpha()
        apple_texture = pygame.transform.scale(apple_texture, (CELL_SIZE, CELL_SIZE))

        # Initialize game objects
        snake = Snake()
        food = Food()

        # Initialize game variables
        score = 0

        # Main loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)

            # Move snake
            if not snake.move():
                running = False

            # Check for collisions with food
            if snake.body[0] == food.position:
                snake.grow_snake()
                food = Food()
                score += 1

            # Clear screen
            screen.fill(WHITE)

            # Draw objects
            snake.draw(screen)
            screen.blit(apple_texture, (food.position[0] * CELL_SIZE, food.position[1] * CELL_SIZE))

            # Display score
            font = pygame.font.Font(None, 24)
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(FPS)

        # Update high score
        if score > high_score:
            high_score = score

        # End screen
        font = pygame.font.Font(None, 36)
        text = font.render(f"Game Over! Score: {score}", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(high_score_text, high_score_rect)
        pygame.display.flip()

        # Ask if the user wants to play again
        play_again_text = font.render("Play Again? (Y/N)", True, BLACK)
        play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(play_again_text, play_again_rect)
        pygame.display.flip()

        # Wait for a moment before getting user input
        pygame.time.wait(2000)

        # Wait for user input to play again or quit
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        waiting_for_input = False
                    elif event.key == pygame.K_n:
                        waiting_for_input = False
                        play_again = False

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()

