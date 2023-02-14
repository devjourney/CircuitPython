import time
from random import seed, randint
import board
import displayio
from adafruit_st7789 import ST7789
import adafruit_imageload


# Sprite cell values
EMPTY = 0
CELL_1 = EMPTY + 1
CELL_2 = CELL_1 + 1
CELL_3 = CELL_2 + 1
CELL_4 = CELL_3 + 1
TOAST = CELL_4 + 1

NUMBER_OF_SPRITES = TOAST + 1

# Animation support

FIRST_CELL = CELL_1
LAST_CELL = CELL_4
NUMBER_OF_CELLS = (LAST_CELL - FIRST_CELL) + 1

# A boolean array corresponding to the sprites, True if it's part of the animation sequence.
ANIMATED = [FIRST_CELL <= _sprite <=
            LAST_CELL for _sprite in range(NUMBER_OF_SPRITES)]

# The chance (out of 10) that toast will enter
CHANCE_OF_NEW_TOAST = 2

# How many sprites to start with
INITIAL_NUMBER_OF_SPRITES = 4

seed(int(time.monotonic()))


def make_display():
    """Set up the display support.
    Return the Display object.
    """
    spi = board.SPI()
    while not spi.try_lock():
        pass
    spi.configure(baudrate=24000000)  # Configure SPI for 24MHz
    spi.unlock()
    displayio.release_displays()
    display_bus = displayio.FourWire(
        spi, command=board.TFT_DC, chip_select=board.TFT_CS
    )

    return ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53, auto_refresh=True)


def make_tilegrid():
    """Construct and return the tilegrid."""
    group = displayio.Group()

    sprite_sheet, palette = adafruit_imageload.load(
        "/img/spritesheet-2x.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
    )
    grid = displayio.TileGrid(
        sprite_sheet,
        pixel_shader=palette,
        width=5,
        height=5,
        tile_height=64,
        tile_width=64,
        x=0,
        y=-64,
        default_tile=EMPTY,
    )
    group.append(grid)
    display.show(group)
    return grid


def random_cell():
    return randint(FIRST_CELL, LAST_CELL)


def evaluate_position(row, col):
    """Return whether how long of a toaster is placeable at the given location.
    :param row: the tile row (0-9)
    :param col: the tile column (0-9)
    """
    return tilegrid[col, row] == EMPTY


def seed_toasters(number_of_toasters):
    """Create the initial toasters so it doesn't start empty"""
    for _ in range(number_of_toasters):
        while True:
            row = randint(0, 4)
            col = randint(0, 4)
            if evaluate_position(row, col):
                break
        tilegrid[col, row] = random_cell()


def next_sprite(sprite):
    if ANIMATED[sprite]:
        return (((sprite - FIRST_CELL) + 1) % NUMBER_OF_CELLS) + FIRST_CELL
    return sprite


def advance_animation():
    """Cycle through animation cells each time."""
    for tile_number in range(25):
        tilegrid[tile_number] = next_sprite(tilegrid[tile_number])


def slide_tiles():
    """Move the tilegrid one pixel to the bottom-left."""
    tilegrid.x -= 1
    tilegrid.y += 1


def shift_tiles():
    """Move tiles one spot to the left, and reset the tilegrid's position"""
    for row in range(4, 0, -1):
        for col in range(4):
            tilegrid[col, row] = tilegrid[col + 1, row - 1]
        tilegrid[4, row] = EMPTY
    for col in range(5):
        tilegrid[col, 0] = EMPTY
    tilegrid.x = 0
    tilegrid.y = -64


def get_entry_row():
    while True:
        row = randint(0, 4)
        if tilegrid[4, row] == EMPTY and tilegrid[3, row] == EMPTY:
            return row


def get_entry_column():
    while True:
        col = randint(0, 3)
        if tilegrid[col, 0] == EMPTY and tilegrid[col, 1] == EMPTY:
            return col


def add_toaster_or_toast():
    """Maybe add a new toaster or toast on the right and/or top at a random open location"""
    if randint(1, 10) <= CHANCE_OF_NEW_TOAST:
        tile = TOAST
    else:
        tile = random_cell()
    tilegrid[4, get_entry_row()] = tile

    if randint(1, 10) <= CHANCE_OF_NEW_TOAST:
        tile = TOAST
    else:
        tile = random_cell()
    tilegrid[get_entry_column(), 0] = tile


display = make_display()
tilegrid = make_tilegrid()
seed_toasters(INITIAL_NUMBER_OF_SPRITES)
display.refresh()

while True:
    for _ in range(64):
        display.refresh(target_frames_per_second=80)
        advance_animation()
        slide_tiles()
    shift_tiles()
    add_toaster_or_toast()
    display.refresh(target_frames_per_second=120)
