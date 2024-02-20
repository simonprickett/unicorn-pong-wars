import random
import time
# TODO make this work with other Unicorns?
from cosmic import CosmicUnicorn as Unicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY

unicorn = Unicorn()
graphics = PicoGraphics(DISPLAY)
squares = []
brightness = 0.1

MIN_BRIGHTNESS = 0.1
MAX_BRIGHTNESS = 0.5
BRIGHTNESS_INCREMENT = 0.1

DISPLAY_WIDTH = unicorn.WIDTH
DISPLAY_HEIGHT = unicorn.HEIGHT
DISPLAY_MID_POINT = DISPLAY_WIDTH // 2

DAY_COLOUR = (0, 255, 0)
NIGHT_COLOUR = (255, 0, 0)
DAY_BALL_COLOUR = (0, 0, 255)
NIGHT_BALL_COLOUR = (255, 255, 255)

DAY_PEN = graphics.create_pen(*DAY_COLOUR)
NIGHT_PEN = graphics.create_pen(*NIGHT_COLOUR)
DEBUG_PEN = graphics.create_pen(0, 0, 255)

SQUARE_SIZE = 2
BALL_SIZE = 2

LOOP_SLEEP_TIME = 0.1

class Square:
    def __init__(self, x, y, size, is_day):
        self.size = size
        self.x = x
        self.y = y
        self.is_day = is_day
        
    def draw(self):
        graphics.set_pen(DAY_PEN if self.is_day else NIGHT_PEN)
        graphics.rectangle(self.x, self.y, self.size, self.size)
        
    def flip(self):
        self.is_day = not self.is_day
        self.draw()
        
    def show(self):
        graphics.set_pen(DEBUG_PEN)
        graphics.rectangle(self.x, self.y, self.size, self.size)
        
class Ball:
    def __init__(self, x, y, is_day):
        self.x = x
        self.y = y
        self.w = BALL_SIZE
        self.h = BALL_SIZE
        self.is_day = is_day
        self.pen = graphics.create_pen(*(DAY_BALL_COLOUR if is_day else NIGHT_BALL_COLOUR))
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

    def __is_opposing(self, x, y):
        # TODO this needs work...
        return False
        
    # TODO consider making this just the initial draw
    # and have next_position do everything else.
    # Or can we just remove this completely?
    def draw(self):
        graphics.set_pen(self.pen)
        graphics.rectangle(self.x, self.y, self.h, self.w)
        
        
    def erase(self):
        graphics.set_pen(DAY_PEN if self.is_day else NIGHT_PEN)
        graphics.rectangle(self.x, self.y, self.h, self.w)
        
    
    def next_position(self):        
        next_x = self.x + self.dx
        next_y = self.y + self.dy
        next_dx = self.dx
        next_dy = self.dy
        
        collisions = {
            "left": False,
            "right": False,
            "top": False,
            "bottom": False
        }
        
        # Check for collisions with the sides of the Unicorn matrix.
        
        if next_x <= 0:
            collisions["left"] = True
            
        if next_y <= 0:
            collisions["top"] = True
            
        if next_x + (self.w - 1) == DISPLAY_WIDTH:
            collisions["right"] = True

        if next_y + (self.h - 1) == DISPLAY_HEIGHT:
            collisions["bottom"] = True
           
        # Check for collisions with a square of the opposing colour.
        check_x = next_x # Left side of the ball.
        check_y = next_y # Top of the ball.
        
        if self.dx == 1:
            # Adjust check_x to be the rightmost side of the ball.
            pass
            
        if self.dy == 1:
            # Adjust check_y to be the bottom of the ball.
            pass
            
        # Adjust movement and position accordingly.
            
        if collisions["top"] == True:
            next_y = 0
            next_dy = 1
            
        if collisions["bottom"] == True:
            next_y = self.y - 1
            next_dy = -1            
            
        if collisions["left"] == True:
            next_x = 0
            next_dx = 1
            
        if collisions["right"] == True:
            next_x = self.x - 1
            next_dx = -1
            
        self.x = next_x
        self.y = next_y
        self.dx = next_dx
        self.dy = next_dy
            

def init_squares():
    graphics.clear()
    
    # Draw the left hand half of the screen using the day colour
    # and the right hand half using the night colour.
    for x in range(0, DISPLAY_HEIGHT, SQUARE_SIZE):
        this_col = []
        
        for y in range(0, DISPLAY_WIDTH, SQUARE_SIZE):
            this_square = Square(x, y, SQUARE_SIZE, x < DISPLAY_MID_POINT)
            this_col.append(this_square)
            this_square.draw()
            
        squares.append(this_col)
        
    unicorn.update(graphics)

    
def draw_balls():
    day_ball.draw()
    #night_ball.draw()
    

def erase_balls():
    day_ball.erase()
    #night_ball.erase()
    
    
def update_ball_positions():
    day_ball.next_position()
    #night_ball.next_position()
    

# Set initial LED brightness.
unicorn.set_brightness(brightness)

frame_counter = 0

# Draw the night/day start point.
init_squares()

# The day ball must start on the left half of the display,
# with the night ball on the right.
day_ball = Ball(
    random.randrange(0, DISPLAY_MID_POINT, BALL_SIZE),
    random.randrange(0, DISPLAY_HEIGHT, BALL_SIZE),
    True
)

night_ball = Ball(
    random.randrange(DISPLAY_MID_POINT, DISPLAY_WIDTH, BALL_SIZE),
    random.randrange(0, DISPLAY_HEIGHT, BALL_SIZE),
    False
)
                
draw_balls()
unicorn.update(graphics)

while True:
    # Update LEDs roughly 60 times per second.
    # TODO maths
    # TODO maybe allow colour cycling.
    # TODO maybe allow frame rate changes.
    
    erase_balls()
    update_ball_positions()
    draw_balls()
    unicorn.update(graphics)
    
    if unicorn.is_pressed(Unicorn.SWITCH_BRIGHTNESS_UP):
        if (brightness + BRIGHTNESS_INCREMENT) <= MAX_BRIGHTNESS:
            brightness = brightness + BRIGHTNESS_INCREMENT
            unicorn.set_brightness(brightness)
            unicorn.update(graphics)

    if unicorn.is_pressed(Unicorn.SWITCH_BRIGHTNESS_DOWN):
        if (brightness - BRIGHTNESS_INCREMENT) >= MIN_BRIGHTNESS:
            brightness = brightness - BRIGHTNESS_INCREMENT
            unicorn.set_brightness(brightness)
            unicorn.update(graphics)

    # TODO check for volume button presses if sound code is added.
  
    # TODO put this back in when we've got movement down.
    #time.sleep(LOOP_SLEEP_TIME)
    # TODO change this for faster loop cycle and calculate when
    # to update ball positions.
    time.sleep(0.4)