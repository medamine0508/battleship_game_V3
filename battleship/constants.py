# Game constan
SERVER_PORT = 5555
BOARD_SIZE = 10
SHIP_SIZES = {
    'carrier': 5,
    'battleship': 4,
    'cruiser': 3,
    'submarine': 3,
    'destroyer': 2
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)

# Pygame settings
CELL_SIZE = 40
MARGIN = 2
BOARD_OFFSET = 50
INFO_PANEL_HEIGHT = 150
WINDOW_WIDTH = BOARD_SIZE * CELL_SIZE * 2 + BOARD_OFFSET * 3
WINDOW_HEIGHT = BOARD_SIZE * CELL_SIZE + BOARD_OFFSET * 2 + INFO_PANEL_HEIGHT
FPS = 60

# Font sizes
FONT_SMALL = 24
FONT_MEDIUM = 32
FONT_LARGE = 48