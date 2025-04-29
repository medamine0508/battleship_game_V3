from typing import Dict, List, Tuple
from .constants import *
from .utils import Orientation

class HumanPlayer:
    def __init__(self, game):
        self.game = game
        self.placed_ships = set()

    def handle_setup_click(self, x: int, y: int) -> bool:
        """Handle ship placement during setup"""
        if self.game.selected_ship is None:
            return False
            
        ship_name = self.game.selected_ship
        if ship_name in self.placed_ships:
            return False
            
        success = self.game.place_ship(ship_name, (x, y), self.game.ship_orientation)
        if success:
            self.placed_ships.add(ship_name)
            if len(self.placed_ships) == len(SHIP_SIZES):
                self.game.game_phase = "playing"
                self.game.message = "Your turn - Attack opponent's board"
            return True
        return False

    def handle_attack_click(self, pos: Tuple[int, int]) -> bool:
        """Handle attack during gameplay"""
        x, y = pos
        if self.game.opponent_board[y][x] in (2, 3):
            return False
            
        hit, sunk = self.game.attack(x, y)
        if hit:
            self.game.message = f"Hit! {'You sunk their ship!' if sunk else ''}"
        else:
            self.game.message = "Miss!"
            
        self.game.switch_player()
        return True