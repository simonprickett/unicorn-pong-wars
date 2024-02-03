import time
# TODO make this work with other Unicorns?
from cosmic import CosmicUnicorn as Unicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY

unicorn = Unicorn()
graphics = PicoGraphics(DISPLAY)

DISPLAY_WIDTH = unicorn.WIDTH
DISPLAY_HEIGHT = unicorn.HEIGHT

DAY_COLOUR = "TODO"
DAY_BALL_COLOUR = "TODO"
NIGHT_COLOUR = "TODO"
NIGHT_BALL_COLOUR = "TODO"

SQUARE_SIZE = "TODO"
BALL_SIZE = "TODO"

SQUARES_X = "TODO"  # How many squares wide
SQUARES_Y = "TODO"  # How many squares tall

LOOP_SLEEP_TIME = 0.1

def draw_squares():
    # TODO


def draw_ball(x, y, colour):
    # TODO
    pass


def check_collision(x, y, dx, dy):
    # TODO
    # TODO acc collision sound, optional?
    pass


def draw_frame():
    # TODO draw a single frame.


# Set initial LED brightness.
# TODO do we need to track this in a variable?
unicorn.set_brightness(0.5)


frame_counter = 0

while True:
    # Update LEDs roughly 60 times per second.
    # TODO maths
    
    if unicorn.is_pressed(CosmicUnicorn.SWITCH_BRIGHTNESS_UP):
        # TODO
        pass

    if unicorn.is_pressed(CosmicUnicorn.SWITCH_BRIGHTNESS_DOWN):
        # TODO
        pass
    
    # TODO check for volume button presses if sound code is added.
  
    time.sleep(LOOP_SLEEP_TIME)