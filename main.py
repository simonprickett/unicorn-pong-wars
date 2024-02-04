import random
import time
# TODO make this work with other Unicorns?
from cosmic import CosmicUnicorn as Unicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY

unicorn = Unicorn()
graphics = PicoGraphics(DISPLAY)

DISPLAY_WIDTH = unicorn.WIDTH
DISPLAY_HEIGHT = unicorn.HEIGHT
DISPLAY_MID_POINT = DISPLAY_WIDTH // 2

DAY_COLOUR = (209, 245, 66)
NIGHT_COLOUR = (69, 66, 245)
DAY_BALL_COLOUR = NIGHT_COLOUR
NIGHT_BALL_COLOUR = DAY_COLOUR

DAY_PEN = graphics.create_pen(*DAY_COLOUR)
NIGHT_PEN = graphics.create_pen(*NIGHT_COLOUR)

SQUARE_SIZE = 2
BALL_SIZE = 2

LOOP_SLEEP_TIME = 0.1

class Ball:
    def __init__(self, x, y, pen_colour, background_pen_colour):
        self.x = x
        self.y = y
        self.w = BALL_SIZE
        self.h = BALL_SIZE
        self.pen = graphics.create_pen(*pen_colour)
        self.background_pen = graphics.create_pen(*background_pen_colour)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        
    # TODO consider making this just the initial draw
    # and have next_position do everything else.
    # Or can we just remove this completely?
    def draw(self):
        graphics.set_pen(self.pen)
        graphics.rectangle(self.x, self.y, self.h, self.w)
        
    def erase(self):
        graphics.set_pen(self.background_pen)
        graphics.rectangle(self.x, self.y, self.h, self.w)
        
    def next_position(self):        
        next_x = self.x + self.dx
        next_y = self.y + self.dy
        next_dx = self.dx
        next_dy = self.dy
        
        if next_x <= 0:
            # Collision with the left hand side of the display.
            next_x = 0
            next_dx = 1
            
        if next_y <= 0:
            # Collision with the top of the display.
            next_y = 0
            next_dy = 1
            
        if next_x + (self.w - (BALL_SIZE // 2)) == DISPLAY_WIDTH:
            # Collision with the right hand side of the display.
            next_x = self.x - 1
            next_dx = -1

        if next_y + (self.h - (BALL_SIZE // 2)) == DISPLAY_HEIGHT:
            # Collision with the bottom of the display.
            next_y = self.y - 1
            next_dy = -1
            
        # TODO work out collision with the coloured squares.
        
        self.x = next_x
        self.y = next_y
        self.dx = next_dx
        self.dy = next_dy
            

def init_squares():
    graphics.clear()
    
    # Draw the left hand half of the screen using the day colour
    # and the right hand half using the night colour.
    for x in range(0, DISPLAY_HEIGHT, SQUARE_SIZE):
        for y in range(0, DISPLAY_WIDTH, SQUARE_SIZE):
            graphics.set_pen(DAY_PEN if x < DISPLAY_MID_POINT else NIGHT_PEN)
            graphics.rectangle(x, y, SQUARE_SIZE, SQUARE_SIZE)
        
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
    
def check_collision(x, y, dx, dy):
    # TODO
    # TODO acc collision sound, optional?
    return "TODO"


def draw_frame():
    # TODO draw a single frame.
    return "TODO"


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
    DAY_BALL_COLOUR,
    NIGHT_BALL_COLOUR
)

night_ball = Ball(
    random.randrange(DISPLAY_MID_POINT, DISPLAY_WIDTH, BALL_SIZE),
    random.randrange(0, DISPLAY_HEIGHT, BALL_SIZE),
    NIGHT_BALL_COLOUR,
    DAY_BALL_COLOUR
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
    time.sleep(1/30)