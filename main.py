import random
import time
# TODO make this work with other Unicorns?
from cosmic import CosmicUnicorn as Unicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY

unicorn = Unicorn()
graphics = PicoGraphics(DISPLAY)
squares = []

DISPLAY_WIDTH = unicorn.WIDTH
DISPLAY_HEIGHT = unicorn.HEIGHT
DISPLAY_MID_POINT = DISPLAY_WIDTH // 2

DAY_COLOUR = (0, 255, 0)
NIGHT_COLOUR = (255, 0, 0)
DAY_BALL_COLOUR = NIGHT_COLOUR
NIGHT_BALL_COLOUR = DAY_COLOUR

DAY_PEN = graphics.create_pen(*DAY_COLOUR)
NIGHT_PEN = graphics.create_pen(*NIGHT_COLOUR)

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
        # Get the co-ordinate for the square that x, y
        # falls in.
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        
        # TODO have a think about this...
        if squares[row][col].is_day == self.is_day:
            print(f"Colour collision {x} {y}.")
            return True
        else:
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
        
        # TODO add checks on all these ifs to see if the pixel is
        # set to the opposing colour.
        if next_x <= 0:
            collisions["left"] = True
            
        if next_y <= 0:
            collisions["top"] = True
            
        if next_x + (self.w - (BALL_SIZE // 2)) == DISPLAY_WIDTH:
            collisions["right"] = True

        if next_y + (self.h - (BALL_SIZE // 2)) == DISPLAY_HEIGHT:
            collisions["bottom"] = True
            
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
        this_row = []
        
        for y in range(0, DISPLAY_WIDTH, SQUARE_SIZE):
            this_square = Square(x, y, SQUARE_SIZE, x < DISPLAY_MID_POINT)
            this_row.append(this_square)
            this_square.draw()
            
        squares.append(this_row)
        
    unicorn.update(graphics)

    
def draw_balls():
    day_ball.draw()
    night_ball.draw()
    

def erase_balls():
    day_ball.erase()
    night_ball.erase()
    
    
def update_ball_positions():
    day_ball.next_position()
    night_ball.next_position()
    

# Set initial LED brightness.
# TODO do we need to track this in a variable?
unicorn.set_brightness(0.1)

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
        # TODO
        pass

    if unicorn.is_pressed(Unicorn.SWITCH_BRIGHTNESS_DOWN):
        # TODO
        pass
    
    # TODO check for volume button presses if sound code is added.
  
    # TODO put this back in when we've got movement down.
    #time.sleep(LOOP_SLEEP_TIME)
    time.sleep(0.5)