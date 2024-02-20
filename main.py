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
DISPLAY_RIGHT = DISPLAY_WIDTH - 1
DISPLAY_BOTTOM = DISPLAY_HEIGHT - 1
DISPLAY_MID_POINT = DISPLAY_WIDTH // 2

DAY_COLOUR = (0, 255, 0)
NIGHT_COLOUR = (255, 0, 0)
DAY_BALL_COLOUR = (0, 0, 255)
NIGHT_BALL_COLOUR = (255, 255, 255)

DAY_PEN = graphics.create_pen(*DAY_COLOUR)
NIGHT_PEN = graphics.create_pen(*NIGHT_COLOUR)
DEBUG_PEN = graphics.create_pen(0, 0, 255)

SQUARE_SIZE = 2
SQUARES_WIDE = DISPLAY_WIDTH // SQUARE_SIZE
SQUARES_HIGH = DISPLAY_HEIGHT // SQUARE_SIZE

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
        self.w = SQUARE_SIZE
        self.h = SQUARE_SIZE
        self.is_day = is_day
        self.pen = graphics.create_pen(*(DAY_BALL_COLOUR if is_day else NIGHT_BALL_COLOUR))
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        
        
    def draw(self):
        graphics.set_pen(self.pen)
        print(f"draw x {self.x} y {self.y}")
        graphics.rectangle(self.x, self.y, self.h, self.w)
        
        
    def erase(self):
        graphics.set_pen(DAY_PEN if self.is_day else NIGHT_PEN)
        graphics.rectangle(self.x, self.y, self.h, self.w)
        
    
    def next_position(self):
        print(f"in: x = {self.x} y = {self.y}")
        next_dy = self.dy
        next_dx = self.dx
        
        ball_right = self.x + (SQUARE_SIZE - 1)
        ball_bottom = self.y + (SQUARE_SIZE - 1)
        ball_col = (self.x if self.dx == -1 else ball_right) // SQUARE_SIZE
        ball_row = (self.y if self.dy == -1 else ball_bottom) // SQUARE_SIZE
        
        #print(f"ball row {ball_row}, col {ball_col}")        
        
        # Will we collide with the top of the display?
        if self.dy == -1 and self.y == 0:
            # Will collide with the top.
            next_dy = 1
            
        # Will we collide with the bottom of the display?
        if self.dy == 1 and ball_bottom == DISPLAY_BOTTOM:
            # Will collide with the bottom.
            next_dy = -1
        
        # Will we collide with the left of the display?
        if self.dx == -1 and self.x == 0:
            # Will collide with the left.
            next_dx = 1
        
        # Will we collide with the right of the display?
        if self.dx == 1 and ball_right == DISPLAY_RIGHT:
            # Will collide with the right.
            next_dx = -1
            
        # Will we collide with a square of the opposing colour?
        # TODO this is still all messed up... and needs to account for
        # hits on all sides.  Also hits one pixel early?
        if self.dx == 1:
            squares_to_check = []
            if (ball_col + 1) < SQUARES_WIDE:
                squares_to_check.append(squares[ball_col + 1][ball_row])
            
            if self.dy == 1 and (ball_row + 1) < SQUARES_HIGH:
                squares_to_check.append(squares[ball_col][ball_row + 1])
            elif self.dy == -1 and ball_row -1 >= 0:
                squares_to_check.append(squares[ball_col][ball_row - 1])
            
            for square in squares_to_check:            
                if square.is_day != self.is_day:
                    square.flip()
                    
                    next_dx = -1
                
        
        self.dx = next_dx
        self.dy = next_dy
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        print(f"out: x = {self.x} y = {self.y}")
            

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
    random.randrange(0, DISPLAY_MID_POINT, SQUARE_SIZE),
    random.randrange(0, DISPLAY_HEIGHT, SQUARE_SIZE),
    True
)

night_ball = Ball(
    random.randrange(DISPLAY_MID_POINT, DISPLAY_WIDTH, SQUARE_SIZE),
    random.randrange(0, DISPLAY_HEIGHT, SQUARE_SIZE),
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
    time.sleep(0.2)