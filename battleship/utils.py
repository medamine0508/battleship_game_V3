from enum import Enum
from typing import Tuple
from .constants import BOARD_OFFSET, CELL_SIZE, BOARD_SIZE

class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

def pos_to_grid(x: int, y: int) -> Tuple[int, int, str]:
    """Convert screen coordinates to grid coordinates and board type"""
    # Check if within vertical bounds
    if not (BOARD_OFFSET <= y < BOARD_OFFSET + BOARD_SIZE * CELL_SIZE):
        return None, None, None

    # Player board (left)
    if BOARD_OFFSET <= x < BOARD_OFFSET + BOARD_SIZE * CELL_SIZE:
        grid_x = (x - BOARD_OFFSET) // CELL_SIZE
        grid_y = (y - BOARD_OFFSET) // CELL_SIZE
        return grid_x, grid_y, "player"

    # Opponent board (right)
    opponent_left = BOARD_OFFSET * 2 + BOARD_SIZE * CELL_SIZE
    if opponent_left <= x < opponent_left + BOARD_SIZE * CELL_SIZE:
        grid_x = (x - opponent_left) // CELL_SIZE
        grid_y = (y - BOARD_OFFSET) // CELL_SIZE
        return grid_x, grid_y, "opponent"

    return None, None, None

def grid_to_pos(x: int, y: int, board_type: str) -> Tuple[int, int]:
    """Convert grid coordinates to screen coordinates"""
    screen_y = BOARD_OFFSET + y * CELL_SIZE
    if board_type == "player":
        screen_x = BOARD_OFFSET + x * CELL_SIZE
    else:
        screen_x = (BOARD_OFFSET * 2 + BOARD_SIZE * CELL_SIZE) + x * CELL_SIZE
    return screen_x, screen_y