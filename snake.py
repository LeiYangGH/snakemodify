"""
 Snake Game template, using classes.
 
 Derived from:
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
"""

import pygame
import random

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen size
height = 600
width = 600

# Margin between each segment
segment_margin = 3

# Set the width and height of each snake segment
segment_width = min(height, width) / 40 - segment_margin
segment_height = min(height, width) / 40 - segment_margin

# Set initial speed
x_change = segment_width + segment_margin
y_change = 0
score = 0


class Obstacle():
    def __init__(self):
        self.spriteslist = pygame.sprite.Group()
        for i in range(2):
            randX = round(random.randrange(0, width - segment_width) / 40) * 30
            randY = round(random.randrange(0, height - segment_height) / 40) * 30 + 50
            randw = round(random.randrange(0, 200))
            randh = round(random.randrange(0, 200))
            ob = pygame.sprite.Sprite()
            ob.image = pygame.Surface([randw, randh])
            ob.image.fill(RED)
            ob.rect = ob.image.get_rect()
            ob.rect.x = randX
            ob.rect.y = randY

            self.spriteslist.add(ob)


class Food():
    def __init__(self):
        self.fooditems = []
        self.spriteslist = pygame.sprite.Group()
        for i in range(2):
            randX = round(random.randrange(0, width - segment_width) / 40) * 40
            randY = round(random.randrange(0, height - segment_height) / 40) * 40
            # print(f'x={randX}y={randY}')
            fooditem = Food_item(randX, randY)
            self.fooditems.append(fooditem)
            self.spriteslist.add(fooditem)

    def replenish(self):
        randX = round(random.randrange(0, width - segment_width) / 40) * 40
        randY = round(random.randrange(0, height - segment_height) / 40) * 40
        fooditem = Food_item(randX, randY)
        while pygame.sprite.spritecollide(fooditem, my_snake.spriteslist, False):
            randX = round(random.randrange(0, width - segment_width) / 40) * 40
            randY = round(random.randrange(0, height - segment_height) / 40) * 40
            fooditem = Food_item(randX, randY)
        self.fooditems.append(fooditem)
        self.spriteslist.add(fooditem)


class Food_item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Snake():
    """ Class to represent one snake. """

    # Constructor
    def __init__(self):
        self.segments = []
        self.spriteslist = pygame.sprite.Group()
        self.without_head_spriteslist = pygame.sprite.Group()
        # is_head = True
        for i in range(15):
            x = (segment_width + segment_margin) * 30 - (segment_width + segment_margin) * i
            y = (segment_height + segment_margin) * 2
            segment = Segment(x, y)
            self.segments.append(segment)
            self.spriteslist.add(segment)


    def move(self):
        # Figure out where new segment will be
        x = self.segments[0].rect.x + x_change
        y = self.segments[0].rect.y + y_change

        # Don't move off the screen
        # At the moment a potential move off the screen means nothing happens, but it should end the game
        if 0 <= x <= width - segment_width and 0 <= y <= height - segment_height:
            # Insert new segment into the list
            segment = Segment(x, y)
            self.segments.insert(0, segment)
            self.spriteslist.add(segment)
            # Get rid of last segment of the snake
            # .pop() command removes last item in list
            old_segment = self.segments.pop()
            self.spriteslist.remove(old_segment)

    def grow(self):
        last_seg = self.segments[-1]
        sec_last_seg = self.segments[-2]
        mx = 1 if last_seg.rect.x > sec_last_seg.rect.x else 0
        my = 1 if last_seg.rect.y > sec_last_seg.rect.y else 0
        x = last_seg.rect.x + mx * segment_width
        y = last_seg.rect.y + my * segment_height
        segment = Segment(x, y)
        self.segments.append(segment)
        self.spriteslist.add(segment)


class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of a snake. """

    # Constructor
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(WHITE)

        # Set top-left corner of the bounding rectangle to be the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Call this function so the Pygame library can initialize itself
pygame.init()
font = pygame.font.SysFont('comicsansms', 48)

# Create a 600x600 sized screen
screen = pygame.display.set_mode([width, height + 150])

# Set the title of the window
pygame.display.set_caption('Snake Game')

# Create an initial snake
my_snake = Snake()
food = Food()
obstacle = Obstacle()
clock = pygame.time.Clock()
done = False
game_ended = False

while not done:
    # print('while not done')
    if game_ended:
        print('game_ended')
        screen.fill(WHITE)
        text = font.render('Game Over', True, (255, 0, 0))
        textrect = text.get_rect()
        textrect.centerx = 300
        textrect.centery = 300
        screen.blit(text, textrect)
        pygame.display.update()
        while game_ended and not done:
            for event in pygame.event.get():
                # print('while game_ended for event')
                if event.type == pygame.QUIT:
                    print('done = True')
                    done = True
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Set the direction based on the key pressed
            # We want the speed to be enough that we move a full
            # segment, plus the margin.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = (segment_width + segment_margin) * -1
                    y_change = 0
                if event.key == pygame.K_RIGHT:
                    x_change = (segment_width + segment_margin)
                    y_change = 0
                if event.key == pygame.K_UP:
                    x_change = 0
                    y_change = (segment_height + segment_margin) * -1
                if event.key == pygame.K_DOWN:
                    x_change = 0
                    y_change = (segment_height + segment_margin)
        head_rect = my_snake.segments[0].rect
        # print(head_rect)
        snake_spriteslist_without_head = pygame.sprite.Group()
        [snake_spriteslist_without_head.add(seg) for seg in my_snake.segments[1:]]
        if head_rect.x <= 15 or head_rect.y <= 15 or head_rect.x >= 580 or head_rect.y >= 580 \
                or pygame.sprite.spritecollide(my_snake.segments[0], obstacle.spriteslist, False) \
                or pygame.sprite.spritecollide(my_snake.segments[0], snake_spriteslist_without_head, False):
            game_ended = True

        # move snake one step
        my_snake.move()

        hit_list = pygame.sprite.spritecollide(my_snake.segments[0], food.spriteslist, True)
        if hit_list:
            print('eating!')
            my_snake.grow()
            food.replenish()
            score += 1

        # -- Draw everything
        # Clear screen
        screen.fill(BLACK)
        my_snake.spriteslist.draw(screen)
        food.spriteslist.draw(screen)
        obstacle.spriteslist.draw(screen)
        empty_rect = pygame.Rect(3, 3, width - 6, height - 6)
        pygame.draw.rect(screen, (255, 255, 255), empty_rect, 3)
        text = font.render('Score = ' + str(score), True, (255, 0, 0))
        textrect = text.get_rect()
        textrect.centerx = 200
        textrect.centery = 700
        screen.blit(text, textrect)
        # Flip screen
        pygame.display.flip()

        # Pause
        clock.tick(5)

pygame.quit()
