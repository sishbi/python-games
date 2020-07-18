import sys
import random
import time
import pygame


class SnakeGame:
    """ Snake Game"""

    def __init__(self):
        # initialise the screen
        self.screen_size = self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode(self.screen_size)
        self.black = pygame.color.THECOLORS['black']
        self.red = pygame.color.THECOLORS['red']
        self.green = pygame.color.THECOLORS['green']
        self.dark_green = pygame.color.THECOLORS['darkgreen']
        self.white = pygame.color.THECOLORS['white']
        self.exit = False
        self.game_over = False
        # start game in 'stopped' mode
        self.stopped = True
        # the snake speed
        self.speed = 2
        self.move_x = 0
        self.move_y = 0
        self.snake_size = 20
        self.food_size = 10
        self.food_dim = (self.food_size, self.food_size)  # width, height
        self.food_left = 250
        self.food_top = 150
        self.food_start_pos = (self.food_left, self.food_top), self.food_dim  # left, top, width, height
        self.snake_dim = (self.snake_size, self.snake_size)  # width, height
        self.start_snake_pos = (150, 150), self.snake_dim  # left, top, width, height
        self.font = pygame.font.Font(None, 50)
        self.snake_head = pygame.Rect(self.start_snake_pos)
        self.snake_food = pygame.Rect(self.food_start_pos)
        # track where the snake head has been
        self.snake_tail = []
        self.tail_length = 0
        self.eat_food = False
        self.eat_time = 0.0
        self.now = time.time()
        self.fps = pygame.time.Clock()
        self.score = 0

    def reset(self):
        """reset the game"""
        self.snake_tail = []
        self.tail_length = 1
        self.snake_head = pygame.Rect(self.start_snake_pos)
        self.snake_food = pygame.Rect(self.food_start_pos)
        self.speed = 2
        # start by moving right
        self.move_x = 2
        self.move_y = 0
        self.eat_food = False
        self.eat_time = 0.0
        self.score = 0

    def start(self):
        """start the game"""
        self.game_over = False
        self.stopped = False
        self.reset()

    def run(self):
        """run the game"""

        # infinite loop
        while 1:
            self.now = time.time()
            self.events()
            self.detect()
            self.render()

    def events(self):
        """handle events"""
        for event in pygame.event.get():
            # detect quit event
            if event.type == pygame.QUIT:
                self.exit = True
                sys.exit()
            # detect a key event
            self.key_pressed(event)

    def key_pressed(self, event: pygame.event.EventType):
        """detect a key event"""
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            # move X
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.move_y = 0
            if event.key == pygame.K_LEFT:
                self.move_x = -self.speed
            if event.key == pygame.K_RIGHT:
                self.move_x = self.speed
            # move Y
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.move_x = 0
            if event.key == pygame.K_UP:
                self.move_y = -self.speed
            if event.key == pygame.K_DOWN:
                self.move_y = self.speed
            # (re)start
            if event.key == pygame.K_SPACE and self.stopped:
                self.start()
            if event.key == pygame.K_ESCAPE and not self.stopped:
                self.stopped = True

    def detect(self):
        """detect edge and touches"""
        if self.stopped:
            return
        self.detect_edge()
        self.detect_touching_food()
        self.detect_touching_tail()

    def detect_edge(self):
        """detect edge of screen"""
        if self.snake_head.left < 0 or self.snake_head.right > self.width \
           or self.snake_head.top < 0 or self.snake_head.bottom > self.height:
            self.game_over = True
            self.stopped = True

    def detect_touching_food(self):
        """detect whether the snake is touching the food"""
        old_eat = self.eat_food
        if self.snake_head.colliderect(self.snake_food) and not old_eat:
            self.eat_food = True
        if not old_eat and self.eat_food:
            self.eat_time = self.now
            self.food_left = random.randrange(self.snake_size, self.width - self.snake_size, 1)
            self.food_top = random.randrange(self.snake_size, self.height - self.snake_size, 1)
            self.snake_food = pygame.Rect((self.food_left, self.food_top), self.food_dim)
            self.tail_length += 5
            self.score += 1
            if self.score % 10 == 0:
                self.speed += 1

        # wait 0.5 seconds before showing food
        if self.eat_food:
            if self.time_since_eat() > 0.5:
                self.eat_food = False
                self.eat_time = 0.0

    def detect_touching_tail(self):
        """detect whether the snake head is touching the tail"""
        # don't detect the first few elements of the tail (to avoid false detection)
        for i in range(0, len(self.snake_tail) - 20):
            tail = self.snake_tail[i]
            if self.snake_head.colliderect(tail):
                self.game_over = True
                self.stopped = True
                break

    def time_since_eat(self):
        """calculate how much time has elapsed since the food was eaten"""
        since_eat = 0.0
        if self.eat_food:
            since_eat = self.now - self.eat_time
        return since_eat

    def print_space_to_start(self):
        """print 'START' message"""
        self.screen.blit(self.font.render("press SPACE to start", True, self.white), (150, 150))

    def print_game_over(self):
        """print 'GAME OVER' message"""
        self.screen.blit(self.font.render("GAME OVER", True, self.red), (200, 100))

    def print_score(self):
        """print current SCORE"""
        self.screen.blit(self.font.render("{}".format(self.score), True, self.white), (0, 0))

    def draw_snake(self):
        """draw the snake + tail"""
        # draw the snake's tail from head to tail
        snake_len = len(self.snake_tail)
        for tail in self.snake_tail:
            pygame.draw.rect(self.screen, self.dark_green, tail)
        # keep the top 5 elements of the snake
        if snake_len > 5 + self.tail_length:
            self.snake_tail.pop(0)
        self.snake_head = self.snake_head.move(self.move_x, self.move_y)
        self.snake_tail.append(self.snake_head.copy())
        pygame.draw.rect(self.screen, self.green, self.snake_head)

    def draw_food(self):
        """draw the food"""
        if not self.eat_food:
            pygame.draw.rect(self.screen, self.red, self.snake_food)

    def render(self):
        """render the screen"""
        self.screen.fill(self.black)
        if self.stopped:
            self.print_space_to_start()
        if self.game_over:
            self.print_game_over()
        self.print_score()
        if not self.stopped and not self.game_over:
            self.draw_snake()
            self.draw_food()
        # flip the off-screen buffer with the on-screen buffer - render the screen
        if not self.exit:
            pygame.display.flip()
            # limit game speed to 60fps
            self.fps.tick(60)


# main function
def main():
    pygame.init()
    pygame.display.set_caption("PySnake!")
    game = SnakeGame()
    game.run()


# execute the main function
if __name__ == "__main__":
    main()
