import random
import numpy as np
from typing import List, Tuple
from .constants import BOARD_SIZE, SHIP_SIZES
from .utils import Orientation

class AIOpponent:
    def __init__(self, game):
        if not hasattr(game, 'opponent_board'):
            raise ValueError("Game object is missing required attributes")
        self.game = game
        self.last_hit = None
        self.hit_direction = None
        self.target_stack = []
        self.place_ships()

    def place_ships(self):
        """Place all ships randomly for the AI opponent"""
        for ship_name, size in SHIP_SIZES.items():
            placed = False
            attempts = 0
            while not placed and attempts < 100:  
                x = random.randint(0, BOARD_SIZE - 1)
                y = random.randint(0, BOARD_SIZE - 1)
                orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
                
                if self.can_place_ship(x, y, size, orientation):
                    self.place_ship(x, y, size, orientation, ship_name)
                    placed = True
                attempts += 1

    def can_place_ship(self, x, y, size, orientation):
        """Check if ship can be placed at given position"""
        if orientation == Orientation.HORIZONTAL:
            if x + size > BOARD_SIZE:
                return False
            return all(self.game.opponent_board[y][x+i] == 0 for i in range(size))
        else:
            if y + size > BOARD_SIZE:
                return False
            return all(self.game.opponent_board[y+i][x] == 0 for i in range(size))

    def place_ship(self, x, y, size, orientation, ship_name):
        """Place a ship on the opponent's board"""
        positions = []
        if orientation == Orientation.HORIZONTAL:
            for i in range(size):
                self.game.opponent_board[y][x+i] = 1
                positions.append((x+i, y))
        else:
            for i in range(size):
                self.game.opponent_board[y+i][x] = 1
                positions.append((x, y+i))
        self.game.opponent_ships[ship_name] = positions

    def make_move(self) -> bool:
        """Make an attack move"""
        if not hasattr(self.game, 'player_board'):
            return False  

        if self.game.game_phase != "playing":
            return False
        if self.game.current_player != "opponent":
            return False

        x, y = self.choose_target()
        self.game.last_ai_move = (x, y)
        
        hit, sunk = self.game.attack(x, y)
        
        if hit:
            if sunk:
                self.game.message = f"AI hit and sunk your ship at {chr(65+y)}{x+1}!"
                self.last_hit = None
                self.hit_direction = None
                self.target_stack = []
            else:
                self.game.message = f"AI hit your ship at {chr(65+y)}{x+1}!"
                self.last_hit = (x, y)
                self.add_adjacent_targets(x, y)
        else:
            self.game.message = f"AI missed at {chr(65+y)}{x+1}"

        self.game.switch_player()
        return True

    def choose_target(self) -> Tuple[int, int]:
        """Choose target coordinates using Hunt/Target algorithm"""
        if self.target_stack:
            return self.target_stack.pop()
        

        while True:
            x, y = random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1)
            if self.game.player_board[y][x] in (0, 1):
                return x, y

    def add_adjacent_targets(self, x: int, y: int):
        """Add adjacent cells to target stack"""
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                if self.game.player_board[ny][nx] in (0, 1):
                    self.target_stack.append((nx, ny))